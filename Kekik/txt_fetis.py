# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

def satir_ekle(dosya_adi:str, eklenecek_metin:str):
    """İstenen Dosyanın Sonuna Verilen Metni Satır Olarak Ekler"""

    # Dosyayı ekleme ve okuma modunda açın ('a+')
    with open(dosya_adi, "a+", encoding="utf-8") as dosya:

        dosya.seek(0)                       # Okuma imlecini dosyanın başına taşıyın

        veri = dosya.read(100)              # Dosya boş değilse '\n' ekleyin
        if len(veri) > 0:
            dosya.write("\n")

        dosya.write(eklenecek_metin)        # Dosyanın sonuna metin ekle

def satirlar_ekle(dosya_adi:str, eklenecek_metinler:list):
    """İstenen Dosyanın Sonuna Verilen Listeyi Satır Satır Ekler"""

    # Dosyayı ekleme ve okuma modunda açın ('a+')
    with open(dosya_adi, "a+", encoding="utf-8") as dosya:

        dosya.seek(0)                       # Okuma imlecini dosyanın başına taşıyın

        veri = dosya.read(100)              # Dosyanın boş olup olmadığını kontrol edin
        satir_atla = len(veri) > 0
        for satir in eklenecek_metinler:    # Listedeki her elemanı gez
            if satir_atla:                  # Dosya boş değilse, ilk satırın başına '\n' ekleyin
                dosya.write("\n")
            else:                           # diğer satırlar her zaman satır eklemeden önce '\n' ekler
                satir_atla = True

            dosya.write(satir)              # Dosyanın sonuna eleman ekle

def satir_sil(dosya:str, metin:str) -> None:
    """İlgili Metnin Geçtiği Satırı İstenen Dosyanın İçerisinden Siler"""

    # Dosyayı yeniden yazılabilir modunda açın ('r+')
    with open(dosya, "r+", encoding="utf-8") as dosya:
        satirlar = dosya.readlines()            # Satırları liste olarak alın
        dosya.seek(0)                           # Okuma imlecini dosyanın başına taşıyın
        for satir in satirlar:                  # Satırları gezin
            if metin not in satir and \
                satir !='\n':                   # Eğer metin satır içinde geçmiyorsa ve \n Değilse
                dosya.write(satir)              # Dosyaya ekleyin
        dosya.truncate()                        # Var olan dosyadakiş tüm verileri silin