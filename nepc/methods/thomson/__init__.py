from .version import __version__
from .thomson import fcf


# if somebody does "from somepackage import *", this is what they will
# be able to access:
__all__ = [
        'fcf',
        ]
