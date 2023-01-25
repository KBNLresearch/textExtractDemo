#! /usr/bin/env python3
"""
EPUB text extraction with Apache Tika demo

Requires tika-python:

https://github.com/chrismattmann/tika-python
"""

import os
import sys
import argparse
import tika

# Create argument parser
argParser = argparse.ArgumentParser(
    description="Extract text from EPUB file ")

def parseCommandLine():
    """Parse command-line arguments"""

    argParser.add_argument('dirIn',
                               action="store",
                               type=str,
                               help='directory with input EPUB file')

    argParser.add_argument('dirOut',
                               action='store',
                               type=str,
                               help='output directory')
    # Parse arguments
    args = argParser.parse_args()

    return args


def errorExit(msg):
    """Print error message and exit"""
    sys.stderr.write("ERROR: " + msg + "\n")
    sys.exit(1)


def errorInfo(msg):
    """Print error message"""
    sys.stderr.write("ERROR: " + msg + "\n")


def extractText(fileIn, fileOut):
    """Extract text from input file and write
    result to output file"""

    # Try to parse the file with Tika, and report an error message if
    # parsing fails
    try:
        parsed = tika.parser.from_file(fileIn, service='text')
        successParse = True
    except:
        successParse = False
        msg = "error parsing " + fileIn
        errorInfo(msg)

    # Write extracted text to a text file if parsing was successful    
    if successParse:
        content = parsed["content"]

        try:
            with open(fileOut, 'w', encoding='utf-8') as fout:
                fout.write(content)
            # TODO: what happens here if extracted content has a decoding that
            # is not UTF-8? Or are the text strings returned by Tika UTF-8 by default?
            #
            # Important, because EPUB allows both UTF-8 and UTF-16:
            #
            # EPUB 2 (https://idpf.org/epub/20/spec/OPS_2.0.1_draft.htm):
            # "Publications may use the entire Unicode character set, using UTF-8 or UTF-16 encodings"
            #
            # EPUB 3 (https://www.w3.org/TR/epub-33/#sec-xml-constraints):
            # "Any publication resource that is an XML-based media type [rfc2046] (...) MUST be encoded in
            # UTF-8 or UTF-16 [unicode], with UTF-8 as the RECOMMENDED encoding.""
            #
        except:
            msg = "error writing " + fileOut
            errorInfo(msg)


def main():
    """Main command line interface"""

    # Get command line arguments
    args = parseCommandLine()
    dirIn = args.dirIn
    dirOut = args.dirOut

    # Check if input and output directories exist, and exit if not
    if not os.path.isdir(dirIn):
        msg = "input dir doesn't exist"
        errorExit(msg)

    if not os.path.isdir(dirOut):
        msg = "output dir doesn't exist"
        errorExit(msg)

    # Initialize Tika
    tika.initVM()

    # Iterate over files in input directory
    for filename in os.listdir(dirIn):
        fIn = os.path.abspath(os.path.join(dirIn, filename))
        if os.path.isfile(fIn):
            # Get base name and extension for each file
            baseName = os.path.splitext(filename)[0]
            extension = os.path.splitext(filename)[1]

            # Only process files with .epub extension (case-insensitive,
            # just to be safe)
            if extension.upper() == ".EPUB":
                fOut = os.path.join(dirOut, baseName + ".txt")
                extractText(fIn, fOut)


if __name__ == "__main__":
    main()
