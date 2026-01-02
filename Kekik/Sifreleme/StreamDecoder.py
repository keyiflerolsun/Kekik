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
        Statement bazlı analiz yaparak gerçek sırayı tespit eder.
        """
        # Fonksiyon başlangıcını bul
        fn_start = re.search(r'function\s+\w+\s*\(\s*value_parts\s*\)\s*\{', self.script_text)
        if not fn_start:
            return ["reverse", "base64", "base64", "shift"]
        
        # Nested braces'i sayarak fonksiyon gövdesini çıkar
        start_pos = fn_start.end()
        brace_count = 1
        pos = start_pos

        while pos < len(self.script_text) and brace_count > 0:
            if self.script_text[pos] == '{':
                brace_count += 1
            elif self.script_text[pos] == '}':
                brace_count -= 1
            pos += 1

        fn_body = self.script_text[start_pos:pos-1]
        
        # Statement'lara ayır (;'e göre)
        statements = fn_body.split(';')
        operations = []
        
        for stmt in statements:
            stmt = stmt.strip()
            if not stmt:
                continue
            
            # Reverse işlemi: .split('').reverse().join('')
            if '.reverse()' in stmt and '.split(' in stmt and '.join(' in stmt:
                operations.append("reverse")
                continue
            
            # Sadece reverse (split-join olmadan)
            if '.reverse()' in stmt and '.split(' not in stmt:
                operations.append("reverse")
                continue
            
            # Base64 decode: atob(...)
            # Bir statement'ta birden fazla atob olabilir
            atob_count = stmt.count('atob(')
            for _ in range(atob_count):
                operations.append("base64")
            if atob_count > 0:
                continue
            
            # ROT13: replace ile charCodeAt(0)+13 veya -13
            if 'replace(' in stmt and ('charCodeAt(0)+13' in stmt or 'charCodeAt(0)-13' in stmt):
                operations.append("rot13")
                continue
            
            # Shift unmix: for loop içinde charCode manipülasyonu
            if 'for(' in stmt and 'charCode' in stmt and '%' in stmt:
                operations.append("shift")
                continue
        
        # Eğer for loop ayrı statement olarak algılanmadıysa, fn_body'de ara
        if 'shift' not in operations and 'for(' in fn_body and 'charCode' in fn_body:
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
        """
        Base64 decode - JavaScript atob() davranışını taklit eder.
        Her byte'ı direkt karaktere çevirir (chr(byte)), latin1 decode kullanmaz.
        Bu, double base64 decode işlemlerinin düzgün çalışmasını sağlar.
        """
        try:
            # Padding ekle (JS atob padding gerektirmez ama Python gerektirir)
            padding = 4 - len(text) % 4
            if padding != 4:
                text += '=' * padding
            
            decoded_bytes = base64.b64decode(text)
            # JS atob davranışı: her byte'ı direkt karaktere çevir
            return ''.join(chr(b) for b in decoded_bytes)
        except Exception:
            return text
    
    def _rot13_decode(self, text: str) -> str:
        """ROT13 decode (Caesar cipher with shift of 13)"""
        result = []
        for char in text:
            if 'a' <= char <= 'z':
                result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
            else:
                result.append(char)
        return ''.join(result)

    def _shift_unmix(self, text: str) -> str:
        """Pozisyon bazlı shift ile decode"""
        output = []
        for i, ch in enumerate(text):
            char_code = ord(ch)
            shifted = (char_code - (self.shift_const % (i + 5)) + 256) % 256
            output.append(shifted)
        
        try:
            return bytes(output).decode('utf-8', errors='ignore')
        except Exception:
            try:
                return bytes(output).decode('latin1')
            except Exception:
                return bytes(output).decode('ascii', errors='ignore')

    def decode(self) -> str:
        """Parse edilen işlemleri sırasıyla uygula"""
        result = ''.join(self.parts)

        for op in self.operations:
            if op == "reverse":
                result = self._reverse(result)
            elif op == "base64":
                result = self._base64_decode(result)
            elif op == "rot13":
                result = self._rot13_decode(result)
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
