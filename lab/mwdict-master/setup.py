#!/usr/bin/env python
#
# EasyInstall setup script for mwdict
#
# $Id$
# ---------------------------------------------------------------------------

import sys
import os
sys.path += [os.getcwd()]

from setuptools import setup, find_packages
import re
import imp

DESCRIPTION = "Look up English words via online Merriam Webster dictionary"

def load_info():
    # Look for identifiers beginning with "__" at the beginning of the line.

    result = {}
    pattern = re.compile(r'^(__\w+__)\s*=\s*[\'"]([^\'"]*)[\'"]')
    here = os.path.dirname(os.path.abspath(sys.argv[0]))
    for line in open(os.path.join(here, 'mwdict', '__init__.py'), 'r'):
        match = pattern.match(line)
        if match:
            result[match.group(1)] = match.group(2)

    sys.path = [here] + sys.path
    mf = os.path.join(here, 'mwdict', '__init__.py')
    try:
        m = imp.load_module('mwdict', open(mf), mf,
                            ('__init__.py', 'r', imp.PY_SOURCE))
        result['long_description'] = m.__doc__
    except:
        result['long_description'] = DESCRIPTION
    return result

info = load_info()

NAME = 'mwdict'

# Now the setup stuff.

print("%s, version %s" % (NAME, info['__version__']))

setup (name             = NAME,
       version          = info['__version__'],
       description      = DESCRIPTION,
       long_description = info['long_description'],
       packages         = find_packages(),
       url              = info['__url__'],
       license          = info['__license__'],
       author           = info['__author__'],
       author_email     = info['__email__'],
       install_requires = ['docopt>=0.6.2',
                           'inflection>=0.3.1',
                           'Markdown>=2.6.5'],
       entry_points     = {'console_scripts' : 'mwdict=mwdict:main'},
       classifiers = [
        'Topic :: Utilities',
       ]
)
