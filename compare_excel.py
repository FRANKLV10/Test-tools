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
        self.result_json = {}

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
        if len(sheet_names) < 2:
            self.result = "表格没有多余sheet"
        else:
            self.origin = pd.read_excel(self.file_path[0], sheet_name=sheet_names[0])

            for i in range(1, len(sheet_names)):
                self.new = pd.read_excel(self.file_path[0], sheet_name=sheet_names[i])
                self._cmp()

    def _cmp(self):
        try:
            self.result = self.origin.compare(other=self.new, keep_shape=False, keep_equal=True)
        except ValueError:
            self.result = '表格有改动'

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
            self.result = "请输入正确路径"

    def change_result(self):
        self.choose_compare_type()

        if isinstance(self.result, str):
            print(self.result)
            return
        if self.result.empty:
            return 0

        else:
            return self.result

    def print_dif(self):
        if isinstance(self.result, str):
            return self.result
        index = self.result.axes[0]
        keys = self.result.columns.tolist()
        values = self.result.values
        print(self.result.to_json(orient='split', force_ascii=False))
        for i in range(len(index)):
            value = np.array_split(values[i], 2)
            key = np.array_split(keys, 2)
            index_num = index[i] + 2
            self.result_json[index[i]] = []
            for j in range(int(len(keys) / 2)):
                filed_name = key[j][0][0]
                value_old = value[j][0]
                value_new = value[j][1]

                if value_old != value_new:
                    msg = "第{}行，{}字段值做过修改，原来的值为{}，现在的值为{}".format(index_num, filed_name, value_old, value_new)
                    print(msg)
                self.result_json[index[i]].append(filed_name)
        # print(self.result_json)

    def revert_json(self):
        print(self.result.to_json(force_ascii=False))
        print(self.result.to_html('1.html'))


def get_excel_file(path):
    file_names = os.listdir(path)
    excel_names = [file_name for file_name in file_names if file_name.endswith('.xlsx')]
    return excel_names


def main(path):
    excel_names = get_excel_file(path)
    excel_name = iter(excel_names)
    while True:
        try:
            a = Compare_Excel(file_path=[next(excel_name)])
            a.change_result()
            a.print_dif()
        except StopIteration:
            break


if __name__ == '__main__':
    a = Compare_Excel(file_path=['1.xlsx', '2.xlsx'])
    a.change_result()
    a.print_dif()
    # main('./')
    # a.revert_json()
