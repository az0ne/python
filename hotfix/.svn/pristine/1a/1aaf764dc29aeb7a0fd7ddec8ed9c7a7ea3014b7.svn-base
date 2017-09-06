# -*- coding: utf-8 -*-
__author__ = 'bobby'

import datetime

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from mz_common.decorators import superuser_required

from django.conf import settings
from django.http import Http404

class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url="/"))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class CSRFExemptMixin(object):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)

class SuperUserMixin(object):

    @method_decorator(superuser_required)
    def dispatch(self, *args, **kwargs):
        return super(SuperUserMixin, self).dispatch(*args, **kwargs)

class IPWriteListMixin(object):
    #ip白名单
    def dispatch(self, *args, **kwargs):
        ip = self.META.get('HTTP_X_REAL_IP') or self.META['REMOTE_ADDR']
        if ip in settings.IP_WHITE_LIST:
            return super(IPWriteListMixin, self).dispatch(*args, **kwargs)
        else:
            raise Http404()