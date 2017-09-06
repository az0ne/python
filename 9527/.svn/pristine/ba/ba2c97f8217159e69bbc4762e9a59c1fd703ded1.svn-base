# -*- coding: utf-8 -*-

from pymongo.mongo_client import MongoClient
from django.conf import settings
from utils.logger import logger as log


MONGO = None

def make_mongo():
    global MONGO
    try:
        MONGO = MongoClient(
            settings.MONGO_HOST,
            settings.MONGO_PORT)
    except Exception as e:
        log.error("mongodb connect failed. details: %s" % e)
    
try:
    from uwsgidecorators import postfork
except ImportError:
    make_mongo()
else:
    make_mongo = postfork(make_mongo)

def get_mongo_db(db_name):
    if not MONGO:
        make_mongo()
    return getattr(MONGO, db_name)
