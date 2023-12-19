import os


def get_test_file_path(file_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), file_name)
