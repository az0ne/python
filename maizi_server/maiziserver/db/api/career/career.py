# -*- coding: utf-8 -*-

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor

def list_career_can_use():

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
                select id,
                        name,
                        type,
                        case type
                        when 0 then '线上'
                        else '线下'
                        end as type_name,
                        remark,
                        is_delete
                from mz_server_career
                where is_delete = 0
                """

        try:
            cursor.execute(sql)
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
        }

        return APIResult(result=result_dict)

    return main()

def list_career():

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
                select id,
                        name,
                        type,
                        case type
                        when 0 then '线上'
                        else '线下'
                        end as type_name,
                        remark,
                        is_delete,
                        case is_delete
                        when 0 then '正常'
                        else '禁用'
                        end as state
                from mz_server_career
                """

        try:
            cursor.execute(sql)
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
        }

        return APIResult(result=result_dict)

    return main()

def get_career_by_id(career_id):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                select id,
                        name,
                        type,
                        case type
                        when 0 then '线上'
                        else '线下'
                        end as type_name,
                        remark,
                        is_delete
                from mz_server_career
                where id=%s
                """

        try:
            cursor.execute(sql, (career_id,))
            info = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=info)

    return main()


def start(career_id):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_career
                set is_delete = 0
                where id=%s
                """
        try:
            cursor.execute(sql, (career_id,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()

def stop(career_id):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_career
                set is_delete = 1
                where id=%s
                """

        try:
            cursor.execute(sql, (career_id,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()

def add(name,type,remark):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                insert into mz_server_career(name,
                            type,
                            remark)
                values (%s,%s,%s)
                """

        try:
            cursor.execute(sql, (name, type, remark,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()

def update(career_id,name,type,remark):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_career set
                            name=%s,
                            type=%s,
                            remark=%s
                where id =%s
                """

        try:
            cursor.execute(sql, ( name, type, remark, career_id,))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


# add by zyf on 05/08/2017
# 操作land
def list_land(name,skip):

    sql = """
    select
    id,
    name,
    remark,
    case state
    when 1 then '正常'
    else '异常'
    end as state
    from mz_lps_land
    where name like %s or %s =''
    limit %s,%s
    """

    sql_count = """
    select count(id) from mz_lps_land
    where name like %s or %s=''
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql_count,("%"+name+"%",name))
            rows_count = cursor.fetchone()

            cursor.execute(sql,("%"+name+"%",name,skip['limit'],skip['offset']))
            infos = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e


        result = {
        "info":infos,
        "rows_count":rows_count.values()[0]
        }

        return APIResult(result=result)

    return main()

def land_page(name):
    sql = """select count(id) from mz_lps_land where name like %s or %s=''"""

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute(sql,("%"+name+"%",name))
            result = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=result)

    return main()

def land_add(name,remark,state=0):

    @dec_make_conn_cursor
    def main(conn,cursor):

        sql = """insert into mz_lps_land (name,remark) values(%s,%s)"""

        try:
            cursor.execute(sql,(name,remark))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(code=True)

    return main()

def land_update(id, name, remark, state=0):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """update mz_lps_land set name=%s,remark=%s where id=%s"""

        try:
            cursor.execute(sql,(name,remark,id))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(code=True)

    return main()

def get_land_by_id(land_id):

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """select id,name,remark from mz_lps_land where id=%s"""

        try:
            cursor.execute(sql,land_id)
            result = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()

def set_land_state(land_id,state):
    sql = """update mz_lps_land set state=%s where id =%s"""
    # sql = """update mz_lps_course set state=%s where id = (select course_id from mz_lps_course_land_relation where land_id=%s)"""
    @dec_make_conn_cursor
    def main(conn, cursor):

        try:
            cursor.execute(sql,(state,land_id))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


# 管理专题课程和小课程之间的关系
def get_course_for_land(land_id):

    sql = """
    select course_id from mz_lps_land_course where land_id=%s
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute(sql, land_id)
            result = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)

        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()

def land_course_add(land_id, course_id):
    sql = """
    insert into mz_lps_land_course
    (land_id,course_id)
    values
    (%s,%s)
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql, (land_id, course_id))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()
