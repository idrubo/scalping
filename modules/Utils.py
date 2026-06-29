'''
System related functions.
'''

import os
import shutil
import inspect
from colorama import Fore, Back, Style

def rmDir (Dir):

    if os.path.exists (Dir):
        try:
            shutil.rmtree (Dir)
        except PermissionError:
            print ("Permission denied")
            exit ()
        except Exception as e:
            print (f"ERROR: rmDir: {e}")
            exit ()

def createDir (Dir):

    if not os.path.exists (Dir): os.makedirs (Dir)

# Available formatting constants in "colorama" are:
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL

def prnTotal (name, value):

    if value < 0: color = Style.BRIGHT + Fore.RED
    else: color = Style.BRIGHT + Fore.GREEN

    prnVal (color, name, '$%.3f', value)

def prnAmount (name, value):

    if value < 0: color = Style.BRIGHT + Fore.RED
    else: color = Fore.GREEN

    prnVal (color, name, '$%.3f', value)

def prnVal (color, name, fmt, value):
    print (name + ': ', end ="")
    print (color, end =""); print (fmt % value, end ="")
    print (Style.RESET_ALL)

