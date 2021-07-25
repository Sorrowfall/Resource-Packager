from os import getenv, walk, path, listdir, chdir, getcwd, mkdir
from zipfile import ZipFile
from shutil import rmtree, copy, copytree
from hashlib import sha1

def generate_zip(filename: str, items: list, output_folder: str = 'build'):
    """Generate .zip files.

    Args:
        filename (str): Name of the finished .zip file.
        items (list): Items to include inside of the .zip file.
        output_folder (str, optional): What folder to output the .zip in. Defaults to 'build'.
    """
    back = getcwd()
    temp = path.join(back, 'temp')
    # Make a new temp folder
    a = ''
    while path.exists(temp):
        a += 'a'
        temp = path.join(back, 'temp'+a)
    mkdir(temp)
    # loop over specified items
    for item in items:
        if path.isfile(item):
            copy(item, temp)
        elif path.isdir(item):
            item = path.join(back, item)
            for newfile in listdir(item):
                newfile = path.join(item, newfile)
                if path.isfile(newfile):
                    copy(newfile, temp)
                else:
                    copytree(path.dirname(newfile), temp, dirs_exist_ok=True)
        else:
            print("Could not find path {} in the main directory".format(item))
    if not path.exists(output_folder):
        mkdir(output_folder)
    with ZipFile(output_folder + filename+".zip", 'w') as file:
        for item in listdir('temp'):
            chdir(temp)
            if path.isfile(item):
                file.write(item)
            else:
                for filepath, sub, filenames in walk(item):
                    for filename in filenames:
                        file.write(path.join(filepath, filename))
    chdir(back)
    if path.exists(temp):
        rmtree(temp)

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

if __name__ == '__main__':
    filename = getenv('FILENAME')
    if not filename:
        raise EnvironException("'filename' field is required")
    items = getenv('ITEMS')
    print(items)
    if not items:
        raise EnvironException("'items' field is required")
    else:
        items = items.split('\n')
    print(items)
    gen_sha1 = getenv('GEN-SHA1')
    if not gen_sha1:
        gen_sha1 = '0'
    output_folder = getenv('OUTPUT-FOLDER')
    if not output_folder:
        output_folder = 'build'
    if not output_folder.endswith('/'):
        output_folder += '/'
    generate_zip(filename, items, output_folder)
    if gen_sha1.lower() in ("yes", "y", "true", "t", "1"):
        generate_sha1(filename, output_folder)