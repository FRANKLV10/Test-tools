import time
from app.settings import TableConfig
import pandas as pd

# key：查询字段 value：中间字段 result:想查询字段
from app.utils.logger import logger




setting = [{"Guide_引导表.xlsx": {"key": "id", "value": "stepId", "result": []},
           "Step_步骤表.xlsx": {"key": "id", "value": "id", "result": ["anchorName"]}}]
# def catch_exception(except_func):
#     def func(*args, **kwargs):
#
#         try:
#             return except_func(*args, **kwargs)
#         except Exception as e:
#             # print('发生错误的文件：', e.__traceback__.tb_frame.f_globals['__file__'])
#             #
#             # print('错误所在的行号：', e.__traceback__.tb_lineno)
#
#             print('未查询到数据', e)
#
#     return func


class Target:
    def __init__(self, word, setting_table):
        self._setting_table = setting_table

        self.name = word
        self.result = dict()

        self.i = 0  # 计数用

    @staticmethod
    def read_csv(path):
        data = pd.read_csv(path)
        return data

    @staticmethod
    def read_excel(path):
        data = pd.read_excel(path, header=1)
        return data

    @staticmethod
    def is_nan(value):
        if pd.isnull(value):
            value = ""
        return value

    def _is_show(self, search_table, context):

        search_result = search_table.get("showWord")
        if len(search_result) != 0 and search_result[0] != "":

            for key in search_result:
                value = context[key].values[0]
                print(value)
                value = self.is_nan(value)
                if key in self.result.keys():

                    self.result[key].append(value)
                else:
                    self.result.setdefault(key, []).append(value)

    def is_new_key(self):
        pass

    def _is_single(self):

        if isinstance(self.name, str):
            '''
            一个字段中多个值情况，单独写规则判断
            '''
            # 格式为1|2|3
            if "|" in self.name:
                self.name = self.name.split("|")
            # 格式为数组[1,2,3]
            if "[" and "]" in self.name:
                self.name = self.name.replace("[", "").replace("]", "").split(",")

                self.name = list(map(int, self.name))

        if isinstance(self.name, list):

            search_word = self.name

            for index, w in enumerate(search_word):

                count = self.i

                self.name = w
                self._get_info()
                if index < len(search_word) - 2:
                    self.i = count

    def print_format(self):
        try:
            self._get_info()
            return self._revert_to_json()
        except Exception as e:
            logger.error(e.with_traceback())
            return "未找到数据"

    def _revert_to_json(self):
        json_result = {}
        table_data = []
        keys = self.result.keys()

        value = self.result.values()
        length = max([len(l) for l in value])

        for i in range(length):
            result_dict = {}
            for j in keys:
                try:
                    result_dict[j] = self.result[j][i]
                except Exception as e:
                    print(e)
                    result_dict[j] = ""
            table_data.append(result_dict)
        json_result["col"] = list(keys)
        json_result["table_data"] = table_data
        print(json_result)
        return json_result

    def _get_info(self):
        if self.i < len(self._setting_table):
            search_table = self._setting_table[self.i]

            search_key = search_table.get("key")

            search_value = search_table.get("value")

            data = self.read_csv(TableConfig.LOCAL_PATH + search_table.get("tableName"))
            # data = self.read_excel(self.tables[self.i])
            self._is_single()

            context = data[data[search_key].isin([self.name])]
            self._is_show(search_table, context)

            self.name = context[search_value].values[0]

            self.i += 1

            self._get_info()


# def search(path, word):
#     data = read_csv(path)
#     t = "文本內容"
#     context = data[data[t].isin([word])]
#     name = context["文本编号"]
#     print(name.values)


if __name__ == '__main__':
    A = Target("", setting)

    A.print_format()

    C = time.time()
