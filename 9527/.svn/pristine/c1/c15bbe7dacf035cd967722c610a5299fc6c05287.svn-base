# -*- coding: utf-8 -*-

import time
from contextlib import closing
from mysql.connector import pooling
from django.conf import settings
from utils.logger import logger as log
from db.api.apiutils import APIResult

UWSGI = True
try:
    from uwsgidecorators import postfork
except ImportError:
    UWSGI = False


def mysql_pool(pool_name, pool_size, dbname, dbuser, dbpassword, dbhost, dbport):
    return pooling.MySQLConnectionPool(
        pool_name=pool_name,
        pool_size=pool_size,
        database=dbname,
        user=dbuser,
        password=dbpassword,
        host=dbhost)

DB_POOL = None


def make_db_pool():
    global DB_POOL
    
    DB_POOL = mysql_pool(
        pool_name=settings.MYSQL_POOL_NAME,
        pool_size=settings.MYSQL_POOL_SIZE,
        dbname=settings.MYSQL_DB,
        dbuser=settings.MYSQL_USER,
        dbpassword=settings.MYSQL_PASSWORD,
        dbhost=settings.MYSQL_HOST,
        dbport=settings.MYSQL_PORT)

make_db_pool()


def get_conn():
    start = time.time()
    
    while True:
        if time.time() - start > settings.MYSQL_POOL_WAIT_SECONDS:
            return None
        else:
            try:
                conn = DB_POOL.get_connection()
            except Exception as e:
                continue
            else:
                if conn:
                    return conn
                else:
                    continue


def dec_make_conn_cursor(func, *args, **kwargs):
    def _func(*args, **kwargs):
        # make connection and cursor
        _conn = get_conn()
        if not _conn:
            log.warn(
                "get database connection timeout.")
            return APIResult(code=False)

        with closing(_conn) as conn:
            cursor = conn.cursor(dictionary=True)
            if not (conn and cursor):
                log.warn(
                    "cursor is none.")
                return APIResult(code=False)
            else:
                try:
                    res = func(conn, cursor, *args, **kwargs)
                except Exception as e:
                    print e
                    return APIResult(code=False)
                else:
                    return res
    return _func
