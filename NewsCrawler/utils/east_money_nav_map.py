import requests
import json
from lxml import etree
from urllib.parse import urljoin

base_url = 'https://kuaixun.eastmoney.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}


def parse_nav():
    """所有有的nav映射关系"""
    r = requests.get(base_url, headers=headers)
    html = etree.HTML(r.text)
    nav_list = html.xpath('//ul[@id="nav"]//li')
    nav_map = {}
    for nav in nav_list:
        nav_link = urljoin(base_url, nav.xpath('./a/@href')[0])
        nav_name = nav.xpath('./a/text()')[0]
        r2 = requests.get(nav_link, headers=headers)
        nav_html = etree.HTML(r2.text)
        nav_detail = nav_html.xpath('//script[contains(text(),"columns")]/text()')
        if nav_detail:
            nav_num = nav_detail[0].split(';')[0].split('=')[1].strip().replace('"', '')
        else:
            nav_num = '100'
        nav_map[nav_num] = nav_name

    f_name = 'east_money_nav_map.json'
    with open(f_name, 'w') as f:
        json.dump(nav_map, f)


if __name__ == '__main__':
    parse_nav()


