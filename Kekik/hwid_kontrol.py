# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from os import name as sistem
from subprocess import check_output, STDOUT
from requests import get
from uuid import uuid5, NAMESPACE_DNS

def str2uuid(metin) -> str:
    return str(uuid5(NAMESPACE_DNS, str(metin))).upper()

def benim_hwid() -> str:
    # HWID Yakala
    if sistem == 'nt':
        benim_hwid = str2uuid(check_output('wmic csproduct get uuid').decode().split('\n')[1])
    else:
        try:
            from GPUtil import getGPUs
        except ModuleNotFoundError:
            from os import system
            system("pip3 install gputil")
            system("clear")
            from GPUtil import getGPUs

        if ekran_kartlari := getGPUs():
            benim_hwid = str2uuid(ekran_kartlari[0].uuid[4:])
        else:
            try:
                benim_hwid = str2uuid(check_output(['cat', '/var/lib/dbus/machine-id'], stderr=STDOUT).decode())
            except Exception:
                benim_hwid = str2uuid(check_output("lscpu").decode() + check_output(["uname", "-a"]).decode())

    return benim_hwid

def hwid_kontrol(kontrol_url:str) -> bool:
    # Çevrimiçi HWID Kontrolü
    return bool(benim_hwid() in get(kontrol_url).text)