# -*- coding: utf-8 -*-

import time

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult
from utils import tool
from mz_fxsys import constant_pool
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def select_user_by_id(conn, cursor, user_id):
    """
    根据用户ID查询用户
    return: {} 字典类型数据
    """
    try:
        cursor.execute("""select uf.*,up.mobile,up.email
                from mz_fxsys_user as uf left JOIN mz_user_userprofile as up ON up.id=uf.maiziedu_id
                  WHERE uf.id = %s""",
                       (user_id,))
        users = cursor.fetchone()
    except Exception as e:
        log.wanr(
            "execute exception: %s"
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=users)


@dec_timeit
@dec_make_conn_cursor
def get_all_user(conn, cursor):
    """获取所有用户的"""
    try:
        cursor.execute("select id,username,full_name from mz_fxsys_user")
        users = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=users)


@dec_timeit
@dec_make_conn_cursor
def get_user_by_username(conn, cursor, username):
    """获取所有用户的"""
    try:
        cursor.execute("select * from mz_fxsys_user WHERE username=%s ORDER BY register_date DESC ", (username,))
        users = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=users)


# @dec_timeit
# @dec_make_conn_cursor
# def get_user_role_by_parent(conn, cursor, _id):
#     """根据父级或爷极ID查询用户表"""
#     try:
#         cursor.execute(
#             "select id,parent_id,grandparent_id from mz_fxsys_user WHERE parent_id = {0} or grandparent_id = {0}".format(_id)
#         )
#         user_info = cursor.fetchall()
#     except Exception as e:
#         log.warn(
#             "execute exception: %s."
#             "statement: %s" % (e, cursor.statement)
#         )
#         raise e
#
#     return APIResult(result=user_info)


@dec_timeit
@dec_make_conn_cursor
def select_user_by_page(conn, cursor, page_index, page_size, type_id, role_id, user_name):
    """
    分页查询用户
    :param conn:
    :param cursor:
    :param page_index:
    :param page_size:
    :param type_id:
    :param role_id:
    :param user_name:
    :return:
    """
    start_index = tool.get_page_info(page_index, page_size)
    base_sql = "select {fields} from mz_fxsys_user as uf left JOIN mz_user_userprofile as up ON up.id=uf.maiziedu_id" \
               " left JOIN mz_fxsys_rebatetype as rt ON rt.id=uf.rebate_type_id" \
               " left join mz_fxsys_new_asset as asset ON uf.id=asset.user_id WHERE 1=1"
    condition = ""
    order_by = " ORDER BY id DESC"
    if int(type_id) != 0:
        condition += " AND type_id={0}".format(type_id)
        if int(role_id) != 0:
            condition += " AND role_id={0}".format(role_id)
    if user_name:
        condition += " AND (uf.username='{0}' OR uf.full_name='{1}' )".format(user_name, user_name)
    limit = " limit {0},{1}".format(start_index, page_size)
    pagination_sql = base_sql.format(fields='uf.*,up.mobile,up.email,rt.rebate_no,asset.reward_count')
    count_sql = base_sql.format(fields="count(uf.id) as counts")
    if condition != "":
        pagination_sql += condition
        count_sql += condition
    pagination_sql += order_by
    pagination_sql += limit
    try:
        cursor.execute(pagination_sql)
        users = cursor.fetchall()

        cursor.execute(count_sql)
        rows_count = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    for us in users:
        us['maiziedu_name'] = us["mobile"] or us["email"]
        us['type_name'] = constant_pool.TYPE_ID_NAME[str(us['type_id'])]
        us['role_name'] = constant_pool.ROLE_ID_NAME[str(us['role_id'])]
    data = {
        "result": users,
        "rows_count": rows_count['counts'],
        "page_count": tool.get_page_count(rows_count['counts'], page_size)
    }
    return APIResult(result=data)


@dec_timeit
@dec_make_conn_cursor
def insert_user(conn, cursor, username, password, full_name='', ID_card_No='', contract_num='', enterprise_name='',
                type_id=0, role_id=0, parent_id='0', grandparent_id='0', activate_date='', rebate_type_id='Null',
                maiziedu_id='Null', fxsys_note='', cash_back_way='null', cash_back_maximum='null',
                cash_back_day='null'):
    """新增用户"""
    try:
        cursor.execute(
            """
                insert into mz_fxsys_user (username,password,full_name,ID_card_No,contract_num,
                enterprise_name,type_id,role_id,parent_id,grandparent_id, register_date,activate_date,
                rebate_type_id,maiziedu_id,fxsys_note, cash_back_way, cash_back_maximum, cash_back_day)
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (username, password, full_name, ID_card_No, contract_num, enterprise_name, type_id, role_id,
                  parent_id, grandparent_id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), activate_date,
                  rebate_type_id, maiziedu_id, fxsys_note, cash_back_way, cash_back_maximum, cash_back_day))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_user(conn, cursor, user_id, full_name, ID_card_No, contract_num, enterprise_name, role_id, activate_date,
                rebate_type_id, maiziedu_id, is_suspend, is_graduate, fxsys_note, cash_back_way, cash_back_maximum,
                cash_back_day):
    """更新user表"""
    try:
        cursor.execute(
            """
              update mz_fxsys_user set full_name=%s, ID_card_No=%s, contract_num=%s, enterprise_name=%s, role_id=%s,
              activate_date=%s,rebate_type_id=%s,maiziedu_id=%s,is_suspend=%s,is_graduate=%s,fxsys_note=%s, 
              cash_back_way=%s, cash_back_maximum=%s, cash_back_day=%s WHERE id = %s
            """,
            (full_name, ID_card_No, contract_num, enterprise_name, role_id, activate_date, rebate_type_id,
             maiziedu_id, is_suspend, is_graduate, fxsys_note, cash_back_way, cash_back_maximum, cash_back_day, user_id)
        )
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_user_role_relation(conn, cursor, user_id, parent_id=None, grandparent_id=None):
    """更新用户角色关系"""
    base_sql = "update mz_fxsys_user set"
    update = ''
    condition = " where id={0}".format(user_id)
    if parent_id:
        if grandparent_id:
            update += " parent_id = {0},".format(parent_id)
        else:
            update += " parent_id = {0}".format(parent_id)
    if grandparent_id:
        update += " grandparent_id = {0}".format(grandparent_id)

    sql = base_sql + update + condition
    if update != '':
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            log.warn(
                "execute exception: %s."
                "statement: %s" % (e, cursor.statement)
            )
            raise e
        return APIResult(result=True)
    else:
        return APIResult(code=False)


@dec_timeit
@dec_make_conn_cursor
def update_activate_date_by_userId(conn, cursor, user_id):
    """用户激活"""
    try:
        cursor.execute("update mz_fxsys_user set activate_date=%s where id=%s",
                       (time.strftime("%Y-%m-%d %H:%M:S", time.localtime()), user_id))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s"
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def del_user(conn, cursor, uid):
    """删除用户"""
    try:
        cursor.execute('delete from mz_fxsys_user where id=%s', (uid,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def validate_user_exist_by_username(conn, cursor, username):
    """验证用户是否存在"""
    try:
        cursor.execute("select count(id) as count from mz_fxsys_user WHERE username=%s", (username,))
        user = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=user)
