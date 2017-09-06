#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse

class sessionMiddleWare(object):

    def process_request(self,request):

        url_list = ['','/login/','/user/login/']

        if not request.get_full_path() in url_list:
            try:
                a = 1
                user_id = request.session['user_id']
                user_name = request.session['user_name']
                real_name = request.session['real_name']
            except KeyError:
                return HttpResponseRedirect(reverse('index'))
