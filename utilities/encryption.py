from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

class Encryption:
    @classmethod
    def _generate_key(cls, plaintext_key: str, salt: bytes) -> bytes:
        """Generates and returns a fixed-length key from the given plaintext password."""

        # 16 bytes is the key length required by AES-128-GCM
        key_length = 16

        # recommended parameters for file encryption
        cost, block_size, parallelization = 2**20, 8, 1

        return scrypt(plaintext_key, salt, key_length, cost, block_size, parallelization)

    @classmethod
    def encrypt(cls, payload: bytes, plaintext_key: str) -> bytes:
        """Encrypts the given payload with the key.
        Returns bytes containing everything needed for decryption (apart from key)."""

        key_salt = get_random_bytes(16)
        key = Encryption._generate_key(plaintext_key, key_salt)

        nonce = get_random_bytes(12)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=16)
        ciphertext, tag = cipher.encrypt_and_digest(payload)

        # lengths 12, 16, 16, variable
        return cipher.nonce + tag + key_salt + ciphertext

    @classmethod
    def decrypt(cls, seal: bytes, plaintext_key: str) -> bytes:
        """Decrypts the given seal with the key.
        Returns payload bytes, or `None` if unsuccessful."""

        # split the seal into components needed in decryption
        nonce, tag, key_salt, ciphertext = seal[:12], seal[12:28], seal[28:44], seal[44:]

        key = Encryption._generate_key(plaintext_key, key_salt)

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        try:
            return cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError:
            return None
