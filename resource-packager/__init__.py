from sys import argv
from pathlib import Path
from shutil import copy2, make_archive, rmtree, copytree
from json import load, dump, JSONDecodeError
from hashlib import sha1

from typing import List

def copy_and_merge_jsons(src, dest):
    if Path(src).suffix == '.json':
        with open(src, 'r') as new:
            try:
                json = load(new)
            except JSONDecodeError as e:
                return print(f"Wrongly formatted .json file '{src}'")
        if Path(dest).exists():
            with open(dest, 'r') as original:
                try:
                    original = load(original)
                    json = {**original, **json}
                except JSONDecodeError as e:
                    print(f"Wrongly formatted .json file '{dest}'")
                    return copy2(src, dest)
        with open(dest, 'w') as original:
            dump(json, original, separators=(',', ':'))
    else:
        copy2(src, dest)

class Resource_Pack:
    """Generate Minecraft Resource packs from multiple directories.
    Args:
        parts (List[Path]): A list of directories to make the Resource Pack out of.
        name (str, optional): What to name the created Resource Pack. Defaults to 'pack'.
        output_dir (Path, optional): What directory to make the Resource Pack in. Defaults to Path('build/').
        optimize_jsons (bool, optional): Whether or not to optimize JSON files. Defaults to True.
        keep_temp (bool, optional): Whether or not to keep the temporary Resource Pack files. Defaults to False.
    """

    _magic_bytes = 65536

    def __init__(self,
        parts: List[Path],
        name: str = 'pack',
        output_dir: Path = Path('build/'),
        optimize_jsons: bool = True,
        keep_temp: bool = False,
    ):
        self.parts = parts
        self.name = name
        self.output = Path(output_dir)
        if not self.output.exists(): self.output.mkdir()
        self.copy_function = copy_and_merge_jsons if optimize_jsons else copy2
        self.keep_temp = keep_temp

        self.gen()
        self.hash()

    def gen(self):
        temp = self.output / 'temp'
        if temp.exists(): rmtree(temp)
        if not temp.exists(): temp.mkdir()

        for part in self.parts:
            part = Path(part)
            if part.exists():
                copytree(part, temp, copy_function=self.copy_function, dirs_exist_ok=True)
            else:
                print(f"Unknown path '{part}'")

        self.file = Path(make_archive(self.output/self.name, 'zip', temp))

        if not self.keep_temp: rmtree(temp)

    def hash(self):
        hasher = sha1()
        with open(self.file, 'rb') as file:
            buf = file.read(self._magic_bytes)
            while len(buf) > 0:
                hasher.update(buf)
                buf = file.read(self._magic_bytes)
        self.hash = hasher.hexdigest()

        with open(self.file.with_suffix('.sha1'), 'w+') as file:
            file.write(self.hash)
