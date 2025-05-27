import os
from typing import Dict
from cryptography.hazmat.primitives.asymmetric import rsa, padding as pad
from cryptography.hazmat.primitives import hashes
from core_helpers import FileControl


class KeyGenerator:
    @staticmethod
    def generate_pair(config: Dict[str, str]) -> None:
        print("[*] Генерация симметричного ключа...")
        secret_key = os.urandom(16)
        print("[+] Симметричный ключ сгенерирован.")

        print("[*] Генерация пары RSA...")
        priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        pub = priv.public_key()

        FileControl.save_pub_key(pub)
        FileControl.save_priv_key(priv)

        print("[*] Шифруем симметричный ключ с помощью RSA...")
        encrypted = pub.encrypt(
            secret_key,
            pad.OAEP(mgf=pad.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None)
        )

        with open(config['encoded_sym_key'], 'wb') as file_out:
            file_out.write(encrypted)

        print("[+] Ключи сохранены и симметричный ключ зашифрован.")
