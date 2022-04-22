from zipfile import ZipFile
from pathlib import Path


def extract_all(archive, out_dir):
    with ZipFile(archive, 'r') as arc:
        arc.extractall(out_dir)


def get_main_file(input_dir):
    mainfile = False

    for filename in ('app.py', 'main.py'):
        try:
            mainfile = next(Path(input_dir).rglob(filename))
        except Exception:
            continue

    return mainfile


if __name__ == '__main__':
    print(get_main_file('../../program'))