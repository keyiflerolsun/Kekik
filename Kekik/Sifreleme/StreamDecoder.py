# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import re, base64

class StreamDecoder:
    """ Stream tabanlı şifreleme ve çözme işlemleri için yardımcı sınıf. """

    # Sabit kaydırma değeri
    SHIFT_CONST = 399756995

    @staticmethod
    def _rot13(text: str) -> str:
        transformed_chars = []

        for char in text:
            ascii_code = ord(char)

            # Büyük harf aralığı (A-Z)
            if 65 <= ascii_code <= 90:
                rotated = chr((ascii_code - 65 + 13) % 26 + 65)
                transformed_chars.append(rotated)

            # Küçük harf aralığı (a-z)
            elif 97 <= ascii_code <= 122:
                rotated = chr((ascii_code - 97 + 13) % 26 + 97)
                transformed_chars.append(rotated)

            else:
                # Harf değilse direkt ekle
                transformed_chars.append(char)

        return ''.join(transformed_chars)

    @staticmethod
    def decrypt(value_parts: list[str]) -> str:
        # Parçaları birleştir ve ters çevir
        joined = ''.join(value_parts)
        reversed_value = joined[::-1]

        # Base64 çözümlemesi
        decoded_bytes = base64.b64decode(reversed_value)
        decoded_text  = decoded_bytes.decode("latin1")

        # ROT13 çözümlemesi
        rot_text = StreamDecoder._rot13(decoded_text)

        # index'e göre karakter kaydırma
        output_chars = []
        for index, ch in enumerate(rot_text):
            code = ord(ch)
            shift = StreamDecoder.SHIFT_CONST % (index + 5)
            restored = (code - shift + 256) % 256
            output_chars.append(chr(restored))

        return ''.join(output_chars)

    @staticmethod
    def encrypt(plain_text: str, split_length: int = 10) -> list[str]:
        # Karakterleri karıştır
        mixed_chars = []
        for index, ch in enumerate(plain_text):
            code = ord(ch)
            shift = StreamDecoder.SHIFT_CONST % (index + 5)
            new_code = (code + shift) % 256
            mixed_chars.append(chr(new_code))

        # Karakterleri birleştir
        mixed_text = ''.join(mixed_chars)

        # ROT13 şifrelemesi
        rot_text = StreamDecoder._rot13(mixed_text)

        # Base64 şifrelemesi
        encoded_bytes = rot_text.encode("latin1")
        base64_text   = base64.b64encode(encoded_bytes).decode("latin1")

        # Metni ters çevir
        reversed_text = base64_text[::-1]

        # Belirtilen uzunlukta parçalara ayır
        return [
            reversed_text[i:i + split_length]
                for i in range(0, len(reversed_text), split_length)
        ]

    @staticmethod
    def extract_stream_url(script_text: str) -> str:
        # 1) Decode fonksiyonunun adını bul: function <NAME>(value_parts)
        match_fn = re.search(
            r'function\s+(\w+)\s*\(\s*value_parts\s*\)',
            script_text
        )
        if not match_fn:
            raise Exception("decode fonksiyonu bulunamadı")

        fn_name = match_fn.group(1)

       # 2) Bu fonksiyonun array ile çağrıldığı yeri bul: <NAME>([ ... ])
        array_call_regex = re.compile(
            rf'{re.escape(fn_name)}\(\s*\[(.*?)\]\s*\)',
            re.DOTALL
        )
        match_call = array_call_regex.search(script_text)
        if not match_call:
            raise Exception(f"{fn_name}(...) array bulunamadı")

        array_body = match_call.group(1)

        # 3) Array içindeki string parçalarını topla: "..." veya '...'
        parts = re.findall(r'["\']([^"\']+)["\']', array_body)
        if not parts:
            raise Exception("array string parçaları bulunamadı")

        # 4) Decode et
        return StreamDecoder.decrypt(parts)
