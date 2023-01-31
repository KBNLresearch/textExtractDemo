#! /usr/bin/env python3
"""
Ebooklib test script

Requires Ebooklib:

https://github.com/aerkalov/ebooklib
"""

import os
import sys
from html.parser import HTMLParser
import ebooklib
from ebooklib import epub


class HTMLFilter(HTMLParser):
    # Source: https://stackoverflow.com/a/55825140/1209004
    text = ""
    def handle_data(self, data):
        self.text += data


fileIn = '/home/johan/kb/epub-tekstextractie/DBNL_EPUBS_moderneromans/berk011veel01_01.epub'

book = epub.read_epub(fileIn)

for item in book.get_items():
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        content = item.get_body_content().decode()
        f = HTMLFilter()
        f.feed(content)
        print(f.text)
