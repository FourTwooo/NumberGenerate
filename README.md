## NumberGenerate
**NumberGenerate** 虚拟信息生成器，提供身份证号码、电话号码、姓名等数据的生成和保存功能。支持多种自定义参数设置，以适应不同的使用场景。

***
## 免责声明

代码生成数据均为虚假并单一数据.本人仅用个人网站虚假用户填写测试为此开发.

所有内容仅限用于学习和研究目的。不得将上述内容用于商业或者非法用途，否则，一切后果请用户自负，通过使用项目代码随之而来的风险与本人无关。
***
### Generate.IDCardGenerate

使用的区域代码数据库： **\[db/area_code.db - city_data\]**

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
| 属性            | 类型     | 默认值 | 是否必填 | 说明            |
|:--------------|:-------|:----|:-----|:--------------|
| id_card       | String | 无   | 是    | 模糊身份证号        |
| address       | String | "\|\|"   | 否    | 地区，格式为 "省\|市\|区"     |
| gender        | String |  None  | 否    | 性别，可选为"男"或"女" |
| constellation | String | "未知星座"   | 否    | 星座，如"狮子座"     |
| zodiac        | String | "未知生肖"   | 否    | 生肖，如"龙"       |

**示例代码**
```python
result = IDCard.get_id_card(
    id_card="44****2000******28",
    address="广东|揭阳|",
    gender="女",
    constellation="狮子座",
    zodiac="龙"
)

# 调用方法后，返回结果
result = ['445201200007230328', '445201200007231128', '445201200007233828', '445201200007234628', ...]
```


### Generate.PhoneGenerate()
本地数据库 **\[db/area_code.db - phone_data\]**

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

# 更换 查号吧
Phone.api_function = api.cha_hao_ba
# 更换 手机号段网 [默认是此手机号段网]
Phone.api_function = api.tel_phone
```

#### Generate.PhoneGenerate().get_phone
| 属性            | 类型     | 默认值 | 是否必填 | 说明            |
|:--------------|:-------|:----|:-----|:--------------|
| incomplete_phone| String | 无   | 是    | 模糊手机号        |
| city_name       | String | None   | 否    | 地区名，格式为 省或市名     |
```python
result = Phone.get_phone(
    city_name="永州",
    incomplete_phone="182***6**03"
)
# 调用方法后，返回结果
result = [18229450003, 18229450103, 18229450203, 18229450303, 18229450403, ...]
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
| 属性            | 类型     | 默认值 | 是否必填 | 说明            |
|:--------------|:-------|:----|:-----|:--------------|
| words       | List | 无   | 是    | 传入的汉字列表. 如果generate_chinese_word生成的汉字并没有包含你需要的        |

**示例代码**

```python
Name.add_words(["汉", "字"])
```


#### Generate.NameGenerate().get_names
| 属性            | 类型     | 默认值 | 是否必填 | 说明            |
|:--------------|:-------|:----|:-----|:--------------|
| name       | List | 无   | 是    | 姓名列表|

**示例代码**

```python
result = Name.get_names(['ou', '阳', 'na', '*'])

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
| 属性            | 类型     | 默认值 | 是否必填 | 说明            |
|:--------------|:-------|:----|:-----|:--------------|
| numbers       | List | 无   | 是    | 储存号码|
| output_file       | String | "data.txt"   | 否    | 储存路径|

**示例代码**
```python
saveFile.generate_vcf(['13812344321', '13812344322', ...])
```


#### Generate.NameGenerate().generate_txt
| 属性            | 类型     | 默认值 | 是否必填 | 说明            |
|:--------------|:-------|:----|:-----|:--------------|
| numbers       | List | 无   | 是    | 储存号码|
| output_file       | String | "contacts.vcf"   | 否    | 储存路径|

**示例代码**
```python
saveFile.generate_txt(['data1', 'data2'])
```

## 交流群
<a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=6JWWosRVV0rtISqQKNVU5QY8KT0sBQP8&jump_from=webapi&authKey=kvD0trmJvJiWSeFVv1+WTUYBpalYGKh+dF3zgfpLDuByEmZF2wT8XXwC8QuT/tzQ"><img border="0" src="https://pub.idqqimg.com/wpa/images/group.png" alt="逆向交流学习" title="逆向交流学习"></a>