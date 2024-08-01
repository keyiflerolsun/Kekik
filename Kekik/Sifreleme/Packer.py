# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import re

def unpack_packer(source: str) -> str:
    """https://github.com/beautifier/js-beautify/blob/main/python/jsbeautifier/unpackers/packer.py"""

    def clean_escape_sequences(source: str) -> str:
        source = re.sub(r'\\\\', r'\\', source)
        source = source.replace("\\'", "'")
        source = source.replace('\\"', '"')
        return source

    source = clean_escape_sequences(source)

    def extract_arguments(source: str) -> tuple[str, list[str], int, int]:
        match = re.search(r"}\('(.*)',(\d+),(\d+),'(.*)'\.split\('\|'\)", source, re.DOTALL)

        if not match:
            raise ValueError("Invalid P.A.C.K.E.R. source format.")

        payload, radix, count, symtab = match.groups()

        return payload, symtab.split("|"), int(radix), int(count)

    def convert_base(s: str, base: int) -> int:
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        return sum(alphabet.index(char) * (base**idx) for idx, char in enumerate(reversed(s)))

    payload, symtab, radix, count = extract_arguments(source)

    if count != len(symtab):
        raise ValueError("Malformed P.A.C.K.E.R. symtab.")

    def lookup_symbol(match: re.Match) -> str:
        word = match[0]

        return symtab[convert_base(word, radix)] or word

    unpacked_source = re.sub(r"\b\w+\b", lookup_symbol, payload)

    return unpacked_source