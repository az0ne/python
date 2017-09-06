#!/usr/bin/env python
# -*- coding: utf8 -*-


import mz_object.MZObject as MZObject
from mz_platform.exceptions.mz_exception import MZException


class MZOrmWrapper(MZObject):
    """
    @brief django ORM object wrapper

    wrapper for ORM object for now
    - functions:
        -# wrap orm implemnetation
        -# collect smth to do functions with data
        -# disable write action default

    @todo disable all write action
    """

    def __init__(self, orm_obj=None):
        super(MZObject, self).__init__()
        self._orm_obj = orm_obj

    def __getattr__(self, name):
        try:
            return getattr(self._orm_obj, name)
        except Exception, e:
            raise MZException(e, '[NotFoundError] get attr:%s in %s' % (name, self.__class__.__name__))

    def save(self):
        """
        @brief save method

        not implement for default
        """
        pass
