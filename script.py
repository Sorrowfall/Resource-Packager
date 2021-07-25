from os import getenv, walk, path, listdir, chdir, getcwd, mkdir
from shutil import rmtree, copy, copytree
from string import ascii_lowercase
from json import load, dump, JSONDecodeError
from random import choice
from zipfile import ZipFile
from hashlib import sha1

cwd = getcwd()

def gen_temp_folder(filename: str, items: list, output_folder: str = 'build') -> str:
    """Generate a temporary folder for further processing.

    Args:
        items (list): Items to put inside of the temporary folder.
    """
    temp = path.join(cwd, 'temp')
    # make a new temp folder
    while path.exists(temp):
        temp = path.join(cwd, temp+choice(list(ascii_lowercase)))
    mkdir(temp)
    # loop over specified items
    for item in items:
        if path.isfile(item):
            copy(item, temp)
        elif path.isdir(item):
            item = path.join(cwd, item)
            for newfile in listdir(item):
                newfile = path.join(item, newfile)
                if path.isfile(newfile):
                    copy(newfile, temp)
                else:
                    copytree(path.dirname(newfile), temp, dirs_exist_ok=True)
        else:
            print("Could not find path {} in the main directory".format(item))
    return temp

def gen_zip(filename: str, input_folder: str, output_folder: str = 'build'):
    """Generate .zip files.

    Args:
        filename (str): Name of the finished .zip file.
        input_folder (list): What folder to generate the .zip from.
        output_folder (str, optional): What folder to output the .zip in. Defaults to 'build'.
    """
    if not path.exists(output_folder):
        mkdir(output_folder)
    if not path.exists(input_folder):
        raise InputException("couldn't find input folder")
    with ZipFile(output_folder + filename+".zip", 'w') as file:
        chdir(input_folder)
        for item in listdir():
            if path.isfile(item):
                file.write(item)
            else:
                for filepath, sub, filenames in walk(item):
                    for filename in filenames:
                        file.write(path.join(filepath, filename))
    chdir(cwd)

def optim_jsons(input_folder: str):
    """Optimize json (and .mcmeta json) files.

    Args:
        input_folder (list): What folder to optimize jsons in.
    """
    walk = os.walk(input_folder)
    for root, d, files in walk:
        for file in files:
            if file.endswith('.json') or file.endswith('.mcmeta'):
                name = path.join(root, file)
                try:
                    with open(name, 'r') as read_file:
                        try:
                            json = load(read_file)
                        except JSONDecodeError:
                            continue
                    with open(name, 'w') as write_file:
                        dump(json, write_file, separators=(',', ':'))
                except UnicodeEncodeError:
                    continue

def generate_sha1(filename: str, output_folder: str):
    """Generate .zip files.

    Args:
        filename (str): Name of the .zip file to get the sha1 hash from.
        output_folder (str, optional): What folder to output the .sha1 file in. Defaults to 'build'.
    """
    hasher = sha1()
    with open(output_folder + filename+".zip", 'rb') as file:
        buf = file.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(65536)
    # Save the hash
    with open(output_folder + filename+".sha1", 'w+') as file:
        file.write(hasher.hexdigest())

class EnvironException(Exception):
    pass

class InputException(Exception):
    pass

if __name__ == '__main__':
    # declare variables
    filename = getenv('INPUT_FILENAME')
    if not filename:
        raise EnvironException("'filename' field is required")
    items = getenv('INPUT_ITEMS')
    if not items:
        raise EnvironException("'items' field is required")
    elif not isinstance(items, list):
        items = items.split('\n')
    gen_sha1 = getenv('INPUT_GEN-SHA1')
    output_folder = getenv('INPUT_OUTPUT-FOLDER', 'build')
    if not output_folder.endswith('/'):
        output_folder += '/'
    optimize_jsons = getenv('INPUT_OPTIMIZE-JSONS')
    # run logic
    temp_folder = gen_temp_folder(items)
    if str(optimize_jsons.lower()) in ("yes", "y", "true", "t", "1"):
        opt_jsons(temp_folder)
    gen_zip(filename, temp_folder, output_folder)
    if path.exists(temp_folder):
        rmtree(temp_folder)
    if str(gen_sha1.lower()) in ("yes", "y", "true", "t", "1"):
        generate_sha1(filename, output_folder)