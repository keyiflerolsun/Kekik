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


# veri = r'''
# jwSetup.sources=[{"default":true,"file":"\x68\x74\x74\x70\x73\x3a\x2f\x2f\x64\x32\x2e\x69\x6d\x61\x67\x65\x73\x70\x6f\x74\x2e\x62\x75\x7a\x7a\x2f\x66\x32\x2f\x4e\x74\x4f\x31\x4e\x51\x5a\x6a\x44\x51\x41\x6b\x78\x6c\x58\x45\x47\x33\x6c\x62\x66\x62\x30\x31\x79\x74\x70\x57\x66\x4e\x30\x66\x62\x66\x50\x58\x5a\x55\x31\x6a\x50\x77\x5a\x6d\x48\x71\x58\x41\x37\x6c\x6d\x6d\x4b\x67\x47\x59\x31\x66\x47\x42\x6d\x6c\x38\x68\x32\x7a\x33\x4f\x5a\x69\x4f\x63\x4c\x6b\x51\x70\x7a\x57\x78\x4b\x45\x4c\x57\x42\x63\x79\x4d\x74\x75\x55\x44\x57\x46\x4e\x6c\x69\x64\x70\x46\x46\x65\x6e\x65\x64\x66\x48\x30\x69\x74\x66\x59\x67\x38\x52\x47\x41\x6b\x38\x6c\x76\x72\x31","label":"0","type":"hls","preload":"none"}];var mu=getLocation(jwSetup.sources[0].file);
# '''

# escaped_hex  = re.findall(r'file":"(.*)","label', veri)[0]
# print(HexCodec.decode(escaped_hex))