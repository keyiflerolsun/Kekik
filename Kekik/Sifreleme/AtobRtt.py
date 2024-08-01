# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import base64

def atob(s:str) -> str:
    return base64.b64decode(s).decode("utf-8")

def rtt(s:str) -> str:
    def rot13_char(c):
        if "a" <= c <= "z":
            return chr((ord(c) - ord("a") + 13) % 26 + ord("a"))
        elif "A" <= c <= "Z":
            return chr((ord(c) - ord("A") + 13) % 26 + ord("A"))
        return c

    return "".join(rot13_char(c) for c in s)