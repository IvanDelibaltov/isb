from core_helpers import AppTools, FileControl
from rsa_handler import KeyGenerator
from seed_cipher import DataEncryptor


def main():
    args = AppTools.get_args()
    config = AppTools.load_config()

    if args.create_keys:
        print("[*] Создание ключей...")
        KeyGenerator.generate_pair(config)
        print("[+] Ключи успешно созданы.")

    elif args.encrypt:
        print("[*] Проверка файлов для шифрования...")
        FileControl.ensure_exists([
            config['encoded_sym_key'], config['rsa_private'], config['plain_data']
        ])
        DataEncryptor.encrypt_content(config)

    elif args.decrypt:
        print("[*] Проверка файлов для дешифровки...")
        FileControl.ensure_exists([
            config['encoded_sym_key'], config['rsa_private'], config['encrypted_data']
        ])
        DataEncryptor.decrypt_content(config)


if __name__ == "__main__":
    main()
