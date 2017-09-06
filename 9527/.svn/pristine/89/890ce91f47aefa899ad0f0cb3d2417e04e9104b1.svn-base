# -*- coding: utf8 -*-

from db.api.apiutils import APIResult
from db.cores.mysqlconn import dec_make_conn_cursor
from utils import tool
from utils.tool import dec_timeit
from utils.logger import logger as log


@dec_make_conn_cursor
@dec_timeit
def get_record_user_career_data(conn, cursor, page_index=1, page_size=10,
                                mobile=None, career_name=None, nick_name=None,
                                email=None, date_range=None, is_all=False):
    """
    用户个人中心感兴趣职业课程点击记录
    :param conn:
    :param cursor:
    :param page_index: 第几页
    :param page_size: 每页多少条
    :param mobile: 手机号
    :param nick_name:
    :param email:
    :param career_name: 职业课程名
    :param date_range: 日期范围 list或者tuple，[0]为起始日期, [1]为结束日期
    :param is_all: 是否导出所有
    :return: 记录
    """

    start_index = tool.get_page_info(page_index, page_size)

    base_sql = """
        SELECT
            {fields}
        FROM
            mz_record_usercareer AS uc
        INNER JOIN mz_user_userprofile AS u ON u.id = uc.user_id
        INNER JOIN mz_course_careercourse AS career ON career.id = uc.career_id
        WHERE 1=1
    """

    base_wheres = []

    if nick_name:
        base_sql += ' AND u.nick_name LIKE %s '
        nick_name = '%' + nick_name + '%'
        base_wheres.append(nick_name)

    if mobile:
        base_sql += ' AND u.mobile LIKE %s '
        mobile = '%' + str(mobile) + '%'
        base_wheres.append(mobile)

    if email:
        base_sql += ' AND u.email LIKE %s '
        email = '%' + email + '%'
        base_wheres.append(email)

    if career_name:
        base_sql += ' AND career.`name` LIKE %s '
        career_name = '%' + career_name + '%'
        base_wheres.append(career_name)

    if date_range and date_range[0] and date_range[1]:
        base_sql += ' AND create_date BETWEEN %s AND %s '
        base_wheres.extend(date_range)

    sql = base_sql.format(fields='uc.user_id, uc.career_id, uc.create_date, '
                                 'u.nick_name, u.mobile, u.email, '
                                 'career.`name` AS career_name')
    count_sql = base_sql.format(fields='COUNT(uc.id) as count')

    sql += ' ORDER BY create_date DESC '

    # 生成查询list用的where条件(->sql)，base_wheres为count查询用(->count_sql)
    wheres = base_wheres[:]
    if not is_all:
        sql += ' LIMIT %s, %s'
        wheres.extend([start_index, page_size])

    try:
        cursor.execute(sql, wheres)
        result = cursor.fetchall()
        log.info("query: %s" % cursor.statement)

        cursor.execute(count_sql, base_wheres)
        rows_count = cursor.fetchone()["count"]
        log.info("query: %s" % cursor.statement)

        page_count = tool.get_page_count(rows_count, page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(
        result=dict(
            user_career_list=result,
            page=dict(rows_count=rows_count, page_count=page_count,
                      page_size=page_size, page_index=page_index)
        )
    )
