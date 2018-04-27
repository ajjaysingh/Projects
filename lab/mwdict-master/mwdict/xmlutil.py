'''
XML utility functions.
'''
# FORMAT_TAGS maps the XML format tags into Markdown

import functools
import string
import itertools
from utils import take

def _surround_with(delim, s):
    '''
    Surround the first group of alphas in a string with a delimiter.
    For instance:

        _surround_with('foo,', '/') # returns '/foo/,'

    Params:

    delim - the delimiter
    s     - the string
    '''
    alphas = itertools.takewhile(lambda c: c.isalpha(), s)
    rest = itertools.dropwhile(lambda c: c.isalpha(), s)
    return delim + ''.join(alphas) + delim + ''.join(rest)

def _pass_through(s):
    '''Return the passed-in string unmodified.'''
    return s

_ital      = functools.partial(_surround_with, '_')
_bold      = functools.partial(_surround_with, '**')

def _bold_ital(s):
    _surround_with('**', _surround_with('_'))

def _prefix_with(prefix, s):
    return prefix + s

FORMAT_TAGS = {
    'it':   _ital,         # italics
    'sc':   string.upper,  # small caps
    'vi':   functools.partial(_prefix_with, ', '),
    'bold': _bold,
    'sx':   string.upper,
    'bit':  _bold_ital,
    'isc':  string.upper,  # italics small caps
    'cl':   _ital,         # cognate xref italics
    'ct':   string.upper,  # cognate xref small caps
}

def assemble_and_join_text(element, skip_tags = None, only_tags = None):
    texts = assemble_text(element, skip_tags=skip_tags, only_tags=only_tags)
    return ' '.join(texts).replace('  ', ' ')

def assemble_text(element, skip_tags = None, only_tags = None):
    '''
    Modification of ElementTree.itertext(). Assembles the text from an
    element and its children, replacing certain tags (such as <it>, for
    "italic") with certain text substitutes.
    '''
    if only_tags is None:
        keep_tag = lambda tag: True
    else:
        keep_tag = lambda tag: tag in only_tags

    if skip_tags is None:
        skip_tags = set()
    else:
        skip_tags = set(skip_tags)

    tag = element.tag
    if (tag not in skip_tags) and keep_tag(tag):
        if element.text:
            text = element.text.strip()
            if len(text) > 0:
                formatter = FORMAT_TAGS.get(tag, _pass_through)
                yield formatter(text)

    for e in element:
        for s in assemble_text(e, skip_tags):
            yield s
        if e.tail:
            yield e.tail

def first_child(elem, child_name):
    '''
    Get the first child element with a specific element name.
    '''
    first = take(1, elem.iter(child_name))
    if (not first) or (len(first) == 0):
        return None
    return first[0]

def first_text(root, element, default=''):
    '''
    Find the first child element of a specific name and assemble its text.
    '''
    first = first_child(root, element)
    if first is None:
        return default
    return assemble_and_join_text(first)

