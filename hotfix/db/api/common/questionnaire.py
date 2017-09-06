# -*- coding: utf-8 -*-
import json
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor


def get_short_name_questionnaire_id(short_name):
    """
    根据问卷id取问卷数据
    :param questionnaire_id:
    :return:
    """
    @dec_timeit('get_short_name_questionnaire_id')
    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            sql = """
            SELECT
                id
            FROM
                mz_free_questionnaire
            WHERE short_name = %s;
            """
            cursor.execute(sql, (short_name,))
            questionnaire_id = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=questionnaire_id)

    return main()


def get_questionnaire_id_questionnaire_item(questionnaire_id):
    """
    根据问卷id取问卷数据
    :param questionnaire_id:
    :return:
    """
    try:
        int(questionnaire_id)
    except:
        log.warn("questionnaire_id is not a int")
        return APIResult(code=False)
    redis_key = 'get_shortname_questionnaire_%s' % questionnaire_id

    @dec_timeit('get_questionnaire_id_questionnaire_item')
    @dec_get_cache(redis_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            sql = """
            SELECT
                qi.id,
                qi.stem,
                qi.ques_options,
                qi.ques_index
            FROM
                mz_free_questionnaire_item AS qi
            WHERE qi.questionnaire_id = %s;
            """
            cursor.execute(sql, (questionnaire_id,))
            questionnaire = cursor.fetchall()
            for row in questionnaire:
                row['ques_options'] = sorted(json.loads(row['ques_options']).iteritems(), key=lambda x: x[0])

            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        # set cache
        cache.set(redis_key, questionnaire, 60 * 5)

        return APIResult(result=questionnaire)

    return main(_enable_cache=True)


def submit_questionnaire(qr_list):
    """
    提交问卷
    :param qr_list:
    :return:
    """
    if not isinstance(qr_list, list):
        log.warn("qr_list is not a list")
        return APIResult(code=False)

    _qr_list = list()
    in_p_list = list()
    for qr in qr_list:
        in_p = '(' + ', '.join(map(lambda x: '%s', qr)) + ')'
        _qr_list += qr
        in_p_list.append(in_p)

    in_p_list = ', '.join(in_p_list)

    @dec_timeit('submit_questionnaire')
    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            sql = """
            REPLACE INTO mz_free_questionnaire_record (
                student_id,
                class_id,
                questionnaire_id,
                questionnaire_item_id,
                record
            )
            VALUES
                %s;
            """
            sql = sql % in_p_list
            cursor.execute(sql, tuple(_qr_list))
            conn.commit()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(code=True)

    return main()


def get_student_questionnaire_is_done(class_id, student_id, questionnaire_id=1):
    """
    判定学生是否做过该问卷
    :param class_id:
    :param student_id:
    :param questionnaire_id:
    :return:
    """
    try:
        class_id = int(class_id)
        student_id = int(student_id)
        questionnaire_id = int(questionnaire_id)
    except:
        log.warn("class_id/student_id/questionnaire_id is not a int")
        return APIResult(code=False)

    @dec_timeit('get_student_questionnaire_is_done')
    @dec_make_conn_cursor
    def main(conn, cursor):
        try:
            sql = """
            SELECT
                1
            FROM
                mz_free_questionnaire_record
            WHERE
                class_id = %s
            AND student_id = %s
            AND questionnaire_id = %s;
            """
            cursor.execute(sql, (class_id, student_id, questionnaire_id))
            qrecord = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement: %s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=qrecord)

    return main()
