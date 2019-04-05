import os
import sys

def userHome():
    user = os.environ.get('USER')
    if sys.platform == 'darwin':
        return '/Users/' + user + '/'
    else:
        return '/home/' + user + '/'
