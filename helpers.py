import argparse
import json


class AppTools:
    @staticmethod
    def load_config() -> dict:
        try:
            with open('settings.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("[!] Файл settings.json не найден.")
            exit(1)

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser(description="Гибридная криптосистема")
        mode = parser.add_mutually_exclusive_group(required=True)
        mode.add_argument('-gen', '--create_keys', action='store_true', help='Создание ключей')
        mode.add_argument('-enc', '--encrypt', action='store_true', help='Шифрование')
        mode.add_argument('-dec', '--decrypt', action='store_true', help='Дешифрование')
        return parser.parse_args()
