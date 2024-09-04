import os

import Generate.errors


class SaveFile:

    def __init__(self):
        # self.current_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.current_dir_path = os.getcwd()

    def __get_save_file(self, output_file: str):
        save_file = f'{self.current_dir_path}\\{output_file}'
        print(save_file)
        return save_file

    def generate_txt(self, numbers: list, output_file: str = "data.txt"):
        output_file = self.__get_save_file(output_file)
        with open(output_file, 'w') as f:
            for phone in numbers:
                f.write(f'{phone}\n')

    def generate_vcf(self, numbers: list, output_file: str = "contacts.vcf"):
        output_file = self.__get_save_file(output_file)
        with open(output_file, 'w') as file:
            for phone_number in numbers:
                if len(str(phone_number)) != 11:
                    raise Generate.errors.NumberValueError(f'{phone_number} len != 11')
                file.write('BEGIN:VCARD\n')
                file.write('VERSION:3.0\n')
                file.write(f'FN:{phone_number}\n')
                file.write(f'TEL;TYPE=CELL:{phone_number}\n')
                file.write('END:VCARD\n')



