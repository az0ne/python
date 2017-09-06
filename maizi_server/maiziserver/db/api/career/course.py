# -*- coding: utf-8 -*-

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor


#操作course
def course_list(name,skip):
    # _sql = """select
    # id,
    # name,
    # order_index,
    # case state
    # when 1
    # then '正常'
    # else '异常'
    # end as state
    # from mz_lps_course
    # where name like %s or %s=''
    # order by
    # order_index
    # limit %s,%s"""

    sql = """
    select
    a.id,
    a.name,
    d.name as author_name,
    b.name as career_name,
    b.id as career_id,
    a.order_index,
    case a.state
    when 1
    then '正常'
    else '异常'
    end as state
    from mz_lps_course as a
    left join
    mz_lps_career_course_relation as c
    on a.id = c.course_id
    left join mz_server_career as b
    on b.id = c.career_id
    left join mz_lps_author as d
    on a.teacher_id = d.id
    where a.name like %s or %s=''
    order by a.order_index
    limit %s,%s
    """

    sql_count = """
    select count(id) from mz_lps_course
    where name like %s or %s=''
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql_count,("%"+name+"%", name))
            rows_count = cursor.fetchone()

            cursor.execute(sql,("%"+name+"%",name,skip['limit'],skip['offset']))
            result = cursor.fetchall()

            # result={}
            # rows_count={"a":10}

            log.info('db execute: ' + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        result_dict = {
        "info":result,
        "rows_count":rows_count.values()[0]
        }

        return APIResult(result_dict)

    return main()

def get_course_by_id(course_id):
    sql = """select id,name,order_index,state,teacher_id
    from mz_lps_course where id=%s"""

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql,(course_id,))
            result = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=result)

    return main()

def update_course(course_id,name,order_index,teacher_id):

    sql = """update mz_lps_course set name=%s,order_index=%s,
    teacher_id=%s
    where id=%s"""

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql, (name, order_index, teacher_id, course_id))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(code=True)

    return main()

def set_course_state(course_id, state):
    sql = """update mz_lps_course set state=%s where id=%s"""

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql, (state,course_id))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(code=True)

    return main()

def course_add(name,order_index,land_id,courseAuthor,state=0):
    sql = """insert into mz_lps_course (name,order_index,state,teacher_id)
    values (%s,%s,%s,%s)"""
    sql_last_id = """select last_insert_id()"""
    sql_relation = """insert into
    mz_lps_career_course_relation (course_id,career_id)
     values (%s,%s)"""
    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql, (name,order_index,state,courseAuthor))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
            if int(land_id) != -1:
                cursor.execute(sql_last_id)
                last_id = cursor.fetchone().values()[0]
                print "*"*110
                print land_id
                print "*"*110
                cursor.execute(sql_relation,(last_id,land_id))
                conn.commit()
                log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()

def course_page(name):
    sql = """select count(id) from mz_lps_course where name like %s or %s =''"""

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql,("%"+name+"%",name))
            result = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()

def list_land_for_course():
    sql = """
    select
    id,
    name
    from mz_server_career
    """
    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()
