import time
from concurrent.futures import ThreadPoolExecutor

import api
import Generate.errors

generate_phone_area = api.get_phone_api.tel_phone


class PhoneGenerate:

    def __init__(self):
        self.complete_phone_list = []

    @staticmethod
    def generate_complete_phones(Mobile_phone_number_range, incomplete_phone):
        complete_phones = []
        new_phone = incomplete_phone[7:11]
        phone_one = Mobile_phone_number_range + new_phone

        js_count = sum(1 for digit in phone_one if digit != '*')

        start = phone_one.replace('*', '0')
        end = phone_one.replace('*', '9')

        phone_range = range(int(start), int(end) + 1)
        for phone_demo in phone_range:
            list_phone = list(phone_one)
            pd_js = sum(1 for i in range(len(list_phone)) if list_phone[i] == str(phone_demo)[i])

            if pd_js == js_count:
                complete_phones.append(phone_demo)

        return complete_phones

    @staticmethod
    def generate_phone_area(incomplete_phone, city_name):
        Mobile_phone_number_range_list = generate_phone_area(incomplete_phone, city_name)

        # 检测是否为正常号段
        Mobile_phone_number_range_phones = []
        for Mobile_phone_number in Mobile_phone_number_range_list:
            hd_js_count = sum(1 for i in range(7) if incomplete_phone[i] != '*')
            pd2_js_count = sum(1 for i in range(7) if incomplete_phone[i] == str(Mobile_phone_number)[i])
            if hd_js_count == pd2_js_count:
                Mobile_phone_number_range_phones.append(Mobile_phone_number)
        return Mobile_phone_number_range_phones

    def get_data(self, data):
        self.complete_phone_list += data.result()

    def get_phone(self, city_name, incomplete_phone):
        """
        :param city_name:               市
        :param incomplete_phone:        手机号
        :return:                        [phone...]
        """
        self.complete_phone_list = []
        Mobile_phone_number_range_phones = self.generate_phone_area(
            city_name=city_name,
            incomplete_phone=incomplete_phone
        )
        # print(f'使用api:{self.mode} 查询号段[{len(Mobile_phone_number_range_phones)}]:{Mobile_phone_number_range_phones}')
        start_time = time.time()
        max_workers = len(Mobile_phone_number_range_phones)
        if max_workers == 0:
            raise Generate.errors.NumberValueError(f"{city_name} {incomplete_phone} 未查询到符合号段")
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            for hd in Mobile_phone_number_range_phones:
                task = pool.submit(
                    self.generate_complete_phones,
                    Mobile_phone_number_range=hd,
                    incomplete_phone=incomplete_phone
                )
                task.add_done_callback(self.get_data)

        end_time = time.time()
        # print(f'生成手机数量{len(self.complete_phone_list)} 耗时:{end_time - start_time}')
        return self.complete_phone_list


if __name__ == '__main__':
    phone_bull = PhoneGenerate()
    phone_numbers = phone_bull.get_phone(city_name="南通", incomplete_phone="177******90")
    print(len(phone_numbers), phone_numbers)


