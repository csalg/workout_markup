import re
from datetime import datetime
from dataclasses import dataclass, asdict
match_number = re.compile('[0-9]')

@dataclass
class Session:
    name: str
    date: datetime
    units: Unit
    comments: str = ""
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Unit:
    name: str
    exercises: list
    comments: str = ""


@dataclass
class Exercise:
    name: str
    work: Work
    resistances: list 


@dataclass
class Measurable:
    value: int
    unit: str


class Resistance(Measurable):
    pass


class Work(Measurable):
    pass
        

def parse_session(session_as_string):
    workout_lines = session_as_string.splitlines()
    session_name = workout_lines[1]
    workout_lines = workout_lines[2:]
    today = datetime.today()
    session_date = today.strftime("%Y%m%d")
    session_units = []
    session_comments = ""

    find_comments = True
    for i, line in enumerate(workout_lines):
        
        if not line or is_instruction(line):
            continue
            
        if is_comment(line) and find_comments:
            session_comments += process_comment(line)
            continue

        if is_start_of_unit(line):
            find_comments = False
            new_unit = parse_unit(workout_lines, i)
            session_units += [new_unit,]
    
    return Session(session_name, session_date, session_units, session_comments)

            
            
def parse_unit(workout_lines, i):
    unit_name = workout_lines[i].strip('++ ')
    unit_comments = ""
    unit_exercises = []
    find_comments = True
    workout_lines= workout_lines[i+1:]
    
    for j, line in enumerate(workout_lines):
        
        if not line or is_instruction(line):
            continue
            
        if is_comment(line) and find_comments:
            unit_comments += process_comment(line)
            continue
            
        if is_start_of_unit(line):
            break
    
        if is_start_of_exercise(line):
            find_comments = False
            new_exercises = parse_exercises(workout_lines, j)
            unit_exercises += new_exercises
        
        if is_start_of_unit(line):
            break
    
    return Unit(unit_name, unit_exercises, unit_comments)
            

def parse_exercises(workout_lines, j):
    exercise_name = workout_lines[j].strip('+ ')
    exercises = []
    for line in workout_lines[j+1:]:
        if not line or is_start_of_unit(line) or is_start_of_exercise(line):
            break
        if is_instruction(line):
            continue
        exercise = parse_exercise(exercise_name, line)
        exercises += [exercise,]
    return exercises


def parse_exercise(exercise_name, line):
    try:
        work, resistances = line.split(' ', maxsplit=1)
        work = parse_work(work)
        resistances = parse_resistances(resistances)
        return Exercise(exercise_name, work, resistances)
    except:
        print('Parsing failed')
        print(line)


def parse_work(work_string):
    
    if match_number.match(work_string[-1]):
        return Work(int(work_string), 'repetitions')
    
    if work_string[-1]=='s':
        return Work(int(work_string[0:-1]), 'seconds')

    
def parse_resistances(resistances_string):
    resistances = []
    for resistance_string in resistances_string.split(' '):
        resistances += [parse_resistance(resistance_string)]
    return resistances

    
def parse_resistance(resistance_string):
    
    if resistance_string[-1]=='k':
        return Resistance(int(resistance_string[0:-1]), 'kilos')

    if resistance_string[-1]=='t':
        return Resistance(int(resistance_string[0:-1]), 'tube')
    
    if resistance_string[-1]=='b':
        return Resistance(int(resistance_string[0:-1]), 'band')
    
    
def is_instruction(line):
    if len(line)>=2:
        if line[0:2] == '##':
                return True
    return False


def is_comment(line):
    if len(line)>=1:
        if line[0]=='#':
            return True
    return False


def is_start_of_unit(line):
    if len(line)>=2:
        if line[0:2]=='++':
            return True
    return False


def is_start_of_exercise(line):
    if len(line)>=1:
        if line[0:1]=='+':
            return True
    return False


def process_comment(line):
    return line.strip('# ')+'\n'
