# https://github.com/Skuzzy_xD/TelePyroBot

def zaman_donustur(saniye: int) -> str:
    dakika, saniye = divmod(saniye, 60)
    saat, dakika   = divmod(dakika, 60)
    gun, saat      = divmod(saat, 24)
    toparla = (
        (f'{gun} gün, ' if gun else "")
        + (f'{saat} saat, ' if saat else "")
        + (f'{dakika} dakika, ' if dakika else "")
        + (f'{saniye} saniye, ' if saniye else "")
    )

    return toparla[:-2]