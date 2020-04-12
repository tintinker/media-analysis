'''
Sorts articles collected by Atlanta Rydzik into race categories using Washington Post dataset. Ignores location
Justin Tinker
'''

import os
import shutil
import re
import csv
import sys
from collections import defaultdict
from pathlib import Path

SOURCE_FOLDERS = ['./articles/2018/rydzik/Midwest', './articles/2018/rydzik/South', './articles/2018/rydzik/West', './articles/2018/rydzik/East']
DESTINATION_DIR = './articles/2018/byrace' #will be created if does not already exist
WAPO_CSV = './articles/wapo-data.csv'

def num_overlap(t1, t2):
    '''number of elements in both lists/tuples'''
    return len([t for t in t1 if t in t2])

def move_to_category(source_folder, category):
    '''move files into subdirectories, named by category, inside DESTINATION_DIR'''
    category_dir = os.path.join(DESTINATION_DIR, category)
    Path(category_dir).mkdir(parents=True, exist_ok=True)
    shutil.move(source_folder, category_dir, copy_function = shutil.copytree)

names_to_race = defaultdict(dict)

with open(WAPO_CSV) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    for row in csv_reader:
        names = row[1].lower().split(' ') #row[1] is full name
        first_name = names[0]
        other_names = tuple(names[1:]) #dictionary requires tuple as keys rather than lists
        race = row[7] if row[7] else 'unknown' #row[7] is race

        #structure: names_to_race[FIRST_NAME][(MIDDLE_NAME, LAST_NAME)] = RACE
        names_to_race[first_name][other_names] = race

for source_folder in SOURCE_FOLDERS:
    for victim_folder in os.listdir(source_folder): #folders are titled with victim's name and additional info not relevant to this project
        identifiers = re.split(' |_',victim_folder.lower()) #split names by space to match line 28, additional info is usually appended after _
        first_name = identifiers[0]
        other_names = tuple(identifiers[1:])

        if first_name not in names_to_race:
            print(f"No Match in WaPo dataset for: {victim_folder}")
            continue

        if len(names_to_race[first_name]) > 1:
            #if multiple entries with the same first name, match on middle and last names
            name_tup = max(list(names_to_race[first_name].keys()), key = lambda name_tup: num_overlap(name_tup, other_names))
        else:
            name_tup = next(iter(names_to_race[first_name]))

        race = names_to_race[first_name][name_tup]
        move_to_category(os.path.join(source_folder, victim_folder), race)
