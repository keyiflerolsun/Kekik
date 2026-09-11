# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

#---------------------------------------------------#
from signal import signal, SIGINT, SIGTERM, SIGABRT

def sinyal_yakala(signal, frame):
    cikis_yap()

for sinyal in (SIGINT, SIGTERM, SIGABRT):
    signal(sinyal, sinyal_yakala)

# from warnings import filterwarnings, simplefilter
# filterwarnings("ignore")
# simplefilter("ignore")

# import sys, logging
# logging.disable(sys.maxsize)

# import asyncio, platform
# if platform.system() == "Windows":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#---------------------------------------------------#

from rich import pretty, traceback

pretty.install()
traceback.install(show_locals=False)

from rich.console     import Console
from contextlib       import suppress
from datetime         import datetime, timezone
from pathlib          import Path
from logging.handlers import RotatingFileHandler
from queue            import Queue, Full
from threading        import Thread
import io, json, logging, os, re, sys

# ---- Bilinen log şekilleri — kendi projelerimizin kalıpları -----------------
# Yeni bir şekil eklerken: (isim, derlenmiş regex, alan haritası) tuple'ı ekle.
# Eşleşmezse otomatik olarak ham "text" alanına düşülür, hiçbir şey kaybolmaz.

_SEKIL_WEB = re.compile(
    r"^»\s+(?P<url>\S+)\s*$"
    r"(?:\n»\s+(?P<veri>\{.*\})\s*$)?"
    r"\n {2}durum:\s*(?P<metod>\S+)\s*-\s*(?P<kod>\d+)\s*-\s*(?P<sure>[\d.]+)\s*sn\s*$"
    r"\n {2}ip\s*:\s*(?P<ip>\S+)\s*$"
    r"(?:\n {2}konum:\s*(?P<konum>.+?)\s*$)?"
    r"\n {2}cihaz:\s*(?P<cihaz>.+?)\s*$",
    re.MULTILINE,
)

_SEKIL_BOT = re.compile(
    r"^(?P<kullanici>[^|\n]+?)\s*\|\|\s*(?P<aksiyon>[^|\n]+?)\s*\|\|\s*(?P<durum>[^|\n]+?)\s*$"
)

def _sekil_ayikla(metin: str) -> dict:
    "Bilinen bir log kalıbına uyuyorsa yapısal alanları çıkarır, uymuyorsa boş sözlük döner."

    if eslesme := _SEKIL_WEB.match(metin):
        alanlar = {
            "format"  : "web_istek",
            "url"     : eslesme["url"],
            "metod"   : eslesme["metod"],
            "kod"     : int(eslesme["kod"]),
            "sure_sn" : float(eslesme["sure"]),
            "ip"      : eslesme["ip"],
            "cihaz"   : eslesme["cihaz"],
        }
        if eslesme["veri"]:
            alanlar["veri"] = eslesme["veri"]
        if eslesme["konum"]:
            alanlar["konum"] = eslesme["konum"]
        return alanlar

    if eslesme := _SEKIL_BOT.fullmatch(metin.strip()):
        return {
            "format"    : "bot_olay",
            "kullanici" : eslesme["kullanici"].strip(),
            "aksiyon"   : eslesme["aksiyon"].strip(),
            "durum"     : eslesme["durum"].strip(),
        }

    return {}

class _KonsolDosyaLoglu(Console):
    """
    rich.Console — tek fark: log()/print() çağrıları terminale ek olarak
    döngüsel (rotating) iki dosyaya da yazılır:
      - konsol.log   : ANSI'siz düz metin + zaman damgası (insan için)
      - konsol.jsonl : {"ts": ..., "text": ...} tek satır JSON (makine için)
    Render (rich markup → düz metin) ve disk I/O'nun ikisi de tek bir arka
    plan thread'inde yapılır — çağıran taraf (event loop dahil) sadece
    kuyruğa atıp anında döner, zayıf/mini PC'lerde bile CPU'yu kilitlemez.
    Kuyruk sınırlı (KUYRUK_TAVANI): worker yetişemeyecek kadar yoğun sürekli
    trafik olursa yeni kayıtlar bloklamadan düşürülür — bellek asla sınırsız
    büyümez, proses asla çökmez; sadece o an loglanamayan kayıt kaybedilir.
    Terminal kapansa da hata izi kaybolmasın diye.
    """

    KUYRUK_TAVANI = 50_000  # worker ~1000-1400/sn yazıyor (ölçüldü) -> ~40-50sn'lik patlama payı

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._is_kuyrugu           = Queue(maxsize=self.KUYRUK_TAVANI)
        self._dusen_kayit_sayisi   = 0
        self._dolu_uyarisi_verildi = False

        log_dizin = Path(os.environ.get("KEKIK_LOG_DIR", "Logs"))

        self._dosya_logu           = logging.getLogger("kekik.konsol")
        self._dosya_logu.propagate = False
        self._dosya_logu.setLevel(logging.INFO)

        self._json_logu           = logging.getLogger("kekik.konsol.json")
        self._json_logu.propagate = False
        self._json_logu.setLevel(logging.INFO)

        if not self._dosya_logu.handlers and not self._json_logu.handlers:
            with suppress(Exception):
                log_dizin.mkdir(parents=True, exist_ok=True)

                dosya_handler = RotatingFileHandler(log_dizin / "konsol.log", maxBytes=10_485_760, backupCount=5, encoding="utf-8")
                dosya_handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
                self._dosya_logu.addHandler(dosya_handler)

                json_handler = RotatingFileHandler(log_dizin / "konsol.jsonl", maxBytes=10_485_760, backupCount=5, encoding="utf-8")
                json_handler.setFormatter(logging.Formatter("%(message)s"))
                self._json_logu.addHandler(json_handler)

        Thread(target=self._arka_plan_isci, daemon=True).start()

    def _arka_plan_isci(self) -> None:
        "Kuyruktan render+dosya işini tek başına yürütür — çağıran tarafı hiç bloklamaz."

        duz_tampon = io.StringIO()
        duz_konsol = Console(file=duz_tampon, no_color=True, width=200, highlight=False, soft_wrap=True)

        while True:
            args = self._is_kuyrugu.get()
            with suppress(Exception):
                duz_tampon.seek(0)
                duz_tampon.truncate(0)
                duz_konsol.print(*args)
                metin = duz_tampon.getvalue().rstrip("\n")

                self._dosya_logu.info(metin)

                kayit = {"ts" : datetime.now(timezone.utc).isoformat(), "text" : metin}
                kayit.update(_sekil_ayikla(metin))
                self._json_logu.info(json.dumps(kayit, ensure_ascii=False))

    def _kuyruga_ekle(self, args) -> None:
        try:
            self._is_kuyrugu.put_nowait(args)
            self._dolu_uyarisi_verildi = False
        except Full:
            self._dusen_kayit_sayisi += 1
            if not self._dolu_uyarisi_verildi:
                self._dolu_uyarisi_verildi = True
                with suppress(Exception):
                    sys.stderr.write(f"[Kekik] log kuyruğu doldu (tavan={self.KUYRUK_TAVANI}), kayıtlar bloklamadan düşürülüyor.\n")

    def log(self, *args, **kwargs):
        super().log(*args, **kwargs)
        self._kuyruga_ekle(args)

    def print(self, *args, **kwargs):
        super().print(*args, **kwargs)
        self._kuyruga_ekle(args)

konsol = _KonsolDosyaLoglu(
    log_path = False,
    # _environ = {"COLUMNS": "112"}
)

#---------------------------------------------------#
import platform

if os.name == "nt":
    kullanici_adi = os.getlogin()
else:
    import pwd
    kullanici_adi = pwd.getpwuid(os.geteuid())[0]

oturum = f"{kullanici_adi}@{platform.node()}"

def temizle():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

konum   = os.getcwd().split("\\") if platform.system() == "Windows" else os.getcwd().split("/")
secenek = lambda : konsol.input(f"[red]{oturum}:[/][cyan]~/../{konum[-2]}/{konum[-1]} >> ")

def hata_salla(hata:Exception) -> None:
    "Yakalanan Exception'ı ekranda gösterir.."

    konsol.print(f"[bold yellow2]{type(hata).__name__}[/] [bold magenta]||[/] [bold grey74]{hata}[/]", width=70, justify="center")

#---------------------------------------------------#
from shutil    import rmtree
from traceback import format_exc
from asyncio   import get_event_loop

def bellek_temizle():
    with suppress(Exception):
        [alt_dizin.unlink() for alt_dizin in Path(".").rglob("*.py[coi]")]
    with suppress(Exception):
        [alt_dizin.rmdir()  for alt_dizin in Path(".").rglob("__pycache__")]
    with suppress(Exception):
        [rmtree(alt_dizin)  for alt_dizin in Path(".").rglob("*.build")]
    with suppress(Exception):
        [alt_dizin.unlink() for alt_dizin in Path(".").rglob("*.bak")]

bellek_temizle()

def cikis_yap(_print=True):
    with suppress(RuntimeError):
        loop = get_event_loop()
    with suppress(RuntimeError, UnboundLocalError):
        if loop.is_running():
            # with suppress(RuntimeError):
            #     loop.run_until_complete(loop.shutdown_asyncgens())
            with suppress(RuntimeError):
                loop.stop()
            with suppress(RuntimeError):
                loop.close()

    if _print:
        konsol.print("\n\n")
        konsol.log("[bold purple]Çıkış Yapıldı..")

    bellek_temizle()
    os._exit(0)

def hata_yakala(hata:Exception):
    if (hata in {KeyboardInterrupt, SystemExit, EOFError, RuntimeError}) or (str(hata).startswith(("'coroutine' object is not iterable", "'KekikT"))):
        cikis_yap()
    konsol.print(f"\n\n[bold red]{format_exc()}")
    cikis_yap()

def log_salla(sol:str, orta:str, sag:str) -> None:
    "Sol orta ve sağ şeklinde ekranda hizalanmış tek satır log verir.."

    sol  = f"{sol[:13]}[bright_blue]~[/]"  if len(sol)  > 14 else sol
    orta = f"{orta[:19]}[bright_blue]~[/]" if len(orta) > 20 else orta
    sag  = f"{sag[:14]}[bright_blue]~[/]"  if len(sag)  > 15 else sag

    bicimlendir = f"[bold red]{sol:14}[/] [green]||[/] [yellow]{orta:20}[/] {'':>2}[green]||[/] [magenta]{sag:^16}[/]"
    konsol.log(bicimlendir)
