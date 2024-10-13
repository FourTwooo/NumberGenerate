import lunardate

# 定义农历年、月、日
year = 2020
month = 5
day = 30
# 将农历日期转换为公历日期
# , isLeapMonth=False
# solar_date = lunardate.LunarDate(year, month, day).toSolarDate()
solar_date = lunardate.LunarDate.fromSolarDate(year, month, day)
# 输出公历日期
print(f"{solar_date.year}{solar_date.month:02}{solar_date.day:02}")

print(solar_date.isLeapMonth)
