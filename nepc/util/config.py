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
    return '/home/neha/nepc'


def removeCRs(mystring):
    return mystring.replace('\n', ' ').replace('\r', '')
