'''
saxsdh is saxs data handler package
'''


import sys

if sys.version_info[:2] < (3, 6):
    m = "Python 3.6 or later is required (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys

#import
from saxsdh.saxs_edf_handler import *
from saxsdh.saxs_edf_symmetry import *