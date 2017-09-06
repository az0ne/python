# -*- coding: utf-8 -*-
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor
import datetime

@dec_make_conn_cursor
def insert_feedback_info(conn, cursor, dict_info):

    sql = """
            insert into mz_common_newfeedback (content,feed_type,publish_date,contact,image_url,user_id,nick_name,current_url)
            values(%s,%s,%s,%s,%s,%s,%s,%s)
          """
    insert_list = list()
    insert_list.append(dict_info.get("content", "Null"))
    insert_list.append(dict_info.get("feed_type", "Null"))
    insert_list.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    insert_list.append(dict_info.get("contact", "Null"))
    insert_list.append(dict_info.get("image_url", "Null"))
    insert_list.append(dict_info.get("user_id", "Null"))
    insert_list.append(dict_info.get("nick_name", "Null"))
    insert_list.append(dict_info.get("current_url", "Null"))

    try:
        cursor.execute(sql, insert_list)
        conn.commit()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e
    return APIResult(code=True)
