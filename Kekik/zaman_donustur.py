# https://github.com/Skuzzy_xD/TelePyroBot

def sure2saniye(zaman:str) -> int:
    return sum(int(dilim) * 60 ** say for say, dilim in enumerate(reversed(zaman.split(":"))))

def zaman_donustur(saniye: int) -> str:
    dakika, saniye = divmod(saniye, 60)
    saat, dakika   = divmod(dakika, 60)
    gun, saat      = divmod(saat, 24)
    toparla = (
        (f"{round(gun)} gün, " if gun else "")
        + (f"{round(saat)} saat, " if saat else "")
        + (f"{round(dakika)} dakika, " if dakika else "")
        + (f"{round(saniye)} saniye, " if saniye else "")
    )

    return toparla[:-2]