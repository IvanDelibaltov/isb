import json
import os
import argparse
from cryptography.hazmat.primitives import serialization


class AppTools:
    @staticmethod
    def load_config() -> dict:
        try:
            with open('settings.json', 'r') as cfg:
                return json.load(cfg)
        except FileNotFoundError:
            print("[!] Не удалось найти settings.json.")
            exit(1)

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser(description="Гибридная криптосистема")
        mode = parser.add_mutually_exclusive_group(required=True)
        mode.add_argument('-gen', '--create_keys', action='store_true', help='Создание ключей')
        mode.add_argument('-enc', '--encrypt', action='store_true', help='Шифрование')
        mode.add_argument('-dec', '--decrypt', action='store_true', help='Дешифрование')
        return parser.parse_args()


class FileControl:
    @staticmethod
    def ensure_exists(paths: list):
        for file in paths:
            if not os.path.exists(file):
                print(f"[!] Не найден файл: {file}")
                exit(1)

    @staticmethod
    def save_pub_key(pub_key):
        with open("rsa_pub_key.txt", 'wb') as out:
            out.write(pub_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    @staticmethod
    def save_priv_key(priv_key):
        with open("rsa_private_key.txt", 'wb') as out:
            out.write(priv_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
