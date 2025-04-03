import json
import os

from read_save import read_from_file, save_to_file
from constant import (
    INPUT_TEXT_FILE,
    FREQ_ANALYSIS_FILE,
    FREQ_RUSSIAN_FILE,
    DECRYPTION_KEY_FILE,
    DECRYPTED_TEXT_OUTPUT_FILE,
)


def calculate_frequency(input_filename: str, output_filename: str):
    """
    Calculates the frequency of each character in the given text (including spaces) and writes the result to a JSON file.
    The characters will be ordered by frequency in descending order.
    """
    if not os.path.exists(input_filename):
        print(f"Error: The input file {input_filename} does not exist.")
        return

    if os.path.getsize(input_filename) == 0:
        print(f"Error: The input file {input_filename} is empty.")
        return

    try:
        text = read_from_file(input_filename)
        char_count = {}

        for char in text:
            char_count[char] = char_count.get(char, 0) + 1

        total_chars = len(text)

        if total_chars == 0:
            print(f"Error: The input file {input_filename} contains no characters.")
            return

        freq = {char: count / total_chars for char, count in char_count.items()}
        sorted_freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

        save_to_file(output_filename, json.dumps(sorted_freq, ensure_ascii=False, indent=4))

        print(f"Frequency analysis saved to {output_filename}")

    except (IOError, OSError) as e:
        print(f"Error: Unable to process the file {input_filename}. {e}")


def load_json_file(filename: str):
    """Loads data from a JSON file."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def match_frequencies(freq_analys: dict, freq_russian: dict) -> dict:
    """Matches characters based on their frequencies."""
    sorted_analys = sorted(freq_analys.items(), key=lambda item: item[1], reverse=True)
    sorted_russian = sorted(freq_russian.items(), key=lambda item: item[1], reverse=True)
    return {analys_char: russian_char for (analys_char, _), (russian_char, _) in zip(sorted_analys, sorted_russian)}


def match_and_save(freq_analys_filename: str, freq_russian_filename: str, output_filename: str):
    """Matches frequencies from two files and saves the result."""
    matched_pairs = match_frequencies(load_json_file(freq_analys_filename), load_json_file(freq_russian_filename))
    save_to_file(output_filename, json.dumps(matched_pairs, ensure_ascii=False, indent=4))
    print(f"Matched character frequencies saved to {output_filename}")


def decrypt_text(encrypted_text_filename: str, key_filename: str, decrypted_text_filename: str):
    """Decrypts text using a key mapping."""
    key = load_json_file(key_filename)
    encrypted_text = read_from_file(encrypted_text_filename)
    decrypted_text = "".join(key.get(char, char) for char in encrypted_text)
    save_to_file(decrypted_text_filename, decrypted_text)
    print(f"The text has been successfully decrypted and saved to {decrypted_text_filename}")



