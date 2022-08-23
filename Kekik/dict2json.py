# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import os, json

def dict2json(sozluk:dict, liste_key:str, dosya_adi:str) -> bool:
    """
    Verilen `sözlük` tipli veriyi ilgili `anahtar`a göre `hedef dosya`ya yazar.

    Parametreler
    ------------
        >>> sozluk    (dict) # Yazılması İstenen Veri
        >>> liste_key (str)  # Sıralanması İstenen Anahtar
        >>> dosya_adi (str)  # Yazılması İstenen Json Dosya Yolu

    Kullanım
    --------
    ```
    dict2json(
        sozluk    = {
            'id'            : 1,
            'kullanici_adi' : "@keyiflerolsun",
            'ad_soyad'      : "Ömer Faruk Sancak"
        },
        liste_key = "kullanici_id",
        dosya_adi = "kullanicilar.json"
    )
    ```

    Dönüt
    -----
        >>> bool
    """
    if os.path.isfile(dosya_adi):
        with open(dosya_adi, encoding='utf-8') as gelen_json:
            gelen_veri    = json.load(gelen_json)
            gelen_kisiler = [kisi[liste_key] for kisi in gelen_veri]

        if sozluk[liste_key] not in gelen_kisiler:
            gelen_veri.append(sozluk)
            gelen_essiz = [dict(sozluk) for sozluk in {tuple(liste_ici.items()) for liste_ici in gelen_veri}]
            gelen_a_z   = sorted(gelen_essiz, key=lambda sozluk: sozluk[liste_key])

            with open(dosya_adi, mode='w', encoding='utf-8') as dosya:
                dosya.write(json.dumps(gelen_a_z, indent=2, ensure_ascii=False, sort_keys=False))

            return True

        return False

    else:
        with open(dosya_adi, mode='w', encoding='utf-8') as dosya:
            liste = [sozluk]
            essiz = [dict(sozluk) for sozluk in {tuple(liste_ici.items()) for liste_ici in liste}]
            a_z   = sorted(essiz, key=lambda sozluk: sozluk[liste_key])

            dosya.write(json.dumps(a_z, indent=2, ensure_ascii=False, sort_keys=False))

            return True