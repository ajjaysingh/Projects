# Change log for mwdict

Version 1.0.6

- Handle empty `<sn>` elements properly when parsing XML response.
- Skip returned entries that don't actually have the original
  (searched-for) word in them. This can happen because the M-W
  REST API can return related words. (For instance, it'll return
  "raise" when "cain" is requested, because "raise cain" is related.)
- Allow dumping of REST API-returned XML, in either raw or
  pretty-printed format.
- Handle empty results (i.e., result with no definitions or
  suggestions).
- Handle empty definition, but multiple sense (`<sn>`) entries.
- Better handling of `<sn>` elements, including keeping them in order.
- Refactored parsing of (ugly) M-W XML format to handle `<dt>` entries better.


Version 1.0.5

- Added `--show-cache` option.
- Updated cache logic to cache both the original word and whatever words
  are returned.

Version 1.0.4

- Modified XML parsing to handling of variant definitions better.
- Put XML utility functions in another module.

Version 1.0.3

- Factored result parsing from formatting; result parsing now produces more or
  less generic objects (with embedded Markdown). Formatters now convert these
  objects into strings.
- Added a quick-and-dirty HTML formatter.
- Added `--type` argument to select output type (embeddable HTML, standalone
  HTML or text).
- Added `--version` argument.

Version 1.0.2

- Added ability to have definitions cached locally, to minimize REST lookups.
- Added etymology to output.
- Added processing of dictionary XML formatting elements (e.g., <it>, <sc>, etc.)
- Added support for multiple definitions.
- Handle variants (i.e., cross-referenced words).
- Added --verbose command line flag, with some verbose messages.
- Display of etymology is now optional.

Version 1.0.1

- Handle abbreviations (which have no pronuniation key).
- Added installation and configuration instructions.
- Handle not-found words.

Version 1.0.0

- Initial version
