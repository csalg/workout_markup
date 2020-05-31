from os import walk
import os
from time import ctime
from datetime import datetime, timedelta
from shutil import copyfile
import pickle

from config import *


def find_new_workout_files(previous_dt, interaction_folder=INTERACTION_FOLDER):
    new_filenames = []
    for (_, _, filenames) in walk(interaction_folder):
        for filename in filenames:
            path = os.path.join(interaction_folder, filename)
            modified = datetime.fromtimestamp(os.path.getmtime(path))
            if modified > previous_dt:
                new_filenames.append(path)
    return new_filenames


def is_sunday():
    today = datetime.now()
    return today.weekday() == 6


def copy_workout_templates_to_interaction_folder(
    templates_folder=TEMPLATES_FOLDER, 
    interaction_folder=INTERACTION_FOLDER
            ):
    
    for (dirpath, dirnames, filenames) in walk(templates_folder):
        for filename in filenames:
            print(filename)
            original = os.path.join(templates_folder, filename)
            workout_names = make_workout_names_from_template(original)
            for workout_name in workout_names:
                target = os.path.join(interaction_folder, workout_name)
                copyfile(original, target)


def make_workout_names_from_template(filename):
    names = []
    
    with open(filename, 'r') as file:
        template_to_parse = file.read()
    
    lines = template_to_parse.splitlines()
    workout_title = lines[0].strip('\n')
    
    for line in lines:
        if len(line)>1:
            if line[0]=='@':
                directive, arguments = parse_directive(line)
                if directive == 'on':
                    for weekday in arguments:
                        weekday = parse_weekday(weekday)
                        workout_date = next_date_from_weekday(weekday)
                        names.append(workout_date + '_' + workout_title)
    return names                


def parse_directive(directive_str):
    directive_str = directive_str.strip('@ ')
    directive, args = directive_str.split(" ", maxsplit=1)
    args = args.split(' ')
    return directive, args


def next_date_from_weekday(desired):
    today = datetime.now()
    lag = (desired - today.weekday()) % 7
    next_desired_day = today + timedelta(days=lag)
    return next_desired_day.strftime("%Y%m%d")

weekdays = {
    'monday':0,
    'tuesday':1,
    'wednesday':2,
    'thursday':3,
    'friday':4,
    'saturday':5,
    'sunday':6
}

def parse_weekday(weekday_str):
    return weekdays[weekday_str.lower()]


def load_previous_dt():
    if os.path.exists('previous_dt.pkl'):
        with open('previous_dt.pkl', 'rb') as file:
            previous_dt = pickle.load(file)
        return previous_dt
    return datetime.fromtimestamp(0)


def dump_current_dt():
    dt = datetime.today()
    with open('previous_dt.pkl', 'wb') as file:
        pickle.dump(dt, file)


def update_nextcloud_database():
    pass
