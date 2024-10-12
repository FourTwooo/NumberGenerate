from datetime import timedelta, datetime

from Generate.lunardate import LunarDate
import Generate.errors
from Generate.db import get_area_codes


class IDCardGenerate:

    def __init__(self):

        self.db_function = get_area_codes

        # 起始年份设定
        self.START_YEAR = 1900
        # 终止年份设定
        self.END_YEAR = datetime.now().year + 1
        # 星座日期表
        self.CONSTELLATIONS = {
            "白羊座": ("0321", "0419"),
            "金牛座": ("0420", "0520"),
            "双子座": ("0521", "0621"),
            "巨蟹座": ("0622", "0722"),
            "狮子座": ("0723", "0822"),
            "处女座": ("0823", "0922"),
            "天秤座": ("0923", "1023"),
            "天蝎座": ("1024", "1122"),
            "射手座": ("1123", "1221"),
            "摩羯座": ("1222", "0119"),
            "水瓶座": ("0120", "0218"),
            "双鱼座": ("0219", "0320"),
        }

    def get_constellation_date(self, constellation):
        """
        :param constellation:   星座
        :return:
        """
        return self.CONSTELLATIONS.get(constellation, None)

    @staticmethod
    def generate_order_code(gender=None, pattern='***'):
        """
        :param gender:  性别
        :param pattern: 后四位前三位
        :return:
        """
        if gender == '男':
            # 男性就用奇数顺序码，例如从 "001" 到 "999"，间隔2
            codes = ['{:03d}'.format(i) for i in range(1, 1000, 2)]
        elif gender == '女':
            # 女性就用偶数顺序码，例如从 "002" 到 "998"，间隔2
            codes = ['{:03d}'.format(i) for i in range(2, 1000, 2)]
        else:
            # 如果不知道性别，就生成所有可能的顺序码
            codes = ['{:03d}'.format(i) for i in range(1, 1000)]

        # 基于模式过滤生成的数据
        return [code for code in codes if all(a == b or b == '*' for a, b in zip(code, pattern))]

    def generator_date(self, date_str, constellation='未知星座', zodiac='未知生肖', lunar_birthday=None):
        """
        :param date_str:        公历日期"****[年]**[月]**[日]"
        :param constellation:   星座
        :param zodiac:          生肖
        :param lunar_birthday:  农历的公历生日
        :return:
        """

        temp_start = date_str[:4].replace('*', '0')
        temp_end = date_str[:4].replace('*', '9')
        start_year_input = int(temp_start)
        end_year_input = int(temp_end)

        if "*" in date_str[:4]:
            start_year = max(self.START_YEAR, start_year_input)
            end_year = min(self.END_YEAR, end_year_input + 1)
        else:
            start_year, end_year = start_year_input, start_year_input + 1

        all_dates = []
        for year in range(start_year, end_year):
            if lunar_birthday:
                lunar_date = LunarDate.fromSolarDate(
                    int(lunar_birthday[0:4]),
                    int(lunar_birthday[4:6]),
                    int(lunar_birthday[6:8])
                )
                solar_date = LunarDate(year, lunar_date.month, lunar_date.day, lunar_date.isLeapMonth).toSolarDate()
                all_dates.append(f"{solar_date.year}{solar_date.month:02}{solar_date.day:02}")
            else:
                start_date = datetime.strptime(str(year) + "0101", "%Y%m%d")
                end_date = datetime.strptime(str(year + 1) + "0101", "%Y%m%d")
                while start_date != end_date:
                    date_str_format = start_date.strftime("%Y%m%d")
                    flag = True
                    for i in range(8):
                        if date_str[i] != '*' and date_str[i] != date_str_format[i]:
                            flag = False
                            break
                    if flag:
                        all_dates.append(date_str_format)
                    start_date += timedelta(days=1)

        def filter_dates(dates, date_range):
            start_month, start_day = int(date_range[0][:2]), int(date_range[0][2:])
            end_month, end_day = int(date_range[1][:2]), int(date_range[1][2:])

            filtered_dates = []

            for date in dates:
                current_month = int(date[4:6])
                current_day = int(date[6:])

                if (start_month < current_month < end_month) or \
                        (start_month == current_month and start_day <= current_day) or \
                        (end_month == current_month and current_day <= end_day):
                    filtered_dates.append(date)

            return filtered_dates

        if constellation != "未知星座":
            constellation_date = self.get_constellation_date(constellation=constellation)
            if constellation_date is not None:
                all_dates = filter_dates(all_dates, constellation_date)
            else:
                raise Generate.errors.NumberValueError(f'{constellation} not in {self.CONSTELLATIONS}')

        def filter_zodiac(dates, __zodiac):
            zodiac_list = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
            if __zodiac not in zodiac_list:
                raise Generate.errors.NumberValueError(f'{__zodiac} not in {zodiac_list}')
                # return dates
            zodiac_offset = zodiac_list.index(__zodiac)
            filtered_dates = [date for date in dates if ((int(date[:4]) - 1900) % 12) == zodiac_offset]
            return filtered_dates

        if zodiac != "未知生肖":
            all_dates = filter_zodiac(all_dates, zodiac)

        return all_dates

    @staticmethod
    def generate_check_code(id_number):
        """
        :param id_number: 身份证号码前17位
        :return:
        """
        coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 系数
        check_code_list = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']  # 校验码对应值

        check_sum = sum([int(a) * b for a, b in zip(id_number, coefficients)])
        check_index = check_sum % 11
        check_code = check_code_list[check_index]  # 校验码

        return check_code

    def generator_area_code(self, area_code, address) -> list:
        if "*" not in area_code:
            return [area_code]

        city_area_codes = self.db_function(address)

        success_city_area_codes = []
        for city_area_code in city_area_codes:
            hd_js_count = sum(1 for i in range(6) if area_code[i] != '*')
            pd2_js_count = sum(1 for i in range(6) if area_code[i] == str(city_area_code)[i])
            if hd_js_count == pd2_js_count:
                success_city_area_codes.append(city_area_code)

        if len(success_city_area_codes) == 0:
            raise Generate.errors.NumberValueError(f'{area_code} != {city_area_codes}')

        return success_city_area_codes

    def get_id_card(
            self,
            id_card: str,
            address: str = None,
            gender: str = None,
            constellation: str = None,
            zodiac: str = None,
            lunar_birthday: str = None
    ):
        """
        :param id_card:         身份证号
        :param address:         地区 -> "省|市|区"
        :param gender:          性别
        :param constellation    星座
        :param zodiac:          生肖
        :param lunar_birthday:  农历的公历生日
        :return: [id_card...]
        """
        if address is None:
            address = "||"
        if constellation is None:
            constellation = "未知星座"
        if zodiac is None:
            zodiac = "未知生肖"

        if len(id_card) != 18:
            raise Generate.errors.NumberValueError(f'{id_card} length must be 18 characters')

        area_codes = self.generator_area_code(area_code=id_card[0:6], address=address)
        # print(id_card[6:14])
        date_codes = self.generator_date(date_str=id_card[6:14], constellation=constellation, zodiac=zodiac, lunar_birthday=lunar_birthday)
        order_codes = self.generate_order_code(pattern=id_card[14:17], gender=gender)

        # print(area_codes, date_codes, order_codes)
        # import time
        # start_time = time.time()
        id_cards = []
        for area_code in area_codes:
            for date_code in date_codes:
                for order_code in order_codes:
                    check_code = self.generate_check_code(id_number=f'{area_code}{date_code}{order_code}')
                    # 对最后一位 18位做过滤
                    if id_card[17:18] != "*":
                        if id_card[17:18] != str(check_code):
                            continue
                    id_cards.append(f'{area_code}{date_code}{order_code}{check_code}')

        # print(time.time() - start_time)
        return id_cards


if __name__ == '__main__':
    IDCard = IDCardGenerate()
    print(IDCard.generator_date('20******', lunar_birthday="20240513", constellation="金牛座", zodiac="马"))
    # date_data = IDCard.generator_date(
    #     "200****1",
    #     constellation="白羊座",
    #     zodiac="马"
    # )
    # print(len(date_data), date_data)
