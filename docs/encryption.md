# Encryption

Optionally, paste modifyers can encrypt paste content with a key.
The key is not stored anywhere, so forgetting it leads to loss of the paste.
Only paste content will be encrypted, but title, votes and chat messages will not.

## Threat model

Encryption on ToothPaste should be considered as one extra layer of security. The feature is designed against hackers and other malicious actors trying to access the database. Even if they succeed, they can not recover the content.

The encryption feature is not, however, designed against law-enforcement or site administrators. Even though it may provide some protection against them, there are still multiple ways (e.g. side-channel attack) they can access the paste content.

## Parameters

* Algorithm: `AES-128-GCM` (relatively secure and wide-spread<sup>[3]</sup>)
* Nonce: 12 bytes (recommendation<sup>[1]</sup>)
* MAC tag length: 16 bytes (default<sup>[1]</sup>)

Used encryption algorithm requires key length to be multipla of 16. It would be inconvenient to require user input a key meeting this requirement, so a suitable key is derived from the user-inputted variable-length plaintext key.

* Algorithm: `scrypt`
* Salt length: 16 bytes (meets recommendation<sup>[2]</sup>)
* Output key length: 32 bytes (largest of the supported options<sup>[4]</sup>)
* Cost parameter: 2^20 (recommendation<sup>[2]</sup>)
* Block size: 8 (recommendation<sup>[2]</sup>)
* Parallelization parameter: 1 (recommendation<sup>[2]</sup>)

## Seal

After encryption, relevant data is gathered together into so-called seal. It is a byte array consisting of four parts: nonce, tag, key salt and ciphertext. The first three have fixed length (12, 16, 16 bytes), so there is no need for separator and parts can just be joined. Seal is then encoded into hex string and saved to database, from where it can be later read and decrypted.

## Sources

1. [https://pycryptodome.readthedocs.io/en/latest/src/cipher/modern.html#gcm-mode](https://pycryptodome.readthedocs.io/en/latest/src/cipher/modern.html#gcm-mode) (accessed 2023-09-29)
2. [https://pycryptodome.readthedocs.io/en/latest/src/protocol/kdf.html#scrypt](https://pycryptodome.readthedocs.io/en/latest/src/protocol/kdf.html#scrypt) (accessed 2023-09-29)
3. [https://en.wikipedia.org/wiki/Galois/Counter_Mode](https://en.wikipedia.org/wiki/Galois/Counter_Mode) (accessed 2023-09-29)
4. [https://en.wikipedia.org/wiki/Advanced_Encryption_Standard](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) (accessed 2023-09-29)
