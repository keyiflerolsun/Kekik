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
        escaped_hex = escaped_hex.strip().replace("\\X", "\\x")

        if isinstance(escaped_hex, str) and not escaped_hex.startswith(r"\x"):
            return escaped_hex.encode("unicode_escape").decode("utf-8")

        hex_string = escaped_hex.replace("\\x", "")
        byte_data  = bytes.fromhex(hex_string)

        return byte_data.decode("utf-8")