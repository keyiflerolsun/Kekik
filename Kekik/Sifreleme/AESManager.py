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



# veri = r'''
#   $(document).ready(function() {
#     bePlayer('S3JScTBsNzMyYlFSMHg4NG5vQXNjUT09', '{"ct":"SjkWeIotWbL6TmnwyhkeLy6wAWvEG1pz8R0g+IsLN6P1vo9WvXuiqqDal5g6FXW3Td+Q+1DIGQAt3sNxydOAr4p3uFxxpVPUwIMwLWzw+5m0ED0tno1KU0\/rCXRwq6ATvmrIqSr+qb95hY0wjm3gfjPsxDn4vJ1fcdiRwrfC38MjfKyJFN3\/n\/xLvNT4vgQJTYTEmNOzFZgEIhsSRFiW1\/8nQCaS\/8Xkw0ySUqLvzSMsVf2SSgXyESxyksn3+kz9KqEI+mQpJFUcLSBz8VKXly+tEcYGpTQChzceyudkZcEGvppKheBAarEQ6e3eR9d04gQcFpEaV+QmHODvI1Ql\/pJ1FSAh9F5ZDtF00XDSLZbIEt00PWRkgfc3kxuNQzcC1C6BULNdoGwHbvo5W6uUsMwxG+sn+EH7B7jWtyhx5VHKpIfkyrjC10+K\/hG29bkS3YNSTaDxJnTa3jj1usbwwMX0A7wApIlce4rEVgWpO5y1ZuiJ+tEE3kH1InUzT1jfY4Y0KrZ5X+p2nrQhJrDOxfDy\/GhaidNmmpfuzF6Iniko6sCGa0QRbhVB8ZbrC9qFB\/sk47ZOP1IHPY\/jCh4BTFMDCy1Qx1\/PbVLZzNLHju\/cLYRzS0vJp5aqkwg\/QNCo1q5HrxXL32lMLNOcWPRDqyZaMpiYP+LzJPVndLsqGlfKJWETuKonEqc4r4M0Eu\/bTji\/S7zQ7bvEPuT3PyIRWXDffuNSX6+nqWFD8LM\/iNyc1cC3bMi+p0TR3YZu1MlIvxjYPK0lYtDvd+vaYgCotFm0lLsqg5cuw3pGb8jnEfM1VzEqDcBvBTkRKrxIao\/WWdvGf1MCmTsr+nVH0sT8PTrh6XcoG7hV\/+y8XCsEj2LKWtDtfK+RxSztteXYUUUI9NVtCvjlW\/b8+h6u+B\/CNLtrwoDQzKhTVZ1rZbe\/TP+HR7SkMXYqyAX3qqiyi9s+TrcqkxdbAHzkjr0q2DshtUeipcL5HVrdxL28iXqtYMT\/ytsRCQHpnswNGqW+D47VAYtDl4VafSaNGUMPfu6nq4k0\/FrxtYkts4lE9YUkueQHip8eOFO8dxTp8O7+Civt88C45wEjBHqaiN+n6wm1+3xUy2hKX0PD4gvlPuUeoHDbm\/HLUlPYmGw5cCEAskuJRXdW+gnFB6XzVIKrF7OUtd2yLqSLhnWcSFkMJoPDuIezn1D60pMi8LlJKb1HXwbPRRcqh00\/bFNdmodGpwybcaeegvRaCJbDqd6fmQUxG1ir9o5O8st2\/oJ9\/HivYvxi\/sicZYNzFtuZFGC\/ubPK5Ld9RsJb\/RQ9rkTZzhkBnmM=","iv":"2fedfd8ae68165490f274b521d5a3291","s":"74a525e8e5746772"}');
#   });
# '''

# be_player      = re.search(r"bePlayer\('([^']+)',\s*'(\{[^\}]+\})'\);", veri).groups()
# be_player_pass = be_player[0]
# be_player_data = be_player[1]

# print(json.loads(AESManager.decrypt(be_player_data, be_player_pass).replace("\\", "")))