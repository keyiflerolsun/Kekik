# https://github.com/Skuzzy_xD/TelePyroBot

def okunabilir_byte(boyut: int) -> str:
    """baytları okunabilir biçime dönüştürür.

    Arg:
        boyut (int):
            12345645123456

    Return:
        (str):
            "135 MB"
    """
    if not boyut:
        return ""

    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    binyirmidort = 2 ** 10

    say = 0
    cikti_sozluk = {0: " ", 1: "K", 2: "M", 3: "G", 4: "T"}

    while boyut > binyirmidort:
        boyut /= binyirmidort
        say += 1

    return f'{str(round(boyut, 2))} {cikti_sozluk[say]}B'