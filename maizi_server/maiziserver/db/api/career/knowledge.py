# -*- coding: utf-8 -*-

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor



def knowledge_list(name,skip):

    sql = """
    select
    a.id,
    a.name,
    a.course_id,
    b.name as course_name,
    a.order_index,
    case a.state
    when 1 then "正常"
    else '不正常'
    end as state
    from mz_lps_knowledge as a
    left join
    mz_lps_course as b
    on a.course_id=b.id
    where a.name like %s or %s =''
    limit %s,%s
    """

    sql_count = """
    select count(id)
    from
    mz_lps_knowledge
    where name like %s or %s=''
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql_count,("%"+name+"%",name))
            rows_count = cursor.fetchone()


            cursor.execute(sql,("%"+name+"%",name,skip['limit'],skip['offset']))
            result = cursor.fetchall()
            log.info('db execute: 1' + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        result_dict = {
        "info":result,
        "rows_count":rows_count.values()[0]
        }

        return APIResult(result=result_dict)

    return main()

def knowledge_page(name):
    sql = """
    select count(id) from mz_lps_knowledge where name like %s or %s =''
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql,("%"+name+"%",name))
            result = cursor.fetchone()
            log.info('db execute: ' + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()

def course_knowledge_add(name,course_id,order_index):
    sql = """insert into mz_lps_knowledge (name,course_id,order_index,state)
    values (%s,%s,%s,0)"""

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql,(name,course_id,order_index))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()

def course_knowledge_update(name,order_index,knowledge_id):
    sql = """
    update mz_lps_knowledge
    set name=%s,
    order_index=%s
    where id=%s"""
    print '3'*100
    print knowledge_id
    print '4'*100

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql, (name,order_index,knowledge_id))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print '1'*100
            print e
            print '2'*100
            raise e

        return APIResult(code=True)

    return main()

def course_knowledge_state_set(knowledge_id,state):
    sql = """
    update mz_lps_knowledge set state=%s where id=%s"""

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql,(state,knowledge_id))
            conn.commit()
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()

def get_knowledge_by_id(knowledge_id):
    sql = """select * from mz_lps_knowledge where id=%s"""

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql,knowledge_id)
            result = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()

def set_knowledge_state(id,state):
    sql = """update mz_lps_knowledge set state=%s where id=%s"""

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql, (state,id))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()

def get_course_knowledge(course_id):
    sql = """
    select
    b.id,
    b.name,
    b.course_id,
    b.order_index,
    case b.state
    when 0 then '异常'
    else '正常'
    end as state,
    a.name as course_name
    from mz_lps_course as a
    left join
    mz_lps_knowledge as b
    on a.id = b.course_id
    where a.id=%s
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql ,course_id)
            result = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()
