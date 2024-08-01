# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib, base64

class CryptoJS:
    """
    Paroladan türetilmiş anahtar ile AES/CBC/PKCS7Padding şifreleme ve şifre çözme işlemleri için bir sınıf.
    CryptoJS AES yöntemine uygundur.
    ! » https://gist.github.com/thackerronak/554c985c3001b16810af5fc0eb5c358f
    """
    KEY_SIZE    = 32
    IV_SIZE     = 16
    HASH_CIPHER = "AES/CBC/PKCS7Padding"
    AES_MODE    = AES.MODE_CBC
    KDF_DIGEST  = "md5"
    APPEND      = b"Salted__"

    @staticmethod
    def evp_kdf(password, salt, key_size=32, iv_size=16, iterations=1, hash_algorithm="md5"):
        """Paroladan Anahtar ve IV oluşturmak için bir KDF fonksiyonu."""
        target_key_size = key_size + iv_size
        derived_bytes   = b""
        block           = None

        while len(derived_bytes) < target_key_size:
            hasher = hashlib.new(hash_algorithm)
            if block:
                hasher.update(block)
    
            hasher.update(password)
            hasher.update(salt)
            block = hasher.digest()

            for _ in range(1, iterations):
                block = hashlib.new(hash_algorithm, block).digest()
    
            derived_bytes += block

        return derived_bytes[:key_size], derived_bytes[key_size:key_size + iv_size]

    @staticmethod
    def encrypt(password, plain_text):
        """Verilen metni AES/CBC/PKCS7Padding şifreleme yöntemi ile şifreler."""
        salt    = CryptoJS.generate_salt(8)
        key, iv = CryptoJS.evp_kdf(password.encode("utf-8"), salt, key_size=CryptoJS.KEY_SIZE, iv_size=CryptoJS.IV_SIZE)

        cipher      = AES.new(key, CryptoJS.AES_MODE, iv)
        cipher_text = cipher.encrypt(CryptoJS._pad(plain_text.encode("utf-8")))

        # Create CryptoJS-like encrypted output
        encrypted_data = CryptoJS.APPEND + salt + cipher_text

        return base64.b64encode(encrypted_data).decode("utf-8")

    @staticmethod
    def decrypt(password, cipher_text):
        """Verilen şifreli metni AES/CBC/PKCS7Padding şifreleme yöntemi ile çözer."""
        ct_bytes          = base64.b64decode(cipher_text)
        salt              = ct_bytes[8:16]
        cipher_text_bytes = ct_bytes[16:]

        key, iv = CryptoJS.evp_kdf(password.encode("utf-8"), salt, key_size=CryptoJS.KEY_SIZE, iv_size=CryptoJS.IV_SIZE)

        cipher     = AES.new(key, CryptoJS.AES_MODE, iv)
        plain_text = cipher.decrypt(cipher_text_bytes)

        return CryptoJS._unpad(plain_text).decode("utf-8")

    @staticmethod
    def _pad(s):
        """Veriyi AES blok boyutuna göre doldurur (PKCS7)."""
        block_size = AES.block_size
        padding    = block_size - len(s) % block_size

        return s + bytes([padding] * padding)

    @staticmethod
    def _unpad(s):
        """Dolguyu kaldırır (PKCS7)."""
        return s[:-ord(s[-1:])]

    @staticmethod
    def generate_salt(length):
        """Belirtilen uzunlukta rastgele bir tuz oluşturur."""
        return get_random_bytes(length)