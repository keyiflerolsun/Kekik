# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from rich.console import Console

konsol = Console(log_path=False, highlight=False)

#---------------------------------------------------#
import os, platform, pwd

try:
    kullanici_adi = os.getlogin()
except OSError:
    kullanici_adi = pwd.getpwuid(os.geteuid())[0]

oturum = f"{kullanici_adi}@{platform.node()}"

def temizle():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

konum   = os.getcwd().split("\\") if platform.system() == "Windows" else os.getcwd().split("/")
secenek = lambda : konsol.input(f'[red]{oturum}:[/][cyan]~/../{konum[-2]}/{konum[-1]} >> ')

#---------------------------------------------------#
from contextlib import suppress
from pathlib    import Path
from sys        import exit
from shutil     import rmtree
from traceback  import format_exc

def bellek_temizle():
    with suppress(Exception):
        [alt_dizin.unlink() for alt_dizin in Path(".").rglob("*.py[coi]")]
        [alt_dizin.rmdir()  for alt_dizin in Path(".").rglob("__pycache__")]
        [rmtree(alt_dizin)  for alt_dizin in Path(".").rglob("*.build")]
        [alt_dizin.unlink() for alt_dizin in Path(".").rglob("*.bak")]

def cikis_yap(_print=True):
    if _print:
        konsol.print("\n\n")
        konsol.log("[bold purple]Çıkış Yapıldı..")
    bellek_temizle()
    exit()

def hata_yakala(hata:Exception):
    if (hata in {KeyboardInterrupt, SystemExit, EOFError, RuntimeError}) or (str(hata).startswith(("'coroutine' object is not iterable", "'KekikT"))):
        cikis_yap()
    print(f"\n\n[bold red]{format_exc()}")
    cikis_yap()

#---------------------------------------------------#
from signal import signal, SIGINT

def sinyal_yakala(signal, frame):
    cikis_yap()

signal(SIGINT, sinyal_yakala)

bellek_temizle()

from warnings import filterwarnings, simplefilter
filterwarnings("ignore")
simplefilter("ignore")

import sys, logging
logging.disable(sys.maxsize)

import asyncio, platform
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#---------------------------------------------------#