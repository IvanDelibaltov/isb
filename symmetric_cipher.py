from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_pad
import os


class SymmetricCipher:
    @staticmethod
    def encrypt(data: bytes, key: bytes) -> bytes:
        padder = sym_pad.ANSIX923(128).padder()
        padded = padder.update(data) + padder.finalize()
        iv = os.urandom(16)
        cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
        encrypted = cipher.encryptor().update(padded) + cipher.encryptor().finalize()
        return iv + encrypted

    @staticmethod
    def decrypt(encrypted_data: bytes, key: bytes) -> bytes:
        iv = encrypted_data[:16]
        content = encrypted_data[16:]
        cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
        decrypted_padded = cipher.decryptor().update(content) + cipher.decryptor().finalize()
        unpadder = sym_pad.ANSIX923(128).unpadder()
        return unpadder.update(decrypted_padded) + unpadder.finalize()
