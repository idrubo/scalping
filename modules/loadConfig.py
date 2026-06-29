'''
Save data using python syntax.
'''

import os

# To print to a file:

config = 'config'

# Depending on our operating system we may adapt the path.
configDir = './'
configFile = config + '.py'
configPath = configDir + configFile

def saveCapital (value):
    with open (configPath, 'w') as f:
        print ('%s = %f' % ('capital', value), file = f)

if not os.path.exists (configPath):
    saveCapital (100000)

# To import our recently created config file.
from config import *

