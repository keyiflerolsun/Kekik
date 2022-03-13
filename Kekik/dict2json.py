# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import os, json

def dict2json(sozluk:dict, liste_key:str, dosya_adi:str) -> bool:
    """
    dict2json({
        'kullanici_id'  : message.from_user.id,
        'kullanici_nick': f"@{message.from_user.username}" if message.from_user.username else None,
        'kullanici_adi' : f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
    }, liste_key="kullanici_id", dosya_adi=kullanicilar)
    """
    if os.path.isfile(dosya_adi):
        with open(dosya_adi, encoding='utf-8') as gelen_json:
            gelen_veri    = json.load(gelen_json)
            gelen_kisiler = [kisi[liste_key] for kisi in gelen_veri]

        if sozluk[liste_key] not in gelen_kisiler:
            gelen_veri.append(sozluk)
            gelen_essiz = [dict(sozluk) for sozluk in {tuple(liste_ici.items()) for liste_ici in gelen_veri}]
            gelen_a_z   = sorted(gelen_essiz, key=lambda sozluk: sozluk[liste_key])

            with open(dosya_adi, mode='w', encoding='utf-8') as f:
                f.write(json.dumps(gelen_a_z, indent=2, ensure_ascii=False, sort_keys=False))

            return True

        return False

    else:
        with open(dosya_adi, mode='w', encoding='utf-8') as f:
            liste = [sozluk]
            essiz = [dict(sozluk) for sozluk in {tuple(liste_ici.items()) for liste_ici in liste}]
            a_z   = sorted(essiz, key=lambda sozluk: sozluk[liste_key])
            f.write(json.dumps(a_z, indent=2, ensure_ascii=False, sort_keys=False))

            return True