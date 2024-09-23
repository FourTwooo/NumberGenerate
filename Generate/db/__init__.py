import os
import sqlite3

current_dir_path = os.path.dirname(os.path.abspath(__file__))
# 创建SQLite连接
conn = sqlite3.connect(f"{current_dir_path}/area_code.db")
cur = conn.cursor()


# import csv
# import pandas as pd
# table = pd.read_csv(f"{current_dir_path}/area_code.csv")
#
#
# def get_area_codes(address: str):
#     province, city, area = address.split("|")
#     results = table.copy()
#     if province:
#         results = results[results['省'].str.contains(province)]
#     if city:
#         results = results[results['市'].str.contains(city)]
#     if area:
#         results = results[results['区'].str.contains(area)]
#
#     result = []
#     for index, row in results.iterrows():
#         source = row['来源']
#         area = row['区']
#         area_code = row['区行政区划代码']
#         city = row['市']
#         city_code = row['市行政区划代码']
#         province = row['省']
#         province_code = row['省行政区划代码']
#         # print(f'[{area_code}]{province} {city} {area}, 数据来源:{source}')
#         result.append(area_code)
#     return result

def get_area_codes(address: str):
    province, city, area = address.split("|")

    query = f"""
        SELECT 省, 市, 区, 区行政区划代码, 来源 
        FROM city_data
        WHERE 省 LIKE '%{province}%' AND 市 LIKE '%{city}%' AND 区 LIKE '%{area}%'
    """
    cur.execute(query)

    result = []
    for item in cur.fetchall():
        # print(item)
        result.append(item[3])
    return result


def get_phone_codes(**conditions):
    city_name = conditions.get('地区')
    if city_name:
        conditions['市'] = city_name
        del conditions['地区']

    query = 'SELECT * FROM phone_data'
    where_clauses = []
    for column, value in conditions.items():
        if value is None:
            continue
        if column == "号段":  # 对号段列进行特殊处理
            # 将*替换为%以进行正确的匹配
            value = value[0:7]
            value = value.replace("*", "%")
        if column == "运营商":  # 对运营商列进行特殊处理
            # 在值的两端添加%使其变为模糊匹配
            value = "%" + value + "%"
        where_clauses.append(f"{column} LIKE '{value}'")

    if where_clauses:
        query += ' WHERE ' + ' AND '.join(where_clauses)
    # print(query)
    cur.execute(query)
    result = []
    for item in cur.fetchall():
        # print(item)
        result.append(item[0])

    if len(result) == 0 and city_name:
        del conditions['市']
        conditions['省'] = city_name
        result = get_phone_codes(**conditions)

    return result


if __name__ == '__main__':
    # print(get_area_codes(address='|南通|市辖区'))
    # {'移动/数据上网卡', '联通', '联通/物联网', '电信/虚拟', '电信', '联通/物联网卡', '电信/卫星', '应急通信/卫星电话卡', '电信/物联网卡', '联通/虚拟运营商', '移动', '电信/数据上网卡/物联网卡', '广电', '电信/虚拟运营商', '移动/物联网卡', '工信/卫星', '联通/数据上网卡', '移动/虚拟运营商', '电信/卫星电话卡', '电信虚拟运营商', '联通/虚拟'}
    print(get_phone_codes(
        # 号段="1386*9*",
        地区="南通",
        运营商="虚拟运营商",
    ))
    # csv_db()
