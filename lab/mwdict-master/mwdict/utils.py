'''
Utility functions.
'''

import sys

WRAP_WIDTH = 79

def die(msg):
    '''
    Call error(msg), then exit abnormally.
    '''
    error(msg)
    sys.exit(1)

def error(msg):
    '''
    Simplified function for writing a message to standard error.

    Params:

    msg (str) - the message to write to stderr. A newline will be appended.
    '''
    sys.stderr.write(msg + '\n')

def utf8(s):
    '''Shorthand function for encoding a string in UTF-8.'''
    return s.encode('utf8')

def take(n, iterable, default=None):
    '''
    Return first n items of the iterable as a list. If the resulting list is
    empty, return the specified default.

    Params:

    n        - number of items to take from the iterable
    iterable - the iterable
    default  - default to return if there are no values to take
    '''
    from itertools import islice
    result = list(islice(iterable, n))
    if len(result) == 0:
        result = default
    return result

def dict_merge(dict1, dict2):
    '''Merge two dictionaries into a third one.'''
    result = dict(dict1)
    for k, v in dict2.iteritems():
        result[k] = v
    return result
