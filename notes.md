# Text extraction from EPUB files

Test environment: local desktop machine running Linux Mint 20.1 Ulyssa, MATE edition.

## Tika-python

See installation instructions here:

<https://github.com/chrismattmann/tika-python>

The Airgap Environment Setup looks useful for running Tika in an environment without Internet access (haven't tried this myself).

Tested version: tika-2.6.0

## Issues


### Font names

Extracted text is followed by what looks like a list of font names, separated by newlines. E.g. for berk011veel01_01.epub: 

```
Charis SIL Bold Italic

::
::

Charis SIL Small Caps
```

BUT if I use Tika directly from the command line this doesn't happen:


```
java -jar ~/tika/tika-app-2.3.0.jar -t /home/johan/kb/epub-tekstextractie/DBNL_EPUBS_moderneromans/berk011veel01_01.epub  > berk.txt
```

Looking at the tika-python code I noticed the "service" parameter:

<https://github.com/chrismattmann/tika-python/blob/master/tika/parser.py#L74>

So I changed the call to: 

```Python
parsed = parser.from_file(fileIn, service='text')
```

After this change the font names are not reported anymore!

Submitted issue for this:

<https://github.com/chrismattmann/tika-python/issues/389>

### Footnotes, index

dhae007euro01_01.epub: contains both.

### Table of Contents, landmarks

Additional tests on some Standard Ebooks (https://standardebooks.org/) files also showed extraction of text from Table of Contents and Landmarks.

E.g. this one:

<https://standardebooks.org/ebooks/e-e-smith/the-skylark-of-space>

Also happens when using Tika directly:

```
java -jar ~/tika/tika-app-2.3.0.jar -t /home/johan/kb/epub-accessibility/standard-ebooks/e-e-smith_the-skylark-of-space.epub > skylark.txt
```

Output originates from toc.xhtml.

### Colophon text

DBNL books *do* contain colophon text (e.g. berk011veel01_01.epub), which is also included in the extraction result.

