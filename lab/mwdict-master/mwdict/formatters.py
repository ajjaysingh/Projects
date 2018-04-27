from __future__ import print_function
from future import standard_library
standard_library.install_aliases()

from abc import ABCMeta, abstractmethod
from textwrap import TextWrapper
from StringIO import StringIO
from utils import *

'''
Formatter classes.
'''

class BaseDefinitionsFormatter(object):
    '''
    Abstract base class for formatters. A formatter takes the abstract parsed
    definitions and renders them into some kind of string.
    '''
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def format(self, definitions):
        '''
        Format a list of definitions (consisting of Definition and
        Suggestions objects) for output. Returns a string, the contents
        of which depend on the particular formatter subclass.
        '''
        pass

class XMLDefinitionsFormatter(BaseDefinitionsFormatter):

    def __init__(self, pretty_print=False, width=WRAP_WIDTH, indent=2):
        '''
        Format a list of XML DOM definitions.

        Params:
        pretty_print - True to pretty print the output, False to print
                       it raw.
        width        - Text wrap width. Only honored when pretty-printing.
        indent       - indentation level. Only honored when pretty-
                       printing
        '''
        BaseDefinitionsFormatter.__init__(self)
        self._wrap_width   = width
        self._pretty_print = pretty_print
        self._indent       = indent

    def format(self, definitions):
        '''
        Format a list of XML DOM definitions.

        Params:
        definitions  - the list of definitions, each of which must be
                       a parsed ElementTree DOM
        '''
        out = StringIO()
        f = self._xml_pprint if self._pretty_print else self._xml_dump
        for index, root in enumerate(definitions):
            if index > 0:
                dom.write('\n')
            f(out, root)

        return out.getvalue()

    def _xml_dump(self, out, root):
        out.write(u'<?xml version="1.0" encoding="ASCII"?>\n')
        root.write(out, xml_declaration=True)

    def _xml_pprint(self, out, root):
        # Cheat: Reparse the DOM in minidom, and use its
        # pretty printer.
        import xml.etree.ElementTree as ET
        from xml.dom import minidom
        import re
        subsequent_indentation = ' ' * self._indent
        mdom = minidom.parseString(ET.tostring(root.getroot()))
        temp = StringIO()
        mdom.writexml(temp, addindent=subsequent_indentation, newl="\n", encoding="UTF-8")
        s = temp.getvalue()
        out.write(re.sub('(\\s*\n)+', '\n', s))

class TextDefinitionsFormatter(BaseDefinitionsFormatter):
    '''
    Formats a set of definitions and suggestions for textual (terminal) output.
    '''

    INDENT_LEVEL = 2
    INDENT = ' ' * INDENT_LEVEL
    WRAPPER_CONFIG = {
        'initial_indent':    '',
        'subsequent_indent': INDENT
    }

    def __init__(self, show_etymology, width = WRAP_WIDTH):
        BaseDefinitionsFormatter.__init__(self)
        self._width = width
        self._show_etymology = show_etymology

    def format(self, definitions):
        '''
        Format a list of definitions (consisting of Definition and
        Suggestions objects) for output. Returns a string suitable for
        display on a terminal, wrapped to the width specified on the
        constructor.
        '''
        result = []
        for defn in definitions:
            if len(defn) == 0:
                result.append(u'No definitions or suggestions for "{0}".'.format(
                    defn.original_word
                ))
            elif defn.is_definition():
                result.append(self._format_definition(defn))
            else:
                result.append(self._format_suggestions(defn))

        return '\n\n'.join(result)

    def _format_suggestions(self, suggestions_object):
        '''
        Format returned suggestions for a not-found word.
        '''
        wrapper_kw = dict_merge(TextDefinitionsFormatter.WRAPPER_CONFIG,
                                {'width': self._width})
        wrapper = TextWrapper(**wrapper_kw)
        suggestions = ', '.join([s for s in suggestions_object.suggestions])
        s = 'No definition for {0}. Suggestions: {1}'.format(
            suggestions_object.original_word, suggestions
        )
        return wrapper.fill(s)

    def _format_definition(self, definitions_object):
        '''
        Format a definition.
        '''
        show_index = len(definitions_object.definitions) > 1
        if show_index:
            word = definitions_object.original_word
            result = [u'{0} (multiple definitions)'.format(word)]
            indent = TextDefinitionsFormatter.INDENT
            wrapper_kw = dict_merge(TextDefinitionsFormatter.WRAPPER_CONFIG,
                                    {'initial_indent':    indent,
                                     'subsequent_indent': '    ' + indent})
        else:
            wrapper_kw = TextDefinitionsFormatter.WRAPPER_CONFIG
            result = []

        wrapper = TextWrapper(**wrapper_kw)

        index = 0
        for defn in definitions_object.definitions:
            index += 1

            if show_index:
                s = u'{0:2d}. '.format(index)
            else:
                s = u''

            s = u'{0}{1}'.format(s, defn.word)

            if defn.part_of_speech:
                s = u'{0} ({1})'.format(s, defn.part_of_speech)

            if defn.pronunciation:
                s = u'{0} [{1}]'.format(s, defn.pronunciation)

            if defn.date:
                s = u'{0} ({1})'.format(s, defn.date)

            if defn.definition_text:
                s = u'{0}: {1}'.format(s, defn.definition_text)

            senses = defn.senses
            if len(senses) > 0:
                texts = []
                for sense in senses:
                    if sense.subordinal:
                        texts.append(u'({0}{1}) {2}'.format(
                            sense.ordinal, sense.subordinal, sense.text
                        ))
                    else:
                        texts.append(u'({0}) {1}'.format(
                            sense.ordinal, sense.text
                        ))

                s = s + ' ' + '; '.join(texts)

            if self._show_etymology and defn.etymology:
                s = u'{0}. Etymology: {1}'.format(s, defn.etymology)

            result.append(wrapper.fill(s))

        return '\n'.join(result)

class HTMLDefinitionsFormatter(BaseDefinitionsFormatter):
    '''
    Formats a set of definitions and suggestions for HTML output. This class
    is simple and trivial; it could easily be made more flexible by, for
    instance, externalizing the standalone template.
    '''

    STANDALONE_TEMPLATE = '''<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>Definitions</title>
<style type="text/css">
body { font-family: sans-serif; }
</style>
</head>
<body>
$html
</body>
</html>
'''

    def __init__(self, show_etymology, standalone=False):
        '''
        Params:

        show_etymology - whether to show the etymology or not
        standalone     - whether to produce a standalone HTML document
        '''
        BaseDefinitionsFormatter.__init__(self)
        self._show_etymology = show_etymology
        self._standalone = standalone

    def format(self, definitions):
        '''
        Format a list of definitions (consisting of Definition and
        Suggestions objects) for output. Returns a string suitable for
        display in an HTML document.
        '''
        from string import Template
        from markdown import markdown

        result = []
        for defn in definitions:
            if len(defn) == 0:
                result.append(u'**No definitions or suggestions for "{0}".**.'.format(
                    defn.original_word
                ))
            elif defn.is_definition():
                result.append(self._format_definition(defn))
            else:
                result.append(self._format_suggestions(defn))

        html = markdown('\n'.join(result))
        if self._standalone:
            t = Template(HTMLDefinitionsFormatter.STANDALONE_TEMPLATE)
            return t.substitute(html=html)
        else:
            return html

    def _format_suggestions(self, suggestions_object):
        '''
        Format returned suggestions for a not-found word.
        '''
        m = '**{0}**: No match. Suggestions: {1}'.format(
            suggestions_object.original_word,
            ', '.join([s for s in suggestions_object.suggestions])
        )
        return m

    def _format_definition(self, definitions_object):
        '''
        Format a definition.
        '''
        show_index = len(definitions_object.definitions) > 1
        if show_index:
            word = definitions_object.original_word
            s = u'**{0}** (multiple definitions):\n\n'.format(word)
        else:
            s = u''

        index = 0
        for defn in definitions_object.definitions:
            index += 1
            if show_index:
                s = s + '{0}. '.format(index)

            s = u'{0}**{1}**'.format(s, defn.word)

            if defn.part_of_speech:
                s = u'{0} ({1})'.format(s, defn.part_of_speech)

            if defn.pronunciation:
                s = u'{0} [**{1}**]'.format(s, defn.pronunciation)

            if defn.date:
                s = u'{0} ({1})'.format(s, defn.date)

            if defn.definition_text:
                s = u'{0}: {1}'.format(s, defn.definition_text)

            senses = defn.senses
            if len(senses) > 0:
                texts = []
                for sense in senses:
                    if sense.subordinal:
                        texts.append(u'({0}{1}) {2}'.format(
                                sense.ordinal, sense.subordinal, sense.text
                        ))
                    else:
                        texts.append(u'({0}) {1}'.format(
                                sense.ordinal, sense.text
                        ))

                s = s + ' ' + '; '.join(texts)

            if self._show_etymology and defn.etymology:
                s = u'{0}. Etymology: {1}'.format(s, defn.etymology)

            s = s + '\n'

        s = s + '\n'
        return s
