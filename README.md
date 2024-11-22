## NumberGenerate
**NumberGenerate** 虚拟信息生成器，提供身份证号码、电话号码、姓名等数据的生成和保存功能。支持多种自定义参数设置，以适应不同的使用场景。

---
## 免责声明

本工具生成的数据均为虚构，仅供测试和学习使用。用户不得将上述内容用于商业或非法用途。使用本工具生成的数据，用户需自行承担相关风险和责任。通过使用本项目代码，用户同意遵守此使用条款，并理解由此带来的任何风险与本人或开发者无关。

---
### Generate.IDCardGenerate

使用的区域代码数据库： [db/area_code.db - city_data](./Generate/db/area_code.db)<!-- @IGNORE PREVIOUS: link -->

**类属性**

| 属性           | 类型     | 默认值  | 说明            |
|:--------------|:-------  |:----|:--------------|
| db_function   | Function | from Generate.db import get_area_codes   | 本地数据库查询函数        |
| START_YEAR    | Int   | 1900   | 生成起始年份|
| END_YEAR      | Int   | datetime.now().year + 1   | 生成终止年份 |
| CONSTELLATIONS| String   | ...   | 星座表     |

**示例代码**

```python
import Generate

IDCard = Generate.IDCardGenerate()

# 自定义查询接口（可选参数）
# 参数说明:
# address: 地区，格式为 "省|市|区"
# 返回值: [区域代码...]
IDCard.db_function = lambda address: ["320505"]

# 设定起始年份
IDCard.START_YEAR = 1900

# 设定终止年份
IDCard.END_YEAR = 2000

```

#### Generate.IDCardGenerate().get_id_card
> 身份证号码生成

| 属性            | 类型     | 默认值 | 是否必填 | 说明            |
|:--------------|:-------|:----|:-----|:--------------|
| id_card       | String | 无   | 是    | 模糊身份证号        |
| address       | String | "\|\|"   | 否    | 地区，格式为 "省\|市\|区"     |
| gender        | String |  None  | 否    | 性别，可选为"男"或"女" |
| constellation | String | "未知星座"   | 否    | 星座，如"狮子座"     |
| zodiac        | String | "未知生肖"   | 否    | 生肖，如"龙"       |
| lunar_birthday        | String |  None  | 否    | 农历的公历生日 |

**示例代码**
```python
import Generate

IDCard = Generate.IDCardGenerate()

result = IDCard.get_id_card(
    id_card="44****2000******28",
    address="广东|揭阳|",
    gender="女",
    constellation="狮子座",
    zodiac="龙"
)
```
**示例输出**
```python
# 调用方法后，返回结果
result = ['445201200007230328', '445201200007231128', '445201200007233828', '445201200007234628', ...]
```

#### Generate.IDCardGenerate().generator_date
> 年份日期生成

| 属性            | 类型     | 默认值 | 是否必填 | 说明            |
|:--------------|:-------|:----|:-----|:--------------|
| date_str       | String | 无   | 是    | 模糊年份日期 - "****\[年\]\*\*\[月\]\*\*\[日\]"  |
| constellation  | String | "未知星座"   | 否    | 星座     |
| zodiac        | String |  "未知生肖"  | 否    | 生肖 |
| lunar_birthday        | String |  None  | 否    | 农历的公历生日 |

**示例代码**
```python
import Generate

IDCard = Generate.IDCardGenerate()

result = IDCard.generator_date(
    '20******', 
    lunar_birthday="20240513", 
    constellation="金牛座", 
    zodiac="马"
)
```
**示例输出**
```python
# 调用方法后，返回结果
result = ['20020517', '20140504']
```


### Generate.PhoneGenerate()
使用的号段数据库 [db/area_code.db - phone_data](./Generate/db/area_code.db)<!-- @IGNORE PREVIOUS: link -->

号段在线查询使用第三方平台 **[[查号吧](https://www.chahaoba.com), [手机号段网](https://telphone.cn)]**

**类属性**

| 属性           | 类型     | 默认值  | 说明            |
|:--------------|:-------  |:----|:--------------|
| api_function   | Function | from Generate import api   | 在线API查询|
| db_function    | Function   | from Generate import db   | 本地数据库查询函数|
| is_db      | Bool   | True  | 是否开启数据库查询,默认开启.关闭才会使用在线查询|

**示例代码**

```python
import Generate

Phone = Generate.PhoneGenerate()
# 关闭离线(本地数据库)查询
Phone.is_db = False

# 更改自定义查询接口
'''
[必选]:param incomplete_phone:        模糊手机号
[可选]:param city_name:               市
:return:                        [号段...]
'''
Phone.api_function = lambda incomplete_phone, city_name: ["1588854"]

from Generate import api

# 运营商号段更换
# {"移动": ["134", "135", ...],"联通": ["130", "131", ...], "电信": ["133", "149", ...]}
api.PHONE_ISP_CODES["移动"].append("188")
# 更换 查号吧
Phone.api_function = api.cha_hao_ba
# 更换 手机号段网 [默认是此手机号段网]
Phone.api_function = api.tel_phone
```

#### Generate.PhoneGenerate().get_phone
> 手机号码生成

| 属性            | 类型     | 默认值 | 是否必填 | 说明            |
|:--------------|:-------|:----|:-----|:--------------|
| incomplete_phone| String | 无   | 是    | 模糊手机号        |
| city_name       | String | None   | 否    | 地区名，格式为 省或市名     |
| isp       | String | None   | 否    | 运营商     |

**示例代码**

```python
import Generate

Phone = Generate.PhoneGenerate()

result = Phone.get_phone(
    city_name="毕节",
    incomplete_phone="13*****3434",
    isp="联通"
)
```
**示例输出**
```python
# 调用方法后，返回结果
result = [13017063434, 13035543434, 13048543434, 13048553434, ...]
```

#### Generate.PhoneGenerate().generate_phone_area
> 手机号段生成

| 属性             | 类型   | 默认值 |是否必填| 说明             |
|:--------------  |:-------|:---- |:----- |:--------------|
| incomplete_phone| String | 无   | 是     | 模糊手机号      |
| city_name       | String | None | 否    | 地区名，格式为 省或市名|
| isp             | String | None | 否    | 运营商          |

**示例代码**

```python
import Generate

Phone = Generate.PhoneGenerate()

result = Phone.generate_phone_area(
    city_name="北京",
    incomplete_phone="1*******434",
    isp="虚拟"
)
```
**示例输出**
```python
# 调用方法后，返回结果
result = ['1621002', '1621003', '1621004', '1621001']
```


### Generate.NameGenerate()
生成姓名,支持未知,拼音,缩写,中文多种传参方式

**类属性**

| 属性           | 类型     | 默认值  | 说明            |
|:--------------|:-------  |:----|:--------------|
| CommonlyUsedSurname   | List | Name.CommonlyUsedSurname  | 百家姓|

**实例化传参**

| 属性            | 类型     | 默认值 | 是否必填 | 说明            |
|:--------------|:-------|:----|:-----|:--------------|
| rare_word       | Bool | False   | 否    | 生僻字        |
| common_words       | Bool | True   | 否    | 常用字|
| secondary_common_words | Bool | True   | 否    | 次要常用字|
| all_words | Bool | False   | 否    | 所有汉字 |

**示例代码**
```python
import Generate

Name = Generate.NameGenerate(
    rare_word=False,
    common_words=True,
    secondary_common_words=True,
    all_words=False
)
```


#### Generate.NameGenerate().add_words
> 添加未知汉字

| 属性            | 类型     | 默认值 | 是否必填 | 说明            |
|:--------------|:-------|:----|:-----|:--------------|
| words       | List | 无   | 是    | 传入的汉字列表. 如果内置的汉字并没有包含你需要的 |

**示例代码**

```python
import Generate

Name = Generate.NameGenerate()

Name.add_words(["汉", "字"])
```


#### Generate.NameGenerate().get_names
> 姓名生成

| 属性            | 类型     | 默认值 | 是否必填 | 说明            |
|:--------------|:-------|:----|:-----|:--------------|
| name       | List | 无   | 是    | 姓名列表|

**示例代码**

```python
import Generate

Name = Generate.NameGenerate()

result = Name.get_names(['ou', '阳', 'na', '*'])
```
**示例输出**
```python
# 调用方法后，返回结果
result = ['殴阳捺蘸', '殴阳捺镶', '殴阳捺瓤', '殴阳捺矗', ...]
```



### Generate.SaveFile()
数据储存

**类属性**

| 属性           | 类型     | 默认值  | 说明            |
|:--------------|:-------  |:----|:--------------|
| current_dir_path   | String | os.getcwd()  | 文件储存默认路径|

**示例代码**

```python
import Generate

saveFile = Generate.SaveFile()
# 更改储存路径
saveFile.current_dir_path = 'C:/'
```

#### Generate.NameGenerate().generate_vcf
> vcf文件生成

| 属性            | 类型     | 默认值 | 是否必填 | 说明            |
|:--------------|:-------|:----|:-----|:--------------|
| numbers       | List | 无   | 是    | 储存号码|
| output_file       | String | "data.txt"   | 否    | 储存路径|

**示例代码**
```python
import Generate

saveFile = Generate.SaveFile()

saveFile.generate_vcf(['13812344321', '13812344322', ...])
```


#### Generate.NameGenerate().generate_txt
> txt文件生成

| 属性            | 类型     | 默认值 | 是否必填 | 说明            |
|:--------------|:-------|:----|:-----|:--------------|
| numbers       | List | 无   | 是    | 储存号码|
| output_file       | String | "contacts.vcf"   | 否    | 储存路径|

**示例代码**
```python
import Generate

saveFile = Generate.SaveFile()

saveFile.generate_txt(['data1', 'data2'])
```