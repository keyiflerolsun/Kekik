# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from json                import loads, dumps
from Crypto.Hash         import MD5
from Crypto.Cipher       import AES
from Crypto.Random       import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64              import b64encode, b64decode

class AESManager:
    """
    AES/CBC/PKCS5Padding şifreleme ve çözme işlemleri için bir sınıf.
    """
    @staticmethod
    def generate_key_and_iv(password, salt, key_length=32, iv_length=16, iterations=1):
        """Anahtar ve IV oluşturmak için bir KDF fonksiyonu."""
        derived_key_iv = b""
        previous_block = b""

        while len(derived_key_iv) < key_length + iv_length:
            current_block = MD5.new(previous_block + password.encode() + salt).digest()

            for _ in range(1, iterations):
                current_block = MD5.new(current_block).digest()

            derived_key_iv += current_block
            previous_block = current_block

        key = derived_key_iv[:key_length]
        iv  = derived_key_iv[key_length:key_length + iv_length]

        return key, iv

    @staticmethod
    def hex_to_bytes(hex_str):
        """Hex string'i byte array'e çevirir."""
        return bytes.fromhex(hex_str)

    @staticmethod
    def encrypt(plain_text, password):
        """Verilen metni AES/CBC/PKCS5Padding şifreleme yöntemi ile şifreler."""
        salt    = get_random_bytes(8)
        key, iv = AESManager.generate_key_and_iv(password, salt)

        cipher   = AES.new(key, AES.MODE_CBC, iv)
        ct_bytes = cipher.encrypt(pad(plain_text.encode("utf-8"), AES.block_size))
        
        return dumps({
            "ct" : b64encode(ct_bytes).decode("utf-8"),
            "iv" : iv.hex(),
            "s"  : salt.hex()
        })

    @staticmethod
    def decrypt(crypted_data, password):
        """Verilen şifreli metni AES/CBC/PKCS5Padding şifreleme yöntemi ile çözer."""
        data = loads(crypted_data)
        salt = AESManager.hex_to_bytes(data["s"])
        iv   = AESManager.hex_to_bytes(data["iv"])
        
        key, iv = AESManager.generate_key_and_iv(password, salt, iv_length=len(iv))

        cipher    = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(b64decode(data["ct"])), AES.block_size)

        return decrypted.decode("utf-8")