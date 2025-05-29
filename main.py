from helpers import AppTools
from file_utils import FileManager
from asymmetric_cipher import AsymmetricCipher
from symmetric_cipher import SymmetricCipher
import os


def create_keys(config):
    print("[*] Генерация ключей...")
    sym_key = os.urandom(16)

    priv_key, pub_key = AsymmetricCipher.generate_rsa_keypair()
    encrypted_sym_key = AsymmetricCipher.encrypt(sym_key, pub_key)

    FileManager.write_file("rsa_pub_key.txt", AsymmetricCipher.serialize_public_key(pub_key))
    FileManager.write_file("rsa_private_key.txt", AsymmetricCipher.serialize_private_key(priv_key))
    FileManager.write_file(config['encoded_sym_key'], encrypted_sym_key)

    print("[+] Ключи успешно созданы.")


def encrypt_data(config):
    print("[*] Загрузка данных для шифрования...")
    FileManager.ensure_exists([config['rsa_private'], config['encoded_sym_key'], config['plain_data']])

    private_key = AsymmetricCipher.load_private_key(FileManager.read_file(config['rsa_private']))
    sym_key = AsymmetricCipher.decrypt(FileManager.read_file(config['encoded_sym_key']), private_key)
    plaintext = FileManager.read_file(config['plain_data'])

    encrypted = SymmetricCipher.encrypt(plaintext, sym_key)
    FileManager.write_file(config['encrypted_data'], encrypted)

    print("[+] Данные зашифрованы.")


def decrypt_data(config):
    print("[*] Загрузка данных для дешифровки...")
    FileManager.ensure_exists([config['rsa_private'], config['encoded_sym_key'], config['encrypted_data']])

    private_key = AsymmetricCipher.load_private_key(FileManager.read_file(config['rsa_private']))
    sym_key = AsymmetricCipher.decrypt(FileManager.read_file(config['encoded_sym_key']), private_key)
    encrypted_data = FileManager.read_file(config['encrypted_data'])

    decrypted = SymmetricCipher.decrypt(encrypted_data, sym_key)
    FileManager.write_file(config['decrypted_output'], decrypted)

    print("[+] Данные расшифрованы.")


def main():
    args = AppTools.get_args()
    config = AppTools.load_config()

    if args.create_keys:
        create_keys(config)
    elif args.encrypt:
        encrypt_data(config)
    elif args.decrypt:
        decrypt_data(config)


if __name__ == "__main__":
    main()
