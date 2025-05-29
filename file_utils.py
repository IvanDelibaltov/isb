import os


class FileManager:
    @staticmethod
    def read_file(path: str) -> bytes:
        with open(path, 'rb') as file:
            return file.read()

    @staticmethod
    def write_file(path: str, data: bytes) -> None:
        with open(path, 'wb') as file:
            file.write(data)

    @staticmethod
    def ensure_exists(paths: list):
        for path in paths:
            if not os.path.exists(path):
                print(f"[!] Не найден файл: {path}")
                exit(1)
