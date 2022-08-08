# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from os.path import isfile

def dosya2set(dosya_yolu:str) -> set[str] | None:
    try:
        return {satir.strip().replace("\n", "") for satir in open(dosya_yolu, "r", encoding="utf-8") if satir.strip()} if isfile(dosya_yolu) else None
    except Exception:
        return None