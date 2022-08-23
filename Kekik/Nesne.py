# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from rich    import print
from decimal import Decimal

def sikici_yaz(sozluk: dict, girinti: int = None, kademe: int = Decimal("Infinity")):
    """
    Sözlük Tipindeki Veriyi Nesne Formatında Ekrana Yazdırır.
        `https://github.com/LonamiWebs/Telethon/blob/master/telethon/_misc/helpers.py#L192`

    Parametreler
    ------------
        >>> sozluk  (dict) # Yazılması İstenen Veri
        >>> girinti (int)  # Kaç Tab Boşluk Bıraksın
        >>> kademe  (int)  # En Fazla Kaç Kademe Göstersin

    Kullanım
    --------
    ```
    sikici_yaz(sozluk={"Merhaba": "Dünya"}, girinti=0, kademe=1)
    ```

    Dönüt
    -----
        >>> None
    """
    kademe -= 1
    if kademe < 0:
        return "..."

    to_d = getattr(sozluk, "to_dict", None)
    if callable(to_d):
        sozluk = to_d()

    if girinti is None:
        if isinstance(sozluk, dict):
            return f"{sozluk.get('_', 'Nesne')}({', '.join(f'{k}={sikici_yaz(v, girinti, kademe)}' for k, v in sozluk.items() if k != '_')})"

        elif isinstance(sozluk, (str, bytes)) or not hasattr(sozluk, "__iter__"):
            return repr(sozluk)

        else:
            return f"[{', '.join(sikici_yaz(x, girinti, kademe) for x in sozluk)}]"
    else:
        sonuc = []

        if isinstance(sozluk, dict):
            sonuc.extend((sozluk.get("_", "Nesne"), "("))
            if sozluk:
                sonuc.append("\n")
                girinti += 1
                for k, v in sozluk.items():
                    if k == "_":
                        continue
                    sonuc.extend(
                        ("\t" * girinti, k, "=", sikici_yaz(v, girinti, kademe), ",\n")
                    )

                sonuc.pop()  # son ',\n'
                girinti -= 1
                sonuc.extend(("\n", "\t" * girinti))
            sonuc.append(")")

        elif isinstance(sozluk, (str, bytes)) or not hasattr(sozluk, "__iter__"):
            sonuc.append(repr(sozluk))

        else:
            sonuc.append("[\n")
            girinti += 1
            for x in sozluk:
                sonuc.extend(("\t" * girinti, sikici_yaz(x, girinti, kademe), ",\n"))
            girinti -= 1
            sonuc.extend(("\t" * girinti, "]"))

        return "".join(sonuc)

class VeriTipiHatasi(Exception):
    """
    Veri Tipi Hatası

    Parametreler
    -----------
        >>> veri        # Hataya Sebep Veri
        >>> mesaj (str) # Hata Sonucu Mesajı
    """
    def __init__(self, veri, mesaj:str="Sözlük Tipinde Bir Veri Değil!"):
        self.veri  = veri
        self.mesaj = mesaj
        super().__init__(self.mesaj)

    def __str__(self):
        return f"\n\n{self.veri} -> {self.mesaj}"

class Nesne:
    """
    Sözlük Veri Tipini Python Nesnesine Çevirir.

    Parametreler
    -----------
        >>> sozluk (dict) # Nesneye Çevrilmek İstenen Sözlük Tipli Veri

    Nitelikler
    ----------
        >>> .sozluk -> dict:
        Verilen Sözlüğün Kendisini Döndürür.

        >>> # Sözlüğün Anahtarları -> Sözlüğün Değeri:
        Anahtarın Değerini Döndürür.

    Metodlar
    ----------
        >>> .gorsel(girinti:int, kademe:int) -> None:
        Oluşan Nesneyi Görsel Biçimde Konsola Yazdırır.

            >>> .gorsel(girinti=0, kademe=1)
    """
    def __repr__(self) -> str:
        mesaj = f"{__class__.__name__}("
        for anahtar in self.sozluk.keys():
            mesaj += f"{anahtar}={self.__dict__[anahtar]}, "

        return f"{mesaj.rstrip(', ')})"

    def __init__(self, sozluk:dict):
        self.sozluk = sozluk

        if not isinstance(self.sozluk, dict):
            raise VeriTipiHatasi(self.sozluk)

        # https://stackoverflow.com/a/1305682/13390799
        for anahtar, deger in self.sozluk.items():
            if isinstance(deger, (list, tuple)):
                setattr(
                    self,
                    anahtar,
                    [
                        Nesne(veri) if isinstance(veri, dict) else veri
                          for veri in deger
                    ]
                )
            else:
                setattr(
                    self,
                    anahtar,
                    Nesne(deger) if isinstance(deger, dict) else deger
                )

    def gorsel(self, girinti:int=None, kademe:int=Decimal('Infinity')) -> None:
        """
        Oluşan Nesneyi Görsel Biçimde Konsola Yazdırır.

        Parametreler
        ------------
            >>> girinti (int) # Kaç Tab Boşluk Bıraksın
            >>> kademe  (int) # En Fazla Kaç Kademe Göstersin

        Kullanım
        --------
        ```
        .gorsel(girinti=0, kademe=1)
        ```

        Dönüt
        -----
        >>> None
        """
        print(sikici_yaz(self.sozluk, girinti, kademe))