from pathlib import Path


def get_folder_path(base_file: str):
    base_folder = Path(__file__).parent.resolve()
    return Path(base_folder / base_file)
