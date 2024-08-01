# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Crypto.Cipher       import AES
from Crypto.Util.Padding import unpad
from hmac                import new as hmac
from hashlib             import sha256
from base64              import b64decode, b64encode
from json                import dumps

class NaysHash:
    """
    HMAC-SHA256 hash üretimi ve API token'ı oluşturma işlemleri için bir sınıf.
    Şifreleme ve hash işlemlerinde kullanılan anahtarlar ve yöntemler hakkında bilgi sağlar.
    # ! https://gist.github.com/keyiflerolsun/e91c6d6f19e79b5cd4cbc73833f74e72
    """
    def __init__(self, default_key:str="+KbPdSgVkYp3s6v9y=B&E)H@McQfThWm", application_key:str="y3o2R7UZg13nVqFAg+B9IVj61M62CLJSw0kPoy3RBJ9kISt0MSU9BBDy7SBUL7MK") -> None:
        # HMAC için kullanılacak anahtarı deşifrele
        self.hmac_key = self.decrypt_aes_cbc_pkcs7(
            encrypted_text = application_key,
            secret_key     = default_key
        )

    def decrypt_aes_cbc_pkcs7(self, encrypted_text:str, secret_key:str) -> str:
        # Şifrelenmiş metni ve anahtarı bayt dizisine çevir
        encrypted_text_bytes = b64decode(encrypted_text.encode("utf-8"))
        key_bytes            = secret_key.encode("utf-8")

        # İlk vektörü (IV) ve şifre çözücüyü (cipher) oluştur
        iv     = key_bytes[:16]
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)

        # Metni deşifre et
        decrypted_bytes = unpad(cipher.decrypt(encrypted_text_bytes), AES.block_size)
        return decrypted_bytes.decode("utf-8")

    def generate_hash_with_hmac256(self, msg:str):
        # Verilen mesaj için HMAC-SHA256 hash oluştur
        hmac256_hash = hmac(
            key       = self.hmac_key.encode("utf-8"), 
            msg       = msg.encode("utf-8"),
            digestmod = sha256
        )

        return b64encode(hmac256_hash.digest()).decode("utf-8")

    def generate_xtoken(self, endpoint:str, payload:dict, timestamp:int) -> str:
        # API isteği için "xtoken" oluştur
        return self.generate_hash_with_hmac256(
            f"{endpoint}{dumps(payload, ensure_ascii=False, sort_keys=False)}{timestamp}".replace(" ", "")
        )