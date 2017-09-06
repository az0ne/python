# -*- coding: utf-8 -*-

import time
from contextlib import closing
import MySQLdb
import MySQLdb.cursors
import sqlalchemy.pool as pool
from django.conf import settings


def mysql_pool(
        max_overflow,
        pool_name, pool_size, dbname, dbuser,
        dbpassword, dbhost, dbport, charset="utf8"):
    def getconn():
        return MySQLdb.connect(
            host=dbhost,
            port=dbport,
            user=dbuser,
            passwd=dbpassword,
            db=dbname,
            charset=charset,
            cursorclass=MySQLdb.cursors.DictCursor,
        )

    return pool.QueuePool(
        getconn,
        max_overflow=max_overflow,
        pool_size=pool_size)


DB_POOL = None


def make_db_pool():
    global DB_POOL

    DB_POOL = mysql_pool(
        max_overflow=settings.MYSQL_POOL_OVERFLOW,
        pool_name=settings.MYSQL_POOL_NAME,
        pool_size=settings.MYSQL_POOL_SIZE,
        dbname=settings.MYSQL_DB,
        dbuser=settings.MYSQL_USER,
        dbpassword=settings.MYSQL_PASSWORD,
        dbhost=settings.MYSQL_HOST,
        dbport=settings.MYSQL_PORT)


def get_conn():
    return DB_POOL.connect()


try:
    from uwsgidecorators import postfork
except ImportError:
    make_db_pool()
else:
    make_db_pool = postfork(make_db_pool)
