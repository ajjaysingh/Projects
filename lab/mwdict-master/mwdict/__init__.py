#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""mwdict - Display word definition from Merriam Webster's online dictionary

Copyright and License
=====================

Copyright © 2016, Brian M. Clapper
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from future.builtins import object

# Info about the module
__version__   = '1.0.6'
__author__    = 'Brian M. Clapper'
__email__     = 'bmc@clapper.org'
__url__       = 'https://github.com/bmc/mwdict'
__copyright__ = '2015 Brian M. Clapper'
__license__   = 'BSD New license'

# Package stuff

__all__     = [
    'BaseDefinition',
    'ConfigException',
    'Definition',
    'Definitions',
    'Suggestions',
    'WordDefiner'
]

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import os
import sys
import tempfile
import urllib
import urllib2
from docopt import docopt
from configparser import SafeConfigParser, NoOptionError, NoSectionError
import xml.etree.ElementTree as ET
import pickle
from abc import ABCMeta, abstractmethod
import re

from formatters import *
from utils import *
import xmlutil

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

NAME = 'mwdict'

DEFAULT_CONFIG = os.path.join(os.getenv("HOME"), ".mwdict")

USAGE="""
Usage: {0} [options] WORD ...
       {0} --version
       {0} --show-cache

Options:
  --config=CFG, -c CFG                specify configuration [default: {1}]
  --etymology, -e                     show word etymology, as well as definition
  --help, -h                          this screen
  --show-cache, -s                    show which words are currently cached
  --type=OUTPUT_TYPE, -t OUTPUT_TYPE  output type [default: text].
                                        'html' is embeddable HTML.
                                        'htmls' is standalone HTML.
                                        'text' is plain text
                                        'xml' is unformatted XML (from the API)
                                        'xmlpp' is pretty-printed XML
  --verbose, -v                       show verbose messages
  --version                           show version and exit.
""".format(NAME, DEFAULT_CONFIG)

DEFAULT_URL = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml"

# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------

is_verbose = False

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def verbose(msg):
    '''
    Issue a message if verbose is enabled.
    '''
    if is_verbose:
        sys.stderr.write(msg + '\n')

# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------

class ConfigException(Exception):
    pass

class WordSense(object):
    '''
    A word sense (a.k.a, a subdefinition)
    '''
    def __init__(self, ordinal, subordinal, text):
        '''
        Create a new WordSense object.

        :param ordinal:    The ordinal text ("1", "2", etc.)
        :param subordinal: The subordinal ("a", "b", etc.) or None
        :param text:       The text
        '''
        self._ordinal = ordinal
        self._subordinal = subordinal
        self._text = text

    @property
    def ordinal(self):
        return self._ordinal

    @property
    def subordinal(self):
        return self._subordinal

    @property
    def text(self):
        return self._text

class BaseEntry(object):
    '''Abstract base class for word entry.'''
    __metaclass__ = ABCMeta

    def __init__(self, original_word):
        '''
        Params:

        original_word - The original word for which the user was searching
        '''
        self._original_word = original_word

    @property
    def original_word(self):
        '''The original word for which the user was searching.'''
        return self._original_word

    @abstractmethod
    def is_definition(self):
        '''
        Return True if this is a definition and False if it's a Suggestions
        object.
        '''
        pass

class WordEntry(object):
    '''
    A single definition for a word.
    '''
    def __init__(self, word, definition_text, senses, part_of_speech,
                 etymology, pronunciation, date):
        '''
        :param word:            the word, as loaded from the dictionary
                                (distinct from original_word, which is what
                                the user sought)
        :param definition_text: the text of the definition, exclusive of senses
        :param senses:          list of WordSense object. May be empty or None
        :param part_of_speech:  text for the part of speech (verb, noun, etc.),
                                or None
        :param etymology:       the words etymology, or None
        :param pronunciation:   pronunciation key
        :param date:            word origin date (text), or None
        '''
        self._word = word
        self._definition_text = definition_text
        self._senses = senses
        self._part_of_speech = part_of_speech
        self._etymology = etymology
        self._pronunciation = pronunciation
        self._date = date

    @property
    def word(self):
        return self._word

    @property
    def date(self):
        return self._date

    @property
    def definition_text(self):
        return self._definition_text

    @property
    def senses(self):
        return self._senses

    @property
    def part_of_speech(self):
        return self._part_of_speech

    @property
    def etymology(self):
        return self._etymology

    @property
    def pronunciation(self):
        return self._pronunciation

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'WordDefinition(word="{0}")'.format(self.word)

class WordEntries(BaseEntry):
    '''Immutable container for all entries for a particular word.'''
    def __init__(self, original_word, definitions):
        BaseEntry.__init__(self, original_word)
        self._definitions = definitions

    @property
    def definitions(self):
        return self._definitions

    def __len__(self):
        return len(self._definitions)

    def __iter__(self):
        return (d for d in self._definitions)

    def is_definition(self):
        return True

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'WordEntries(original_word="{0}")'.format(self.original_word)

class Suggestions(BaseEntry):
    '''Immutable suggestion object (for unmatched words)'''

    def __init__(self, original_word, suggestions):
        BaseEntry.__init__(self, original_word)
        self._suggestions = suggestions

    @property
    def suggestions(self):
        return self._suggestions

    def __len__(self):
        return len(self._suggestions)

    def __iter__(self):
        return (s for s in self._suggestions)

    def is_definition(self):
        return False

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Suggestions(original_word="{0}")'.format(self.original_word)

class WordDefiner(object):
    '''
    Reads word definitions and produces WordEntries and Suggestions
    objects. Text formatting instructions (italics, etc.) are converted to
    a Markdown-like syntax.
    '''
    SENSE_RE = re.compile(r'^\s*([^\s]+)\s*([^\s]*)\s*$')

    def __init__(self, config_file):
        self._cache = {}
        self._cache_file = None

        self._config = self._read_config(config_file)
        self._api_key = self._config.get('main', 'api_key')
        if self._config.has_option('main', 'dictionary_url'):
            self._url = config.get('main', 'dictionary_url')
        else:
            self._url = DEFAULT_URL

        self._load_cache()

    @property
    def cache_file(self):
        return self._cache_file

    @property
    def cache(self):
        '''
        Get the cache, a dictionary of words and XML.
        '''
        return self._cache

    def find_definitions(self, words, xml=False):
        '''
        Find the definitions for various words, returning an array of
        formatted results.

        Params:

        url     - the base URL
        words   - iterable of words to find
        xml     - True to return the raw XML, False to return WordEntry objects
        '''
        u_key = urllib.quote(self._api_key)
        return [self._find_definition(u_key, word, xml) for word in words]

    def save_cache(self):
        '''
        Save the cache. Call this just before exiting.
        '''
        if self._cache_file:
            pickle.dump(self._cache, open(self._cache_file, 'w'))

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    def _find_definition(self, u_key, word, return_xml):
        '''
        Find the definition of a word, returning the WordEntry result.

        Params:

        u_key      - the API key, already URL-encoded
        url        - the base URL to which to connect
        word       - the word to fine
        return_xml - True to return parsed XML DOM, False to return WordEntry
                     objects
        '''
        t = tempfile.NamedTemporaryFile(suffix=".xml", delete=False)
        u = None

        try:
            if word in self._cache:
                xml = self._cache[word]
            else:
                u_word = urllib.quote(word)
                full_url = "{0}/{1}?key={2}".format(self._url, u_word, u_key)
                verbose(
                    'Getting definition for "{0}" from {1}...'.format(
                        word, full_url
                    )
                )
                opener = urllib2.build_opener()
                opener.addheaders = [('Accept-Charset', 'utf-8')]
                u = opener.open(full_url)
                xml = u.read().decode('utf-8')

            t.write(utf8(xml))
            t.close()
            # Cache both the word the user typed and the word(s) we got
            # back.
            (entries, root) = self._parse(word, t.name)
            self._cache[word] = xml
            if entries.is_definition():
                for entry in entries:
                    self._cache[entry.word] = xml

            return root if return_xml else entries
        finally:
            os.unlink(t.name)
            if u:
                u.close()

    def _parse_suggestions(self, word, suggestion_elements):
        '''
        Parse the result for a not-found word, which contains suggestions.
        '''
        return Suggestions(word, [e.text for e in suggestion_elements])

    def _parse_found_word(self, word, root):
        '''
        Parse the result for a found word.

        Face it: This is one ugly XML format. See
        http://dictionaryapi.com/content/products/documentation/collegiate-tag-description.txt
        '''
        def fix_text(s):
            s = s.strip()
            if (len(s) > 0) and (s[0] == ':'):
                s = s[1:]
            return s.replace(' ,', ',').replace('  ', ' ')

        def parse_dt(elem):
            text = ''
            xrefs = []

            def add_xrefs(text, xrefs):
                if len(xrefs) > 0:
                    return text + ' ' + ', '.join(xrefs)
                else:
                    return text

            for d in elem.iter():
                if d.tag == 'sx':
                    xrefs.append(fix_text(d.text.upper()))
                else:
                    text = add_xrefs(text, xrefs)
                    xrefs = []

                    if d.tag == 'dt':
                        text = text + ' ' + fix_text(d.text)
                    elif d.tag == 'un':
                        # Usage note
                        text = text + ' ' + "[USAGE NOTE: {0}]".format(d.text)
                    elif d.tag == 'dx':
                        text = text + ' ' + xmlutil.assemble_and_join_text(d)
                    elif d.tag == 'sd':
                        text = text + '; ' + xmlutil.assemble_and_join_text(d)
                    else:
                        text = text + ' ' + xmlutil.assemble_and_join_text(d)

                    if d.tail:
                        text = text + ' ' + fix_text(d.tail)

            text = add_xrefs(text, xrefs)
            if elem.tail:
                text = text + ' ' + elem.tail

            return fix_text(text)

        def parse_definition(defn_container):
            text = ''
            senses = []
            sn_seen = None
            for element in defn_container.iter():
                if element.tag == 'dt':
                    t = parse_dt(element)
                    if sn_seen:
                        (ord, subord) = sn_seen
                        senses.append(WordSense(ord, subord, t))
                    else:
                        text = text + ' ' + t

                elif element.tag == 'sd':
                    if len(text) > 0:
                        text = text + ', '
                    text = text + ' ' + element.text

                elif (element.tag == 'sn') and (element.text is not None):
                    m = WordDefiner.SENSE_RE.match(element.text)
                    if m:
                        groups = m.groups()
                        ordinal = groups[0]
                        subordinal = groups[1] if len(groups) == 2 else None
                        sn_seen = (ordinal, subordinal)

            text = text.strip().replace(' ,', ',')
            if len(text) > 0:
                defn = text
            else:
                defn = None

            return (defn, senses)

        entries = list(root.iter('entry'))
        definitions = []
        for entry in entries:
            defn_container = xmlutil.first_child(entry, 'def')
            defn = None
            entry_word = xmlutil.first_text(entry, 'ew', None)

            # Skip entries that don't have the original word anywhere in
            # them. This can happen because the API returns related phrases
            # (e.g., "raise" comes back for "cain", as in "raise cain").
            # For now, a simple substring match is fine.
            if word.lower() not in entry_word.lower():
                continue

            date = xmlutil.first_text(entry, 'date', None)
            pron = xmlutil.first_text(entry, 'pr', None)
            kind = xmlutil.first_text(entry, 'fl', None)

            if defn_container is not None:
                (defn, senses) = parse_definition(defn_container)
            else:
                (defn, senses) = (xmlutil.first_text(entry, 'cx', None), {})

            if (not defn) and (len(senses) == 0):
                continue

            if defn is not None:
                defn = defn.strip()
                if defn[0] == ':':
                    defn = defn[1:]

            definitions.append(
                WordEntry(word            = entry_word,
                          date            = date,
                          definition_text = defn,
                          senses          = senses,
                          part_of_speech  = kind,
                          etymology       = xmlutil.first_text(entry, 'et'),
                          pronunciation   = pron)
            )

        return WordEntries(original_word=word, definitions=definitions)

    def _parse(self, word, xml_file):
        '''
        Parse an XML definition and format it for display.
        '''
        root = ET.parse(xml_file)
        # If there are <suggestion> objects, then there was no match.
        suggestion_elements = list(root.iter('suggestion'))
        if len(suggestion_elements) > 0:
            return (self._parse_suggestions(word, suggestion_elements), root)
        else:
            return (self._parse_found_word(word, root), root)


    def _read_config(self, path):
        '''
        Load the configuration. Returns None on error.

        Params:

        path - the path to the configuration
        '''
        if not os.path.exists(path):
            raise ConfigException(
                'Configuration file "{0}" does not exist.'.format(path)
            )

        config = SafeConfigParser()
        config.read(path)
        return config

    def _load_cache(self):
        self._cache_file = None
        self._cache = {}
        if self._config.has_option('main', 'cache_file'):
            self._cache_file = os.path.expanduser(
                self._config.get('main', 'cache_file')
            )
            if not os.path.exists(self._cache_file):
                cache_dir = os.path.dirname(self._cache_file)
                if not os.path.exists(cache_dir):
                    verbose(
                        'Creating cache directory "{0}"...'.format(cache_dir)
                    )
                    os.makedirs(cache_dir)
            else:
                verbose('Loading cache file "{0}"'.format(self._cache_file))
                self._cache = pickle.load(open(self._cache_file))

def show_cache(definer):
    from textwrap import TextWrapper
    import inflection

    def singular_plural(n, word):
        if word == 0:
            return ('no', inflection.pluralize(word))
        elif word == 1:
            return (1, word)
        else:
            return (str(n), inflection.pluralize(word))

    cache_file = definer.cache_file
    if cache_file is None:
        print("Caching is not enabled.")
    else:
        words = sorted(definer.cache.keys())
        n = len(words)
        wrapper = TextWrapper(width=WRAP_WIDTH)
        print(wrapper.fill(
            'Definition cache "{0}" contains {1} {2}.'.format(
                cache_file, *singular_plural(n, 'word')
            ))
        )
        if n > 0:
            print('\n' + wrapper.fill(', '.join(words)))

def show_definitions(definer, words, formatter, show_xml):
    defs = definer.find_definitions(words, xml=show_xml)
    if is_verbose:
        print()
    print(utf8(formatter.format(defs)))

# ---------------------------------------------------------------------------
# Main Program
# ---------------------------------------------------------------------------

def main():
    global is_verbose

    try:
        args = docopt(USAGE)

        if args.get('--version'):
            print('{0}, version {1}'.format(NAME, __version__))
            sys.exit(0)

        is_verbose = args.get('--verbose')
        config_file = args.get('--config')
        etymology = args.get('--etymology')
        output_type = args.get('--type')
        show_xml = False
        if output_type == 'html':
            formatter = HTMLDefinitionsFormatter(etymology)
        elif output_type == 'htmls':
            formatter = HTMLDefinitionsFormatter(etymology, standalone=True)
        elif output_type == 'text':
            formatter = TextDefinitionsFormatter(etymology)
        elif output_type in 'xml':
            formatter = XMLDefinitionsFormatter()
            show_xml = True
        elif output_type in 'xmlpp':
            formatter = XMLDefinitionsFormatter(pretty_print=True)
            show_xml = True
        else:
            die('Unknown output type: "{0}"'.format(output_type))

        definer = WordDefiner(config_file)

        if args.get('--show-cache'):
            show_cache(definer)
        else:
            show_definitions(definer, args.get('WORD'), formatter, show_xml)
        definer.save_cache()

    except (NoOptionError, NoSectionError) as ex:
        die("{0}: {1}".format(config_file, ex.message))

    except ConfigException as ex:
        die(ex.message)

if __name__ == "__main__":
    main()
