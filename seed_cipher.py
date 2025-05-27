import os
from typing import Dict
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_pad, hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding as rsa_pad


class DataEncryptor:
    @staticmethod
    def encrypt_content(config: Dict[str, str]) -> None:
        print("[*] Загрузка зашифрованного ключа...")
        with open(config['encoded_sym_key'], 'rb') as file:
            encrypted_key = file.read()

        print("[*] Загрузка закрытого RSA ключа...")
        with open(config['rsa_private'], 'rb') as file:
            private_key = load_pem_private_key(file.read(), password=None)

        print("[*] Дешифровка симметричного ключа...")
        sym_key = private_key.decrypt(
            encrypted_key,
            rsa_pad.OAEP(mgf=rsa_pad.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None)
        )

        print("[*] Чтение исходного файла...")
        with open(config['plain_data'], 'rb') as file:
            original = file.read()

        padder = sym_pad.ANSIX923(128).padder()
        padded = padder.update(original) + padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.SEED(sym_key), modes.CBC(iv))
        encrypted = cipher.encryptor().update(padded) + cipher.encryptor().finalize()

        with open(config['encrypted_data'], 'wb') as file:
            file.write(iv + encrypted)

        print("[+] Данные зашифрованы и записаны.")

    @staticmethod
    def decrypt_content(config: Dict[str, str]) -> None:
        print("[*] Чтение зашифрованного ключа...")
        with open(config['encoded_sym_key'], 'rb') as file:
            encrypted_key = file.read()

        print("[*] Загрузка приватного ключа...")
        with open(config['rsa_private'], 'rb') as file:
            private_key = load_pem_private_key(file.read(), password=None)

        print("[*] Дешифровка симметричного ключа...")
        sym_key = private_key.decrypt(
            encrypted_key,
            rsa_pad.OAEP(mgf=rsa_pad.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None)
        )

        print("[*] Загрузка зашифрованного содержимого...")
        with open(config['encrypted_data'], 'rb') as file:
            data = file.read()

        iv = data[:16]
        encrypted_content = data[16:]

        cipher = Cipher(algorithms.SEED(sym_key), modes.CBC(iv))
        decrypted_padded = cipher.decryptor().update(encrypted_content) + cipher.decryptor().finalize()

        unpadder = sym_pad.ANSIX923(128).unpadder()
        result = unpadder.update(decrypted_padded) + unpadder.finalize()

        with open(config['decrypted_output'], 'wb') as file:
            file.write(result)

        print("[+] Файл успешно расшифрован.")
