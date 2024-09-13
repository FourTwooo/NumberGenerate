## NumberGenerate

**NumberGenerate** 虚拟信息生成器.

***

> IDCardGenerate
>> 区域代码使用本地数据 **[db/city_db_data.csv]**

```python

import Generate

IDCard = Generate.IDCardGenerate()
# 生成器
'''
[必选]:param id_card:         模糊身份证号
[可选]:param address:         地区 -> "省|市|区"
[可选]:param gender:          性别
[可选]:param constellation    星座
[可选]:param zodiac:          生肖
:return: [id_card...]
'''
result = IDCard.get_id_card(
    id_card="44****2000******28",
    address="广东|揭阳|",
    gender="女",
    constellation="狮子座",
    zodiac="龙"
)

result = ['445201200007230328', '445201200007231128', '445201200007233828', '445201200007234628', ...]

# 更改自定义查询接口
'''
[可选]:param address:         地区 -> "省|市|区"
:return: [区域代码...]
'''
IDCard.api_function = lambda address: ["320505"]

# 起始年份设定
IDCard.START_YEAR = 1900
# 终止年份设定
IDCard.END_YEAR = 2000
```

> PhoneGenerate
>> 号段使用第三方平台 **[[查号吧](https://www.chahaoba.com), [手机号段网](https://telphone.cn)]**

```python
import Generate

Phone = Generate.PhoneGenerate()

# 生成器
'''
[必选]:param incomplete_phone:        模糊手机号
[可选]:param city_name:               市
:return:                        [phone...]
'''
result = Phone.get_phone(
    city_name="永州",
    incomplete_phone="182***6**03"
)
result = [18229450003, 18229450103, 18229450203, 18229450303, 18229450403, ...]

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
# 更换 手机号段网 [默认就是手机号段网]
Phone.api_function = api.tel_phone

```

> NameGenerate
>> 生成姓名,支持未知,拼音,缩写,中文多种传参方式

```python
import Generate

# 文字库选择
'''
[可选]:param rare_word:               生僻字
[可选]:param common_words:            常用字
[可选]:param secondary_common_words:  次要常用字
[可选]:param all_words:               所有汉字
'''

Name = Generate.NameGenerate(
    rare_word=False,
    common_words=True,
    secondary_common_words=True,
    all_words=False
)

# 添加汉字
"""
[必选]:param words:   传入的汉字列表. 如果generate_chinese_word生成的汉字并没有包含你需要的
"""
Name.add_words(["汉", "字"])

'''
[必选]:param name:    [["用"], ["*"], ["ce"], ["s"]]
:return:        [name...]
'''
result = Name.get_names(['ou', '阳', 'na', '*'])

result = ['殴阳捺蘸', '殴阳捺镶', '殴阳捺瓤', '殴阳捺矗', ...]





```

> SaveFile
>> 数据储存

```python
'''
[必选]:param numbers:         [数据...]
[可选]:param output_file:     储存路径[未传入路径默认为运行路径下]
'''
import Generate

saveFile = Generate.SaveFile()
saveFile.generate_vcf(['13812344321', '13812344322', ...])
saveFile.generate_txt(['data1', 'data2'])
```
