# mwdict

## Introduction

*mwdict* is a simple REST client for the [Merriam Webster REST API][]. It
takes one or more words on the command line, retrieves their definitions,
and displays them to standard output in UTF-8. It requires a configuration
file (in `~/.mwdict` by default) that contains the API key for Merriam Webster.

## Installation

*mwdict* is a Python command line program. It has _not_ been registered with the
Python Package Index, so it's not installable via `pip`. To install, clone this
repository (or download and unpack the source from
<https://github.com/bmc/mwdict/archive/master.zip>), and install via:

    python setup.py install

## Configuration

The [Merriam Webster REST API][] requires an application key before you're
allowed to issue requests. You can't have mine, so you'll have to register
with the site and create your own key for the Collegiate dictionary. Then,
you'll need put that key in a configuration file, which defaults to
`$HOME/.mwdict`. See `dot-mwdict` for a sample configuration file.

The configuration file also allows you to define the location of a cache file
(which is disabled by default). If a cache file is defined, then `mwdict` will
look in the cache before issuing a REST query and will save any definitions
back to the cache file. A cache file can reduce the number of REST queries,
which ensures faster response time for cached entries. (The cache is stored
as a pickled Python dictionary.)

## Usage

Type

    mwdict -h
    
to get a full usage message.

## Sample output

```
$ mwdict -e zoea elain phiz vina boride page
zoea (noun) [zō-ˈē-ə]: a free-swimming planktonic larval form of many decapod
  crustaceans and especially crabs that has a relatively large cephalothorax,
  conspicuous eyes, and fringed antennae and mouthparts. Etymology: New Latin,
  from Greek /zōē/ life

No definition for elain. Suggestions: alien, Elion, Elaine, eolian, elan,
  olein, Eilean, Ealing, align, all in, all-in, A-line, El Aiun, Ellyn,
  aeolian, eloign, Ohlin, healing, uhlan

phiz (noun) [ˈfiz]: face. Etymology: by shortening & alteration from
  /physiognomy/

vina (multiple definitions)
   1. vina (noun) [ˈvē-nə]: a stringed instrument of India having usually four
      strings on a long bamboo fingerboard with movable frets and a gourd
      resonator at each end. Etymology: Hindi /vīṇā/, from Sanskrit
   2. veena: /variant/ of VINA.
   3. Vina del Mar (geographical name) [ˈvē-nyä-(ˌ)t͟hel-ˈmär]: city & port
      /cen/ Chile E of Valparaiso /pop/ 286,931.

boride (noun) [ˈbȯr-ˌīd]: a binary compound of boron with a more
  electropositive element or radical.

page (multiple definitions)
   1. page (noun) [ˈpāj]: a youth being trained for the medieval rank of knight
      and in the personal service of a knight. Etymology: Middle English, from
      Anglo-French
   2. page (verb): to wait on or serve in the capacity of a page.
   3. page (noun): one of the leaves of a publication or manuscript. Etymology:
      Middle French, from Latin /pagina/; akin to Latin /pangere/ to fix,
      fasten pact
   4. page (verb): to number or mark the pages of.
   5. Page (biographical name) [ˈpāj]: Walter Hines 1855–1918 Am. journalist &
      diplomat.
   6. page boy (noun): a boy serving as a page.
   7. page-turner (noun) [ˈpāj-ˌtər-nər]: an engrossing book or story.
   8. front-page (adjective) [ˈfrənt-ˈpāj]: printed on the front page of a
      newspaper.
   9. front-page (verb): to print or report on the front page.
  10. home page (noun): the page typically encountered first on a Web site that
      usually contains links to the other pages of the site.
```

[Merriam Webster REST API]: http://www.dictionaryapi.com
