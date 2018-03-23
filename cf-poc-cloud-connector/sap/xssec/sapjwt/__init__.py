""" sapjwt module """
import os
import sys
import imp
# import sapjwt.deps
imp.load_source('deps', './sap/xssec/sapjwt/deps/__init__.py')
imp.load_source('jwtValidation', './sap/xssec/sapjwt/jwtValidation.py')
# from .jwtValidation import jwtValidation

def getFullLibraryName(): # pylint: disable=E0602,C0103
    """ return full library name to SAPJWT """
    return os.path.join(os.path.dirname(deps.__file__), deps.getFolderName(), deps.getLibraryName())  # pylint: disable=E0602,C0103
