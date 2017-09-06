# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor


# 专业课程与小课程关联表添加
def add_major_course(major_id, course_id):
    print "*********************"
    _sql = """
        insert into 
        mz_lps_course_major_relation 

        (major_id,

        course_id) 

        values 

        (%s,%s)
    """
    @dec_make_conn_cursor
    def main(conn, cursor):

        try:
            cursor.execute(_sql, (major_id, course_id))
            conn.commit()
        except Exception as e:

            raise e

        return APIResult(result=True)

    return main()


# 专业课程与小课程关联表查询
def get_major_course(id):
    _sql = """
            select
            
            major_id,
            course_id
            
            from
            mz_lps_course_major_relation 
            where
            id=%s
        """

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute(_sql, (id,))
            result = cursor.fetchone()
        except Exception as e:
            print e
            raise e

        return APIResult(result=result)

    return main()


# 专业课程与小课程关联表修改
def update_major_course(id, major_id, course_id):
    _sql = """
              update
              mz_lps_course_major_relation 
              set
              major_id = %s,
              course_id = %s

              WHERE 
              id = %s
            """

    @dec_make_conn_cursor
    def main(conn, cursor):

        try:
            cursor.execute(_sql, (major_id, course_id, id))
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor.statement)
            )
            raise e

        return APIResult(result=True)

    return main()


# 获得专业课程与小课程关联表列表
def get_major_course_list():
    _sql = """
                select
                major_id,
                course_id
                from
                mz_lps_course_major_relation 
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
