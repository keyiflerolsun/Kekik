# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import re

class Packer:
    """
    P.A.C.K.E.R. sıkıştırma ve çözme işlemleri için kapsamlı bir sınıf.
    ! » https://github.com/beautifier/js-beautify/blob/main/python/jsbeautifier/unpackers/packer.py
    """

    # Regex kalıpları - daha gevşek, farklı varyasyonları yakalayabilecek şekilde
    PACKED_PATTERN = re.compile(
        r"\}\s*\(\s*['\"](.*?)['\"],\s*(\d+),\s*(\d+),\s*['\"](.+?)['\"]\.split\(['\"]\\?\|['\"]\)",
        re.IGNORECASE | re.MULTILINE | re.DOTALL
    )

    # Alternatif regex pattern, farklı formatlarda paketlenmiş kodu yakalamak için
    ALTERNATIVE_PATTERNS = [
        # Standart pattern
        re.compile(
            r"\}\('(.*)',\s*(\d+),\s*(\d+),\s*'(.*?)'\.split\('\|'\)",
            re.IGNORECASE | re.MULTILINE | re.DOTALL
        ),
        # Daha gevşek pattern
        re.compile(
            r"\}\s*\(\s*['\"](.*?)['\"],\s*(\d+),\s*(\d+),\s*['\"](.+?)['\"]\.split\(['\"]\\?\|['\"]\)",
            re.IGNORECASE | re.MULTILINE | re.DOTALL
        ),
        # Eval formatı
        re.compile(
            r"eval\(function\(p,a,c,k,e,(?:r|d|)\)\{.*?return p\}(.*?\.split\('\|'\))",
            re.IGNORECASE | re.MULTILINE | re.DOTALL
        )
    ]

    # Kelime değiştirme deseni
    REPLACE_PATTERN = re.compile(
        r"\b\w+\b",
        re.IGNORECASE | re.MULTILINE
    )

    # Alfabeler
    ALPHABET = {
        52: "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP",
        54: "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQR",
        62: "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        95: " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    }

    @staticmethod
    def clean_escape_sequences(source: str) -> str:
        """Kaçış dizilerini temizler."""
        source = re.sub(r'\\\\', r'\\', source)
        source = source.replace("\\'", "'")
        source = source.replace('\\"', '"')
        return source

    @staticmethod
    def extract_arguments(source: str) -> tuple[str, list[str], int, int]:
        """P.A.C.K.E.R. formatındaki kaynak koddan argümanları çıkarır."""
        # Önce standart pattern ile dene
        match = Packer.PACKED_PATTERN.search(source)

        # Eğer bulunamazsa, alternatif pattern'leri dene
        if not match:
            for pattern in Packer.ALTERNATIVE_PATTERNS:
                match = pattern.search(source)
                if match:
                    break

        if not match:
            # Son çare: daha serbest bir string arama 
            if "'.split('|')" in source or '".split("|")' in source:
                # Manuel olarak parçalama işlemi yap
                try:
                    # Basit bir yaklaşım, çoğu vakada çalışır
                    parts = re.findall(r"\((['\"](.*?)['\"],\s*(\d+),\s*(\d+),\s*['\"](.*?)['\"]\.split", source)
                    if parts:
                        payload, radix, count, symtab = parts[0][1:]
                        return payload, symtab.split("|"), int(radix), int(count)
                except Exception:
                    pass

            raise ValueError("Invalid P.A.C.K.E.R. source format. Pattern not found.")

        # Eval formatını işle
        if len(match.groups()) == 1:
            # Eval formatı yakalandı, içeriği çıkar
            eval_content = match.group(1)
            if inner_match := re.search(r"\('(.*)',(\d+),(\d+),'(.*)'\)", eval_content):
                payload, radix, count, symtab = inner_match.groups()
            else:
                raise ValueError("Cannot extract arguments from eval pattern")
        else:
            # Standart format yakalandı
            payload, radix, count, symtab = match.groups()

        return payload, symtab.split("|"), int(radix), int(count)

    @staticmethod
    def unbase(value: str, base: int) -> int:
        """
        Verilen değeri belirtilen tabandan ondalık sayıya dönüştürür.
        Geniş taban desteği (2-95 arası) sağlar.
        """
        # Standart Python taban dönüşümü (2-36 arası)
        if 2 <= base <= 36:
            try:
                return int(value, base)
            except ValueError:
                return 0

        # Geniş taban desteği (37-95 arası)
        if base > 95:
            raise ValueError(f"Desteklenmeyen taban: {base}")

        # Uygun alfabeyi seç
        if base > 62:
            selector = 95
        elif base > 54:
            selector = 62
        elif base > 52:
            selector = 54
        else:
            selector = 52

        # Alfabeden karakter-indeks sözlüğü oluştur
        char_dict = {char: idx for idx, char in enumerate(Packer.ALPHABET[selector])}

        # Değeri dönüştür
        result = 0
        for index, char in enumerate(reversed(value)):
            digit = char_dict.get(char, 0)
            result += digit * (base ** index)

        return result
    
    @staticmethod
    def lookup_symbol(match: re.Match, symtab: list[str], radix: int) -> str:
        """Sembolleri arar ve yerine koyar."""
        word = match[0]

        try:
            index = Packer.unbase(word, radix)
            if 0 <= index < len(symtab):
                replacement = symtab[index]
                return replacement or word
        except (ValueError, IndexError):
            pass

        return word

    @staticmethod
    def unpack(source: str) -> str:
        """
        P.A.C.K.E.R. formatındaki sıkıştırılmış bir JavaScript kodunu çözer.
        Birden fazla format ve varyasyonu destekler.
        """
        # Kaçış dizilerini temizle
        source = Packer.clean_escape_sequences(source)

        # Argümanları çıkar
        try:
            payload, symtab, radix, count = Packer.extract_arguments(source)

            # Sembol tablosunun doğruluğunu kontrol et (ancak sıkı değil)
            if len(symtab) != count:
                print(f"Uyarı: Sembol tablosu sayısı ({len(symtab)}) ile belirtilen sayı ({count}) eşleşmiyor, ancak devam ediliyor.")

            # Kelimeleri değiştir ve sonucu döndür
            return Packer.REPLACE_PATTERN.sub(
                lambda match: Packer.lookup_symbol(match, symtab, radix), 
                payload
            )
        except Exception as e:
            # Detaylı hata mesajı
            raise ValueError(f"Unpacking failed: {str(e)}\nSource preview: {source[:100]}...")

    @staticmethod
    def detect_packed(source: str) -> bool:
        """Verilen kodun P.A.C.K.E.R. formatında sıkıştırılmış olup olmadığını kontrol eder."""
        # Standart pattern'i kontrol et
        if Packer.PACKED_PATTERN.search(source):
            return True

        # Alternatif pattern'leri kontrol et
        for pattern in Packer.ALTERNATIVE_PATTERNS:
            if pattern.search(source):
                return True

        # Yaygın belirteçleri kontrol et
        indicators = [
            ".split('|')",
            '.split("|")',
            "function(p,a,c,k,e,",
            "function(p, a, c, k, e, "
        ]

        return any(indicator in source for indicator in indicators)