import sys
import os
import io
import re
from sys import argv, exit

def combine(path):
    combined_text = ''
    print(f"Path: {path}")
    for filename in os.scandir(path):
        combined_text += '\n'
        if filename.is_dir():
            combined_text += combine(filename.path)
        elif filename.path.endswith('.txt'):
            print(f"processing file: {filename.path}")
            with open(filename.path) as f:
                combined_text += f.read()
        elif filename.path.lower().endswith('.pdf'):
            os.remove(filename.path)
    return combined_text


if len(argv) < 2:
    print("usage combine.py [ROOT FOLDER] [combined_filename (optional)]")
    print("ex. combine.py ./articles/2018/byrace")
    print("ex. combine.py ./articles/2018/byrace all.txt")

root_folder = argv[1]
postfix = argv[2] if len(argv) > 2 else 'combined.txt'

combined_text = combine(root_folder)
with open(os.path.join(root_folder, postfix), 'w+') as f:
    f.write(combined_text)
