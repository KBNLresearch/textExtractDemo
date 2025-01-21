# EPUB text extraction demo

## Contents of this repo

- [Tika demo script](./scripts/extract-tika.py)
- [Textract demo script](./scripts/extract-textract.py)
- [Ebooklib demo script](./scripts/extract-ebooklib.py)
- [PyMuPDF demo script](./scripts/extract-pymupdf.py)
- [Working notes](./doc/notes.md)

## Demo scripts

Each of these demo scripts iterates over files with an .epub extension in a user-defined input directory. For each of these files, it extracts the text, and writes the extracted text (using UTF-8 encoding) to a file in a user-defined output directory. It also writes a summary file with the word count for each EPUB.

## Tika-python script

### Usage

```
python3 extract-tika.py dirIn dirOut
```
positional arguments:

- dirIn: directory with input EPUB files
- dirOut: output directory

### Example

```
python3 ./textExtractDemo/scripts/extract-tika.py DBNL_EPUBS_moderneromans/ out-dbnl/
```

## Textract script

### Usage

```
python3 extract-textract.py dirIn dirOut
```
positional arguments:

- dirIn: directory with input EPUB files
- dirOut: output directory

### Example

```
python3 ./textExtractDemo/scripts/extract-textract.py DBNL_EPUBS_moderneromans/ out-dbnl/
```

## Ebooklib script

### Usage

```
python3 extract-ebooklib.py dirIn dirOut
```
positional arguments:

- dirIn: directory with input EPUB files
- dirOut: output directory

### Example

```
python3 ./textExtractDemo/scripts/extract-ebooklib.py DBNL_EPUBS_moderneromans/ out-dbnl/
```

## PyMuPDF script

### Usage

```
python3 extract-pymupdf.py dirIn dirOut
```
positional arguments:

- dirIn: directory with input EPUB files
- dirOut: output directory

### Example

```
python3 ./textExtractDemo/scripts/extract-pymupdf.py DBNL_EPUBS_moderneromans/ out-dbnl/
```

