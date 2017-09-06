# -*- coding: utf-8 -*-

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor


#操作item
def item_page(name):
    sql = """select count(id) from mz_lps_item where (name like %s or %s = '')"""

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql,("%"+name+"%",name))
            result = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e# coding=utf-8
        return APIResult(result=result)

    return main()

def item_list(name,skip):

    sql = """
    select a.id,
    a.name,
    a.knowledge_id,
    b.name as knowledge_name,
    case a.type
    when 1 then '视频'
    else "作业"
    end as type,
    a.course_id,
    c.name as course_name,
    a.order_index,
    case
    a.state
    when 1 then '正常'
    else '异常'
    end as state
    from mz_lps_item as a
    left join mz_lps_knowledge as b
    on a.knowledge_id = b.id
    left join mz_lps_course as c
    on a.course_id = c.id
    where (a.name like %s or %s ='')
    limit %s,%s
    """

    sql_count = """
    select count(id) from mz_lps_item
    where name like %s or %s=''
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql_count,("%"+name+"%",name))
            rows_count = cursor.fetchone()

            cursor.execute(sql ,("%"+name+"%",name,skip['limit'],skip['offset']))
            result = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        result_dict = {
        "info":result,
        "rows_count":rows_count.values()[0]
        }

        return APIResult(result=result_dict)

    return main()

def item_list_for_course(name,knowledge_id,course_id):
    sql = """
    select a.id,
    a.name,
    a.knowledge_id,
    a.resource_id,
    b.name as knowledge_name,
    case a.type
    when 1 then '视频'
    else "作业"
    end as type,
    a.course_id,
    c.name as course_name,
    a.order_index,
    case
    a.state
    when 1 then '正常'
    else '异常'
    end as state
    from mz_lps_item as a
    left join mz_lps_knowledge as b
    on a.knowledge_id = b.id
    left join mz_lps_course as c
    on a.course_id = c.id
    where (a.name like %s or %s ='')
    and (a.knowledge_id=%s)
    and (a.course_id=%s)
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql ,("%"+name+"%",name,knowledge_id,course_id))
            result = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()

def get_item_by_knowledge_id(item_id,knowledge_id,course_id):
    sql = """
    select a.id,
    a.name,
    a.knowledge_id,
    case a.type
    when 1 then '视频'
    else "作业"
    end as type,
    b.name as knowledge_name,
    a.course_id,
    c.name as course_name,
    a.order_index,
    case
    a.state
    when 1 then '正常'
    else '异常'
    end as state
    from mz_lps_item as a
    left join mz_lps_knowledge as b
    on a.knowledge_id = b.id
    left join mz_lps_course as c
    on a.course_id = c.id
    where (a.knowledge_id=%s)
    and (a.course_id=%s)
    and (a.id=%s)
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql,(knowledge_id,course_id,item_id))
            result = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()

def update_item(name,order_index,item_id,knowledge_id,course_id):
    sql = """
    update
    mz_lps_item
    set
    name=%s,
    order_index=%s,
    knowledge_id=%s,
    course_id=%s
    where
    (id=%s)
    and (knowledge_id=%s)
    and (course_id=%s)
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql,(name,order_index,knowledge_id,course_id,item_id,knowledge_id,course_id))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()

def add_item(name,item_type,order_index,knowledge_id,course_id,state=0):
    sql = """
    insert
    into mz_lps_item
    (name,
    type,
    order_index,
    knowledge_id,
    course_id,
    state)
    values
    (%s,%s,%s,%s,%s,%s)
    """

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql, (name,item_type,order_index,knowledge_id,course_id,state))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()

def set_item_state(course_id,knowledge_id,item_id,state):
    sql = """
    update
    mz_lps_item
    set
    state=%s
    where
    course_id=%s
    and
    knowledge_id=%s
    and
    id=%s"""

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql, (state,course_id,knowledge_id,item_id))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        return APIResult(code=True)

    return main()

def item_page(name):
    sql = """select count(id) from mz_lps_item where (name like %s or %s = '')"""

    @dec_make_conn_cursor
    def main(conn,cursor):
        try:
            cursor.execute(sql,("%"+name+"%",name))
            result = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e# coding=utf-8
        return APIResult(result=result)

    return main()
