# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor


# item添加
def add_item(item_name, course_id, knowledge_id, item_state, sequence, item_type, resource_id):
    _sql = """
        insert into 
        mz_lps_major_item 
        (
        item_name, 
        course_id, 
        knowledge_id,
        item_state,
        sequence,
        item_type,
        resource_id
        ) 

        values 
        (%s,%s,%s,%s,%s,%s,%s)
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        try:
            cursor.execute(_sql, (item_name, course_id, knowledge_id, item_state, sequence, item_type, resource_id))
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor.statement)
            )
            raise e

        return APIResult(result=True)

    return main()


# item查询
def get_item(id):
    _sql = """
        select
        
        item_name, 
        course_id, 
        knowledge_id,
        item_state,
        sequence,
        item_type,
        resource_id
        
        from
        mz_lps_major_item
        
        where
        id=%s
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            cursor.execute(_sql, (id,))
            result = cursor.fetchone()
        except Exception as e:
            print "query get_item error "
            print e
            raise e

        return APIResult(result=result)

    return main()


# item修改
def update_item(id, item_name, course_id, knowledge_id, item_state, sequence, item_type, resource_id):
    _sql = """

            update
            mz_lps_major_item
            set
            item_name = %s, 
            course_id = %s, 
            knowledge_id = %s,
            item_state = %s,
            sequence = %s,
            item_type = %s,
            resource_id = %s

            WHERE id = %s

        """

    @dec_make_conn_cursor
    def main(conn, cursor):

        try:
            cursor.execute(_sql, (item_name, course_id, knowledge_id, item_state, sequence, item_type, resource_id, id))
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor.statement)
            )
            raise e

        return APIResult(result=True)

    return main()


# 获得全部item信息
def get_item_list():
    _sql = """
               select
            
                item_name, 
                course_id, 
                knowledge_id,
                item_state,
                sequence,
                item_type,
                resource_id
                
                from
                mz_lps_major_item
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
