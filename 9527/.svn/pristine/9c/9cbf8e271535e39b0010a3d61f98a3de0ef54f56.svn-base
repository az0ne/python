# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor


# 小课程添加
def add_course(course_name, author_id, sequence, course_state):
    _sql = """
        insert into 
        mz_lps_major_course
        (course_name,
        author_id,
        sequence,
        course_state) 
        values 
        (%s,%s,%s,%s)
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        try:
            cursor.execute(_sql, (course_name, author_id, sequence, course_state))
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor.statement)
            )
            raise e

        return APIResult(result=True)

    return main()


# 专业课程查询
def get_course(course_id):
    _sql = """
            select
            course_name,
            author_id,
            sequence,
            course_state
            from
            mz_lps_major_course
            where
            id=%s
        """

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute(_sql, (course_id,))
            result = cursor.fetchone()
        except Exception as e:
            print "query course_name error "
            print e
            raise e

        return APIResult(result=result)

    return main()


# 专业课程修改
def update_course(id, course_name, author_id, sequence, course_state):
    _sql = """

            update
            mz_lps_major_course
            set
            course_name = %s,
            author_id = %s,
            sequence = %s,
            course_state = %s

            WHERE id = %s

        """

    @dec_make_conn_cursor
    def main(conn, cursor):

        try:
            cursor.execute(
                _sql,
                (course_name, author_id, sequence, course_state, id))
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor.statement)
            )
            raise e

        return APIResult(result=True)

    return main()


# 获得全部course信息
def get_course_list():
    _sql = """
            select
            course_name,
            author_id,
            sequence,
            course_state
            from
            mz_lps_major_course
            """

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute(_sql)
            result = cursor.fetchall()
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()
