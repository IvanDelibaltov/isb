import argparse
import json
from functions_1 import tritemius_cipher, read_from_file, save_to_file
from functions_2 import load_json_file


def main():
    """
    Main function to read the text from a file, encrypt it, and save the encrypted text to another file.
    Additionally, print the contents of the key2.json.
    """
    parser = argparse.ArgumentParser(description="Encrypt text using Trithemius cipher.")
    parser.add_argument("text", help="File with the original text")
    parser.add_argument("key", help="File with the encryption key")
    parser.add_argument("output", help="File to save the encrypted text")
    parser.add_argument("key2", help="File with the decryption key (key2.json)")

    args = parser.parse_args()

    try:
        # Шифрование текста с использованием шифра Тритемия
        text = read_from_file(args.text)
        key = read_from_file(args.key)

        encrypted_text = tritemius_cipher(text, key)

        save_to_file(args.output, encrypted_text)

        print("Task 1:")
        print(f"The text has been successfully encrypted and saved to {args.output}")
        print("Original text:")
        print(text)
        print("Encrypted text:")
        print(encrypted_text)

        print("Task 2:")
        print("\nKey:")
        key2_data = load_json_file(args.key2)
        print(json.dumps(key2_data, ensure_ascii=False, indent=4))


        print("\nOriginal crypted text")
        code6_text = read_from_file('code6.txt')
        print(code6_text)

        print("\nDecrypted text by programm: ")
        decrypted_text = read_from_file('decrypted_text_output.txt')
        print(decrypted_text)

        print("\nDecrypted text :")
        code6decrypted_text = read_from_file('code6decrypted.txt')
        print(code6decrypted_text)

    except (FileNotFoundError, IOError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
