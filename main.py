import Generate

if __name__ == '__main__':
    IDCard = Generate.IDCardGenerate()
    date_data = IDCard.get_id_card(
        id_card="44****2000******28",
        address="广东|揭阳|",
        # gender="女",
        # constellation="狮子座",
        # zodiac="龙"
    )
    print(len(date_data), str(date_data)[:200])
    #
    Phone = Generate.PhoneGenerate()
    phones = Phone.get_phone(
        city_name="永州",
        incomplete_phone="182***6**03"
    )
    print(len(phones), phones)

    Name = Generate.NameGenerate()
    names = Name.get_names(['ou', '阳', 'na', '*'])
    print(len(names), names)

    saveFile = Generate.SaveFile()

    saveFile.generate_vcf(phones)
    saveFile.generate_txt(phones)
