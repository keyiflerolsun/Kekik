# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import re, base64, itertools

class StreamDecoder:
    """ Stream tabanlı şifrelenmiş parçaları brute-force yöntemiyle çözmek için sınıf. """

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
                # Harf değilse olduğu gibi ekle
                transformed_chars.append(char)

        return ''.join(transformed_chars)

    @staticmethod
    def _reverse(text: str) -> str:
        # Metni ters çevir
        return text[::-1]

    @staticmethod
    def _shift_back(text: str) -> str:
        # Her karakterin ASCII değerini pozisyona bağlı olarak kaydırarak geri al
        output_chars = []
        for index, ch in enumerate(text):
            code     = ord(ch)
            shift    = StreamDecoder.SHIFT_CONST % (index + 5)
            restored = (code - shift + 256) % 256
            output_chars.append(chr(restored))

        return ''.join(output_chars)

    @staticmethod
    def _base64_decode(text: str):
        # Base64 çözme işlemi
        try:
            decoded_bytes = base64.b64decode(text)
            return decoded_bytes.decode("latin1")
        except Exception:
            return None

    @staticmethod
    def _brute_force(value_parts: list[str]):
        """
        value_parts dizisini 24 farklı sıralamada çözer.
        En okunabilir (printable) sonuca göre en olası doğru çözümü döndürür.
        """

        joined = ''.join(value_parts)   # ! Parçaları birleştir

        # ! Kullanılan işlem adımları
        operations = {
            "B64D": StreamDecoder._base64_decode,
            "ROT" : StreamDecoder._rot13,
            "REV" : StreamDecoder._reverse,
            "SHF" : StreamDecoder._shift_back,
        }

        results = []

        # ! 24 farklı sıralamayı dene
        for order in itertools.permutations(operations.keys()):

            text = joined
            valid = True

            # Sıradaki her fonksiyonu uygula
            for op_name in order:
                func = operations[op_name]
                text = func(text)

                # Eğer bir adım çökerse bu sıra geçersizdir
                if text is None:
                    valid = False
                    break

            if valid:
                # ! Okunabilirlik oranı hesapla
                printable = sum(1 for c in text if 32 <= ord(c) <= 126)
                ratio = printable / max(1, len(text))

                results.append((order, text, ratio))

        # ! Sonuçları en okunabilirden başlayarak sırala
        results.sort(key=lambda x: x[2], reverse=True)

        # ! İlk 10 olası sonucu ekrana dökelim
        # print("\n### Olası Çözümler ###\n")
        # for order, text, ratio in results[:10]:
        #     print(f"Sıra: {' → '.join(order)} | Okunabilirlik: %{ratio*100:.1f}")
        #     print(f"Çözüm: {text}\n" + "-" * 60)

        # ! En iyi sonucu döndür
        if results:
            return results[0][1]

        return None

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
        return StreamDecoder._brute_force(parts)

