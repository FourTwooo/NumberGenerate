import re

import requests
from lxml import etree


def cha_hao_ba(incomplete_phone, city_name):
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    response = requests.get(url=f'https://www.chahaoba.com/{city_name}{incomplete_phone[0:3]}',
                            headers=headers)
    Mobile_phone_number_range_list = re.findall('title="([0-9]{4,7})"', response.text)
    return Mobile_phone_number_range_list


def tel_phone(incomplete_phone, city_name):

    def is_valid_href(href):
        parts = href.split('/')
        last_part = parts[-2]  # 获取倒数第二个部分
        if last_part.isdigit() and len(last_part) == 7:
            return last_part
        return False

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    response = requests.get(f'https://telphone.cn/prefix/{city_name}{incomplete_phone[0:3]}/', headers=headers)
    hrefs = etree.HTML(response.text).xpath('//div[@class="list-box"]/ul/li/a/@href')
    Mobile_phone_number_range_list = []
    for i in hrefs:
        Mobile_phone_number = is_valid_href(href=i)
        if Mobile_phone_number:
            Mobile_phone_number_range_list.append(Mobile_phone_number)
    # print(Mobile_phone_number_range_list)
    return Mobile_phone_number_range_list


if __name__ == '__main__':
    print(tel_phone('138********', '淮安'))