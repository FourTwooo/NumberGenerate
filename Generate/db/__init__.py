import csv
import os
import sqlite3

current_dir_path = os.path.dirname(os.path.abspath(__file__))
# 创建SQLite连接
conn = sqlite3.connect(f"{current_dir_path}/city_db_data.db")
cur = conn.cursor()


def csv_db():
    global cur
    # 创建表
    cur.execute("""
        CREATE TABLE city_data(
            省 TEXT,
            省行政区划代码 TEXT,
            市 TEXT,
            市行政区划代码 TEXT,
            区 TEXT,
            区行政区划代码 TEXT,
            来源 TEXT
        )
    """)

    # 将CSV数据插入数据库
    with open(f"{current_dir_path}/city_db_data.csv", 'r', encoding='utf-8') as fin:
        dr = csv.DictReader(fin)  # 使用csv.DictReader读取CSV文件
        to_db = [(i['省'], i['省行政区划代码'], i['市'], i['市行政区划代码'], i['区'], i['区行政区划代码'], i['来源'])
                 for i in dr]

    cur.executemany("""
        INSERT INTO city_data (省, 省行政区划代码, 市, 市行政区划代码, 区, 区行政区划代码, 来源)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, to_db)
    conn.commit()


# import pandas as pd
# table = pd.read_csv(f"{current_dir_path}/city_db_data.csv")
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


if __name__ == '__main__':
    print(get_area_codes(
        address='|南通|市辖区'
    ))

    # csv_db()

