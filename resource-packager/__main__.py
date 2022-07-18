from argparse import ArgumentParser
from __init__ import Resource_Pack
from typing import List

parser = ArgumentParser(description='generate Minecraft Resource Pack files from multiple directories')
parser.add_argument('-p', '--parts', type=str, help='a list of directories to make the Resource Pack out of', nargs='+')
parser.add_argument('-n', '--name', type=str, help="what to name the created Resource Pack", default='pack', nargs="?")
parser.add_argument('-d', '--output_dir', type=str, help="what directory to make the Resource Pack in", default='build/', nargs="?")
parser.add_argument('-o', '--optimize_jsons', type=bool, help="whether or not to optimize JSON files", default=True, nargs="?")
parser.add_argument('-k', '--keep_temp', type=bool, help="whether or not to keep the temporary Resource Pack files", default=False, nargs="?")

args = parser.parse_args()
Resource_Pack(args.parts, args.name, args.output_dir, args.optimize_jsons, args.keep_temp)