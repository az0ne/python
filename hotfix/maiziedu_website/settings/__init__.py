# -*- coding: utf-8 -*-

import os


env = os.environ.get("ENV", "local")

if env == "prod":
    from maiziedu_website.settings.prod import *
elif env == "staging":
    from maiziedu_website.settings.staging import *
elif env == "local":
    from maiziedu_website.settings.local import *
else:
    raise Exception("error environ: ENV=%s" % env)