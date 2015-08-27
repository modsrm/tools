#!/usr/bin/python

import argparse
import os
import shutil
from subprocess import check_call

xresources_file_path = os.path.expanduser('~') + '/.Xresources'
temp_file_path = '/tmp/tmp_xresources'

def parse_args():
    parser = argparse.ArgumentParser(description='Changes the Xresources font size')
    parser.add_argument('font_size', metavar='font_size', type=int, nargs='?',
                        help='The new size')

    return parser.parse_args()

def replace_size(new_size):
    with open(xresources_file_path, 'r') as old_file:
        with open(temp_file_path, 'w') as new_file:
            for line in old_file:
                if line.startswith('xterm*faceName'):
                    line = line.rstrip()
                    splits = line.split(':')

                    # Look for the size and remove it.
                    for elem in splits:
                        if elem.startswith('size='):
                            splits.remove(elem)

                    # Append new size.
                    splits.append('size=' + str(new_size))
                    line = ':'.join(splits) + '\n'

                new_file.write(line)

    # Overwrite Xresources
    shutil.move(temp_file_path, xresources_file_path)

def xrdb_merge():
    check_call(['xrdb', '-merge', xresources_file_path], shell=False)

def main():
    new_size = parse_args().font_size
    replace_size(new_size)
    xrdb_merge()

if __name__ == "__main__":
    main()

