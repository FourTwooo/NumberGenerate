# from dataclasses import dataclass


# @dataclass

class PhoneInfo:
    number: int
    isp: str
    city: str
    area_code: int
    zip_code: int


class Idcard:
    number: int
    age: int
    date_of_birth: str
    gender: str
    constellation: str
    zodiac: str
    zodiac_code: str
    county: str
    county_code: str
    city: str
    city_code: str
    province: str


class UserInfo:
    name: str
    phone: PhoneInfo
    idcard: Idcard


if __name__ == '__main__':
    user_info = UserInfo()
    user_info.name = "123"
