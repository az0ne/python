# -*- coding: utf-8 -*-
"""
@time: 2016/9/16 0006 14:57
@note:  1v1直播
"""

import datetime
from django.http.response import Http404

from db.api.apiutils import dec_make_conn_cursor, APIResult
from utils.logger import logger
from mz_lps4.common import create_onevone_live_room


def check_meeting_time(teacher_id, start_time, end_time):
    """
    检查直播时间是否合法
    :param teacher_id:
    :param start_time:
    :param end_time:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select
            1
        from mz_onevone_meeting
        where teacher_id =%s and (%s between start_time and end_time AND %s != end_time
            or %s between start_time and end_time AND %s != start_time)
            AND status != 'CANCEL';
        """
        try:
            cursor.execute(sql, (teacher_id, start_time, start_time, end_time, end_time))
            result = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def create_onevone_meeting(career_id, user_id, teacher_id, teacher_name, start_time, end_time, question):
    """
    学生添加新的1v1直播
    :param career_id:
    :param user_id:
    :param teacher_id:
    :param teacher_name:
    :param start_time:
    :param end_time:
    :param question:
    :return:
    """

    try:
        flags, data = create_onevone_live_room(teacher_name)
    except Exception, e:
        logger.warn('create_onevone_metting fail teacher_id:%s except%s' % (teacher_id, str(e)))
        return APIResult(result=False)

    if not flags:
        return APIResult(result=False)

    onevone_meeting = (
        career_id,
        user_id,
        teacher_id,
        start_time,
        end_time,
        question,
        data['teacher_join_url'],
        data['student_join_url'],
        data['teacher_token'],
        data['assistant_token'],
        data['student_client_token'],
        data['student_token'],
        data['live_code'],
        data['live_id'],
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'CREATE'
    )

    @dec_make_conn_cursor
    def main(conn, cursor):
        # user_count是否超过最大次数
        sql_over_max_count = """
SELECT 1
FROM mz_onevone_meeting_user_count
WHERE career_id = %s AND user_id = %s AND count >= max_count FOR UPDATE;
        """

        # 插入或更新user_count
        sql_count_insert = """
INSERT INTO mz_onevone_meeting_user_count (career_id, user_id, count, max_count)
VALUES (%s, %s, 1, (SELECT count
                        FROM mz_onevone_meeting_count
                        WHERE career_id = %s))
ON DUPLICATE KEY UPDATE count = count + 1;
        """

        # 插入回复数据
        sql_insert = """
INSERT INTO mz_onevone_meeting(
    career_id,
    user_id,
    teacher_id,
    start_time,
    end_time,
    question,
    teacher_url,
    student_url,
    teacher_token,
    assistant_token,
    student_client_token,
    student_web_token,
    live_code,
    live_id,
    create_date_time,
    status
)VALUES (%s)
        """ % (','.join(map(lambda x: '%s', onevone_meeting)))

        try:
            # 判断次数
            cursor.execute(sql_over_max_count, (career_id, user_id))
            logger.info("query:%s" % cursor._last_executed)
            is_not_over_max_count = cursor.fetchone()

            if not is_not_over_max_count:
                # 如果次数符合要求，执行insert语句
                cursor.execute(sql_count_insert, (career_id, user_id, career_id))
                logger.info("query:%s" % cursor._last_executed)

                cursor.execute(sql_insert, onevone_meeting)
                logger.info("query:%s" % cursor._last_executed)

                cursor.execute('SELECT LAST_INSERT_ID();')
                logger.info("query:%s" % cursor._last_executed)
                result = cursor.fetchone()

                conn.commit()
            else:
                return APIResult(code=False, result=u'你已经超过预约次数')
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def is_ordered_onevone_meeting(meeting_id):
    """
    1v1直播是否已经被预约
    :param meeting_id:
    :return:
    """
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select
            1
        from mz_onevone_meeting
        where id=%s and user_id is not null
        limit 1
        """
        try:
            cursor.execute(sql, (meeting_id,))
            result = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def order_onevone_meeting(meeting_id, career_id, user_id, mobile, content):
    """
    预约1v1直播
    :param meeting_id:
    :param career_id:
    :param user_id:
    :param mobile:
    :return:
    """
    create_date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql_exist = """
        select 1 from
        mz_onevone_meeting_user_count
        where career_id =%s and user_id=%s and count<max_count
        limit 1
        """

        sql_up = """
        update mz_onevone_meeting_user_count set count=count+1 where career_id =%s and user_id=%s
        """
        sql = """
        update mz_onevone_meeting
        set user_id=%s, career_id=%s, create_date_time=%s, phone=%s, status=%s, question=%s
        where id=%s AND user_id is Null
        """

        sql_count = """select row_count() as row_count"""

        try:
            cursor.execute(sql_exist, (career_id, user_id))
            is_exist = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
            if is_exist:
                cursor.execute(sql, (user_id, career_id, create_date_time, mobile, 'DATED', content, meeting_id))
                logger.info("query:%s" % cursor._last_executed)
                cursor.execute(sql_count)
                logger.info("query:%s" % cursor._last_executed)
                row_count = cursor.fetchone()['row_count']
                if row_count == 1:
                    cursor.execute(sql_up, (career_id, user_id))
                    logger.info("query:%s" % cursor._last_executed)
                conn.commit()
            else:
                return APIResult(result=False)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        if row_count == 1:
            return APIResult(result=True)
        else:
            return APIResult(result=False)
    return main()


def add_onevone_meeting(meeting_id, user_id, small_image_path, image_path, question):
    """
    添加1v1直播，提问内容
    :param meeting_id:
    :param user_id:
    :param small_image_path:
    :param image_path:
    :param question:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        if small_image_path and image_path:
            onevone_meeting = (
                small_image_path,
                image_path,
                question,
                meeting_id,
                user_id
            )
            sql = """
            update mz_onevone_meeting
            set small_image_path=%s, image_path=%s, question=%s
            where id=%s and user_id=%s
            """
        else:
            onevone_meeting = (
                question,
                meeting_id,
                user_id
            )
            sql = """
            update mz_onevone_meeting
            set question=%s
            where id=%s and user_id=%s
            """
        sql_count = """select row_count() as row_count"""

        try:
            cursor.execute(sql, onevone_meeting)
            logger.info("query:%s" % cursor._last_executed)
            cursor.execute(sql_count)
            logger.info("query:%s" % cursor._last_executed)
            row_count = cursor.fetchone()['row_count']
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        if row_count == 1:
            return APIResult(result=True)
        else:
            return APIResult(result=False)
    return main()


def get_onevone_meeting_count_by_teacher_id(teacher_id, is_current=True):
    """
    老师端查看1v1直播总数
    :param teacher_id:
    :param is_current: 是否当前未结束的直播
    :return:
    """
    if is_current:
        str_status = """('START', 'CREATE', 'DATED');"""
    else:
        str_status = """('ENDED', 'CANCEL');"""

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT count(m.id) AS count
FROM mz_onevone_meeting AS m
  LEFT JOIN mz_lps4_teacher_warning_backlog AS twb
    ON (twb.type = 5 AND twb.obj_id = m.id)
WHERE m.teacher_id = %s AND m.user_id IS NOT NULL AND m.status IN """ + str_status

        try:
            cursor.execute(sql, (teacher_id,))
            count = cursor.fetchone()['count']
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=count)

    return main()


def show_onevone_meeting_list_by_teacher_id(teacher_id, page_index, page_size, is_current=True):
    """
    老师端查看1v1直播列表
    :param teacher_id:
    :param page_index:
    :param page_size:
    :param is_current: 是否是当前未结束的直播
    :return:
    """
    start_index = (page_index - 1) * page_size  # 开始条数
    if is_current:
        sql1 = """('START', 'CREATE', 'DATED')"""
        sql2 = """m.start_time"""
    else:
        sql1 = """('ENDED', 'CANCEL')"""
        sql2 = """-m.start_time"""

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT
  if(u.real_name = '' OR u.real_name IS NULL, u.nick_name, u.real_name) AS user_name,
  u.avatar_small_thumbnall AS user_head,
  m.*,
  teacher.nick_name              AS teacher_nick_name,
  teacher.real_name              AS teacher_real_name
FROM mz_onevone_meeting AS m
  LEFT JOIN mz_lps4_teacher_warning_backlog AS twb
    ON (twb.type = 5 AND twb.obj_id = m.id)
  LEFT JOIN mz_user_userprofile AS teacher ON m.teacher_id = teacher.id
  LEFT JOIN mz_user_userprofile AS u ON m.user_id = u.id
WHERE m.teacher_id = %s AND m.user_id IS NOT NULL AND m.status IN {0}
ORDER BY {1}
LIMIT %s, %s;
        """.format(sql1, sql2)

        try:
            cursor.execute(sql, (teacher_id, start_index, page_size))
            onevone_meeting_list = cursor.fetchall()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=onevone_meeting_list)

    return main()


def show_onevone_meeting_list_by_user_id(user_id, career_id):
    """
    学生端查看往期1v1直播列表
    :param user_id:
    :param career_id:
    :return:
    """
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select
            meeting.id,
            meeting.start_time,
            meeting.end_time,
            meeting.question,
            meeting.small_image_path,
            meeting.image_path,
            meeting.teacher_id,
            teacher.nick_name,
            teacher.real_name,
            teacher.avatar_small_thumbnall
        from mz_onevone_meeting as meeting
        inner join mz_user_userprofile as teacher on meeting.teacher_id=teacher.id
        where user_id=%s and career_id=%s and status = 'ENDED'
        order by meeting.start_time
        """

        try:
            cursor.execute(sql, (user_id, career_id))
            onevone_meeting_list = cursor.fetchall()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=onevone_meeting_list)

    return main()


def get_onevone_meeting_by_id(meeting_id):
    """
    根据ID获取1v1直播详情
    :param meeting_id:
    :return:
    """
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select
            meeting.*,
            user.nick_name as user_nick_name,
            user.real_name as user_real_name,
            user.avatar_small_thumbnall as user_head,
            teacher.nick_name as teacher_nick_name,
            teacher.real_name as teacher_real_name,
            teacher.avatar_middle_thumbnall as teacher_head
        from mz_onevone_meeting as meeting
        left join mz_user_userprofile as user on meeting.user_id=user.id
        left join mz_user_userprofile as teacher on meeting.teacher_id=teacher.id
        where meeting.id=%s
        """

        try:
            cursor.execute(sql, (meeting_id,))
            onevone_meeting = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=onevone_meeting)

    return main()


def get_latest_onevone_meeting(teacher_id, now_after_3):
    """
    查询最近的为预约的1v1直播
    :param teacher_id:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select
            meeting.*,
            teacher.id,
            teacher.nick_name as teacher_nick_name,
            teacher.real_name as teacher_real_name,
            teacher.avatar_middle_thumbnall as teacher_head
        from mz_onevone_meeting as meeting
        inner join mz_user_userprofile as teacher on meeting.teacher_id=teacher.id
        where teacher_id=%s and status='CREATE' AND meeting.start_time > %s
        order by meeting.start_time
        limit 1
        """

        try:
            cursor.execute(sql, (teacher_id, now_after_3))
            onevone_meeting = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=onevone_meeting)

    return main()


def get_recent_onevone_meeting(teacher_id, is_all, date_time, index_start, index_end):
    """
    查询最近的未预约 未预约和他人已预约 的1v1直播
    :param teacher_id:
    :param date_time:
    :param is_all: 是否查询
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select
            meeting.*,
            teacher.id,
            teacher.nick_name as teacher_nick_name,
            teacher.real_name as teacher_real_name,
            teacher.avatar_middle_thumbnall as teacher_head
        from mz_onevone_meeting as meeting
        inner join mz_user_userprofile as teacher on meeting.teacher_id=teacher.id
        where teacher_id=%s and status='CREATE' AND meeting.start_time > %s
        order by meeting.start_time
        limit 3
        """

        sql1 = """
        select
            meeting.*,
            teacher.id,
            teacher.nick_name as teacher_nick_name,
            teacher.real_name as teacher_real_name,
            teacher.avatar_middle_thumbnall as teacher_head
        from mz_onevone_meeting as meeting
        inner join mz_user_userprofile as teacher on meeting.teacher_id=teacher.id
        where teacher_id=%s and status in ('CREATE','DATED')  AND meeting.start_time > %s
        order by meeting.start_time
        limit %s, %s
        """

        try:
            if is_all:
                cursor.execute(sql1, (teacher_id, date_time, index_start, index_end))
            else:
                cursor.execute(sql, (teacher_id, date_time))
            onevone_meeting = cursor.fetchall()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=onevone_meeting)

    return main()


def get_ordered_onevone_meeting(career_id, user_id):
    """
    查询最近的已经预约未结束的1v1直播
    :param career_id:
    :param user_id:
    :return:
    """
    try:
        career_id = int(career_id)
        user_id = int(user_id)
    except Exception as e:
        logger.warn(str(e))
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select
            meeting.*,
            teacher.id,
            teacher.nick_name as teacher_nick_name,
            teacher.real_name as teacher_real_name,
            teacher.avatar_small_thumbnall as teacher_head
        from mz_onevone_meeting as meeting
        inner join mz_user_userprofile as teacher on meeting.teacher_id=teacher.id
        where career_id=%s and user_id =%s and status in ('START','DATED')
        order by meeting.start_time
        limit 1
        """

        try:
            cursor.execute(sql, (career_id, user_id))
            onevone_meeting = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=onevone_meeting)

    return main()


def app_get_ordered_onevone_meeting(career_id, user_id, is_old=False):
    """
    学生端查询最近的已经预约未结束的1v1直播
    :param career_id:
    :param user_id:
    :param is_old:
    :return:
    """
    try:
        career_id = int(career_id)
        user_id = int(user_id)
    except Exception as e:
        logger.warn(str(e))
        return APIResult(code=False)

    if not is_old:
        sql1 = """('START', 'CREATE', 'DATED')"""
        sql2 = """m.start_time"""
    else:
        sql1 = """('ENDED', 'CANCEL')"""
        sql2 = """-m.start_time"""

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT
  if(u.real_name = '' OR u.real_name IS NULL, u.nick_name, u.real_name) AS user_name,
  m.*,
  teacher.nick_name                                                     AS teacher_nick_name,
  teacher.real_name                                                     AS teacher_real_name,
  teacher.avatar_small_thumbnall                                        AS teacher_head
FROM mz_onevone_meeting AS m
  LEFT JOIN mz_lps4_teacher_warning_backlog AS twb
    ON (twb.type = 5 AND twb.obj_id = m.id)
  LEFT JOIN mz_user_userprofile AS teacher ON m.teacher_id = teacher.id
  LEFT JOIN mz_user_userprofile AS u ON m.user_id = u.id
WHERE m.career_id = %s AND m.user_id = %s AND m.status IN {0}
ORDER BY {1};
        """.format(sql1, sql2)

        try:
            cursor.execute(sql, (career_id, user_id))
            onevone_meeting = cursor.fetchall()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=onevone_meeting)

    return main()


def is_ended_onevone_meeting(career_id, user_id):
    """
    是否有已经结束的直播
    :param career_id:
    :param user_id:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select 1 from mz_onevone_meeting where career_id=%s and user_id=%s and status='ENDED' limit 1
        """

        try:
            cursor.execute(sql, (career_id, user_id))
            result = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def save_video_record(live_id, video_url, video_token):
    """
    保存录播视频记录
    :param live_id:
    :param video_url:
    :param video_token:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        update
            mz_onevone_meeting
        set video_url=%s, video_token=%s
        where live_id=%s and video_url is null
        """

        try:
            cursor.execute(sql, (video_url, video_token, live_id))
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=True)
    return main()


def get_not_ended_onevone_meeting():
    """
    查询所有的未结束的1v1直播
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select
            meeting.*,
            teacher.nick_name,
            teacher.real_name
        from mz_onevone_meeting as meeting
        left join mz_user_userprofile as teacher on meeting.teacher_id=teacher.id
        where status not in ('ENDED', 'CANCEL');
        """
        try:
            cursor.execute(sql)
            not_ended_meeting_list = cursor.fetchall()
            logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=not_ended_meeting_list)

    return main()


def update_onevone_meeting(meeting_id, status):
    """
    更改1v1直播状态
    :param meeting_id: 主键
    :param status: 状态（str）
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        update
            mz_onevone_meeting
        set status=%s
        where id=%s
        """

        try:
            cursor.execute(sql, (status, meeting_id))
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=True)
    return main()


def update_onevone_meeting_is_sendsms(meeting_id):
    """
    更改1v1直播为已发送短信状态
    :param meeting_id: 主键
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        update
            mz_onevone_meeting
        set is_sendsms_start30=1
        where id=%s
        """

        try:
            cursor.execute(sql, (meeting_id,))
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=True)
    return main()


def get_onevone_meeting_user_count(user_id, career_id):
    """
    查询用户可预约的1v1直播的次数,没有的话就插入
    :param user_id:
    :param career_id:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql_insert = """
INSERT INTO mz_onevone_meeting_user_count (career_id, user_id, count, max_count)
VALUES (%s, %s, 0, (SELECT count
                    FROM mz_onevone_meeting_count
                    WHERE career_id = %s))
ON DUPLICATE KEY UPDATE count = count;
        """

        sql_select = """
SELECT
  count,
  max_count
FROM mz_onevone_meeting_user_count
WHERE career_id = %s AND user_id = %s
LIMIT 1;
        """

        try:
            cursor.execute(sql_insert, (career_id, user_id, career_id))
            logger.info("query:%s" % cursor._last_executed)
            cursor.execute(sql_select, (career_id, user_id))
            user_count = cursor.fetchone()
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
            residue_count = user_count.get('max_count', 0)-user_count.get('count', 0)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=residue_count)

    return main()


# 20161024 1v1直播迭代
def get_onevone_meeting_by_teacher_id(teacher_id, begin_date, end_date):
    """
    查询老师相关直播班会
    :param teacher_id:
    :param begin_date:
    :param end_date:
    :return:
    """
    try:
        teacher_id = int(teacher_id)
        assert isinstance(begin_date, datetime.datetime)
        assert isinstance(end_date, datetime.datetime)
    except AssertionError as e:
        logger.warn(str(e))
        raise Http404

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT *
FROM mz_onevone_meeting
WHERE teacher_id = %s AND start_time BETWEEN %s AND %s ORDER BY start_time;
        """

        try:
            cursor.execute(sql, (teacher_id, begin_date, end_date))
            result = cursor.fetchall()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def del_onevone_meeting(teacher_id, meeting_list):
    """
    删除直播列表
    :param teacher_id:
    :param meeting_list:
    :return:
    """
    try:
        teacher_id = int(teacher_id)
        assert isinstance(meeting_list, list)
    except (ValueError, AssertionError) as e:
        logger.warn(str(e))
        raise Http404

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
DELETE FROM mz_onevone_meeting WHERE teacher_id = %s AND id IN (%s);
            """ % ('%s', ','.join(map(lambda x: '%s', meeting_list)))

        try:
            cursor.execute(sql, tuple([teacher_id] + meeting_list))
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=True)

    return main()


def get_onevone_meeting_by_user_id(teacher_id, now_after_3, user_id, begin_date, end_date):
    """
    查询学生相关直播班会
    :param teacher_id:
    :param user_id:
    :param now_after_3:
    :param begin_date:
    :param end_date:
    :return:
    """
    try:
        teacher_id = int(teacher_id)
        user_id = int(user_id)
        assert isinstance(now_after_3, datetime.datetime)
        assert isinstance(begin_date, datetime.datetime)
        assert isinstance(end_date, datetime.datetime)
    except AssertionError as e:
        logger.warn(str(e))
        raise Http404

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT *
FROM mz_onevone_meeting
WHERE ((teacher_id = %s AND start_time > %s AND status = 'CREATE')
      OR (user_id = %s AND ((status = 'ENDED' AND video_url IS NOT NULL) OR status IN ('DATED', 'START'))))
      AND start_time BETWEEN %s AND %s ORDER BY start_time;
        """

        try:
            cursor.execute(sql, (teacher_id, now_after_3, user_id, begin_date, end_date))
            result = cursor.fetchall()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def get_onevone_meeting_range_by_user_id(teacher_id, now_after_3, user_id):
    """
    查询学生相关直播班会时间范围
    :param teacher_id:
    :param user_id:
    :param now_after_3:
    :return:
    """
    try:
        teacher_id = int(teacher_id)
        user_id = int(user_id)
        assert isinstance(now_after_3, datetime.datetime)
    except AssertionError as e:
        logger.warn(str(e))
        raise Http404

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT
max(start_time) AS end_time,
min(start_time) AS start_time
FROM mz_onevone_meeting
WHERE (teacher_id = %s AND start_time > %s OR user_id = %s AND status = 'ENDED' AND video_url IS NOT NULL)
ORDER BY start_time;
        """

        try:
            cursor.execute(sql, (teacher_id, now_after_3, user_id))
            result = cursor.fetchone()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def get_onevone_created_meeting_range_by_teacher_id(teacher_id, now_after_3):
    """
    查询老师可撤销直播班会时间范围
    :param teacher_id:
    :return:
    """
    try:
        teacher_id = int(teacher_id)
    except AssertionError as e:
        logger.warn(str(e))
        raise Http404

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT
max(start_time) AS end_time,
min(start_time) AS start_time
FROM mz_onevone_meeting
WHERE teacher_id = %s AND start_time > %s AND status = 'CREATE';
        """

        try:
            cursor.execute(sql, (teacher_id, now_after_3))
            result = cursor.fetchone()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def get_onevone_meeting_can_be_date(teacher_id, now_after_3):
    """
    1v1班会可预约班会
    :param teacher_id:
    :param now_after_3:
    :return:
    """
    try:
        teacher_id = int(teacher_id)
        assert isinstance(now_after_3, datetime.datetime)
    except AssertionError as e:
        logger.warn(str(e))
        raise Http404

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT *
FROM mz_onevone_meeting
WHERE teacher_id = %s AND start_time > %s AND status = 'CREATE'
ORDER BY start_time;
        """

        try:
            cursor.execute(sql, (teacher_id, now_after_3))
            result = cursor.fetchall()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def get_to_begin_meeting(user_id, career_id, time_limit):
    """
    获取时间线内可以进入的直播（显示直到已开始）
    :param user_id:
    :param career_id:
    :param time_limit:
    :return:
    """
    try:
        career_id = int(career_id)
        user_id = int(user_id)
        assert isinstance(time_limit, datetime.datetime)
    except AssertionError as e:
        logger.warn(str(e))
        raise Http404

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT
  twb.content,
  m.*,
  u.nick_name              AS user_nick_name,
  u.real_name              AS user_real_name,
  u.avatar_small_thumbnall AS user_head
FROM mz_onevone_meeting AS m
  JOIN mz_lps4_teacher_warning_backlog AS twb
    ON (twb.type = 5 AND twb.obj_id = m.id AND m.career_id = %s AND m.user_id = %s AND
        ((m.status = 'START') OR (m.status = 'CREATE' AND m.start_time < %s)))
  LEFT JOIN mz_user_userprofile AS u ON m.user_id = u.id;
        """

        try:
            cursor.execute(sql, (career_id, user_id, time_limit))
            result = cursor.fetchone()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()


def create_onevone_meeting_attendance(meeting_id, user_id, role_type):
    """
    创建1v1直播考勤记录表
    :param meeting_id:
    :param user_id:
    :param role_type:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        # 插入考勤数据
        sql_insert = """
        INSERT INTO mz_onevone_meeting_attendance(
            meeting_id,
            join_date,
            user_id,
            role_type
        )VALUES (%s,%s,%s,%s)
        """

        try:
            cursor.execute(sql_insert, (meeting_id, datetime.datetime.now(), user_id, role_type))
            logger.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=True)

    return main()


@dec_make_conn_cursor
def get_created_onevone_meeting(conn, cursor, career_id, user_id, end_date):
    """
    获取现在至end_date前一天已经创建的班会列表
    :param conn:
    :param cursor:
    :param career_id:
    :param user_id:
    :param end_date:
    :return:
    """
    try:
        career_id = int(career_id)
        user_id = int(user_id)
        assert isinstance(end_date, datetime.date)
    except Exception as e:
        logger.warn(str(e))
        return APIResult(code=False)

    try:
        cursor.execute(
            """
SELECT start_time
FROM mz_onevone_meeting AS m
WHERE m.status = 'CREATE'
      AND m.start_time < %s
      AND m.teacher_id = (SELECT teacher_id
                          FROM mz_lps4_student
                          WHERE career_id = %s AND user_id = %s AND type != 2)
ORDER BY start_time;
            """, (end_date, career_id, user_id)
        )
        logger.info("query:%s" % cursor._last_executed)
        data = cursor.fetchall()
    except Exception as e:
        logger.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=data)


@dec_make_conn_cursor
def cancel_meeting_by_meeting_id(conn, cursor, meeting_id, cancel_reason, user_id):
    """
    取消班会
    :param conn:
    :param cursor:
    :param meeting_id:
    :param user_id:
    :return:
    """
    try:
        meeting_id = int(meeting_id)
        cancel_reason = int(cancel_reason)
        user_id = int(user_id)
    except Exception as e:
        logger.warn(str(e))
        return APIResult(code=False)

    try:
        # 看是否已经取消
        cursor.execute(
            """
SELECT start_time, `status`
FROM mz_onevone_meeting
WHERE id = %s FOR UPDATE;
            """, (meeting_id,)
        )
        logger.info("query:%s" % cursor._last_executed)
        result = cursor.fetchone()
        if result['status'] == 'CANCEL':
            return APIResult(code=False, result=u'该班会已被取消过')

        # 取消
        cursor.execute(
            """
UPDATE mz_onevone_meeting
SET status = 'CANCEL', cancel_reason = %s
WHERE id = %s;
            """, (cancel_reason, meeting_id)
        )
        logger.info("query:%s" % cursor._last_executed)

        # 减少用户班会次数
        cursor.execute(
            """
UPDATE mz_onevone_meeting_user_count
SET count = count - 1
WHERE career_id = (SELECT career_id FROM mz_onevone_meeting WHERE id = %s) AND user_id = %s;
            """, (meeting_id, user_id)
        )
        conn.commit()
    except Exception as e:
        logger.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=result)


@dec_make_conn_cursor
def evaluate_meeting_by_meeting_id(conn, cursor, meeting_id, star, suggest):
    """
    班会评分
    :param conn:
    :param cursor:
    :param meeting_id:
    :param star:
    :param suggest:
    :return:
    """
    try:
        meeting_id = int(meeting_id)
        star = int(star)
    except Exception as e:
        logger.warn(str(e))
        return APIResult(code=False)

    try:
        cursor.execute(
            """
UPDATE mz_onevone_meeting
SET star = %s, suggest = %s
WHERE id = %s;
            """, (star, suggest, meeting_id)
        )
        logger.info("query:%s" % cursor._last_executed)
        conn.commit()
    except Exception as e:
        logger.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e

    return APIResult(code=True)


@dec_make_conn_cursor
def check_meeting_is_belong_to_user(conn, cursor, meeting_id, student_id):
    """
    check 班会是否是属于这个学生
    :param conn:
    :param cursor:
    :param meeting_id:
    :param student_id:
    :return:
    """
    try:
        meeting_id = int(meeting_id)
        student_id = int(student_id)
    except Exception as e:
        logger.warn(str(e))
        return APIResult(code=False)

    try:
        cursor.execute(
            """
SELECT 1
FROM mz_onevone_meeting
WHERE id = %s AND user_id = %s;
            """, (meeting_id, student_id)
        )
        result = cursor.fetchone()
        logger.info("query:%s" % cursor._last_executed)
    except Exception as e:
        logger.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=result)
