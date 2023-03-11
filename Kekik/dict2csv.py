# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pathlib import Path
from csv     import DictWriter

def dict2csv(dosya_adi:str, veriler:list[dict]) -> bool:
    # * CSV Kaydet
    dizin = "/".join(dosya_adi.split("/")[:-1]) + "/"
    Path(dizin).mkdir(parents=True, exist_ok=True)
    with open(dosya_adi, "w+", encoding="utf-8") as dosya:
        csv = DictWriter(dosya, fieldnames=veriler[0].keys(), lineterminator="\n")
        csv.writeheader()
        for veri in veriler:
            csv.writerow(veri)

    return True