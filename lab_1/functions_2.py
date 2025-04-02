import json
import os


def calculate_frequency(input_filename: str, output_filename: str):
    """
    Calculates the frequency of each character in the given text (including spaces) and writes the result to a JSON file.
    The characters will be ordered by frequency in descending order.
    :param input_filename: The name of the file from which to read the text.
    :param output_filename: The name of the file where the results will be saved.
    """
    if not os.path.exists(input_filename):
        print(f"Error: The input file {input_filename} does not exist.")
        return

    if os.path.getsize(input_filename) == 0:
        print(f"Error: The input file {input_filename} is empty.")
        return

    if not input_filename.lower().endswith('.txt'):
        print(f"Error: The input file {input_filename} is not a .txt file.")
        return

    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            text = file.read()

        char_count = {}

        for char in text:
            if char in char_count:
                char_count[char] += 1
            else:
                char_count[char] = 1

        total_chars = len(text)

        if total_chars == 0:
            print(f"Error: The input file {input_filename} contains no characters.")
            return

        freq = {char: count / total_chars for char, count in char_count.items()}

        sorted_freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(sorted_freq, f, ensure_ascii=False, indent=4)

            print(f"Frequency analysis saved to {output_filename}")

        except (IOError, OSError) as e:
            print(f"Error: Unable to write to the file {output_filename}. {e}")

    except (IOError, OSError) as e:
        print(f"Error: Unable to read the file {input_filename}. {e}")


def load_json_file(filename: str):
    """
    Loads data from a JSON file.
    :param filename: The name of the JSON file to load.
    :return: The content of the file as a dictionary.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def match_frequencies(freq_analys: dict, freq_russian: dict) -> dict:
    """
    Matches characters from freq_analys with characters from freq_russian based on their frequencies.
    :param freq_analys: A dictionary containing the frequency of characters in the analyzed text.
    :param freq_russian: A dictionary containing the frequency of characters in the Russian language.
    :return: A dictionary with matched characters.
    """
    sorted_analys = sorted(freq_analys.items(), key=lambda item: item[1], reverse=True)
    sorted_russian = sorted(freq_russian.items(), key=lambda item: item[1], reverse=True)

    matched_pairs = {}
    min_length = min(len(sorted_analys), len(sorted_russian))

    for i in range(min_length):
        analys_char, analys_freq = sorted_analys[i]
        russian_char, russian_freq = sorted_russian[i]

        matched_pairs[analys_char] = russian_char

    return matched_pairs


def save_to_json(data: dict, output_filename: str):
    """
    Saves the matched pairs to a JSON file.
    :param data: The data to be saved in the file.
    :param output_filename: The name of the output JSON file.
    """
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Matched character frequencies saved to {output_filename}")


def match_and_save(freq_analys_filename: str, freq_russian_filename: str, output_filename: str):
    """
    Matches character frequencies from two files and saves the result to a new JSON file.
    :param freq_analys_filename: The file containing the analyzed frequencies.
    :param freq_russian_filename: The file containing the Russian language frequencies.
    :param output_filename: The file to save the matched frequencies.
    """
    freq_analys = load_json_file(freq_analys_filename)
    freq_russian = load_json_file(freq_russian_filename)

    matched_pairs = match_frequencies(freq_analys, freq_russian)

    save_to_json(matched_pairs, output_filename)


def decrypt_text(encrypted_text_filename: str, key_filename: str, decrypted_text_filename: str):
    """
    Decrypts the text using the character mappings from the provided key file.
    :param encrypted_text_filename: The file containing the encrypted text.
    :param key_filename: The file containing the character mappings (key).
    :param decrypted_text_filename: The file to save the decrypted text.
    """
    key = load_json_file(key_filename)

    if not os.path.exists(encrypted_text_filename):
        print(f"Error: The encrypted text file {encrypted_text_filename} does not exist.")
        return

    with open(encrypted_text_filename, 'r', encoding='utf-8') as file:
        encrypted_text = file.read()

    decrypted_text = ""
    for char in encrypted_text:
        decrypted_text += key.get(char, char)

    with open(decrypted_text_filename, 'w', encoding='utf-8') as file:
        file.write(decrypted_text)

    print(f"The text has been successfully decrypted and saved to {decrypted_text_filename}")


calculate_frequency('code6.txt', 'freq_analys.json')

match_and_save('freq_analys.json', 'freq_russian.json', 'key2.json')

decrypt_text('code6.txt', 'key2.json', 'decrypted_text_output.txt')
