import os
from constant import ALPHABET

ALPHABET = ALPHABET.lower()


def get_encrypted_char(text_char: str, key_char: str) -> str:
    """
    Returns the encrypted character using the Trithemius cipher method.
    :param text_char: The character from the text.
    :param key_char: The character from the key.
    :return: The encrypted character or the original character if it's not in the alphabet.
    """
    if text_char not in ALPHABET:
        return text_char  # Return the character unchanged if it's not in the alphabet

    text_pos = ALPHABET.find(text_char)
    key_pos = ALPHABET.find(key_char)

    encrypted_pos = (text_pos + key_pos) % len(ALPHABET)

    return ALPHABET[encrypted_pos]


def tritemius_cipher(text: str, key: str) -> str:
    """
    Encrypts the text using the Trithemius cipher with the given key.
    :param text: The original text to encrypt.
    :param key: The key to use for encryption.
    :return: The encrypted text.
    """
    if not text:
        raise ValueError("The text to encrypt cannot be empty.")
    if not key:
        raise ValueError("The encryption key cannot be empty.")

    text = text.lower()
    key = key.lower()

    encrypted_text = []
    key_index = 0

    for char in text:
        if key_index >= len(key):
            key_index = 0

        encrypted_char = get_encrypted_char(char, key[key_index])
        encrypted_text.append(encrypted_char)

        if char in ALPHABET:
            key_index += 1

    return ''.join(encrypted_text)


def read_from_file(filename: str) -> str:
    """Reads data from a file and returns the text."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"The file {filename} was not found.")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read().strip()
    except IOError as e:
        raise IOError(f"Error reading file {filename}: {e}")


def save_to_file(filename: str, content: str) -> None:
    """Saves data to a file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        raise IOError(f"Error writing to file {filename}: {e}")
