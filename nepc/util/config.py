import os
import sys


# TODO: remove userHome from nepc
def userHome():
    user = os.environ.get('USER')
    if sys.platform == 'darwin':
        return '/Users/' + user + '/'
    else:
        return '/home/' + user + '/'


def nepc_home():
    return os.environ.get('NEPC_HOME')


def removeCRs(mystring):
    return mystring.replace('\n', ' ').replace('\r', '')
