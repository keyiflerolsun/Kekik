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
from pathlib          import Path
from logging.handlers import RotatingFileHandler
from threading        import Lock
import io, logging, os

class _KonsolDosyaLoglu(Console):
    """
    rich.Console — tek fark: log()/print() çağrıları terminale ek olarak
    döngüsel (rotating) bir dosyaya da ANSI'siz düz metin + zaman damgasıyla
    yazılır. Terminal kapansa da hata izi kaybolmasın diye.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._dosya_kilit = Lock()
        self._duz_tampon  = io.StringIO()
        self._duz_konsol  = Console(file=self._duz_tampon, no_color=True, width=200, highlight=False)

        self._dosya_logu           = logging.getLogger("kekik.konsol")
        self._dosya_logu.propagate = False
        self._dosya_logu.setLevel(logging.INFO)
        if not self._dosya_logu.handlers:
            with suppress(Exception):
                log_dizin = Path(os.environ.get("KEKIK_LOG_DIR", "Logs"))
                log_dizin.mkdir(parents=True, exist_ok=True)
                handler = RotatingFileHandler(log_dizin / "konsol.log", maxBytes=10_485_760, backupCount=5, encoding="utf-8")
                handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
                self._dosya_logu.addHandler(handler)

    def _dosyaya_yaz(self, *args) -> None:
        with suppress(Exception), self._dosya_kilit:
            self._duz_tampon.seek(0)
            self._duz_tampon.truncate(0)
            self._duz_konsol.print(*args)
            self._dosya_logu.info(self._duz_tampon.getvalue().rstrip("\n"))

    def log(self, *args, **kwargs):
        super().log(*args, **kwargs)
        self._dosyaya_yaz(*args)

    def print(self, *args, **kwargs):
        super().print(*args, **kwargs)
        self._dosyaya_yaz(*args)

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
