import requests
from bs4 import BeautifulSoup, Tag
import re

url = 'https://contests.arrl.org/contestmultipliers.php?a=wve'
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57"}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

#getting the html
html_0 = str(soup.find("table"))
html_1= str(soup.find(style="margin-left: 220px;"))

html = html_0 + html_1


def bs_preprocess(html):
    """remove distracting whitespaces and newline characters"""
    #pat = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
    #html = re.sub(pat, '', html)       # remove leading and trailing whitespaces
    html = re.sub('\n', '', html)     # convert newlines to spaces
                                       # this preserves newline delimiters
    #html = re.sub('[\s]+<', '<', html) # remove whitespaces before opening tags
    #html = re.sub('>[\s]+', '>', html) # remove whitespaces after closing tags
    return html

def rm_1(html):
    html = re.sub(r'[0-9]', '', str(html))
    return html
def rm_2(html):
    html = re.sub('<th colspan="">U.S. Call Area </th>','',html)
    return html
def rm_3(html):
    html = re.sub(r'<.*?>', ' ', html)
    return html
def rm_4(html):
    html = re.sub(r'\s+', ' ', html)
    return html
def rm_all(html):
    html = bs_preprocess(html)
    html= rm_1(html)
    html= rm_2(html)
    html = rm_3(html)
    html = rm_4(html)
    return html

html = rm_all(html)

#Printing that text
#TODO Change print into start a DB or input into absenths db
print(html)
