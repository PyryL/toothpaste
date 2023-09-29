import unittest
from random import seed, randbytes
from utilities.encryption import Encryption

class TestEncryption(unittest.TestCase):
    def test_data_does_not_change_during_encryption(self):
        payload = "my UTF-8 ṡŧ𝔯ĩȵɠ"
        key = "mys€cr3tKEY".encode("utf-8")
        seal = Encryption.encrypt(payload.encode("utf-8"), key)
        plaintext = Encryption.decrypt(seal, key).decode("utf-8")
        self.assertEqual(payload, plaintext)

    def test_encryption_with_empty_payload(self):
        key = "helloworld".encode("utf-8")
        seal = Encryption.encrypt("".encode("utf-8"), key)
        decrypted = Encryption.decrypt(seal, key).decode("utf-8")
        self.assertEqual(decrypted, "")

    def test_encryption_with_long_payload(self):
        seed(42)
        payload = randbytes(100_000)
        key = "helloworld".encode("utf-8")
        seal = Encryption.encrypt(payload, key)
        decrypted = Encryption.decrypt(seal, key)
        self.assertEqual(payload, decrypted)
