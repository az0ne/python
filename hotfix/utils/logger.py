import os
import sys
import inspect
import json
import platform
import logging
from logging.handlers import SysLogHandler
from datetime import datetime
from django.conf import settings


if hasattr(sys, 'frozen'): #support for py2exe
    _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

try:
    import syslog
except:
    syslog = None


class NewLogger(logging.Logger):

    def __init__(self, *args, **kwargs):
        facility = kwargs.pop("facility")

        logging.Logger.__init__(self, *args, **kwargs)

        self.use_biz_log = False

        if platform.platform().startswith('Linux'):
            syslog.openlog(facility=facility)
            self.use_biz_log = True

    def _create_syslog_string(self, data):
        data.update({
            "logtype": "biz",
            "datetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        text = json.dumps(data)

        return text

    def findCaller(self):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """

        f = logging.currentframe().f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename in (_srcfile, logging._srcfile): # This line is modified.
                f = f.f_back
                continue
            rv = (filename, f.f_lineno, co.co_name)
            break
        return rv

    def biz(self, msg, *args, **kwargs):
        if self.use_biz_log:
            syslog.syslog(syslog.LOG_INFO, self._create_syslog_string(msg))
        else:
            if self.isEnabledFor(logging.INFO):
                self._log(logging.INFO, "[businesslog] %s" % msg, args, **kwargs)

    def _log(self, level, msg, args, exc_info=None, extra=None):
        if settings.DEBUG == False and level == logging.DEBUG:
            return None
        else:
            return logging.Logger._log(self, level,
                msg.replace("\n", " "), args, exc_info, extra)

logformat = "%(levelname)s %(filename)s %(funcName)s %(lineno)d %(message)s"

if platform.platform().startswith('Windows'):
    handler = logging.StreamHandler()
else:
    handler = SysLogHandler("/dev/log", SysLogHandler.LOG_LOCAL1)
handler.setFormatter(logging.Formatter(logformat))

logger = NewLogger("web", facility=SysLogHandler.LOG_LOCAL1)

if settings.DEBUG == True:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

logger.addHandler(handler)

if settings.DEBUG == True:
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
