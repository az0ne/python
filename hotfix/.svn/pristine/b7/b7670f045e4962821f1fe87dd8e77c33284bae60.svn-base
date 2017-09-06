# -*- coding: utf-8 -*-

from utils.logger import logger as log
from db.api.apiutils import APIResult, dec_make_conn_cursor
import datetime
from utils.tool import strip_tags


def create_teacher_warning_backlog(**kwargs):
    """
    创建老师告警的待办项
    :param kwargs:
    :return:
    """
    def kwargs_get(key):
        return kwargs.get(key, None)
    try:
        teacher_warning_backlog = (
            kwargs['user_id'],
            kwargs['user_name'],
            kwargs['user_head'],
            kwargs['teacher_id'],
            strip_tags(kwargs.get('content', '')),
            kwargs['type'],
            kwargs['obj_id'],
            kwargs['obj_child_id'],
            kwargs.get('is_new', 1),
            kwargs.get('is_done', 0),
            kwargs.get('create_date', datetime.datetime.now()),
            kwargs_get('done_date'),
            kwargs_get('warn_one_date'),
            kwargs_get('warn_two_date'),
            kwargs_get('warn_three_date'),
            kwargs_get('career_id')
        )
    except Exception, e:
        log.warn("execute exception: %s. " % e)
        return APIResult(code=False)

    @dec_make_conn_cursor
    def main(conn, cursor):
        # 插入回复数据
        sql_insert = """
        INSERT INTO mz_lps4_teacher_warning_backlog(
            user_id,
            user_name,
            user_head,
            teacher_id,
            content,
            type,
            obj_id,
            obj_child_id,
            is_new,
            is_done,
            create_date,
            done_date,
            warn_one_date,
            warn_two_date,
            warn_three_date,
            career_id
        )VALUES (%s)
        """ % (','.join(map(lambda x: '%s', teacher_warning_backlog)))

        sql_select = """
        SELECT
          id
        FROM mz_lps4_teacher_warning_backlog
        WHERE user_id=%s  and teacher_id=%s and obj_id=%s and type=%s and is_done=0
        limit 1
        """

        sql_update = """
        UPDATE mz_lps4_teacher_warning_backlog
        SET is_new=is_new+1
        WHERE user_id=%s  and teacher_id=%s and obj_id=%s and type=%s and is_done=0
        """

        # 获取最新的id
        last_id = """
            SELECT last_insert_id() AS last_id
        """
        try:
            cursor.execute(sql_select, (kwargs['user_id'], kwargs['teacher_id'], kwargs['obj_id'], kwargs['type']))
            log.info("query:%s" % cursor._last_executed)
            select_result = cursor.fetchone()
            if select_result:  # 已经存在就更新数量
                cursor.execute(sql_update, (kwargs['user_id'], kwargs['teacher_id'], kwargs['obj_id'], kwargs['type']))
                log.info("query:%s" % cursor._last_executed)
                last_id = select_result['id']
            else:  # 不存在就插入
                cursor.execute(sql_insert, teacher_warning_backlog)
                log.info("query:%s" % cursor._last_executed)
                cursor.execute(last_id)
                log.info("query:%s" % cursor._last_executed)
                last_id = cursor.fetchone()['last_id']
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=last_id)

    return main()


def is_exist_teacher_warning_backlog_type(user_id, teacher_id, obj_id, type):
    """
    根据类型判断是否已经存在老师告警待办项
    :param user_id:
    :param teacher_id:
    :param obj_id:
    :param type:
    :return:
    """
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        SELECT
          1
        FROM mz_lps4_teacher_warning_backlog
        WHERE user_id=%s  and teacher_id=%s and obj_id=%s and type=%s and is_done=0
        limit 1
        """
        try:
            cursor.execute(sql, (user_id, teacher_id, obj_id, type))
            result = cursor.fetchone()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=result)
    return main()


def update_teacher_warning_backlog_is_done(obj_id, teacher_child_id, teacher_id, user_id, type):
    """
    更新老师告警待办状态为已经完成
    :param obj_id:
    :param teacher_child_id:
    :param teacher_id:
    :param user_id:
    :param type: 待办的类型
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        if type in [11, 12, 13, 14]:
            sql = """
            update mz_lps4_teacher_warning_backlog
            set is_done=1,done_date=now(),teacher_child_id=%s, done_status= case
                                                        when now()>warn_three_date then 1
                                                        when now()>warn_two_date then 2
                                                        when now()>warn_one_date then 3
                                                        else 4 END
            where obj_id=%s and teacher_id=%s and type=%s and user_id=%s and is_done=0
            """
        elif type == 5:
            sql = """
            update mz_lps4_teacher_warning_backlog
            set is_done=1,done_date=now(),teacher_child_id=%s,done_status= case
                                                        when now()>warn_two_date then 1
                                                        when now()>warn_one_date then 2
                                                        else 4 END
            where obj_id=%s and teacher_id=%s and type=%s and user_id=%s and is_done=0
            """
        sql_count = """select row_count() as row_count"""

        try:
            cursor.execute(sql, (teacher_child_id, obj_id, teacher_id, type, user_id))
            log.info("query:%s" % cursor._last_executed)
            cursor.execute(sql_count)
            log.info("query:%s" % cursor._last_executed)
            row_count = cursor.fetchone()['row_count']
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        if row_count > 0:
            return APIResult(result=True)
        else:
            return APIResult(result=False)
    return main()


def get_teacher_warning_by_type(type):
    """
    或许老师告警管理设置的阀值
    :param type:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
        select *
        from mz_lps4_teacher_warning
        where type=%s
        """

        try:
            cursor.execute(sql, (type,))
            log.info("query:%s" % cursor._last_executed)
            teacher_warning = cursor.fetchone()
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=teacher_warning)

    return main()


def get_backlog_id_by_meeting_id(meeting_id):
    """
    根据meeting_id获取backlog_id
    :param meeting_id:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
        select *
        from mz_lps4_teacher_warning_backlog
        where type=5 and obj_id=%s
        """

        try:
            cursor.execute(sql, (meeting_id,))
            log.info("query:%s" % cursor._last_executed)
            backlog_id = cursor.fetchone()
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=backlog_id)

    return main()


def filter_warning_backlog():
    """
    筛选已经发生严重告警并且没有发送短信的代办
    :return:
    """
    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
        select *
        from mz_lps4_teacher_warning_backlog
        where warn_three_date<=%s and is_done=0 and type!=5 and is_send_sms=0
        and warn_three_date > %s
        UNION
        select *
        from mz_lps4_teacher_warning_backlog
        where warn_two_date<=%s and is_done=0 and type=5 and is_send_sms=0
        and warn_two_date > %s
        """

        try:
            date_time = datetime.datetime.now()
            today = date_time.strftime('%Y-%m-%d')
            cursor.execute(sql, (date_time, today, date_time, today))
            log.info("query:%s" % cursor._last_executed)
            warning_backlog = cursor.fetchall()
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=warning_backlog)

    return main()


def update_teacher_warning_backlog_is_send_sms(backlog_id):
    """
    更新老师告警待办状态为已经完成
    :param backlog_id:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
        update mz_lps4_teacher_warning_backlog
        set is_send_sms=1
        where id=%s
        """
        sql_count = """select row_count() as row_count"""

        try:
            cursor.execute(sql, (backlog_id,))
            log.info("query:%s" % cursor._last_executed)
            cursor.execute(sql_count)
            log.info("query:%s" % cursor._last_executed)
            row_count = cursor.fetchone()['row_count']
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        if row_count > 0:
            return APIResult(result=True)
        else:
            return APIResult(result=False)
    return main()


def get_backlog_doing_all_teacher_id():
    """
    获取代办警告中所有未完成任务的老师ID
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
        select distinct teacher_id
        from mz_lps4_teacher_warning_backlog
        where is_done=0
        """

        try:
            cursor.execute(sql)
            log.info("query:%s" % cursor._last_executed)
            teacher_ids = cursor.fetchall()
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        return APIResult(result=teacher_ids)

    return main()


def get_backlog_briefing_by_teacher_id(teacher_id):
    """
    根据老师ID   获取每个老师的代办信息
    :param teacher_id:
    :return:
    """
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select count(id),type
        from mz_lps4_teacher_warning_backlog
        where  is_done=0 and teacher_id=%s and type!=5
        group by type
        UNION
        select count(id),type
        from mz_lps4_teacher_warning_backlog
        where  is_done=0 and teacher_id=%s and warn_two_date like %s and warn_two_date>=%s and type=5
        group by type
        """

        try:
            date_time = datetime.datetime.now()
            cursor.execute(sql, (teacher_id, teacher_id, date_time.strftime("%Y-%m-%d")+'%', date_time))
            log.info("query:%s" % cursor._last_executed)
            backlog_counts = cursor.fetchall()

        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        learning_count, q_a_count, coach_count, project_count, meeting_count = 0, 0, 0, 0, 0

        for backlog_count in backlog_counts:
            if backlog_count['type'] == 11:
                learning_count = backlog_count['count(id)']
            if backlog_count['type'] == 12:
                q_a_count = backlog_count['count(id)']
            if backlog_count['type'] == 13:
                coach_count = backlog_count['count(id)']
            if backlog_count['type'] == 14:
                project_count = backlog_count['count(id)']
            if backlog_count['type'] == 5:
                meeting_count = backlog_count['count(id)']

        total_count = learning_count+q_a_count+coach_count+project_count+meeting_count

        return APIResult(result=dict(learning_count=learning_count,
                                     q_a_count=q_a_count,
                                     coach_count=coach_count,
                                     project_count=project_count,
                                     meeting_count=meeting_count,
                                     total_count=total_count))

    return main()


def get_new_backlog_count_by_teacher_id(teacher_id):
    """
    获取老师所有带处理的任务数任务记录条数
    :param teacher_id:
    :return:
    """
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT
  sum(is_new) AS sum_num
FROM mz_lps4_teacher_warning_backlog
WHERE teacher_id = %s
      AND is_done = 0
      AND is_new != 0
        """
        try:
            cursor.execute(sql, (teacher_id,))
            data = cursor.fetchone()["sum_num"]
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "excute exception: %s."
                "statement: %s"(e, cursor._last_executed)
            )
            raise e

        return APIResult(result=data)

    return main()


def get_teacher_warning_backlog_by_teacher_id(teacher_id=0):
    """
    获取老师处理待处理任务记录
    :param teacher_id:
    :return:
    """
    try:
        teacher_id = int(teacher_id)
    except Exception as e:
        log.info('parameters error, teacher_id, %s' % str(e))

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT
  id        AS backlog_id,
  obj_id        AS service_id,
  user_name AS name,
  user_head AS avatar,
  content,
  `type`    AS service_type,
  is_new,
  warn_one_date,
  warn_two_date,
  warn_three_date
FROM mz_lps4_teacher_warning_backlog
WHERE teacher_id = %s
      AND is_done = 0
      AND TYPE != 5
ORDER BY warn_three_date
        """
        try:
            cursor.execute(sql, (teacher_id,))
            data = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "excute exception: %s."
                "statement: %s"(e, cursor._last_executed)
            )
            raise e

        return APIResult(result=data)

    return main()


def get_teacher_warning_backlog_count_by_teacher_id(teacher_id=0):
    """
    获取老师处理待处理任务记录条数
    :param teacher_id:
    :return:
    """
    try:
        teacher_id = int(teacher_id)
    except Exception as e:
        log.info('parameters error, teacher_id, %s' % str(e))

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT
  sum(is_new) AS sum_num
FROM mz_lps4_teacher_warning_backlog
WHERE teacher_id = %s
      AND is_done = 0
      AND TYPE != 5
      AND is_new != 0
        """
        try:
            cursor.execute(sql, (teacher_id,))
            data = cursor.fetchone()['sum_num']
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "excute exception: %s."
                "statement: %s"(e, cursor._last_executed)
            )
            raise e

        return APIResult(result=data)

    return main()


def get_backlog_detail_by_id(backlog_id):
    """
    获取待办详情
    :param backlog_id:
    :return:
    """
    try:
        backlog_id = int(backlog_id)
    except Exception as e:
        log.info('parameters error, id, %s' % str(e))

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT
  *
FROM mz_lps4_teacher_warning_backlog
WHERE id = %s
        """
        try:
            cursor.execute(sql, (backlog_id,))
            data = cursor.fetchone()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "excute exception: %s."
                "statement: %s"(e, cursor._last_executed)
            )
            raise e

        return APIResult(result=data)

    return main()


def update_backlog_status_by_obj_id(status_choice, obj_id, *obj_type):
    """
    更新is_new
    :param status_choice:
    :param obj_id:
    :param obj_type:
    :return:
    """
    try:
        assert status_choice in ['is_done', 'is_new']
        obj_id = int(obj_id)
        assert isinstance(obj_type, tuple)
    except Exception as e:
        log.info('parameters error, id, %s' % str(e))

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
UPDATE mz_lps4_teacher_warning_backlog
SET %s = 0
WHERE obj_id = %s AND `type` IN (%s);
        """ % (status_choice, '%s', ','.join(map(lambda x: '%s', obj_type)))
        try:
            cursor.execute(sql, tuple([obj_id] + list(obj_type)))
            log.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            log.warn(
                "excute exception: %s."
                "statement: %s"(e, cursor._last_executed)
            )
            raise e

        return APIResult(result=True)

    return main()


def update_backlog_new_status_by_id(backlog_id):
    """
    更新is_new数量
    :param backlog_id:
    :return:
    """
    try:
        backlog_id = int(backlog_id)
    except Exception as e:
        log.info('parameters error, id, %s' % str(e))

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
UPDATE mz_lps4_teacher_warning_backlog
SET is_new = 0
WHERE id = %s
        """
        try:
            cursor.execute(sql, (backlog_id,))
            log.info("query:%s" % cursor._last_executed)
            conn.commit()
        except Exception as e:
            log.warn(
                "excute exception: %s."
                "statement: %s"(e, cursor._last_executed)
            )
            raise e

        return APIResult(result=True)

    return main()


def get_project_detail_by_project_id_and_user_id(project_id, user_id, career_id):
    """
    获取任务详情
    :param project_id:
    :param user_id:
    :param career_id:
    :return:
    """
    try:
        project_id = int(project_id)
        user_id = int(user_id)
        career_id = int(career_id)
    except Exception as e:
        log.info('parameters error, id, %s' % str(e))

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT
  e.id                    AS project_id,
  e.title                 AS project_name,
  e.description           AS `require`,
  pr.`desc`               AS content,
  s.name                  AS source,
  group_concat(pri.image) AS images
FROM mz_lps_examine AS e
  JOIN mz_lps_examinerecord AS er ON (er.examine_id = e.id AND er.student_id = %s AND e.id = %s)
  JOIN mz_lps_projectrecord AS pr ON er.id = pr.examinerecord_ptr_id
  JOIN mz_lps_projectrecordimage AS pri ON pri.project_record_id = er.id
  JOIN mz_lps3_task AS t ON t.project_id = e.id
  JOIN mz_lps3_stagetaskrelation AS str ON str.task_id = t.id
  JOIN mz_course_stage AS s ON (s.id = str.stage_id AND s.career_course_id = %s);
        """
        try:
            cursor.execute(sql, (user_id, project_id, career_id))
            data = cursor.fetchone()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "excute exception: %s."
                "statement: %s"(e, cursor._last_executed)
            )
            raise e

        return APIResult(result=data)

    return main()


def get_meeting_list(teacher_id):
    """
    获取直播列表
    :param teacher_id:
    :return:
    """
    try:
        teacher_id = int(teacher_id)
    except Exception as e:
        log.info('parameters error, id, %s' % str(e))

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
SELECT
  wb.obj_id      AS meeting_id,
  wb.user_name   AS name,
  wb.user_head   AS avatar,
  wb.content,
  wb.create_date AS create_time,
  wb.is_new,
  wb.warn_one_date,
  wb.warn_two_date,
  wb.id          AS backlog_id,
  m.start_time,
  m.end_time,
  wb.user_id
FROM mz_onevone_meeting AS m
  JOIN mz_lps4_teacher_warning_backlog AS wb
    ON (m.id = wb.obj_id AND wb.type = 5)
WHERE
  m.teacher_id = %s
  AND m.status IN ('CREATE', 'START')
  AND m.user_id IS NOT NULL
ORDER BY m.start_time;
        """
        try:
            cursor.execute(sql, (teacher_id,))
            data = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "excute exception: %s."
                "statement: %s"(e, cursor._last_executed)
            )
            raise e

        return APIResult(result=data)

    return main()


def get_meeting_detail(backlog_id):
    """
    获取直播列表
    :param backlog_id:
    :return:
    """
    try:
        backlog_id = int(backlog_id)
    except Exception as e:
        log.info('parameters error, id, %s' % str(e))

    @dec_make_conn_cursor
    def main(conn, cursor):
        # name为学生的name，如果real_name是null或空字符串，则取nick_name
        sql = """
SELECT
  wb.obj_id      AS meeting_id,
  m.start_time,
  m.end_time,
  wb.id          AS backlog_id,
  if(t.real_name IS NULL OR t.real_name = '', t.nick_name, t.real_name) AS name,
  wb.user_head   AS avatar,
  wb.warn_one_date,
  wb.warn_two_date,
  wb.create_date AS create_time,
  m.question     AS content,
  m.star,
  m.status,
  m.live_code     AS room_number,
  m.teacher_token AS token
FROM mz_lps4_teacher_warning_backlog AS wb
  JOIN mz_onevone_meeting AS m ON m.id = wb.obj_id
  JOIN mz_user_userprofile AS t ON t.id = wb.user_id
WHERE wb.id = %s;
        """
        try:
            cursor.execute(sql, (backlog_id,))
            data = cursor.fetchone()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "excute exception: %s."
                "statement: %s"(e, cursor._last_executed)
            )
            raise e

        return APIResult(result=data)

    return main()


def get_backlog_history(teacher_id, types, order_type, page_index, page_size=20):
    """
    获取老师历史代办详情
    :param teacher_id:
    :param types:
    :param order_type:
    :param page_index:
    :param page_size:
    :return:
    """
    try:
        start_index = (page_index - 1) * page_size  # 开始条数
        assert order_type in ['ASC', 'DESC']
        teacher_id = int(teacher_id)
        assert isinstance(types, list)
    except Exception as e:
        log.info('parameters error, id, %s' % str(e))
        raise e

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
        select * from mz_lps4_teacher_warning_backlog
        where is_done=1  and teacher_id=%s  %s
        order by done_date %s
        limit %s,%s
        """ % ('%s', 'and type in ('+','.join(map(lambda x: '%s', types))+')' if types else '',
               order_type, start_index, page_size)
        try:
            cursor.execute(sql, tuple([teacher_id]+types))
            data = cursor.fetchall()
            log.info("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "excute exception: %s."
                "statement: %s"(e, cursor._last_executed)
            )
            raise e

        return APIResult(result=data)

    return main()


def get_coach_history_comments(coach_id, start_index, end_index):
    """
    获取辅导评论列表
    :param coach_id:
    :param start_index:
    :param end_index:
    :return:
    """
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
            SELECT
              cc.coach_id,
              cc.comment,
              cc.user_type,
              cc.user_id,
              cc.nick_name,
              cc.head,
              cc.create_date,
              backlog.done_status
            FROM mz_coach_comment as cc
            LEFT join mz_lps4_teacher_warning_backlog as backlog on cc.id=backlog.teacher_child_id and backlog.is_done=1
            WHERE coach_id = %s
            ORDER BY create_date
            LIMIT %s,%s
        """
        try:
            cursor.execute(sql, (coach_id, start_index, end_index))
            data = cursor.fetchall()
            log.debug("query:%s" % cursor._last_executed)
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e

        return APIResult(result=data)
    return main()


def update_backlog_cancel_is_done_by_id(backlog_id):
    """
    根据ID取消完成状态
    :param backlog_id:
    :return:
    """
    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
        update mz_lps4_teacher_warning_backlog
        set is_done=2
        where id=%s
        """
        sql_count = """select row_count() as row_count"""

        try:
            cursor.execute(sql, (backlog_id,))
            log.info("query:%s" % cursor._last_executed)
            cursor.execute(sql_count)
            log.info("query:%s" % cursor._last_executed)
            row_count = cursor.fetchone()['row_count']
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor._last_executed))
            raise e
        if row_count > 0:
            return APIResult(result=True)
        else:
            return APIResult(result=False)
    return main()




