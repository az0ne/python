# -*- coding: utf-8 -*-

import datetime

from maiziserver.utils.logger import logger as log
from maiziserver.db.api.apiutils import APIResult, dec_make_conn_cursor

_sql = """ select
                a.id            ,
                a.account       ,
                a.student_name  ,
                a.phone         ,
                a.qq            ,
                a.address       ,
                a.career_id     ,
                a.career_job    ,
                a.pay_money     ,
                a.pay_type      ,
                a.sailer        ,
                a.sail_at       ,
                a.assistant_id  ,
                a.teacher_id    ,
                a.start_at  ,
                a.graduate_at   ,
                a.stage         ,
                a.state         ,
                a.company       ,
                a.sail_remark   ,
                a.student_remark,
                a.pay_order_num,
                a.pay_real,
                a.filename1,
                a.filename2,
                a.filename3,
                a.extension,
                b.name as career_name,
                c.name as assistant_name,
                d.name as teacher_name,

                case a.career_job
                when '0' then '非就业'
                else '就业'
                end as career_job_name,

                a.reward,
                case a.reward
                when 0 then '不参加'
                else '参加'
                end as reward_name,

                case a.stage
                when '0' then '学习未开始'
                when '1' then '学习期'
                when '2' then '结业期'
                when '3' then '就业期'
                when '4' then '服务结束'
                else '请修改'
                end as stage_name,

                case a.state
                when '0' then '正常'
                when '1' then '休学'
                when '2' then '放弃'
                when '3' then '退学'
                when '4' then '失联'
                else '请修改'
                end as state_name,

                a.reward_month,
                a.bank,
                a.bank_account,
                a.idcard,

                a.loan,
                case a.loan
                when 0 then '未贷款'
                else '参加'
                end as loan_name,

                a.loan_company,
                a.loan_type,
                a.loan_interest,

                a.loan_person ,
                a.loan_money,
                a.subsidy,
                a.reduction

                from mz_server_career_student as a
                left join mz_server_career as b on a.career_id = b.id
                left join mz_server_assistant as c on a.assistant_id = c.id
                left join mz_server_teacher as d on a.teacher_id = d.id """


def list_student_sailer(account,
                        student_name,
                        sailer,
                        phone,
                        qq,
                        start_time,
                        end_time,
                        skip,
                        is_all=False,
                        ):

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql_count = """
                        select count(*) as count from mz_server_career_student
                        where (account like  %s or %s = '')
                        and (student_name like  %s or %s = '')
                        and (sailer like  %s or %s = '')
                        and (phone like  %s or %s = '')
                        and (qq like  %s or %s = '')
                        and (sail_at > %s or %s = '')
                        and (sail_at < %s or %s = '')
                        """

        sql = _sql + """
                where (a.account like  %s or %s = '')
                and (a.student_name like  %s or %s = '')
                and (a.sailer like  %s or %s = '')
                and (a.phone like  %s or %s = '')
                and (a.qq like  %s or %s = '')
                and (sail_at > %s or %s = '' )
                and (sail_at < %s or %s = '')
                order by id desc
                limit %s,%s
                """

        try:
            if is_all != '':
                sql = _sql + """
                                where (a.account like  %s or %s = '')
                                and (a.student_name like  %s or %s = '')
                                and (a.sailer like  %s or %s = '')
                                and (a.phone like  %s or %s = '')
                                and (a.qq like  %s or %s = '')
                                and (sail_at > %s or %s = '' )
                                and (sail_at < %s or %s = '')
                                order by id desc
                                """
                cursor.execute(sql, ('%' + account + '%',
                                      account,
                                      '%' + student_name + '%',
                                      student_name,
                                      '%' + sailer + '%',
                                      sailer,
                                      '%' + phone + '%',
                                      phone,
                                      '%' + qq + '%',
                                      qq,
                                      start_time,
                                      start_time,
                                      end_time,
                                      end_time,
                                      ))

                info = cursor.fetchall()

                log.info("db execute: " + cursor._last_executed)


            else:
                cursor.execute(sql, ('%' + account + '%',
                                     account,
                                     '%' + student_name + '%',
                                     student_name,
                                     '%' + sailer + '%',
                                     sailer,
                                     '%' + phone + '%',
                                     phone,
                                     '%' + qq + '%',
                                     qq,
                                     start_time,
                                     start_time,
                                     end_time,
                                     end_time,
                                     skip["limit"], skip["offset"]))

                info = cursor.fetchall()

                log.info("db execute: " + cursor._last_executed)

            cursor.execute(sql_count, ('%' + account + '%',
                                       account,
                                       '%' + student_name + '%',
                                       student_name,
                                       '%' + sailer + '%',
                                       sailer,
                                       '%' + phone + '%',
                                       phone,
                                       '%' + qq + '%',
                                       qq,
                                       start_time,
                                       start_time,
                                       end_time,
                                       end_time,
                                       ))
            rows_count = cursor.fetchone()

            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            print e
            raise e

        result_dict = {
            "result": info,
            "rows_count": rows_count["count"],
        }

        return APIResult(result=result_dict)

    return main()


def list_student_assistant(account,
                           student_name,
                           career_id,
                           career_job,
                           assistant_id,
                           teacher_id,
                           reward,
                           start_time,
                           end_time,
                           is_all,
                           skip,
                           ):
    @dec_make_conn_cursor
    def main(conn, cursor):
        print skip["limit"]
        print skip["offset"]

        sql_count = """
                        select count(*) as count from mz_server_career_student
                        where (account like  %s or %s = '')
                        and (student_name like  %s or %s = '')
                        and (career_id  = %s or %s = -1)
                        and (career_job = %s or %s = -1)
                        and (assistant_id = %s or %s = -1)
                        and (teacher_id = %s or %s = -1)
                        and (reward = %s or %s = -1)
                        and (start_at > %s or %s = '')
                        and (start_at < %s or %s = '')
                        """

        sql = _sql + """
                            where (account like  %s or %s = '')
                            and (student_name like  %s or %s = '')
                            and (career_id  = %s or %s = -1)
                            and (career_job = %s or %s = -1)
                            and (assistant_id = %s or %s = -1)
                            and (teacher_id = %s or %s = -1)
                            and (reward = %s or %s = -1)
                            and (start_at > %s or %s = '')
                            and (start_at < %s or %s = '')
                    order by id desc
                    limit %s,%s
                    """

        try:

            if is_all != '':
                sql = _sql + """
                                 where (account like  %s or %s = '')
                                 and (student_name like  %s or %s = '')
                                 and (career_id  = %s or %s = -1)
                                 and (career_job = %s or %s = -1)
                                 and (assistant_id = %s or %s = -1)
                                 and (teacher_id = %s or %s = -1)
                                 and (reward = %s or %s = -1)
                                 and (start_at > %s or %s = '' )
                                 and (start_at < %s or %s = '')
                                 order by id desc
                         """
                cursor.execute(sql, ('%' + account + '%',
                                     account,
                                     '%' + student_name + '%',
                                     student_name,
                                     career_id,
                                     career_id,
                                     career_job,
                                     career_job,
                                     assistant_id,
                                     assistant_id,
                                     teacher_id,
                                     teacher_id,
                                     reward,
                                     reward,
                                     start_time,
                                     start_time,
                                     end_time,
                                     end_time,
                                     ))
                info = cursor.fetchall()

                log.info("db execute: " + cursor._last_executed)



            else:
                cursor.execute(sql, ('%' + account + '%',
                                     account,
                                     '%' + student_name + '%',
                                     student_name,
                                     career_id,
                                     career_id,
                                     career_job,
                                     career_job,
                                     assistant_id,
                                     assistant_id,
                                     teacher_id,
                                     teacher_id,
                                     reward,
                                     reward,
                                     start_time,
                                     start_time,
                                     end_time,
                                     end_time,
                                     skip["limit"], skip["offset"]))
                info = cursor.fetchall()

                log.info("db execute: " + cursor._last_executed)

            cursor.execute(sql_count, ('%' + account + '%',
                                       account,
                                       '%' + student_name + '%',
                                       student_name,
                                       career_id,
                                       career_id,
                                       career_job,
                                       career_job,
                                       assistant_id,
                                       assistant_id,
                                       teacher_id,
                                       teacher_id,
                                       reward,
                                       reward,
                                       start_time,
                                       start_time,
                                       end_time,
                                       end_time,
                                       ))
            rows_count = cursor.fetchone()

            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        result_dict = {
            "result": info,
            "rows_count": rows_count["count"],
        }

        return APIResult(result=result_dict)

    return main()


def list_student_assistant_change_teacher(student_id):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                select
                a.id,
                a.student_id,
                b.student_name,
                a.old_teacher_id,
                c.name as old_teacher_name,
                a.new_teacher_id,
                d.name as new_teacher_name,
                a.change_at,
                a.create_at,
                a.reason,
                a.op_person

                from mz_server_career_teacher_change as a

                left join mz_server_career_student as b on a.student_id = b.id
                left join mz_server_teacher as c on a.old_teacher_id = c.id
                left join mz_server_teacher as d on a.new_teacher_id = d.id
                where a.student_id=%s

                """

        try:
            cursor.execute(sql, (student_id,))
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
            result_dict = {
                "result": info,
            }
        except Exception as e:
            raise e

        return APIResult(result=result_dict)

    return main()


def list_student_assistant_change_assistant(student_id):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                select
                a.id,
                a.student_id,
                b.student_name,
                a.old_assistant_id,
                c.name as old_assistant_name,
                a.new_assistant_id,
                d.name as new_assistant_name,
                a.change_at,
                a.create_at,
                a.reason,
                a.op_person

                from mz_server_career_assistant_change as a

                left join mz_server_career_student as b on a.student_id = b.id
                left join mz_server_assistant as c on a.old_assistant_id = c.id
                left join mz_server_assistant as d on a.new_assistant_id = d.id
                where a.student_id=%s

                """

        try:
            cursor.execute(sql, (student_id,))
            info = cursor.fetchall()
            log.info("db execute: " + cursor._last_executed)
            result_dict = {
                "result": info,
            }
        except Exception as e:
            raise e

        return APIResult(result=result_dict)

    return main()


def list_student_assistant_communication(student_id):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                select
                a.id,
                a.student_id,
                b.student_name,
                a.assistant_id,
                c.name as assistant_name,
                a.communicate_at,
                a.stage,
                case a.stage
                when '0' then '学习未开始'
                when '1' then '学习期'
                when '2' then '结业期'
                when '3' then '就业期'
                when '4' then '服务结束'
                else '请修改'
                end as stage_name,
                a.create_at,
                a.content

                from mz_server_assistant_communication as a

                left join mz_server_career_student as b on a.student_id = b.id
                left join mz_server_assistant as c on a.assistant_id = c.id
                where a.student_id=%s
                order by a.id desc
                """

        try:
            cursor.execute(sql, (student_id,))
            info = cursor.fetchall()
            result_dict = {
                "result": info,
            }
        except Exception as e:
            raise e

        return APIResult(result=result_dict)

    return main()


def get_student_assistant_communication_by_id(id):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                select
                a.id,
                a.student_id,
                b.student_name,
                a.assistant_id,
                c.name as assistant_name,
                a.communicate_at,
                a.stage,
                case a.stage
                when '0' then '学习未开始'
                when '1' then '学习期'
                when '2' then '结业期'
                when '3' then '就业期'
                when '4' then '服务结束'
                else '请修改'
                end as stage_name,
                a.create_at,
                a.content

                from mz_server_assistant_communication as a

                left join mz_server_career_student as b on a.student_id = b.id
                left join mz_server_assistant as c on a.assistant_id = c.id
                where a.id=%s
                """

        try:
            cursor.execute(sql, (id,))
            info = cursor.fetchone()
        except Exception as e:
            raise e

        return APIResult(result=info)

    return main()


def list_student_assistant_communication_all(career_id, assistant_id, phone, skip):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql_count = """
                                select count(*) as count from mz_server_assistant_communication as a
                                left join mz_server_career_student as b on a.student_id = b.id
                                left join mz_server_assistant as c on a.assistant_id = c.id
                                left join mz_server_teacher as d on b.teacher_id = d.id
                                left join mz_server_career as e on b.career_id = e.id

                                where (b.career_id  = %s or %s = -1)
                               and (a.assistant_id = %s or %s = -1)
                               and (b.phone like %s or %s= '')
                               
                    """

        sql = """
                    select
                    a.id,
                    a.student_id,
                    b.student_name,

                    a.assistant_id,
                    c.name as assistant_name,

                    b.teacher_id,
                    d.name as teacher_name,

                    b.career_id,
                    e.name as career_name,

                    a.communicate_at,
                    a.stage,
                    case a.stage
                    when '0' then '学习未开始'
                    when '1' then '学习期'
                    when '2' then '结业期'
                    when '3' then '就业期'
                    when '4' then '服务结束'
                    else '请修改'
                    end as stage_name,
                    a.create_at,
                    a.content

                    from mz_server_assistant_communication as a

                    left join mz_server_career_student as b on a.student_id = b.id
                    left join mz_server_assistant as c on a.assistant_id = c.id
                    left join mz_server_teacher as d on b.teacher_id = d.id
                    left join mz_server_career as e on b.career_id = e.id
                    where (b.career_id  = %s or %s = -1)
                    and (a.assistant_id = %s or %s = -1)
                    and (b.phone like %s or %s= '')
                    order by a.id desc
                    limit %s,%s
                    """

        try:

            cursor.execute(sql_count, (career_id, career_id, assistant_id, assistant_id, '%'+phone+'%', phone))
            rows_count = cursor.fetchone()
            print cursor._last_executed
            cursor.execute(sql, (career_id, career_id, assistant_id, assistant_id,'%'+phone+'%',phone, skip["limit"], skip["offset"]))
            info = cursor.fetchall()
            print cursor._last_executed
            result_dict = {
                "result": info,
                "rows_count": rows_count["count"],
            }

        except Exception as e:
            print e
            raise e

        return APIResult(result=result_dict)

    return main()


def list_student_assistant_suspend(student_id):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                select
                a.id,
                a.student_id,
                b.student_name,
                a.assistant_id,
                c.name as assistant_name,
                a.start_at,
                a.end_at,
                a.create_at,
                a.reason

                from mz_server_assistant_suspend as a

                left join mz_server_career_student as b on a.student_id = b.id
                left join mz_server_assistant as c on a.assistant_id = c.id
                where a.student_id=%s
                order by a.id desc
                """

        try:
            cursor.execute(sql, (student_id,))
            info = cursor.fetchall()
            result_dict = {
                "result": info,
            }
        except Exception as e:
            raise e

        return APIResult(result=result_dict)

    return main()


def get_student_assistant_suspend_by_id(id):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                select
                a.id,
                a.student_id,
                b.student_name,
                a.assistant_id,
                c.name as assistant_name,
                a.start_at,
                a.end_at,
                a.create_at,
                a.reason

                from mz_server_assistant_suspend as a

                left join mz_server_career_student as b on a.student_id = b.id
                left join mz_server_assistant as c on a.assistant_id = c.id
                where a.id=%s
                """

        try:
            cursor.execute(sql, (id,))
            info = cursor.fetchone()
        except Exception as e:
            raise e

        return APIResult(result=info)

    return main()


def list_student_assistant_suspend_all(career_id, assistant_id, skip):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql_count = """
                                select count(*) as count from mz_server_assistant_suspend as a
                                left join mz_server_career_student as b on a.student_id = b.id
                                left join mz_server_assistant as c on a.assistant_id = c.id
                                left join mz_server_teacher as d on b.teacher_id = d.id
                                left join mz_server_career as e on b.career_id = e.id

                                where (b.career_id  = %s or %s = -1)
                                and (a.assistant_id = %s or %s = -1)
                    """

        sql = """
                    select
                    a.id,
                    a.student_id,
                    b.student_name,

                    a.assistant_id,
                    c.name as assistant_name,

                    b.teacher_id,
                    d.name as teacher_name,

                    b.career_id,
                    e.name as career_name,

                    a.start_at,
                    a.end_at,
                    a.create_at,
                    a.reason

                    from mz_server_assistant_suspend as a

                    left join mz_server_career_student as b on a.student_id = b.id
                    left join mz_server_assistant as c on a.assistant_id = c.id
                    left join mz_server_teacher as d on b.teacher_id = d.id
                    left join mz_server_career as e on b.career_id = e.id
                    where (b.career_id  = %s or %s = -1)
                    and (a.assistant_id = %s or %s = -1)
                    order by a.id desc
                    limit %s,%s
                    """

        try:

            cursor.execute(sql_count, (career_id, career_id, assistant_id, assistant_id,))
            rows_count = cursor.fetchone()
            print cursor._last_executed
            cursor.execute(sql, (career_id, career_id, assistant_id, assistant_id, skip["limit"], skip["offset"]))
            info = cursor.fetchall()
            print cursor._last_executed
            result_dict = {
                "result": info,
                "rows_count": rows_count["count"],
            }

        except Exception as e:
            print e
            raise e

        return APIResult(result=result_dict)

    return main()


def list_student_assistant_interview(student_id):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                select
                a.id,
                a.student_id,
                b.student_name,
                b.career_id,
                c.name as career_name,
                a.interviewer,
                a.interview_at,
                a.state,
                case a.state
                when '0' then '未面试'
                when '1' then '不通过'
                when '2' then '通过'
                else '请修改'
                end as state_name,
                a.create_at,
                a.remark


                from mz_server_assistant_interview as a

                left join mz_server_career_student as b on a.student_id = b.id
                left join mz_server_career as c on b.career_id = c.id
                where a.student_id=%s
                order by a.id desc
                """

        try:
            cursor.execute(sql, (student_id,))
            info = cursor.fetchall()
            result_dict = {
                "result": info,
            }
        except Exception as e:
            raise e

        return APIResult(result=result_dict)

    return main()


def get_student_assistant_interview_by_id(id):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                select
                a.id,
                a.student_id,
                b.student_name,
                b.career_id,
                c.name as career_name,
                a.interviewer,
                a.interview_at,
                a.state,
                case a.state
                when '0' then '未面试'
                when '1' then '不通过'
                when '2' then '通过'
                else '请修改'
                end as state_name,
                a.create_at,
                a.remark

                from mz_server_assistant_interview as a

                left join mz_server_career_student as b on a.student_id = b.id
                left join mz_server_career as c on b.career_id = c.id
                where a.id=%s
                order by a.id desc
                """

        try:
            cursor.execute(sql, (id,))
            info = cursor.fetchone()
        except Exception as e:
            raise e

        return APIResult(result=info)

    return main()


def get_student_by_id(student_id):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = _sql + """

                where a.id=%s
                """

        try:
            cursor.execute(sql, (student_id,))
            info = cursor.fetchone()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=info)

    return main()


def sailer_add(account,
               student_name,
               phone,
               qq,
               address,
               career_id,
               career_job,
               pay_money,
               pay_type,
               sailer,
               sail_at,
               assistant_id,
               teacher_id,
               sail_remark,
               student_remark,
               reward,
               reward_month,
               bank,
               bank_account,
               idcard,
               loan,
               loan_company,
               loan_type,
               loan_interest,
               loan_person,
               loan_money,
               subsidy,
               reduction,
               pay_order_num,
               pay_real,
               filename1,
               filename2,
               filename3,
               extension
               ):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                insert into mz_server_career_student(
                                      account,
                                    student_name,
                                    phone,
                                    qq,
                                    address,
                                    career_id,
                                    career_job,
                                    pay_money,
                                    pay_type,
                                    sailer,
                                    sail_at,
                                    assistant_id,
                                    teacher_id,
                                    sail_remark,
                                    student_remark,
                                    reward,
                                    reward_month,
                                    bank,
                                    bank_account,
                                    idcard,
                                    loan,
                                    loan_company,
                                    loan_type,
                                    loan_interest,
                                    loan_person,
                                    loan_money,
                                    subsidy,
                                    reduction,
                                    pay_order_num,
                                    pay_real,
                                    filename1,
                                    filename2,
                                    filename3,
                                    extension)
                values (%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s)
                """
        print "打印的数据"
        try:
            cursor.execute(sql, (account,
                                 student_name,
                                 phone,
                                 qq,
                                 address,
                                 career_id,
                                 career_job,
                                 pay_money,
                                 pay_type,
                                 sailer,
                                 sail_at,
                                 assistant_id,
                                 teacher_id,
                                 sail_remark,
                                 student_remark,
                                 reward,
                                 reward_month,
                                 bank,
                                 bank_account,
                                 idcard,
                                 loan,
                                 loan_company,
                                 loan_type,
                                 loan_interest,
                                 loan_person,
                                 loan_money,
                                 subsidy,
                                 reduction,
                                 pay_order_num,
                                 pay_real,
                                 filename1,
                                 filename2,
                                 filename3,
                                 extension
                                 ))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def sailer_update(student_id,
                  account,
                  student_name,
                  phone,
                  qq,
                  address,
                  career_id,
                  career_job,
                  pay_money,
                  pay_type,
                  sailer,
                  sail_at,
                  assistant_id,
                  teacher_id,
                  sail_remark,
                  student_remark,
                  reward,
                  reward_month,
                  bank,
                  bank_account,
                  idcard,
                  loan,
                  loan_company,
                  loan_type,
                  loan_interest,
                  loan_person,
                  loan_money,
                  subsidy,
                  reduction,
                  pay_order_num,
                  pay_real,
                  filename1,
                  filename2,
                  filename3,
                  extension
                  ):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_career_student set
                                        account=%s,
                                        student_name=%s,
                                        phone=%s,
                                        qq=%s,
                                        address=%s,
                                        career_id=%s,
                                        career_job=%s,
                                        pay_money=%s,
                                        pay_type=%s,
                                        sailer=%s,
                                        sail_at=%s,
                                        assistant_id=%s,
                                        teacher_id=%s,
                                        sail_remark=%s,
                                        student_remark=%s,
                                        reward=%s,
                                        reward_month=%s,
                                        bank=%s,
                                        bank_account=%s,
                                        idcard=%s,
                                        loan=%s,
                                        loan_company=%s,
                                        loan_type=%s,
                                        loan_interest=%s,
                                        loan_person=%s,
                                        loan_money=%s,
                                        subsidy=%s,
                                        reduction=%s,
                                        pay_order_num=%s,
                                        pay_real=%s,
                                        filename1=%s,
                                        filename2=%s,
                                        filename3=%s,
                                        extension=%s
                                      where id =%s
                                      """

        try:
            cursor.execute(sql, (account,
                                 student_name,
                                 phone,
                                 qq,
                                 address,
                                 career_id,
                                 career_job,
                                 pay_money,
                                 pay_type,
                                 sailer,
                                 sail_at,
                                 assistant_id,
                                 teacher_id,
                                 sail_remark,
                                 student_remark,
                                 reward,
                                 reward_month,
                                 bank,
                                 bank_account,
                                 idcard,
                                 loan,
                                 loan_company,
                                 loan_type,
                                 loan_interest,
                                 loan_person,
                                 loan_money,
                                 subsidy,
                                 reduction,
                                 pay_order_num,
                                 pay_real,
                                 filename1,
                                 filename2,
                                 filename3,
                                 extension,
                                 student_id,
                                 ))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def assistant_update(student_id,
                     start_at,
                     graduate_at,
                     stage,
                     state,
                     company):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_career_student set
                            start_at = %s,
                            graduate_at = %s,
                            stage = %s,
                            state = %s,
                            company = %s
                where id =%s
                """

        try:
            cursor.execute(sql, (start_at,
                                 graduate_at,
                                 stage,
                                 state,
                                 company,
                                 student_id,
                                 ))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def change_teacher(student_id,
                   old_teacher_id,
                   new_teacher_id,
                   change_at,
                   reason,
                   op_person):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_career_student set
                teacher_id = %s
                where id =%s
                """

        sql2 = """
                        insert into mz_server_career_teacher_change(
                                    student_id,
                                    old_teacher_id,
                                    new_teacher_id,
                                    change_at,
                                    reason,
                                    op_person)
                        values
                        (%s,%s,%s,%s,%s,%s)
                        """

        try:
            cursor.execute(sql, (new_teacher_id,
                                 student_id,
                                 ))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
            cursor.execute(sql2, (student_id,
                                  old_teacher_id,
                                  new_teacher_id,
                                  change_at,
                                  reason,
                                  op_person,
                                  ))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def change_assistant(student_id,
                     old_assistant_id,
                     new_assistant_id,
                     change_at,
                     reason,
                     op_person):
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
                update mz_server_career_student set
                assistant_id = %s
                where id =%s
                """

        sql2 = """
                        insert into mz_server_career_assistant_change(
                                    student_id,
                                    old_assistant_id,
                                    new_assistant_id,
                                    change_at,
                                    reason,
                                    op_person)
                        values
                        (%s,%s,%s,%s,%s,%s)
                        """

        try:
            cursor.execute(sql, (new_assistant_id,
                                 student_id,
                                 ))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
            cursor.execute(sql2, (student_id,
                                  old_assistant_id,
                                  new_assistant_id,
                                  change_at,
                                  reason,
                                  op_person,
                                  ))
            conn.commit()
            log.info("db execute: " + cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def add_communication(student_id,
                      assistant_id,
                      stage,
                      communicate_at,
                      content
                      ):
    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
                            insert into mz_server_assistant_communication(
                                        student_id,
                                        assistant_id,
                                        stage,
                                        communicate_at,
                                        content)
                            values
                            (%s,%s,%s,%s,%s)
                            """

        try:
            print("xxxxxxxxxxxxx")

            cursor.execute(sql, (student_id,
                                 assistant_id,
                                 stage,
                                 communicate_at,
                                 content,
                                 ))

            conn.commit()
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def add_suspend(student_id,
                assistant_id,
                start_at,
                end_at,
                reason
                ):
    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
                            insert into mz_server_assistant_suspend(
                                        student_id,
                                        assistant_id,
                                        start_at,
                                        end_at,
                                        reason)
                            values
                            (%s,%s,%s,%s,%s)
                            """

        try:

            cursor.execute(sql, (student_id,
                                 assistant_id,
                                 start_at,
                                 end_at,
                                 reason,
                                 ))
            conn.commit()
            print("yyyyyyyyyyyyyyy")
            print(cursor._last_executed)
        except Exception as e:
            raise e

        return APIResult(result=True)

    return main()


def add_interview(student_id,
                  interviewer,
                  interview_at,
                  state,
                  remark):
    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
                            insert into mz_server_assistant_interview(
                                        student_id,
                                        interviewer,
                                        interview_at,
                                        state,
                                        remark)
                            values
                            (%s,%s,%s,%s,%s)
                            """

        try:

            cursor.execute(sql, (student_id,
                                 interviewer,
                                 interview_at,
                                 state,
                                 remark,
                                 ))
            conn.commit()
        except Exception as e:
            print e
            raise e

        return APIResult(result=True)

    return main()


def update_interview(id,
                     interviewer,
                     interview_at,
                     state,
                     remark):
    @dec_make_conn_cursor
    def main(conn, cursor):

        sql = """
                  update mz_server_assistant_interview
                  set interviewer = %s,
                      interview_at = %s,
                      state = %s,
                      remark = %s
                      where id = %s
                            """

        try:

            cursor.execute(sql, (interviewer,
                                 interview_at,
                                 state,
                                 remark,
                                 id,
                                 ))
            conn.commit()
        except Exception as e:
            print e
            raise e

        return APIResult(result=True)

    return main()

def excel_data():
    @dec_make_conn_cursor
    def main(conn, cursor):

        try:
            cursor.execute(_sql)
            info = cursor.fetchall()

        except Exception as e:
            print e
            raise e
        return APIResult(result=info)

    return main()
