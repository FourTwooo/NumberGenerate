import csv
import os
import sqlite3

current_dir_path = os.path.dirname(os.path.abspath(__file__))
# 创建SQLite连接
conn = sqlite3.connect(f"{current_dir_path}/area_code.db")
cur = conn.cursor()


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
        where_clauses.append(f"{column} LIKE '%{value}%'")

    if where_clauses:
        query += ' WHERE ' + ' AND '.join(where_clauses)
    # print(query)
    cur.execute(query)
    result = []
    for item in cur.fetchall():
        # print(item)
        result.append(item[0])

    if len(result) == 0 and city_name:
        result = get_phone_codes(省=city_name)

    return result


if __name__ == '__main__':
    # print(get_area_codes(address='|南通|市辖区'))
    print(get_phone_codes(
        # 号段="1386*9*",
        地区="南通"
        # 省="江苏",
        # 市="南通",
        # 运营商="移动",
    ))
    # csv_db()
