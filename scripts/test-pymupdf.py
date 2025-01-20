#! /usr/bin/env python3

import sys
import pymupdf

fileIn = "/home/johan/kb/epub-tekstextractie/DBNL_EPUBS_moderneromans/berk011veel01_01.epub"
fileOut = "/home/johan/kb/epub-tekstextractie/out-dbnl-2025/test-pymupdf.txt"

# Try to parse the file with PyMuPDF, and report an error message if
# parsing fails
try:
    with pymupdf.open(fileIn) as doc:
        content = chr(12).join([page.get_text() for page in doc])
        successParse = True
        #pathlib.Path(fname + ".txt").write_bytes(text.encode())
except Exception:
    successParse = False
    msg = "error parsing " + fileIn
    print(msg)

# Write extracted text to a text file if parsing was successful   
if successParse:
    try:
        with open(fileOut, 'w', encoding='utf-8') as fout:
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
        print(msg)