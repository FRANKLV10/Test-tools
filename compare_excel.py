from typing import List

import pandas as pd
import numpy as np
import os


class Compare_Excel:
    def __init__(self, file_path: List[str]):
        """

        :param file_path: list：str

        """

        if file_path is None:
            file_path = list()
        self.file_path = file_path
        self.origin = ''
        self.new = ''

    def _compare_dif_excel(self):
        """
        比较不同excel
        """

        self.origin = pd.read_excel(self.file_path[0])
        self.new = pd.read_excel(self.file_path[1])
        self._cmp()

    def _compare_dif_sheet(self):
        """
        比较同一个excel 不同sheet
        """
        excel = pd.ExcelFile(self.file_path[0])
        sheet_names = excel.sheet_names
        self.origin = pd.read_excel(self.file_path[0], sheet_name=sheet_names[0])

        for i in range(1, len(sheet_names)):
            self.new = pd.read_excel(self.file_path[0], sheet_name=sheet_names[i])
            self._cmp()

    def _cmp(self):
        try:
            result = self.origin.compare(other=self.new, keep_shape=False, keep_equal=True)
            return result
        except ValueError:
            return "表格有增删"

    def choose_compare_type(self):
        if len(self.file_path) == 2:
            self._compare_dif_excel()
        elif len(self.file_path) == 1:
            self._compare_dif_sheet()
        else:
            return '请输入正确路径'

    def change_result(self):
        cmp_result = self.choose_compare_type()
        print(cmp_result)


if __name__ == '__main__':
    a = Compare_Excel(file_path=['1.xlsx'])
    print(a.choose_compare_type())

