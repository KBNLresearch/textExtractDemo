#! /usr/bin/env python3
"""
EPUB text extraction with PyMuPDF demo

Requires PyMuPDF (version => 1.24.3):

https://pymupdf.readthedocs.io/
"""

import os
import sys
import argparse
import csv
import pymupdf

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


def extractPyMuPDF(fileIn, fileOut):
    """Extract text from input file using PyMuPDF
    and write result to output file"""

    # Word count
    noWords = 0

    # Try to parse the file with PyMuPDF, and report an error message if
    # parsing fails
    try:
        with pymupdf.open(fileIn) as doc:
            content = ""
            noChapters = doc.chapter_count
            # Iterate over chapters
            for i in range(noChapters):
                chapter_page_count = doc.chapter_page_count(i)
                chapter_text = ""
                # Iterate over pages in chapter
                for j in range(chapter_page_count):
                    page = doc[(i, j)]
                    chapter_text += page.get_text()
                content += chapter_text
                # Add linebreak to mark end of chapter
                content += "\n"
            successParse = True
    except Exception:
        successParse = False
        msg = "error parsing " + fileIn
        errorInfo(msg)

    # Write extracted text to a text file if parsing was successful   
    if successParse:
        try:
            noWords = len(content.split())
            with open(fileOut, 'w', encoding='utf-8') as fout:
                fout.write(content)
        except UnicodeError:
            msg = "Unicode error on writing " + fileOut
            errorInfo(msg)    
        except OSError:
            msg = "error writing " + fileOut
            errorInfo(msg)
        except Exception:
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
    csvOut = os.path.join(dirOut, "summary-mupdf.csv")
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
                fOutMuPDF = os.path.join(dirOut, baseName + "_mupdf.txt")
                noWords = extractPyMuPDF(fIn, fOutMuPDF)
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
        msg = "unknown error writing " + csvOut
        errorInfo(msg)


if __name__ == "__main__":
    main()
