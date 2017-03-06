import glob
import json
import html

import arrow
import os
import re
import requests

from arc.ids.import_state_saver import ImportStateHolder
from html2ans import Html2Ans
from bs4 import BeautifulSoup

from tgamadapter.parsers.utilities import process_related_content, generate_reference
from tgamadapter.parsers.utilities import get_text, get_bool, replace_hosted_images, replace_static_assets
from tgamadapter.parsers.operations import generate_operations
from tgamadapter.parsers.customparsers import PtagParser, BlockquoteParser, StraightUpImageParser

ANS_VERSION = '0.5.7'
html2ans_converter = Html2Ans()
html2ans_converter.add_parser('p', PtagParser(), replace=True)
html2ans_converter.add_parser('blockquote', BlockquoteParser(), replace=True)
html2ans_converter.add_parser('img', StraightUpImageParser(), replace=True)

def search_text_field(soup):

    # "storyelement", attrs={"userlabelname": "WebText"}
    if soup.find("storyelement", attrs={"userlabelname": "WebText"}) and not soup.find("storyelement", attrs={"userlabelname": "BlogText"}):
        body_contents = ''
        body_field = soup.find("storyelement", attrs={"userlabelname": "WebText"})
        if body_field is not None:
            body_contents = html.unescape((''.join([str(s) for s in body_field])))
            body_contents = replace_static_assets(replace_hosted_images(body_contents))

    # "storyelement", attrs={"userlabelname": "Text"}
    elif soup.find("storyelement", attrs={"userlabelname": "Text"}) and not soup.find("storyelement", attrs={"userlabelname": "BlogText"}):
        body_contents = ''
        body_field = soup.find("storyelement", attrs={"userlabelname": "Text"})
        if body_field is not None:
            body_contents = (''.join([str(s) for s in body_field])).replace('<p class="SUBHEAD_Bullets"> —</p>\n', '')
            body_contents = replace_static_assets(replace_hosted_images(body_contents))

    # "storyelement", attrs={"userlabelname": "BlogText"}
    elif soup.find("storyelement", attrs={"userlabelname": "BlogText"}):
        body_contents = ''
        body_field = soup.find("storyelement", attrs={"userlabelname": "BlogText"})
        if body_field is not None:
            body_contents = html.unescape((''.join([str(s) for s in body_field])))
            body_contents = replace_static_assets(replace_hosted_images(body_contents))

    # "storyelement", attrs={"userlabelname": "HTMLText"}
    elif soup.find("storyelement", attrs={"userlabelname": "HTMLText"}):
        body_contents = ''
        body_field = soup.find("storyelement", attrs={"userlabelname": "HTMLText"})
        if body_field is not None:
            body_contents = html.unescape((''.join([str(s) for s in body_field])))
            body_contents = replace_static_assets(replace_hosted_images(body_contents))

    content_elements = html2ans_converter.parse_body('<body>{soup}</body>'.format(soup=body_contents), start_tag="div")

    return content_elements

def search_text_field_main():

    xml_files = ['/10120827.xml', '/12176931.xml', '/12123801.xml', '/12006948.xml', '/12134699.xml', '/12147707.xml']

    for file in xml_files:
        file = open(file, 'r')
        souped = BeautifulSoup(file, 'lxml')
        search_text_field(souped)

search_text_field_main()