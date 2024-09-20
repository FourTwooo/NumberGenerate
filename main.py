import Generate

if __name__ == '__main__':
    # IDCard = Generate.IDCardGenerate()
    # IDCard.START_YEAR = 2000
    # IDCard.END_YEAR = 2010
    # # IDCard.api_function = lambda address: ["320505"]
    # date_data = IDCard.get_id_card(
    #     id_card="5*****20050319***4",
    #     # id_card="320***200205071516",
    #     # address="广东|揭阳|",
    #     gender="男",
    #     # constellation="狮子座",
    #     # zodiac="龙"
    # )
    # print(len(date_data), str(date_data)[:200])

    Phone = Generate.PhoneGenerate()
    # Phone.is_db = False
    from Generate import api

    # print(api.PHONE_ISP_CODES)
    # Phone.api_function = api.cha_hao_baw
    # Phone.api_function = api.tel_phone
    phones = Phone.get_phone(
        # city_name="北京",
        incomplete_phone="1******3434",
        # isp="虚拟"
    )
    print(len(phones), phones[:20])

    # Name = Generate.NameGenerate()
    # names = Name.get_names(['huang', 'zhi', 'chao'])
    # print(len(names), names)
    #
    # saveFile = Generate.SaveFile()
    #
    # saveFile.generate_vcf(phones)
    # saveFile.generate_txt(date_data)


