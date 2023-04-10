# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

XU030 = ["AKBNK", "AKSEN", "ALARK", "ARCLK", "ASELS", "BIMAS", "EKGYO", "ENKAI", "EREGL", "FROTO", "GARAN", "GUBRF", "HEKTS", "ISCTR", "KCHOL", "KOZAA", "KOZAL", "KRDMD", "ODAS", "PETKM", "PGSUS", "SAHOL", "SASA", "SISE", "TAVHL", "TCELL", "THYAO", "TOASO", "TUPRS", "YKBNK"]
XU030.sort()

XU050 = [*XU030, "AEFES", "AKSA", "BERA", "DOHOL", "EGEEN", "ENJSA", "GESAN", "HALKB", "ISGYO", "KONTR", "KORDS", "MGROS", "OYAKC", "SMRTG", "SOKM", "TKFEN", "TSKB", "TTKOM", "VAKBN", "VESTL"]
XU050.sort()

XU100 = [*XU050, "AGHOL", "AKFGY", "ALBRK", "ALFAS", "ALKIM", "ASUZU", "AYDEM", "BAGFS", "BASGZ", "BIOEN", "BRYAT", "BUCIM", "CCOLA", "CEMTS", "CIMSA", "DOAS", "ECILC", "ERBOS", "EUREN", "FENER", "GENIL", "GLYHO", "GSDHO", "GWIND", "IPEKE", "ISDMR", "IZMDC", "KARSN", "KCAER", "KERVT", "KLRHO", "KMPUR", "KONYA", "KZBGY", "MAVI", "OTKAR", "PSGYO", "SELEC", "SKBNK", "SNGYO", "TKNSA", "TMSN", "TTRAK", "TUKAS", "TURSG", "ULKER", "ULUUN", "VESBE", "YYLGD", "ZOREN"]
XU100.sort()

marketler = {
    "XU100" : XU100,
    "XU050" : XU050,
    "XU030" : XU030
}

def sembol_sorgu(sembol:str) -> dict[str, list[str]]:
    sembol = sembol.upper()

    return {
        sembol : [
            market
            for market, semboller in marketler.items()
                if sembol in semboller
        ]
    }