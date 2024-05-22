from pathlib import Path


def get_db_path(base_file):
    base_folder = Path(__file__).parent.resolve()
    return Path(base_folder / base_file)
