from typing import List

import pandas as pd
import os


class Compare_Excel:
    def __init__(self, file_path: List[str]):
        """

        :param file_path: list：str

        """

        if file_path is None:
            file_path = list()
        self.file_path = file_path
        self.excel_origin = ''
        self.excel_new = ''

    def _compare_dif_excel(self):

        self.excel_origin = pd.read_excel(self.file_path[0])
        self.excel_new = pd.read_excel(self.file_path[1])
        result = self.excel_origin.compare(other=self.excel_new, keep_shape=True, keep_equal=True)
        if len(result.values) == 0:
            print('表格没有不同')
        else:
            print(result.head())

    def _compare_dif_sheet(self):
        self.excel_origin = pd.ExcelFile(self.file_path[0])
        sheet_names = self.excel_origin.sheet_names

        base_sheet = pd.read_excel(self.file_path[0], sheet_name=sheet_names[0])
        for i in range(1, len(sheet_names)):
            other = pd.read_excel(self.file_path[0], sheet_name=sheet_names[i])
            result = base_sheet.compare(other=other, keep_shape=False, keep_equal=True)
            print(result)

    def cmp_file(self):
        if len(self.file_path) == 2:
            self._compare_dif_excel()
        elif len(self.file_path) == 1:
            self._compare_dif_sheet()
        else:
            raise Exception('请输入正确')


if __name__ == '__main__':
    a = Compare_Excel(file_path=['1.xlsx'])
    a.cmp_file()
