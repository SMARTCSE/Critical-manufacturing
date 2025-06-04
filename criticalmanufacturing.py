import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def abstract_cleaner(abstract):
    """Converts all the sup and sub script when passing the abstract block as html"""
    conversion_tags_sub = BeautifulSoup(str(abstract), 'html.parser').find_all('sub')
    conversion_tags_sup = BeautifulSoup(str(abstract), 'html.parser').find_all('sup')
    abstract_text = str(abstract).replace('<.', '< @@dot@@')
    for tag in conversion_tags_sub:
        original_tag = str(tag)
        key_list = [key for key in tag.attrs.keys()]
        for key in key_list:
            del tag[key]
        abstract_text = abstract_text.replace(original_tag, str(tag))
    for tag in conversion_tags_sup:
        original_tag = str(tag)
        key_list = [key for key in tag.attrs.keys()]
        for key in key_list:
            del tag[key]
        abstract_text = abstract_text.replace(original_tag, str(tag))
    abstract_text = sup_sub_encode(abstract_text)
    abstract_text = BeautifulSoup(abstract_text, 'html.parser').text
    abstract_text = sup_sub_decode(abstract_text)
    abstract_text = re.sub('\\s+', ' ', abstract_text)
    text = re.sub('([A-Za-z])(\\s+)?(:|\\,|\\.)', r'\1\3', abstract_text)
    text = re.sub('(:|\\,|\\.)([A-Za-z])', r'\1 \2', text)
    text = re.sub('(<su(p|b)>)(\\s+)(\\w+)(</su(p|b)>)', r'\3\1\4\5', text)
    text = re.sub('(<su(p|b)>)(\\w+)(\\s+)(</su(p|b)>)', r'\1\3\5\4', text)
    text = re.sub('(<su(p|b)>)(\\s+)(\\w+)(\\s+)(</su(p|b)>)', r'\3\1\4\6\5', text)
    abstract_text = re.sub('\\s+', ' ', text)
    abstract_text = abstract_text.replace('< @@dot@@', '<.')
    return abstract_text.strip()

def sup_sub_encode(html):
    """Encodes superscript and subscript tags"""
    encoded_html = html.replace('<sup>', 's#p').replace('</sup>', 'p#s').replace('<sub>', 's#b').replace('</sub>',
                                                                                                         'b#s') \
        .replace('<Sup>', 's#p').replace('</Sup>', 'p#s').replace('<Sub>', 's#b').replace('</Sub>', 'b#s')
    return encoded_html


def sup_sub_decode(html):
    """Decodes superscript and subscript tags"""
    decoded_html = html.replace('s#p', '<sup>').replace('p#s', '</sup>').replace('s#b', '<sub>').replace('b#s',
                                                                                                         '</sub>')
    return decoded_html

if __name__ == '__main__':
    all_data = []
    headers = {
        'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language' : 'en-US,en;q=0.9',
        'Cache-Control' : 'max-age=0',
        'Cookie' : 'pll_language=en; _gcl_au=1.1.1471142597.1719905594; _gid=GA1.2.1213051242.1719905594; _fbp=fb.1.1719905596838.945413853217585660; cookie_notice_accepted=true; msd365mkttr=5YWw9DHzVQcaZjQlR6fn6EiUY44KQ7NrxdpAsWzO; _ga_SF3K0C6VLJ=GS1.1.1720067655.4.1.1720067791.34.0.0; _ga=GA1.1.1410705210.1719905594',
        'Priority' : 'u=0, i',
        'Referer' : 'https://www.criticalmanufacturing.com/',
        'Sec-Ch-Ua' : '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform ' : 'Windows',
        'Sec-Fetch-Dest' : 'document',
        'Sec-Fetch-Mode' : 'navigate',
        'Sec-Fetch-Site' : 'same-origin',
        'Sec-Fetch-User' : '?1',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    response = requests.get("https://www.criticalmanufacturing.com/insights/?type=46", headers=headers)
    data_soup = BeautifulSoup(response.text, 'html.parser')
    data = data_soup.prettify()
    print(data_soup.prettify())
