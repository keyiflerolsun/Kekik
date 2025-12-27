# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import re, base64

class StreamDecoder:
    """
    Stream tabanlı şifrelenmiş parçaları dinamik olarak çözmek için sınıf.
    Unpacked JS kodundan işlem sırasını parse eder ve uygular.
    """

    DEFAULT_SHIFT_CONST = 399756995

    def __init__(self, script_text: str):
        """
        Args:
            script_text: Unpacked JavaScript kodu
        """
        self.script_text = script_text
        self.shift_const = self._extract_shift_const()
        self.operations  = self._parse_operations()
        self.parts       = self._extract_parts()

    def _extract_shift_const(self) -> int:
        """Script'ten shift sabitini çıkar"""
        match = re.search(r'charCode-\((\d+)%\(i\+(\d+)\)', self.script_text)
        if match:
            return int(match.group(1))
        return self.DEFAULT_SHIFT_CONST

    def _parse_operations(self) -> list[str]:
        """
        JS kodundan işlem sırasını dinamik olarak parse eder.
        Desteklenen işlemler: reverse, atob (base64), shift
        """
        # Fonksiyon gövdesini bul
        fn_match = re.search(
            r'function\s+\w+\s*\(\s*value_parts\s*\)\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}',
            self.script_text
        )
        if not fn_match:
            return ["reverse", "base64", "base64", "shift"]

        fn_body    = fn_match.group(1)
        operations = []

        # İşlemleri sırasıyla tespit et
        # split('').reverse().join('') -> reverse
        # atob(...) -> base64
        # charCode-(CONST%(i+N)) -> shift

        # Satır satır analiz et
        statements = fn_body.split(';')
        for stmt in statements:
            stmt = stmt.strip()

            if "split('')" in stmt and "reverse()" in stmt and "join('')" in stmt:
                operations.append("reverse")
            elif "atob(" in stmt:
                operations.append("base64")
            elif "charCode" in stmt and "%" in stmt:
                operations.append("shift")

        return operations if operations else ["reverse", "base64", "base64", "shift"]

    def _extract_parts(self) -> list[str]:
        """Script'ten şifreli parçaları çıkar"""
        # Fonksiyon adını bul
        match_fn = re.search(r'function\s+(\w+)\s*\(\s*value_parts\s*\)', self.script_text)
        if not match_fn:
            raise Exception("decode fonksiyonu bulunamadı")

        fn_name = match_fn.group(1)

        # Array çağrısını bul
        array_call_regex = re.compile(rf'{re.escape(fn_name)}\(\s*\[(.*?)\]\s*\)', re.DOTALL)
        match_call = array_call_regex.search(self.script_text)
        if not match_call:
            raise Exception(f"{fn_name}(...) array bulunamadı")

        array_body = match_call.group(1)

        # String parçalarını topla
        parts = re.findall(r'["\']([^"\']+)["\']', array_body)
        if not parts:
            raise Exception("array string parçaları bulunamadı")

        return parts

    def _reverse(self, text: str) -> str:
        """Metni ters çevir"""
        return text[::-1]

    def _base64_decode(self, text: str) -> str:
        """Base64 decode"""
        try:
            return base64.b64decode(text).decode("latin1")
        except Exception:
            return text

    def _shift_unmix(self, text: str) -> str:
        """Pozisyon bazlı shift ile decode"""
        output = []
        for i, ch in enumerate(text):
            char_code = ord(ch)
            char_code = (char_code - (self.shift_const % (i + 5)) + 256) % 256
            output.append(chr(char_code))
        return ''.join(output)

    def decode(self) -> str:
        """Parse edilen işlemleri sırasıyla uygula"""
        result = ''.join(self.parts)

        for op in self.operations:
            if op == "reverse":
                result = self._reverse(result)
            elif op == "base64":
                result = self._base64_decode(result)
            elif op == "shift":
                result = self._shift_unmix(result)

        return result

    @classmethod
    def extract_stream_url(cls, script_text: str) -> str:
        """
        Unpacked JS kodundan stream URL'sini çıkar.
        
        Args:
            script_text: Unpacked JavaScript kodu
            
        Returns:
            Decoded stream URL
        """
        decoder = cls(script_text)
        return decoder.decode()
