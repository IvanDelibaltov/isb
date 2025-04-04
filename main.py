import argparse
import json
import os

from functions_1 import tritemius_cipher
from read_save import read_from_file, save_to_file
from functions_2 import (
    calculate_frequency,
    match_and_save,
    decrypt_text,
    load_json_file,
)
from constant import (
    INPUT_TEXT_FILE,
    DECRYPTED_TEXT_OUTPUT_FILE,
    CODE6_DECRYPTED_FILE,
    FREQ_ANALYSIS_FILE,
    FREQ_RUSSIAN_FILE,
    DECRYPTION_KEY_FILE,
)


def check_file_exists(filename: str) -> bool:
    """Check if the file exists and is readable."""
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' does not exist.")
        return False
    if not os.path.isfile(filename):
        print(f"Error: The path '{filename}' is not a file.")
        return False
    return True


def check_file_readable(filename: str) -> bool:
    """Check if the file is readable."""
    try:
        with open(filename, 'r', encoding='utf-8'):
            pass
        return True
    except IOError:
        print(f"Error: The file '{filename}' is not readable.")
        return False


def check_file_writable(filename: str) -> bool:
    """Check if the file is writable."""
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            pass
        return True
    except IOError:
        print(f"Error: The file '{filename}' is not writable.")
        return False


def process_files_for_decryption():
    """Calculates frequencies, matches them, and decrypts the text."""
    calculate_frequency(INPUT_TEXT_FILE, FREQ_ANALYSIS_FILE)

    match_and_save(FREQ_ANALYSIS_FILE, FREQ_RUSSIAN_FILE, DECRYPTION_KEY_FILE)

    decrypt_text(INPUT_TEXT_FILE, DECRYPTION_KEY_FILE, DECRYPTED_TEXT_OUTPUT_FILE)


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
        if not (check_file_exists(args.text) and check_file_readable(args.text)):
            return
        if not (check_file_exists(args.key) and check_file_readable(args.key)):
            return
        if not (check_file_exists(args.key2) and check_file_readable(args.key2)):
            return

        if not check_file_writable(args.output):
            return

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

        process_files_for_decryption()

        if not (check_file_exists(INPUT_TEXT_FILE) and check_file_readable(INPUT_TEXT_FILE)):
            return
        if not (check_file_exists(DECRYPTED_TEXT_OUTPUT_FILE) and check_file_readable(DECRYPTED_TEXT_OUTPUT_FILE)):
            return
        if not (check_file_exists(CODE6_DECRYPTED_FILE) and check_file_readable(CODE6_DECRYPTED_FILE)):
            return

        print("\nOriginal crypted text")
        code6_text = read_from_file(INPUT_TEXT_FILE)
        print(code6_text)

        print("\nDecrypted text by program: ")
        decrypted_text = read_from_file(DECRYPTED_TEXT_OUTPUT_FILE)
        print(decrypted_text)

        print("\nDecrypted text:")
        code6decrypted_text = read_from_file(CODE6_DECRYPTED_FILE)
        print(code6decrypted_text)

    except (FileNotFoundError, IOError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
