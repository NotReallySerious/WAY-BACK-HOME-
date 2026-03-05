import requests as rq 
import colorama
from colorama import Fore,init,Style
import os 
import threading 
import time

# user enters the compiled wayback link files , store it as a dictionary, and display it
file_select = input('Enter the links directory (full directory (C:\Downloads)): ').strip()
index = 0 
links_repo = dict()
if os.path.dirname(file_select):
    with open(file_select, 'r') as f:
        lines = f.readlines()
        for line in lines:
            values = line.strip()
            index += 1
            links_repo[index] = values
        print(links_repo)
else:
    print("File doesn't exist, please enter another file")
