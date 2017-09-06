# -*- coding: utf8 -*-

import datetime
from contextlib import closing
from django.db.models.base import ModelBase

from mz_platform.orms.mz_db_model import MZDBModel
from mz_platform.utils.debug_tool import deb_print
from db.cores.mysqlconn import get_conn

DB_OPERATION_TYPE = 'sql'


class DBOperationORMWrapper(object):
    """
    ORM 交互方式
    """
    pass


class SQLHandler(object):
    """将sql的各个字段由str格式拼接为完整的可执行的sql语句

    """
    def __init__(self, engine='mysql'):
        pass

    @classmethod
    def handle_join(cls, join):
        """
        @brief 返回处理后的join

        @param join: join参数，类型为列表，格式如下:
                     [('inner join', ('tb2', 'tb1'), ('tb2_column', 'tb1_column'), ('tb2_column2', 'tb1_column2'), ...),
                      ('left join', ('tb3', 'tb2'), ('tb3_column', 'tb2_column'), ('tb3_column2', 'tb2_column2'), ...),
                     ]
        @return: 处理后的join, 类型为str, 返回的例子如下:
                 inner join tb2 on tb2.tb2_column = tb1.tb1_column and tb2.tb2_column2 = tb1.tb1_column2
                 left join tb3 on tb3.tb3_column = tb2.tb2_column and tb3.tb3_column2 = tb2.tb2_column2
        """
        assert join and isinstance(join, list)
        temp_joins = []
        for item in join:
            way = item[0]   # join 方式
            tb1, tb2 = item[1]  # join 的 table1 和　table2
            columns = item[2:]  # join on 的字段
            on_sql = ' and '.join(list('%s.%s = %s.%s' % (tb1, c[0], tb2, c[1]) for c in columns))
            temp_joins.append('%s join %s on %s' % (way, tb1, on_sql))
        return ' '.join(temp_joins)

    @classmethod
    def handle_what(cls, what):
        """
        @brief 返回处理后的what

        @param what: 查询什么字段，应该为'*', 一个字符串列表, 或者一个字典．如
                     'where.*'
                     ['where.id', 'where.name']
        @return:　处理之后的what，字符串
                  上述3种情况分布返回的结果为:
                  'where.*',
                  'where.id, where.name',
        """
        assert isinstance(what, (str, unicode, list, tuple))
        if isinstance(what, (str, unicode)):
            return what
        elif isinstance(what, (list, tuple)):
            return ', '.join(what)

    @classmethod
    def handle_where(cls, where):
        """
        @brief 返回处理后的where

        @param where: 查询的表名
        @return: 处理之后的表名

        @note 目前直接返回表名
        """
        assert isinstance(where, (str, unicode))
        return where

    @classmethod
    def handle_condition(cls, conditions):
        """
        目前仅考虑 and　条件的情况
        """
        assert isinstance(conditions, (tuple, list))
        return ' and '.join(conditions)

    @classmethod
    def handle_limit(cls, limit):
        """
        简单返回
        """
        assert isinstance(limit, (str, unicode))
        return limit

    @classmethod
    def handle_order_by(cls, order_by):
        """
        简单返回
        """
        return order_by

    @classmethod
    def handle_values(cls, values):
        """
        @brief 处理values
        @param values:
        @return:
        """
        assert isinstance(values, (list, tuple))
        return ' , '.join(values)

    @classmethod
    def handle_select(cls, where, what='*', join=[], conditions=None, limit=None, order_by=None):
        """
        @brief 处理生成完整的select sql

        @param where: 查询的表
        @param what: 查询what的字段
        @param join: join的必要参数
        @param conditions: 查询的条件
        @param limit: 切片
        @param order_by: 排序
        @return:

        @todo join的处理需要持续的润色
        """
        sql = '''select %s from %s''' % (what if what == '*' else cls.handle_what(what), cls.handle_where(where))
        if join:
            sql = '''%s %s''' % (sql, cls.handle_join(join))
        if conditions:
            sql = '''%s where %s''' % (sql, cls.handle_condition(conditions))
        if order_by:
            sql = '''%s order by %s''' % (sql, cls.handle_order_by(order_by))
        if limit:
            sql = '''%s limit %s''' % (sql, cls.handle_limit(limit))
        return sql

    @classmethod
    def handle_insert(cls, where, values):
        """
        @brief 处理完整的insert语句

        @param where: 要插入的表的名字
        @param values: 相关字段的值，应该是一个列表
        @return:
        """
        sql = '''
            insert into %s set %s
            ''' % (cls.handle_where(where), cls.handle_values(values))
        return sql

    @classmethod
    def handle_update(cls):
        pass

    @classmethod
    def handle_delete(cls):
        pass


class DBOperationSQLWrapper(object):
    """SQL 交互方式
    @todo 处理SQL注入
    """
    def __init__(self):
        pass

    def _query(self, sql, commit=False):
        """
        @brief 执行sql语句

        @param sql:
        @return:

        @todo: 研究mysql & mysqldb 的 autocommit机制，取消自动提交，更好的支持事务
        """
        _conn = get_conn()
        with closing(_conn) as conn:
            with closing(conn.cursor()) as cursor:
                deb_print(sql=sql)
                cursor.execute(sql)
                if commit:
                    conn.commit()
                    return
                return cursor.fetchall()
                # return list(dict(zip([x[0] for x in cursor.description], item)) for item in data)

    def __query_insert2(self, sql, para):
        """
        @brief 执行insert语句

        @param sql:
        @return: 返回此次插入的id

        @note 单条插入的sql语句会被封装成事务执行，因为需要返回此次插入的id
        @todo 考虑批量插入的情况
        """
        _conn = get_conn()
        with closing(_conn) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(sql, para)
                conn.commit()
                cursor.execute('select LAST_INSERT_ID() as id;')
                insert_id = cursor.fetchone()
                return insert_id.get('id')

    def select(self, sql=None, *args, **kwargs):
        if sql:
            return self._query(sql)
        return self._query(SQLHandler.handle_select(*args, **kwargs))

    def insert2(self, sql, para):
        return self.__query_insert2(sql, para)

    def update(self, sql, para=None):
        """
        目前只支持para为空的sql
        @param sql:
        @param para:
        @return:
        """
        if para:
            pass
        self._query(sql, commit=True)

    def delete(self):
        pass


class Orm2Str(object):
    """将条件从orm转换为固定格式的string

    """

    @staticmethod
    def __get_join_table(orm_tuple):
        """

        @param orm_tuple:
        @return:

        @todo 让MZDBModel的子类成为MZDBModel的示例
        """
        if isinstance(orm_tuple, tuple):
            if isinstance(orm_tuple[0], type(MZDBModel)):
                return tuple(orm.db_table for orm in orm_tuple)
        return orm_tuple

    @staticmethod
    def __get_condition_table(more_conditions):
        """
        @brief 将条件列表(ORM表示)转化为字符串列表, 如果某个参数为空，则丢弃

        @param more_conditions: 条件列表，格式为[(Course, ('id', 'name'), (5, '')),]
        @return: 字符串列表

        @note example:
              参数为[(Course, ('id', 'name'), (5, 'python')),]
              返回为['course_table_name.id = 5', ]
        """
        cond_str = []
        for item in more_conditions:
            assert len(item[1]) == len(item[2])  # 条件和条件的值应该一样多
            for index in range(len(item[1])):
                if item[2][index]:  # 如果某个参数为空，则丢弃
                    if isinstance(item[2][index], (str, unicode)):
                        cond_str.append('%s.%s="%s"' % (item[0].db_table, item[1][index], item[2][index]))
                    else:
                        cond_str.append('%s.%s=%s' % (item[0].db_table, item[1][index], item[2][index]))
        return cond_str

    @staticmethod
    def __convert_what(what, where):

        def handle_what(what, where):
            """
            将what转化为符合条件的str或者str列表

            @param what: 查询什么字段，应该为'*', 一个字符串列表, 或者一个字典．如
                         '*'
                         ['id', 'name']
                         {'table_name1': ['id', 'name'], 'table_name2': ['*']}
            @param where: 查询的表
            @return:　处理之后的what，字符串
                      上述3种情况分布返回的结果为:
                      'where.*',
                      'where.id, where.name',
                      'table_name1.id, table_name1.name, table_name2.*'

            """
            assert what == '*' or isinstance(what, (list, tuple, dict))
            assert isinstance(where, (str, unicode))
            if what == '*':
                return '%s.%s' % (where, what)
            elif isinstance(what, (list, tuple)):
                return ', '.join(list('%s.%s' % (where, item) for item in what))
            else:
                return ', '.join(list('%s.%s' % (k, item) for item in v for k, v in what.items()))
            return what

        return handle_what(what, where) if what else what

    @staticmethod
    def __convert_conditions(more_conditions, conditions, where):
        """

        @param more_conditions:
        @param conditions:
        @return:
        """
        assert isinstance(where, (str, unicode))
        cond = []

        # 处理额外的条件, 将其从ORM表示转化为str表示
        if more_conditions:
            more_conditions = Orm2Str.__get_condition_table(more_conditions)

        # 处理用户传递的条件，将'key=value'转化为'where.key=value'的格式
        if conditions:
            conditions = list('%s.%s' % (where, item) for item in conditions)

        # 将conditions 和 more_conditions 合并到一起
        for item in [more_conditions, conditions]:
            if item:
                cond.extend(item)
        return cond if cond else None

    @staticmethod
    def __convert_order_by(order_by, where):
        """
        @brief 处理order by, 将 order by column 转化为 order by where.column

        @param order_by:
        @param where:
        @return:
        """
        order_bys = []
        if order_by:
            items = list(item.strip(' ') for item in order_by.split(','))
            for item in items:
                if item.startswith('-'):
                    order_bys.append('-%s.%s' % (where, item.split('-')[1]))
                else:
                    order_bys.append('%s.%s' % (where, item))

        return ', '.join(order_bys) if order_bys else None

    @staticmethod
    def orm2str_insert(*args, **kwargs):
        """
        @brief 将insert从orm转换为固定格式的string

        @param args:
        @param kwargs:
        @return:
        """
        # 处理values
        def if_str(item):  # 把有关的类型转化为str
            if isinstance(item, (str, unicode, datetime.datetime)):
                return "'%s'" % item
            return item
        values = kwargs.get('values')
        return dict(where=kwargs.get('where').db_table,
                    values=list('%s=%s' % (k, if_str(v)) for k, v in values.items()))

    @staticmethod
    def orm2str_select(*args, **kwargs):
        """
        @brief 将条件从orm转换为固定格式的string

        @param args:
        @param kwargs: 传入的关键字参数,支持 what, where, join, conditions, limit, order_by
        @return:

        @note: 处理的字段包含： where, join, conditions,
               未处理的字段包含：　what, limit, order_by
        """

        where = kwargs.get('where').db_table

        # 处理 what
        what = Orm2Str.__convert_what(kwargs.get('what'), where)

        # 处理conditions 和 more_conditions
        cond = Orm2Str.__convert_conditions(kwargs.get('more_conditions'), kwargs.get('conditions'), where)

        # 处理join
        join = kwargs.get('join')
        join = list(tuple(Orm2Str.__get_join_table(sub_item) for sub_item in item) for item in join) if join else None

        # 处理 order by
        order_by = Orm2Str.__convert_order_by(kwargs.get('order_by'), where)

        return dict(what=what,
                    where=where,
                    join=join,
                    conditions=cond,
                    limit=kwargs.get('limit'),
                    order_by=order_by)

    @staticmethod
    def orm2str(op_type='select', *args, **kwargs):
        """
        @brief 将insert从orm转换为固定格式的string

        @param op_type: 操作类型，可以为'select', 'insert', 'update' or 'delete'
        @param args:
        @param kwargs:
        @return:
        """
        oper_map = dict(select=Orm2Str.orm2str_select,
                        insert=Orm2Str.orm2str_insert)
        return oper_map[op_type.lower()](*args, **kwargs)

class MZService (object):
    """
    @brief Service类的基类,任何为业务逻辑提供支持的service类(如CourseService),需要从此类继承

    @note 该类会动态生成上层服务的基础方法.
         举例来说,对于上层服务CourseService, 该类会动态生成 get_course 和 get_all_course 方法,
         在CourseService内部,无需实现这个两个方法
    """

    if DB_OPERATION_TYPE == 'sql':
        db = DBOperationSQLWrapper()
    else:
        db = DBOperationORMWrapper()

    def __init__(self):
        super(MZService, self).__init__()

    @staticmethod
    def execute_select(sql):
        """
        @brief 开放接口，可直接执行select sql语句

        @param sql:  执行的sql语句，格式为字符串
        @return: 返回结果的信息字典
        """
        assert isinstance(sql, (str, unicode))
        return MZService.db.select(sql)

    @staticmethod
    def execute(sql):
        """
        @brief 开放接口，可直接执行sql语句
        @param sql:
        @return:

        @deprecated 已弃用
        """
        assert isinstance(sql, (str, unicode))
        return MZService.db.select(sql)

    @staticmethod
    def execute_insert(sql, para):
        """
        直接执行的insert语句
        @param sql:
        @param para:
        @return:
        """
        return MZService.db.insert2(sql, para)

    @staticmethod
    def execute_update(sql, para=None):
        """

        @param sql:
        @param para:
        @return:
        """
        return MZService.db.update(sql, para)

    @classmethod
    def obj2pyo(cls, data, patterns):
        """
        @brief 将返回的数据按照既定格式格式化.

        @param data:
        @param patterns:
        @return:

        @deprecated 目前的做法是,利用数据库表的列名作为返回字典的key. 因此,该函数目前被弃用
        """
        assert len(data) == len(patterns)
        return dict(zip(patterns, data))

    def _format_patterns(self, model_obj, fields=None):
        """
        @brief 依据Model的字段返回生成字典key的列表

        @param model_obj: Django Model 示例
        @param fields:  select的字段
        @return:

        @deprecated 目前的做法是,利用数据库表的列名作为返回字典的key. 因此,该函数目前被弃用
        """
        assert isinstance(model_obj, ModelBase)
        if fields:
            assert isinstance(fields, (list, tuple))
            return fields
        return list(str(field).split('.')[-1] for field in model_obj._meta.fields)

    def __get_function(self, what='*', where=None, conditions=None, limit=None, order_by=None):
        """
        get　模式函数
        :param where:
        :param conditions:
        :param limit:
        :param order_by:
        :return:
        """
        return self.db.select(what=what, where=where, conditions=conditions, limit=limit, order_by=order_by)

    def __get_all_function(self, item, what='*', limit=None, order_by=None):
        """
        @brief get_all_xx 函数的模板函数. get_all_xx 会调用 get_xx
        @param item: 用以构造get_xx的xx部分
        @param limit: 切片
        @param order_by: 排序
        @return 字典的列表
        """
        return getattr(self, 'get_%s' % item)(what=what, limit=limit, order_by=order_by)

    def __insert_function(self, *args, **kwargs):
        """
        insert　模式函数
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def __update_function(self, *args, **kwargs):
        """
        update　模式函数
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def __delete_function(self, *args, **kwargs):
        """
        delete 模式函数
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def __function_factory(self, func, item):
        """
        包装模式函数(get_xx, insert_xx, update_xx, delete_xx)
        :param func:
        :param item:
        :return:
        """
        def __wrapper(*args, **kwargs):
            return func(where=self.factory_functions[item].db_table, *args, **kwargs)
        return __wrapper

    def __all_function_factory(self, func, item):
        def __wrapper(*args, **kwargs):
            return func(item, *args, **kwargs)
        return __wrapper

    def __getattr__(self, item):
        """
        根据调研名称获取对应的函数
        :param item:
        :return:
        """
        if item in list('get_all_%s' % x for x in self.factory_functions):  # get_all_xx
            return self.__all_function_factory(self.__get_all_function, item.split('get_all_')[1])
        elif item in list('get_%s' % x for x in self.factory_functions):
            return self.__function_factory(self.__get_function, item.split('get_')[1])
        elif item in list('insert_%s' % x for x in self.factory_functions):
            return self.__function_factory(self.__insert_function, item.split('insert_')[1])
        elif item in list('update_%s' % x for x in self.factory_functions):
            return self.__function_factory(self.__update_function, item.split('update_')[1])
        elif item in list('delete_%s' % x for x in self.factory_functions):
            return self.__function_factory(self.__delete_function, item.split('delete_')[1])

class Pager(MZService):
    """
    简单的分页类
    """
    def __init__(self, sql, count_sql, number_each_page=10):
        """

        @param number_each_page:
        @return:
        """
        assert isinstance(number_each_page, int)
        self.sql = sql
        # self.count_sql = 'select count(*) from {}'.format(self.sql.split('from')[1])  #  无法应付更加复杂的查询
        # self.count_sql = 'select count(*) from (%s) as count' % self.sql
        self.count_sql = count_sql
        self.count_each_page = number_each_page
        self.page = 0
        self.total = self.db.select(self.count_sql)[0].values()[0]

    def page_total(self):
        if self.total % self.count_each_page > 0:
            return self.total/self.count_each_page + 1
        return self.total/self.count_each_page

    def data_total(self):
        return self.total

    def page_data(self, page):
        assert isinstance(page, int)
        self.page = page
        start, offset = self.__get_offset(page)
        return self.db.select('%s limit %s, %s' % (self.sql, start, offset))

    def page_list(self):
        result = []
        if self.page_total() <= 10:
            result.extend(range(1, self.page_total()+1))
        else:
            if self.page > 5:
                if self.page < self.page_total()-5:
                    result.extend(range(self.page-5, self.page))
                    result.extend(range(self.page, self.page+5))
                else:
                    result.extend(range(self.page_total()-9, self.page_total()+1))
            else:
                result.extend(range(1, 11))
        return result

    def __get_offset(self, page):
        return (page-1) * self.count_each_page, self.count_each_page

    def page_safe(self, page):
        num_pages = self.page_total()
        if num_pages != 0 and page > num_pages:
            page = num_pages
        return page

    def get_page_info(self, page, page_num, pages=None):
        """
        @brief 不知道这段代码在干嘛。暂时先从语法上优化

        @param page:
        @param page_num:
        @param pages:
        @return:

        @todo 搞清楚这段代码到底在做什么。
        """
        pages = range(1, page_num+1) if not pages else pages
        if page_num >= 2:
            pages = pages[1:-1]
        banner = False
        if page_num > 6:
            if page+4 <= page_num:
                banner = True
            if page < 4:
                pages = pages[:4]
            elif page >= page_num-2:
                pages = pages[-4:]
            else:
                pages = pages[page-4:page+1]
        return pages, banner