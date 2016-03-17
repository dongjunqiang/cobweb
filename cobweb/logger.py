# 记录日志
import logging
import os


class Logger:

    def __init__(self, log_path=None):
        self.format_str = '%(name)s %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
        self.formatter = logging.Formatter(self.format_str)
        self.log_path = str(log_path)

        self.logger = logging.getLogger('app_logger')
        self.logger.setLevel(logging.NOTSET)

        logging.basicConfig(
                level=logging.DEBUG,
                format=self.format_str,
                filemode='a'
        )

    def do_log(self, data, context=None, path=''):
        file_handler = logging.FileHandler(path)
        file_handler.setFormatter(self.formatter)

        self.logger.addHandler(file_handler)
        # TODO level
        self.logger.debug(data + ' ' + str(context))
        self.logger.removeHandler(file_handler)
        return True

    def do_log_simple(self, data, context=None):
        self.logger.warning(data + ' ' + str(context))
        return True

    def gen_path(self, path):
        path = self.log_path + path + '/' + self.get_log_file_name()
        if not os.path.exists(path):
            dirname = os.path.dirname(path)
            # 创建目录
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            # 创建文件
            f = open(path, 'w')
            f.close()
        return path

    @staticmethod
    def get_log_file_name():
        return 'Information.log'
