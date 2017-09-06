# -*- coding: utf-8 -*-
"""
对分页的封装
pg=Pt(objs,per_page=10).page(page)
objs=pg.objects

author:Jackie
"""

from django.core.paginator import Paginator, Page, InvalidPage, EmptyPage


class Pt:
    def __init__(self, object_list, per_page):
        self.object_list = object_list
        self.per_page = per_page

    def page(self, number):
        """
        分页方法
        :param object_list:
        :param per_page:每页数量
        :param number:页码
        :return:本页对象列表,当前页码,上一页,下一页,总页码,每页数量
        """
        try:
            number = int(number)
        except:
            number = 1

        instance = Paginator(self.object_list, self.per_page)
        try:
            page = instance.page(number)
        except (InvalidPage, EmptyPage):
            if number <= 0:
                page = instance.page(1)
            else:
                page = instance.page(instance.num_pages)
        return Pg(page)


class Pg(object):
    def __init__(self, instance):
        assert isinstance(instance, Page), 'Must be django Page instance!'
        self.page = instance

    @property
    def objects(self):
        """当前页对象list"""
        return self.page.object_list

    @property
    def total(self):
        return self.page.paginator.num_pages

    @property
    def current(self):
        """当前页码"""
        return self.page.number

    @property
    def next(self):
        """下一页码"""
        return self.page.next_page_number()

    @property
    def previous(self):
        """上一页码"""
        return self.page.previous_page_number()
