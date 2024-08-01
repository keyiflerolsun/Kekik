# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Crypto.Cipher import AES
import hashlib, base64

class CryptoJS:
    """
    AES-256 encryption and decryption with key derivation from a password using a KDF (Key Derivation Function).
    Source: https://gist.github.com/thackerronak/554c985c3001b16810af5fc0eb5c358f
    """
    KEY_SIZE    = 32
    IV_SIZE     = 16
    HASH_CIPHER = "AES/CBC/PKCS7Padding"
    AES_MODE    = AES.MODE_CBC
    KDF_DIGEST  = "md5"
    APPEND      = b"Salted__"

    @staticmethod
    def evp_kdf(password, salt, key_size=32, iv_size=16, iterations=1, hash_algorithm="md5"):
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
    def decrypt(password, cipher_text):
        ct_bytes          = base64.b64decode(cipher_text)
        salt              = ct_bytes[8:16]
        cipher_text_bytes = ct_bytes[16:]

        key, iv = CryptoJS.evp_kdf(password.encode("utf-8"), salt, key_size=CryptoJS.KEY_SIZE, iv_size=CryptoJS.IV_SIZE)

        cipher     = AES.new(key, CryptoJS.AES_MODE, iv)
        plain_text = cipher.decrypt(cipher_text_bytes)

        return CryptoJS._unpad(plain_text).decode("utf-8")

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[-1:])]