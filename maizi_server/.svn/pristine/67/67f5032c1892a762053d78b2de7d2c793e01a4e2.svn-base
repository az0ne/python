#-*- coding:utf-8 -*-

from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

class DebugMiddleWare(object):

    def process_exception(self, request, exception):
        if settings.DEBUG:
            print exception
