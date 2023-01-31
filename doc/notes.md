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

### Text encoding?

What happens if extracted content has a decoding that is not UTF-8? Or are the text strings returned by Tika UTF-8 by default? Important, because EPUB allows both UTF-8 and UTF-16.

For EPUB 2 (<https://idpf.org/epub/20/spec/OPS_2.0.1_draft.htm>):

> Publications may use the entire Unicode character set, using UTF-8 or UTF-16 encodings

EPUB 3 (<https://www.w3.org/TR/epub-33/#sec-xml-constraints>):

> Any publication resource that is an XML-based media type \[rfc2046\] (...) MUST be encoded in
> UTF-8 or UTF-16 \[unicode\], with UTF-8 as the RECOMMENDED encoding.

Possible test: create test EPUB with some UTF-16 encoded resources.

### Xhtml output

It is possible to extract the text to XHTML output instead of unformatted text. This is done by changing the call to Tika's parser function to:

```python
parsed = parser.from_file(fileIn, xmlContent=True)
```

Even though this does preserve the internal document structure, it's still not that straightforward to identify things like footnotes, because they're not explicitly tagged. See below example: 

```html
<div class="voetnoten"><a class="footnote-link zz_voetnootcijfer" href="dhae007euro01_01-0003.xhtml#n001T" id="n001">1</a>Voor Nieuwenhuys is de conversatie, zelfs de roddel, de belangrijkste ontstaansgrond, maar daarbij heeft hij uiteraard de latere koloniale samenleving (negentiende en begin twintigste eeuw) in gedachten.</div>
```

Here the footnote is wrapped inside a *div* element, where the value of the *class*  attribute identifies it as a footnote. But the *class* values are not in any way standardized, and there are no controlled vocabularies for this. So the implementation will vary from one publisher to another. See also:

<https://stackoverflow.com/questions/18162068/semantic-elements-for-footnote-list-and-content>

and:

<https://www.davidmacd.com/blog/html51-footnotes.html>

Also, in the tested (2.6.0) version of Tika-python the resulting output is not well-formed XHTML, as it also includes metadata. This looks like a bug, so I reported this here:

<https://github.com/chrismattmann/tika-python/issues/389#issuecomment-1405087039>


## Textract

> Extract text from any document. No muss. No fuss.

<https://github.com/deanmalmgren/textract>

This uses Ebooklib for EPUB:

<https://github.com/aerkalov/ebooklib>

Installation:

```
pip install textract
```

This installed Textract v1.6.5. In my case this gave me some errors:

```
ERROR: launchpadlib 1.10.13 requires testresources, which is not installed.
ERROR: pdfx 1.4.1 has requirement chardet==4.0.0, but you'll have chardet 3.0.4 which is incompatible.
ERROR: pdfx 1.4.1 has requirement pdfminer.six==20201018, but you'll have pdfminer-six 20191110 which is incompatible.
```

As these are all pdf-related, so I'm assuming they won't affect EPUB behaviour.

Basic usage:

```python
import textract

fileIn = "e-e-smith_the-skylark-of-space.epub"
fileOut = "test.txt"
content = textract.process(fileIn, encoding='utf-8').decode()

with open(fileOut, 'w', encoding='utf-8') as fout:
                fout.write(content)
```

BUT for DBNL books "content" is empty in most cases (zero-byte bytes object) or just a few words. It did work OK with the Standard Ebooks examples I tried, no idea why.


## Handling of whitespace characters

Example:

[The Strange Case of Dr. Jekyll and Mr. Hyde](https://standardebooks.org/ebooks/robert-louis-stevenson/the-strange-case-of-dr-jekyll-and-mr-hyde/downloads/robert-louis-stevenson_the-strange-case-of-dr-jekyll-and-mr-hyde.epub)

Tika output:


```
			The pair walked on again for a while in silence; and then “Enfield,” said Mr. Utterson, “that’s a good rule of yours.”

			“Yes, I think it is,” returned Enfield.

```

Textract output:

```
The pair walked on again for a while in silence; and then “Enfield,” said Mr. Utterson, “that’s a good rule of yours.”
“Yes, I think it is,” returned Enfield.
```

Xhtml source:

```xhtml
			<p>The pair walked on again for a while in silence; and then “Enfield,” said <abbr>Mr.</abbr> Utterson, “that’s a good rule of yours.”</p>
			<p>“Yes, I think it is,” returned Enfield.</p>
```

Note how the tab characters in the Xhtml source file are added to the extracted text by Tika. On the other hand, Textract only extracts the text that is *inside* the paragraph element (ignoring any indentation of the XHTML source).

If this is a problem: split Tika output into separate lines, and then trim leading/trailing whitespace characters. See demo script.


## Word counts

King Lear: 28442 words with Tika, 18621 with Textract!

## Demo scripts

Iterate over all files with .epub extension in input directory, and write extracted text to text files in output directory. Also writes summary file with word count for each EPUB.

### Tika script

Usage:

```
python3 extract-tika.py [-h] [--trim] dirIn dirOut
```
positional arguments:

- dirIn: directory with input EPUB files
- dirOut: output directory
- --trim, -t: trim leading and trailing whitespace from Tika output
- -h, --help:  show help message and exit

### Textract script

```
python3 extract-textract.py [-h] dirIn dirOut
```
positional arguments:

- dirIn: directory with input EPUB files
- dirOut: output directory
- -h, --help:  show help message and exit

### Ebooklib script

```
python3 extract-ebooklib.py [-h] dirIn dirOut
```
positional arguments:

- dirIn: directory with input EPUB files
- dirOut: output directory
- -h, --help:  show help message and exit


### Examples

Tika:

```
python3 ./textExtractDemo/scripts/extract-tika.py DBNL_EPUBS_moderneromans/ out-dbnl/ -t
```

Textract:

```
python3 ./textExtractDemo/scripts/extract-textract.py DBNL_EPUBS_moderneromans/ out-dbnl/
```

Ebooklib:

```
python3 ./textExtractDemo/scripts/extract-ebooklib.py DBNL_EPUBS_moderneromans/ out-dbnl/
```

## Word counts DBNL

|fileName|Tika|Textract|Ebooklib|
|:--|:--|:--|:--|
|eern001lief01_01.epub|25450|1|25446|
|spro002mure01_01.epub|50553|0|50549|
|berk011veel01_01.epub|67978|0|67974|
|sche034drie01_01.epub|203853|3|203352|
|jous010supe01_01.epub|202495|0|202491|
|dele035wegv01_01.epub|76536|0|76530|
|verv017eerl01_01.epub|33844|0|33840|
|dhae007euro01_01.epub|394455|2|394400|
|gomm002uurw01_01.epub|43754|0|43731|
|gang009lalb01_01.epub|28453|4|28381|
|geel005bloe01_01.epub|76316|0|76312|
|hart008droo02_01.epub|77283|0|77279|
|eede003vand04_01.epub|120481|6|120310|
|meij031tuss02_01.epub|145678|4|145665|
|maas013blau01_01.epub|55099|0|55093|

## Word counts Standard Ebooks

|fileName|Tika|Textract|Ebooklib|
|:--|:--|:--|:--|
|william-shakespeare_king-lear.epub|28442|18621|28430|
|david-garnett_lady-into-fox.epub|25240|25223|25228|
|joseph-conrad_heart-of-darkness.epub|38717|38698|38705|
|anthony-trollope_the-dukes-children.epub|223014|222995|223002|
|agatha-christie_the-mysterious-affair-at-styles.epub|57401|57229|57271|
|edgar-allan-poe_the-narrative-of-arthur-gordon-pym-of-nantucket.epub|71931|71837|71863|
|p-g-wodehouse_short-fiction.epub|212224|212182|212212|
|robert-louis-stevenson_the-strange-case-of-dr-jekyll-and-mr-hyde.epub|26370|26345|26358|
|h-g-wells_the-time-machine.epub|33044|33024|33032|
|thorstein-veblen_the-theory-of-the-leisure-class.epub|106537|106515|106525|

