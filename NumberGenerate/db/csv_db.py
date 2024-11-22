import csv
import os
import sqlite3


DB_NAME = 'area_code.db'

current_dir_path = os.path.dirname(os.path.abspath(__file__))
# 创建SQLite连接
conn = sqlite3.connect(f"{current_dir_path}/{DB_NAME}")
cur = conn.cursor()


def city_data_csv_db():
    CSV_NAME = 'area_code.csv'
    global cur
    # 创建表
    # cur.execute("""
    #     CREATE TABLE city_data(
    #         省 TEXT,
    #         省行政区划代码 TEXT,
    #         市 TEXT,
    #         市行政区划代码 TEXT,
    #         区 TEXT,
    #         区行政区划代码 TEXT,
    #         来源 TEXT
    #     )
    # """)

    # 将CSV数据插入数据库
    with open(f"{current_dir_path}/{CSV_NAME}", 'r', encoding='utf-8') as fin:
        dr = csv.DictReader(fin)  # 使用csv.DictReader读取CSV文件
        to_db = [(i['省'], i['省行政区划代码'], i['市'], i['市行政区划代码'], i['区'], i['区行政区划代码'], i['来源'])
                 for i in dr]

    print(to_db[0][-1], type(to_db[0][-1]))
    # cur.executemany("""
    #     INSERT INTO city_data (省, 省行政区划代码, 市, 市行政区划代码, 区, 区行政区划代码, 来源)
    #     VALUES (?, ?, ?, ?, ?, ?, ?);
    # """, to_db)
    # conn.commit()


def phone_csv_db():
    CSV_NAME = 'phone_3.csv'
    global cur
    # 创建表
    cur.execute("""
        CREATE TABLE phone_data(
            号段 TEXT,
            省 TEXT,
            市 TEXT,
            邮政编码 TEXT,
            区号 TEXT,
            运营商 TEXT,
            来源 TEXT
        )
    """)

    # 将CSV数据插入数据库
    with open(f"{current_dir_path}/{CSV_NAME}", 'r', encoding='utf-8') as fin:
        dr = csv.DictReader(fin)  # 使用csv.DictReader读取CSV文件
        to_db = [(i['号段'], i['省'], i['市'], i['邮政编码'], i['区号'], i['运营商'], i['来源'])
                 for i in dr]
    print(to_db)
    cur.executemany("""
        INSERT INTO phone_data(号段, 省, 市, 邮政编码, 区号, 运营商, 来源)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, to_db)
    conn.commit()


if __name__ == '__main__':
    phone_csv_db()
    # city_data_csv_db()