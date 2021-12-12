from os import getenv, listdir
from pathlib import Path
from shutil import copy2, make_archive, rmtree, copytree, make_archive
from json import load, dump, JSONDecodeError
from hashlib import sha1


def gen_pack(items: list, filename: str = 'pack', output_folder: Path = Path('build/'), optim_jsons: bool = True):
    """Generates a compressed .zip file of Minecraft Resource Packs.

    Args:
        items (list[str]): A list of folders or files to add to the file.
        filename (str, optional): Name of the file to generate. Defaults to 'pack'.
        output_folder (Path, optional): What folder to output the file in. Defaults to 'build/'.
        optim_jsons (bool, optional): Whether or not to optimize .json (and .mcmeta json) files. Defaults to True.
    """

    temp = Path(f'{output_folder}/temp')
    if not temp.exists(): temp.mkdir()

    for item in items:
        path = Path(item)
        if path.exists():
            copytree(path, temp, copy_function=copy_and_merge_jsons if optim_jsons else copy2, dirs_exist_ok=True)

    zip = make_archive(f'{output_folder}/{filename}', 'zip', temp)

    rmtree(temp)
    return zip

def copy_and_merge_jsons(src, dest):
    if Path(src).suffix in ('.json', '.mcmeta'):
        with open(src, 'r') as new:
            try:
                json = load(new)
            except JSONDecodeError as e:
                return print(f"Invalid .json file '{src}'")
        if Path(dest).exists():
            with open(dest, 'r') as original:
                try:
                    original = load(original)
                    json = {**original, **json}
                except JSONDecodeError as e:
                    print(f"Invalid .json file '{dest}'")
                    return copy2(src, dest)
        with open(dest, 'w') as original:
            dump(json, original, separators=(',', ':'))
    else:
        copy2(src, dest)

def pack_hash_sha1(filename: str, output_folder: Path = Path('build/')) -> str:
    """Hash .zip files for Server Resource Pack caching.

    Args:
        filename (str): Name of the .zip file to get the sha1 hash from.
        output_folder (str, optional): What folder to output the .sha1 file in. Defaults to 'build'.
    """
    hasher = sha1()
    with open(output_folder / f"{filename}.zip", 'rb') as file:
        buf = file.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(65536)
    hash = hasher.hexdigest()

    with open(output_folder / f"{filename}.sha1", 'w+') as file:
        file.write(hash)

    return hash


def is_true(boolean):
    return (str(boolean).lower()) in ("yes", "y", "true", "t", "1")

class EnvironException(Exception):
    pass


if __name__ == '__main__':

    # declare variables

    filename = getenv('INPUT_FILENAME', None)
    if not filename: raise EnvironException("'filename' field is required")

    items = getenv('INPUT_ITEMS', None)
    if not items: raise EnvironException("'items' field is required")
    if not isinstance(items, list):
        items = items.split('\\n')

    output_folder = Path(getenv('INPUT_OUTPUT-FOLDER', 'build'))
    if not output_folder.exists(): output_folder.mkdir()

    gen_sha1 = is_true(getenv('INPUT_GEN-SHA1'))
    optimize_jsons = is_true(getenv('INPUT_OPTIMIZE-JSONS'))

    # run logic

    pack_zip = gen_pack(items, filename, output_folder, optimize_jsons)
    if gen_sha1: 
        hash = pack_hash_sha1(filename, output_folder)