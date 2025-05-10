import math
from scipy.special import gammaincc as gamma_func
from consts import *


def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read().strip()
    except IOError as err:
        print(f"File read error: {err}")
        return ""


def save_results(output_path, content):
    try:
        with open(output_path, 'w') as f:
            f.write(content)
    except IOError as err:
        print(f"File save error: {err}")


def check_bit_distribution(bit_str):
    length = len(bit_str)
    if not length:
        raise ValueError("Empty sequence")

    balance = sum(1 if b == '1' else -1 for b in bit_str)
    return math.erfc(abs(balance) / math.sqrt(2 * length))


def evaluate_runs_pattern(bit_str):
    n = len(bit_str)
    ones_prob = bit_str.count('1') / n

    if abs(ones_prob - 0.5) >= 2 / math.sqrt(n):
        return 0.0

    transitions = sum(1 for i in range(n - 1) if bit_str[i] != bit_str[i + 1])

    mean = 2 * n * ones_prob * (1 - ones_prob)
    std_dev = 2 * math.sqrt(2 * n) * ones_prob * (1 - ones_prob)

    return math.erfc(abs(transitions - mean) / std_dev)


def analyze_blocks(bit_str):
    if len(bit_str) < 128:
        raise ValueError("Minimum 128 bits required")

    block_count = len(bit_str) // 8
    categories = [0] * 4

    for i in range(block_count):
        segment = bit_str[i * 8: (i + 1) * 8]
        max_run = current = 0

        for bit in segment:
            current = current + 1 if bit == '1' else 0
            max_run = max(max_run, current)

        if max_run <= 1:
            categories[0] += 1
        elif max_run == 2:
            categories[1] += 1
        elif max_run == 3:
            categories[2] += 1
        else:
            categories[3] += 1

    chi_sq = sum((obs - 16 * exp) ** 2 / (16 * exp) for obs, exp in zip(categories, PI))

    return gamma_func(1.5, chi_sq / 2)


def process_sequences():
    cpp_bits = load_data(cpp_sequence_txt)
    java_bits = load_data(java_sequence_txt)

    cpp_results = (f"CPP sequence analysis:\n{cpp_bits}\n\n"
                   f"Bit distribution test: {check_bit_distribution(cpp_bits):.6f}\n"
                   f"Runs pattern test: {evaluate_runs_pattern(cpp_bits):.6f}\n"
                   f"Block analysis test: {analyze_blocks(cpp_bits):.6f}")

    java_results = (f"Java sequence analysis:\n{java_bits}\n\n"
                    f"Bit distribution test: {check_bit_distribution(java_bits):.6f}\n"
                    f"Runs pattern test: {evaluate_runs_pattern(java_bits):.6f}\n"
                    f"Block analysis test: {analyze_blocks(java_bits):.6f}")

    save_results(results_cpp, cpp_results)
    save_results(results_java, java_results)


if __name__ == "__main__":
    process_sequences()