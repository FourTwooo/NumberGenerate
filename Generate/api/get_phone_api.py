import re

import requests
from lxml import etree

PHONE_ISP_CODES = {
    "移动": [
        "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "157", "158", "159",
        "165", "172", "178", "182", "183", "184", "187", "188", "195", "197", "198"
    ],
    "联通": [
        "130", "131", "132", "145", "146", "155", "156", "166", "167", "171", "175", "176", "185",
        "186", "196"
    ],
    "电信": [
        "133", "149", "153", "162", "173", "174", "177", "180", "181", "189", "191", "193", "199"
    ]
}


def get_codes_by_carrier_and_segment(carrier, segment):
    segment = segment.replace("*", ".*")  # 把*替换成.*以实现模糊匹配
    pattern = re.compile(segment)  # 编译正则表达式
    matched_codes = [code for code in PHONE_ISP_CODES[carrier] if re.match(pattern, code)]
    return matched_codes


def cha_hao_ba(incomplete_phone, city_name, isp=None):
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    if isp and "*" in incomplete_phone[0:3]:
        phone_codes = get_codes_by_carrier_and_segment(carrier=isp, segment=incomplete_phone[0:3])
    else:
        phone_codes = [incomplete_phone[0:3]]

    Mobile_phone_number_range_list = []
    for phone_code in phone_codes:
        response = requests.get(url=f'https://www.chahaoba.com/{city_name}{phone_code}',
                                headers=headers)
        Mobile_phone_number_range_list += re.findall('title="([0-9]{4,7})"', response.text)

    return Mobile_phone_number_range_list


def tel_phone(incomplete_phone, city_name, isp=None):

    def is_valid_href(href):
        parts = href.split('/')
        last_part = parts[-2]  # 获取倒数第二个部分
        if last_part.isdigit() and len(last_part) == 7:
            return last_part
        return False

    if isp and "*" in incomplete_phone[0:3]:
        phone_codes = get_codes_by_carrier_and_segment(carrier=isp, segment=incomplete_phone[0:3])
    else:
        phone_codes = [incomplete_phone[0:3]]

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    Mobile_phone_number_range_list = []
    for phone_code in phone_codes:
        response = requests.get(f'https://telphone.cn/prefix/{city_name}{phone_code}/', headers=headers)
        hrefs = etree.HTML(response.text).xpath('//div[@class="list-box"]/ul/li/a/@href')

        for i in hrefs:
            Mobile_phone_number = is_valid_href(href=i)
            if Mobile_phone_number:
                Mobile_phone_number_range_list.append(Mobile_phone_number)

    return Mobile_phone_number_range_list


if __name__ == '__main__':
    # print(tel_phone('138********', '淮安'))
    print(get_codes_by_carrier_and_segment("联通", "13*"))  # 返回结果：['130', '131', '132']
    # print(get_codes_by_carrier_and_segment("联通", "1*5"))  # 返回结果：['145', '155', '156', '175', '185']