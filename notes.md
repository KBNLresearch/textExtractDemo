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

### Colophon text

DBNL books *do* contain colophon text (e.g. berk011veel01_01.epub), which is also included in the extraction result.

