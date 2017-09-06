# -*- coding: utf-8 -*-

import os


env = os.environ.get("ENV", "local")

if env == "prod":
    from maiziserver.settings.prod import *
elif env == "staging":
    from maiziserver.settings.staging import *
elif env == "local":
    from maiziserver.settings.local import *
else:
    raise Exception("error environ: ENV=%s" % env)
