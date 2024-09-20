from concurrent.futures import ThreadPoolExecutor

import Generate.errors
from Generate import api, db


class PhoneGenerate:

    def __init__(self):
        self.api_function = Generate.api.get_phone_api.tel_phone
        self.db_function = Generate.db.get_phone_codes
        # 是否开启数据库查询
        self.is_db = True

    @staticmethod
    def generate_complete_phones(Mobile_phone_number_range, incomplete_phone):
        def generate(phone_arr, start, __phones):
            try:
                i = start + phone_arr[start:].index('*')
                for digit in range(10):
                    new_arr = phone_arr.copy()
                    new_arr[i] = str(digit)
                    generate(new_arr, i + 1, __phones)
            except ValueError:
                # no more '*'
                __phones.append(''.join(phone_arr))

        phones = []
        generate(list(Mobile_phone_number_range + incomplete_phone[7:11]), 0, phones)

        return [int(phone) for phone in phones]

    def generate_phone_area(self, incomplete_phone, city_name=None, isp=None):
        """
        :param incomplete_phone:    模糊手机号
        :param city_name:           地区
        :param isp:                 运营商
        :return:
        """
        # {'移动/数据上网卡', '联通', '联通/物联网', '电信/虚拟', '电信', '联通/物联网卡', '电信/卫星', '应急通信/卫星电话卡', '电信/物联网卡', '联通/虚拟运营商', '移动', '电信/数据上网卡/物联网卡', '广电', '电信/虚拟运营商', '移动/物联网卡', '工信/卫星', '联通/数据上网卡', '移动/虚拟运营商', '电信/卫星电话卡', '电信虚拟运营商', '联通/虚拟'}
        if self.is_db:
            phoneRangeList = self.db_function(号段=incomplete_phone, 地区=city_name, 运营商=isp)
        else:
            if city_name:
                phoneRangeList = self.api_function(incomplete_phone, city_name, isp)
            else:
                phoneRangeList = [str(_) for _ in range(1300000, 1999999+1)]

        # 检测是否为正常号段n y
        phoneRange = []
        for Mobile_phone_number in phoneRangeList:
            hd_js_count = sum(1 for i in range(7) if incomplete_phone[i] != '*')
            pd2_js_count = sum(1 for i in range(7) if incomplete_phone[i] == str(Mobile_phone_number)[i])
            if hd_js_count == pd2_js_count:
                phoneRange.append(Mobile_phone_number)

        return phoneRange

    def get_phone(self, incomplete_phone, city_name=None, isp=None):
        """
        :param incomplete_phone:        手机号
        :param city_name:               市
        :param isp:                     运营商
        :return:                        [phone...]
        """
        # import time
        # start_time = time.time()
        phoneRange = self.generate_phone_area(
            city_name=city_name,
            incomplete_phone=incomplete_phone,
            isp=isp
        )

        def map_start(arg):
            # print(arg)
            return self.generate_complete_phones(arg[0], arg[1])

        if not phoneRange:
            raise Generate.errors.NumberValueError(f"{city_name} {incomplete_phone} 未查询到符合号段")
        tasks = [(p, incomplete_phone) for p in phoneRange]

        max_workers = 100 if len(phoneRange) >= 100 else len(phoneRange)
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            results = pool.map(map_start, tasks)

        complete_phone_list = []
        for i in results:
            complete_phone_list += i

        # end_time = time.time()
        # print(f'生成手机数量{len(complete_phone_list)} 耗时:{end_time - start_time}')
        return complete_phone_list


if __name__ == '__main__':
    phone_bull = PhoneGenerate()
    phone_numbers = phone_bull.generate_phone_area(
        city_name="北京",
        incomplete_phone="1*******434",
        isp="虚拟"
    )
    # phone_numbers = phone_bull.get_phone(city_name="南通", incomplete_phone="177******90")
    print(len(phone_numbers), phone_numbers[:20])
