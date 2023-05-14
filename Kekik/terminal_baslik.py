# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import os, sys

def terminal_baslik(mesaj:str):
    if os.name == "nt":
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(mesaj)
        return

    if "KONSOLE_VERSION" in os.environ:
        # https://stackoverflow.com/questions/19897787/change-konsole-tab-title-from-command-line-and-make-it-persistent
        # TODO this works only once per stage where it's updated at the very beginning
        sys.stdout.write(f"\033]30;{mesaj}\007")
    else:
        # https://stackoverflow.com/questions/25872409/set-gnome-terminal-window-title-in-python/47262154#47262154
        sys.stdout.write(f"\33]0;{mesaj}\a")

    sys.stdout.flush()