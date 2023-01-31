#! /usr/bin/env python3
"""
EPUB text extraction with Apache Tika demo

Requires tika-python:

https://github.com/chrismattmann/tika-python
"""

import os
import sys
import argparse
import csv
import tika
from tika import parser

# Create argument parser
argParser = argparse.ArgumentParser(
    description="Extract text from EPUB files")


def parseCommandLine():
    """Parse command-line arguments"""

    argParser.add_argument('dirIn',
                               action="store",
                               type=str,
                               help='directory with input EPUB files')

    argParser.add_argument('dirOut',
                               action='store',
                               type=str,
                               help='output directory')

    argParser.add_argument('--trim', '-t',
                               action="store_true",
                               dest='trimFlag',
                               default=False,
                               help="trim leading and trailing whitespace from Tika output")

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


def extractTika(fileIn, fileOut, trimFlag):
    """Extract text from input file using Tika
    and write result to output file"""

    # Try to parse the file with Tika, and report an error message if
    # parsing fails
    try:
        parsed = parser.from_file(fileIn, service='text')
        #parsed = parser.from_file(fileIn, xmlContent=True)
        successParse = True
    except Exception:
        raise
        successParse = False
        msg = "error parsing " + fileIn
        errorInfo(msg)

    # Write extracted text to a text file if parsing was successful    
    if successParse:
        content = parsed["content"]
        # Word count
        noWords = 0
        # Split content string into separate lines
        # so we can do some processing id needed
        lines = content.splitlines()
        try:
            # TODO: test behaviour here if extracted content has a decoding that
            # is not UTF-8 (EPUB 2 and EPUB 3 also allow UTF-16!)
            with open(fileOut, 'w', encoding='utf-8') as fout:
                for line in lines:
                    if trimFlag:
                        # Trim leading / trailing whitespace characters
                        line = line.strip()
                    # Update word count
                    noWords += len(line.split())
                    fout.write(line + '\n')
        except UnicodeError:
            msg = "Unicode error on writing " + fileOut
            errorInfo(msg)    
        except OSError:
            msg = "error writing " + fileOut
            errorInfo(msg)
        except Exception:
            raise
            msg = "unknown error writing " + fileOut
            errorInfo(msg)
    
    return noWords


def main():
    """Main command line interface"""

    # Get command line arguments
    args = parseCommandLine()
    dirIn = args.dirIn
    dirOut = args.dirOut
    trimFlag = args.trimFlag

    # Check if input and output directories exist, and exit if not
    if not os.path.isdir(dirIn):
        msg = "input dir doesn't exist"
        errorExit(msg)

    if not os.path.isdir(dirOut):
        msg = "output dir doesn't exist"
        errorExit(msg)

    # Summary output file
    csvOut = os.path.join(dirOut, "summary-tika.csv")
    csvList = [["fileName", "noWords"]]

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
                fOutTika = os.path.join(dirOut, baseName + "_tika.txt")
                noWords = extractTika(fIn, fOutTika, trimFlag)
                csvList.append([filename, noWords])

    # Write summary file
    try:
        with open(csvOut, 'w', encoding='utf-8') as csvout:
            csvWriter = csv.writer(csvout)
            for row in csvList:
                csvWriter.writerow(row)
    except UnicodeError:
        msg = "Unicode error on writing " + csvOut
        errorInfo(msg)    
    except OSError:
        msg = "error writing " + csvOut
        errorInfo(msg)
    except Exception:
        raise
        msg = "unknown error writing " + csvOut
        errorInfo(msg)


if __name__ == "__main__":
    main()
