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
        self.result = None

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
            self.result = self.origin.compare(other=self.new, keep_shape=False, keep_equal=True)
        except ValueError:
            return "表格有增改"

    def choose_compare_type(self):
        """
        1.两个文件路径对比不同excel
        2一个文件路径对比同一个excel中的不同sheet
        """
        if len(self.file_path) == 2:
            return self._compare_dif_excel()
        elif len(self.file_path) == 1:
            return self._compare_dif_sheet()
        else:
            return '请输入正确路径'

    def change_result(self):
        self.choose_compare_type()

        if self.result.empty:
            return 0
        else:
            self.print_dif()

    def print_dif(self):

        index = self.result.axes[0]
        keys = self.result.columns.tolist()

        values = self.result.values

        for i in range(len(index)):
            value = np.array_split(values[i], 2)
            key = np.array_split(keys, 2)
            index_num = index[i] + 2

            for j in range(int(len(keys) / 2)):
                filed_name = key[j][0][0]
                value_old = value[j][0]
                value_new = value[j][1]
                if value_old != value_new:
                    print("第{}行，{}字段值做过修改，原来的值为{}，现在的值为{}".format(index_num, filed_name, value_old, value_new))


if __name__ == '__main__':
    a = Compare_Excel(file_path=['1.xlsx', '2.xlsx'])
    print(a.change_result())
