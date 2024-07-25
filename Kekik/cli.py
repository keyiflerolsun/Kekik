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

from rich.console import Console

konsol = Console(
    log_path = False,
    _environ = {"COLUMNS": "112"}
)

#---------------------------------------------------#
import os, platform

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
from contextlib import suppress
from pathlib    import Path
from shutil     import rmtree
from traceback  import format_exc
from asyncio    import get_event_loop

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
    loop = get_event_loop()
    if loop.is_running():
        with suppress(RuntimeError):
            loop.stop()
        with suppress(RuntimeError):
            loop.run_until_complete(loop.shutdown_asyncgens())
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