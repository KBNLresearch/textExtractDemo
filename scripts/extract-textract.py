#! /usr/bin/env python3
"""
EPUB text extraction with Textract demo

Requires Textract:

https://github.com/deanmalmgren/textract
"""

import os
import sys
import csv
import argparse
import textract


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


def extractTextract(fileIn, fileOut):
    """Extract text from input file using Textract
    and write result to output file"""

    # Try to parse the file with Textract, and report an error message if
    # parsing fails
    try:
        content = textract.process(fileIn, encoding='utf-8').decode()
        successParse = True
    except Exception:
        raise
        successParse = False
        msg = "error parsing " + fileIn
        errorInfo(msg)

    # Write extracted text to a text file if parsing was successful    
    if successParse:
        # Word count
        noWords = len(content.split())
        try:
            with open(fileOut, 'w', encoding='utf-8') as fout:
                fout.write(content)
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

    # Check if input and output directories exist, and exit if not
    if not os.path.isdir(dirIn):
        msg = "input dir doesn't exist"
        errorExit(msg)

    if not os.path.isdir(dirOut):
        msg = "output dir doesn't exist"
        errorExit(msg)

    # Summary output file
    csvOut = os.path.join(dirOut, "summary-textract.csv")
    csvList = [["fileName", "noWords"]]

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
                fOutTextract = os.path.join(dirOut, baseName + "_textract.txt")
                noWords = extractTextract(fIn, fOutTextract)
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
