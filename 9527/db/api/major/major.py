# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor


# 专业课程添加
def add_major(major_name, major_state, major_price):
    _sql = """
        insert into 
        mz_lps_major_major 
        
        (major_name,
        
        major_state,
        
        major_price) 
        
        values 
        
        (%s,%s,%s)
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        try:
            cursor.execute(_sql, (major_name, major_state, major_price))
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
def get_major(id):
    _sql = """
            select
            major_name,
            major_price,
            major_state
            from
            mz_lps_major_major
            where
            id=%s
        """

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute(_sql, (id,))
            result = cursor.fetchone()
        except Exception as e:
            print "query major error "
            print e
            raise e

        return APIResult(result=result)

    return main()


# 专业课程修改
def update_major(id, major_name, major_state, major_price):
    _sql = """
            update
            mz_lps_major_major
            set
            major_name = %s,
            major_state = %s,
            major_price = %s
            
            WHERE 
            id = %s
            """

    @dec_make_conn_cursor

    def main(conn, cursor):

        try:
            cursor.execute(_sql, (major_name, major_state, major_price, id))
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor.statement)
            )
            raise e

        return APIResult(result=True)

    return main()  # 获得全部专业课程信息

def get_major_list():
    _sql = """
              select
              major_name,
              major_price,
              major_state
              from
              mz_lps_major_major
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
