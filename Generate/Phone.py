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

    # @staticmethod
    # def generate_complete_phones(Mobile_phone_number_range, incomplete_phone):
    #     complete_phones = []
    #     new_phone = incomplete_phone[7:11]
    #     phone_one = Mobile_phone_number_range + new_phone
    #
    #     js_count = sum(1 for digit in phone_one if digit != '*')
    #
    #     start = phone_one.replace('*', '0')
    #     end = phone_one.replace('*', '9')
    #
    #     phone_range = range(int(start), int(end) + 1)
    #     for phone_demo in phone_range:
    #         list_phone = list(phone_one)
    #         pd_js = sum(1 for i in range(len(list_phone)) if list_phone[i] == str(phone_demo)[i])
    #
    #         if pd_js == js_count:
    #             complete_phones.append(phone_demo)
    #
    #     return complete_phones

    def generate_phone_area(self, incomplete_phone, city_name=None):
        if self.is_db:
            phoneRangeList = self.db_function(号段=incomplete_phone, 地区=city_name, 运营商=None)
        else:
            if city_name:
                phoneRangeList = self.api_function(incomplete_phone, city_name)
            else:
                phoneRangeList = [str(_) for _ in range(1300000, 1999999)]

        # 检测是否为正常号段n y
        phoneRange = []
        for Mobile_phone_number in phoneRangeList:
            hd_js_count = sum(1 for i in range(7) if incomplete_phone[i] != '*')
            pd2_js_count = sum(1 for i in range(7) if incomplete_phone[i] == str(Mobile_phone_number)[i])
            if hd_js_count == pd2_js_count:
                phoneRange.append(Mobile_phone_number)

        return phoneRange

    # def get_phone(self, city_name, incomplete_phone):
    #     """
    #     :param city_name:               市
    #     :param incomplete_phone:        手机号
    #     :return:                        [phone...]
    #     """
    #
    #     def get_data(data):
    #         self.complete_phone_list += data.result()
    #
    #     self.complete_phone_list = []
    #     Mobile_phone_number_range_phones = self.generate_phone_area(
    #         city_name=city_name,
    #         incomplete_phone=incomplete_phone
    #     )
    #     # print(f'使用api:{self.mode} 查询号段[{len(Mobile_phone_number_range_phones)}]:{Mobile_phone_number_range_phones}')
    #     start_time = time.time()
    #     max_workers = len(Mobile_phone_number_range_phones)
    #     if max_workers == 0:
    #         raise Generate.errors.NumberValueError(f"{city_name} {incomplete_phone} 未查询到符合号段")
    #     with ThreadPoolExecutor(max_workers=max_workers) as pool:
    #         for hd in Mobile_phone_number_range_phones:
    #             task = pool.submit(
    #                 self.generate_complete_phones,
    #                 Mobile_phone_number_range=hd,
    #                 incomplete_phone=incomplete_phone
    #             )
    #             task.add_done_callback(self.get_data)
    #
    #     end_time = time.time()
    #     print(f'生成手机数量{len(self.complete_phone_list)} 耗时:{end_time - start_time}')
    #     return self.complete_phone_list

    def get_phone(self, incomplete_phone, city_name=None):
        """
        :param incomplete_phone:        手机号
        :param city_name:               市
        :return:                        [phone...]
        """
        phoneRange = self.generate_phone_area(
            city_name=city_name,
            incomplete_phone=incomplete_phone
        )

        def map_start(arg):
            # print(arg)
            return self.generate_complete_phones(arg[0], arg[1])

        if not phoneRange:
            raise Generate.errors.NumberValueError(f"{city_name} {incomplete_phone} 未查询到符合号段")
        tasks = [(p, incomplete_phone) for p in phoneRange]

        # import time
        # start_time = time.time()
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
    # print(phone_bull.generate_complete_phones(Mobile_phone_number_range='1504447', incomplete_phone='150*****3*4'))
    phone_numbers = phone_bull.get_phone(city_name="南通", incomplete_phone="177******90")
    print(len(phone_numbers), phone_numbers[:20])


