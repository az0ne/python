# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor


# 知识点添加
def add_knowledge(knowledge_name, course_id, sequence, knowledge_state):
    _sql = """
        insert into 
        mz_lps_major_knowledge 
        (
        knowledge_name,
        course_id, 
        sequence,
        knowledge_state
        ) 
        values 
        (%s,%s,%s,%s)
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        try:
            cursor.execute(_sql, (knowledge_name, course_id, sequence, knowledge_state))
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor.statement)
            )
            raise e

        return APIResult(result=True)

    return main()


# 知识点查询
def get_knowledge(id):
    _sql = """
            select
            knowledge_name,
            course_id, 
            sequence,
            knowledge_state
             
            from
            mz_lps_major_knowledge
            
            where
            id=%s
        """

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute(_sql, (id,))
            result = cursor.fetchone()
        except Exception as e:
            print "query knowledge error "
            print e
            raise e

        return APIResult(result=result)

    return main()


# 知识点修改
def update_knowledge(id, knowledge_name, course_id, sequence, knowledge_state):
    _sql = """

                update
                mz_lps_major_knowledge
                set
                knowledge_name = %s,
                course_id = %s,
                sequence = %s,
                knowledge_state = %s

                WHERE id = %s

            """

    @dec_make_conn_cursor
    def main(conn, cursor):

        try:
            cursor.execute(_sql, (knowledge_name, course_id, sequence, knowledge_state, id))
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
def get_knowledge_list():
    _sql = """
          select
          knowledge_name,
          course_id, 
          sequence,
          knowledge_state
          from
          mz_lps_major_knowledge                       
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
