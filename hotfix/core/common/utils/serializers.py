# -*- coding: utf-8 -*-
import datetime
from utils.logger import logger as log


class SimpleModelSerializer(object):
    def __init__(self, obj, fields=[]):
        self.obj = obj
        self._fields = fields
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = {}
            for field in self.obj._meta.local_fields:
                if self._fields and field.attname not in self._fields:
                    continue
                self._data[field.attname] = getattr(self.obj, field.attname)
        return self._data


def get_week_dict():
    """
    获取week_dict
    :return:
    """
    try:
        now = datetime.datetime.now()
        week_dict = {0: u'日', 1: u'一', 2: u'二', 3: u'三', 4: u'四', 5: u'五', 6: u'六', }
        day_dict = dict(
            zip(map(lambda x: (now + datetime.timedelta(x)).strftime('%F'), range(0, 3)), (u'今天', u'明天', u'后天')))
    except Exception as e:
        log.warn(str(e))
        week_dict, day_dict = {}, {}
    return week_dict, day_dict
