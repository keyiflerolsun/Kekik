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

class Nesne(object):
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
        >>> # Oluşan Nesneyi Görsel Biçimde Konsola Yazdırır.

        >>> # Örnek; <---------------------------------- #
        >>> .gorsel(girinti=0, kademe=1)

        >>> # ------------------------------------------ #
        >>> .anahtarlar(nesne:Nesne) -> list:
        >>> ['isSuccess', 'statusCode', 'error', 'result', 'headers']

        >>> # ------------------------------------------ #
        >>> .sozluk -> dict:
        >>> # girdinin son hali
    """
    def __repr__(self) -> str:
        mesaj = f"{__class__.__name__}("
        for anahtar in self.__sozluk.keys():
            mesaj += f"{anahtar}={self.__dict__[anahtar]}, "

        return f"{mesaj.rstrip(', ')})"

    def __str__(self) -> str:
        return repr(self)

    def __init__(self, sozluk:dict):
        self.__sozluk = sozluk

        if not isinstance(self.__sozluk, dict):
            raise VeriTipiHatasi(self.__sozluk)

        # https://stackoverflow.com/questions/1305532/how-to-convert-a-nested-python-dict-to-object
        for anahtar, deger in self.__sozluk.items():
            if isinstance(deger, (tuple, list, set, frozenset)):
                object.__setattr__(
                    self,
                    anahtar,
                    [
                        Nesne(veri) if isinstance(veri, dict) else veri
                          for veri in deger
                    ]
                )
            else:
                object.__setattr__(
                    self,
                    anahtar,
                    Nesne(deger) if isinstance(deger, dict) else deger
                )

    # * Sözlük Benzeri -> erişim / güncellemeler
    def __getitem__(self, anahtar):
        deger = self.__dict__[anahtar]
        if isinstance(deger, dict):  # * Yinelemeli olarak alt sözlükleri nesne olarak görüntüle
            deger = Nesne(deger)
        return deger

    def __setitem__(self, anahtar, deger):
        self.__dict__[anahtar] = deger

    def __delitem__(self, anahtar):
        del self.__dict__[anahtar]

    # * Nesne Benzeri -> erişim / güncellemeler
    def __getattr__(self, anahtar):
        return self[anahtar]

    def __setattr__(self, anahtar, deger):
        self[anahtar] = deger

    def __delattr__(self, anahtar):
        del self[anahtar]

    @property
    def sozluk(self) -> dict:
        """Girdinin Son Hali"""
        veri = self.__dict__.copy()
        del veri["_Nesne__sozluk"]

        return veri

    @staticmethod
    def anahtarlar(veri) -> list | None:
        """
        Parametre olarak verilen Nesne Verisinin Anahtarlarını döndürür.

        Parametreler
        ------------
            >>> veri (Nesne) # Anahtarları İstenen Nesne Verisi

        Dönüt
        -----
        >>> list | None
        """
        if isinstance(veri, Nesne):
            veri = veri.__dict__.copy()
            del veri["_Nesne__sozluk"]

            if sozluk := veri:
                if isinstance(sozluk, dict):
                    return list(veri.keys())

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
        try:
            veri = self.__dict__.copy()
            del veri["_Nesne__sozluk"]

            print(sikici_yaz(veri, girinti, kademe))
        except KeyError:
            print(sikici_yaz(self.__sozluk, girinti, kademe))