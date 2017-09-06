# -*- coding: utf-8 -*-

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
