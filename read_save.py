import os


def read_from_file(filename: str) -> str:
    """Reads data from a file and returns the text."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"The file {filename} was not found.")

    if not os.path.isfile(filename):
        raise ValueError(f"The path {filename} is not a valid file.")

    if not os.access(filename, os.R_OK):
        raise PermissionError(f"The file {filename} is not readable.")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read().strip()

            if not content:
                raise ValueError(f"The file {filename} is empty.")

            return content

    except IOError as e:
        raise IOError(f"Error reading file {filename}: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while reading {filename}: {e}")


def save_to_file(filename: str, content: str) -> None:
    """Saves data to a file."""
    if not content:
        raise ValueError("Content to save is empty.")

    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")

    if directory and not os.access(directory, os.W_OK):
        raise PermissionError(f"The directory {directory} is not writable.")

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        raise IOError(f"Error writing to file {filename}: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while writing to {filename}: {e}")