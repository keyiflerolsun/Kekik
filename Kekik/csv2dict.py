# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from csv import reader as csv_oku
from typing import List, Dict

def csv2dict(dosya_adi:str) -> List[Dict[str, str]]:
    with open(dosya_adi, "r", encoding="utf-8") as dosya:
        csv_veri = csv_oku(dosya)

        basliklar = next(csv_veri)
        icerik    = list(csv_veri)

    return [dict(zip(basliklar, satir)) for satir in icerik]
