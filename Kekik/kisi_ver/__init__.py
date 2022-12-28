# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from typing                      import Literal
from Kekik.kisi_ver.isimler      import en_isimler, tr_isimler
from Kekik.kisi_ver.soyisimler   import en_soyisimler, tr_soyisimler
from Kekik.kisi_ver.biyografiler import en_biyografiler, tr_biyografiler
from random                      import choice, randint
# from thispersondoesnotexist      import save_online_person
from Kekik                       import slugify
from pathlib                     import Path

async def kisi_ver(dil:Literal["tr", "en"], dizin:str="tmp") -> dict[str, str]:
    match dil:
        case "en":
            isim      = choice(en_isimler)
            soyisim   = choice(en_soyisimler)
            biyografi = choice(en_biyografiler)
        case "tr":
            isim      = choice(tr_isimler)
            soyisim   = choice(tr_soyisimler)
            biyografi = choice(tr_biyografiler)

    kullanici_adi = f"{slugify(isim[:4]).title()}{randint(0,99)}{slugify(soyisim[:4]).title()}"

    # Path(dizin).mkdir(parents=True, exist_ok=True)
    # await save_online_person(f"{dizin}/{kullanici_adi}.jpg")

    return {
        "isim"          : isim,
        "soyisim"       : soyisim,
        "kullanici_adi" : kullanici_adi,
        "biyografi"     : biyografi,
        # "profil_resmi"  : f"{dizin}/{kullanici_adi}.jpg"
    }