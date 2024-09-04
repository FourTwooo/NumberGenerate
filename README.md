# NumberGenerate

**NumberGenerate** 生成虚假信息(姓名,身份证,手机号)


IDCardGenerate

区域代码使用本地数据[db/city_db_data.csv]
```python
:param id_card:         模糊身份证号
:param address:         地区 -> "省|市|区"
:param gender:          性别
:param constellation    星座
:param zodiac:          生肖
:return: [id_card...]

>>> import Generate
>>> Generate.IDCardGenerate().get_id_card(
        id_card="44****2000******28",
        address="广东|揭阳|",
        gender="女",
        constellation="狮子座",
        zodiac="龙"
    )
result => ['445201200007230328', '445201200007231128', '445201200007233828', '445201200007234628', ...]
```

IDCardGenerate

号段使用第三方平台[[查号吧](https://www.chahaoba.com), [手机号段网](https://telphone.cn)]
```python
:param city_name:               市
:param incomplete_phone:        模糊手机号
:return:                        [phone...]

>>> Generate.PhoneGenerate().get_phone(
        city_name="永州",
        incomplete_phone="182***6**03"
    )
result => [18229450003, 18229450103, 18229450203, 18229450303, 18229450403, ...]
```

NameGenerate


```python
:param name:    [["张"], ["*"]]
:return:        [name...]

>>> Generate.NameGenerate().get_names(['ou', '阳', 'na', '*'])
result => ['殴阳捺蘸', '殴阳捺镶', '殴阳捺瓤', '殴阳捺矗', ...]
```


SaveFile

数据储存
```python
:param numbers:         [数据...]
:param output_file:     储存路径

>>> saveFile = Generate.SaveFile()
>>> saveFile.generate_vcf(['13812344321', '13812344322', ...])
>>> saveFile.generate_txt(['data1', 'data2'])
```
