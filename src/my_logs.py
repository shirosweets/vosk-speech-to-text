import os
import sys
import errno
import logging
import datetime

from json import loads, dumps


class Log():
    def __init__(self, logpath, filename):
        self.filename = filename
        self.logpath = logpath
        r_path_log = f"{self.logpath}{self.filename}.log"
        self.full_path_log = os.getcwd()+'/logs/'+r_path_log

    def append_msg_log(self, msg):
        logpath = self.full_path_log
        try:
            with open(logpath, 'a') as op_path:
                op_path.write(msg+'\n')
        except FileNotFoundError:
            try:
                os.makedirs(os.path.dirname(logpath))
                with open(logpath, 'a') as op_path:
                    op_path.write(msg+'\n')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise e

    def save_message_on_log(self, message):
        self.append_msg_log(message)


class Logger(object):
    _logger = None

    @classmethod
    def logger(cls):
        if not Logger._logger:
            Logger._logger = logging.getLogger('Welo-Speech-to-text')
            Logger._logger.setLevel(logging.DEBUG)

            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter('[%(levelname)s %(module)s.py: %(lineno)d ]')  # noqa
            handler.setFormatter(formatter)

            Logger._logger.addHandler(handler)
        return Logger._logger
