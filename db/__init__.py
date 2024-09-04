import os
import pandas as pd

current_dir_path = os.path.dirname(os.path.abspath(__file__))
table = pd.read_csv(f"{current_dir_path}/city_db_data.csv")
# with open(f"{current_dir_path}/CommonlyUsedSurname.txt", 'r', encoding='utf-8') as file:
#     CommonlyUsedSurname = list(file.read())


def get_area_codes(address: str):
    province, city, area = address.split("|")
    results = table.copy()
    if province:
        results = results[results['省'].str.contains(province)]
    if city:
        results = results[results['市'].str.contains(city)]
    if area:
        results = results[results['区'].str.contains(area)]

    result = []
    for index, row in results.iterrows():
        source = row['来源']
        area = row['区']
        area_code = row['区行政区划代码']
        city = row['市']
        city_code = row['市行政区划代码']
        province = row['省']
        province_code = row['省行政区划代码']
        # print(f'[{area_code}]{province} {city} {area}, 数据来源:{source}')
        result.append(area_code)
    return result


if __name__ == '__main__':
    # print(get_area_codes(
    #     address='福建|三明|'
    # ))
    print(CommonlyUsedSurname)