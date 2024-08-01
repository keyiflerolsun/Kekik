# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

class HexCodec:
    @staticmethod
    def encode(utf8_string: str) -> str:
        """UTF-8 stringini kaçış dizileriyle birlikte hex stringine dönüştürür."""
        byte_data   = utf8_string.encode("utf-8")
        hex_string  = byte_data.hex()
        escaped_hex = "\\x".join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))

        return f"\\x{escaped_hex}"

    @staticmethod
    def decode(escaped_hex: str) -> str:
        """Kaçış dizileri içeren bir hex stringini UTF-8 formatındaki stringe dönüştürür."""
        hex_string = escaped_hex.replace("\\x", "")
        byte_data  = bytes.fromhex(hex_string)

        return byte_data.decode("utf-8")