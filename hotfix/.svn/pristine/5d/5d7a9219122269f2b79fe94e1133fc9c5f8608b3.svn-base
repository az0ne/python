# -*- coding: utf-8 -*-

from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
import re
from django.core import signing
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

class CheckBrowser(object):

    def process_request(self, request):
        try:
            #agent = request.META.get('HTTP_USER_AGENT')
            #p = re.findall('MSIE [678]\.0', agent)
            #if len(p) > 0 and request.get_full_path().find("services-api/app") == -1:
            #    warning = request.META.get('PATH_INFO')
            #    war = re.findall('common/browser/warning/',warning)
            #    if len(war) == 0:
            #        return HttpResponsePermanentRedirect('/common/browser/warning/')
            pass
        except  Exception as e:
            pass

class SyncLoginMiddleware(object):
    '''同步登录
    '''
    def process_request(self, request):
        if 'maizi_token' in request.REQUEST:
            maizi_token = request.REQUEST['maizi_token']
            if maizi_token:
                try:
                    data = signing.loads(maizi_token, key=settings.MAIZI_KEY,
                                         max_age=settings.KEY_EXPIRE_SECONDS)
                    user = authenticate(uuid=data['uuid'])
                    login(request, user)
                    return HttpResponseRedirect(request.path)
                except Exception, e:
                    print e

