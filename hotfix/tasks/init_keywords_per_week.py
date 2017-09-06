# -*- coding: utf-8 -*-
"""
每一周生成一次keyword, 用Crontab执行
"""
import djevn

djevn.load()

import datetime
from utils.logger import logger as log
from mz_lps3.functions_nj import exec_sql


def init_keywords():
    try:
        log.info('begin init_keywords at %s' % datetime.datetime.now())
        sql = """
            DELETE FROM mz_common_objtagindex;

            INSERT mz_common_objtagindex (obj_type, obj_id, keywords) SELECT DISTINCT
                otr.obj_type,
                otr.obj_id,
                CONCAT(
                    REPLACE (c. NAME, ' ', ''),
                    ',',
                    GROUP_CONCAT(DISTINCT(t. NAME)),
                    ',',
                    GROUP_CONCAT(DISTINCT(ncc. NAME))
                )
            FROM
                mz_common_objtagrelation AS otr
            RIGHT JOIN mz_course_tag AS t ON t.id = otr.tag_id
            RIGHT JOIN mz_course_newcareercatagory AS ncc ON ncc.id = otr.careercatagory_id
            RIGHT JOIN mz_course_course AS c ON c.id = otr.obj_id
            WHERE
                obj_type = 'COURSE'
            AND is_active = '1'
            GROUP BY
                otr.obj_id;
        """

        exec_sql(sql)
        log.info('completed init_keywords at %s' % datetime.datetime.now())

    except Exception as e:
        log.warn('execute exception: %s. ' % e)
        raise e


if __name__ == '__main__':
    pass
    init_keywords()
