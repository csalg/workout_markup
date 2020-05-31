#! python3
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open('config/resistance.yaml', 'r') as file:
    resistance = load(file.read(), Loader=Loader)
    print(resistance)
