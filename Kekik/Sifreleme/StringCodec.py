# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import base64

class StringCodec:
    """
    Base64 ve ROT13 kodlama/çözme işlemleri için bir sınıf.
    """

    @staticmethod
    def atob(encoded_string: str) -> str:
        """Base64 kodlu bir stringi çözer ve UTF-8 string olarak döndürür."""
        return base64.b64decode(encoded_string).decode("utf-8")

    @staticmethod
    def btoa(plain_text: str) -> str:
        """Bir stringi Base64 formatında kodlar."""
        return base64.b64encode(plain_text.encode("utf-8")).decode("utf-8")

    @staticmethod
    def rtt(input_string: str) -> str:
        """Verilen stringin ROT13 kodlamasını uygular veya çözer."""
        def rot13_char(char):
            if "a" <= char <= "z":
                return chr((ord(char) - ord("a") + 13) % 26 + ord("a"))
            elif "A" <= char <= "Z":
                return chr((ord(char) - ord("A") + 13) % 26 + ord("A"))
            return char

        return "".join(rot13_char(char) for char in input_string)

    @staticmethod
    def decode(encoded_string: str) -> str:
        """Önce ROT13 uygular, ardından Base64 çözer."""
        return StringCodec.atob(StringCodec.rtt(encoded_string))

    @staticmethod
    def encode(plain_text: str) -> str:
        """Önce Base64 kodlar, ardından ROT13 uygular."""
        return StringCodec.rtt(StringCodec.btoa(plain_text))