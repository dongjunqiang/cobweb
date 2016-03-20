# 存储器
import types
import os


class Storage:

    def __init__(self, func=None):
        self.base_dir = 'E:\Cobweb\cobweb\\'
        if func is not None:
            self.save = types.MethodType(func, self)

    # 默认使用file储存
    def save(self, filename, data):
        path = self.base_dir + filename
        # 如果文件存在则返回
        if os.path.exists(path):
            return False
        try:
            with open(path, 'w', encoding='utf8') as out:
                print(str(data), file=out)
        except IOError as err:
            return False
        return True

    def set_base_dir(self, base_dir):
        self.base_dir = base_dir
        return self


def redis_save(self, key, value):
    return True


def mysql_save(self, value):
    return True

