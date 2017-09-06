# -*- coding: utf-8 -*-

__author__ = 'changfu'

from mz_platform.services.functions.mz_service import MZService, Orm2Str

from mz_platform.orms.mz_common import ObjTagRelation

class SearchService(MZService):
    """课程service

    @note get_course 和 get_all_course 在基类MZService中动态生成, 定义如下：
          get_course(what='*', conditions=None, limit=None, order_by=None)
          get_all_course(what='*', limit=None, order_by=None)
    """

    def __init__(self):
        """
        :return:
        """
        super(SearchService, self).__init__()

    def search_by_keywords(self, keywords, obj_type='', what='*', conditions=None, limit=None, order_by=None):
        """
        @brief 按关键字搜索。搜过内容为 老师，文章或者课程

        @param keywords: 搜索的关键字，类型为字符串，或者字符串列表。
        @param obj_type: 搜索类型，类型为字符串，值可以是'COURSE', 'TEACHER', 'ARTICLE'.值为''时，表示全部类型，缺省值为''
        @param what: 需要的字段，类型为列表，如['id', 'name'], 缺省值为'*'
        @param conditions: 额外的条件， 如['id>5', 'name like "%python%"'], 缺省值为None
        @param limit: 切片， 类型为字符串， 如'5, 8', 缺省值为None
        @param order_by: 排序, 类型为字符串, 如'name', 缺省值为None
        @return: 课程信息的字典列表

        @note 调用example:
              search_by_keywords(keywords=['java', 'python'], obj_type='COURSE'
                                 what=['id', 'name'], conditions=['student_count>20'], limit='8, 10'
                                 order_by='-click_count')
              获取关键字为java或者python, 并且student_count>20的课程的id,name字段，从结果的第8条开始取，取10条, 按播放次数排列

        @todo 条件处理支持like
              支持多种类型，目前仅支持course。
              上两步实现之后， 重新实现该函数
        """
        if isinstance(keywords, (str, unicode)):
            like = 'keywords like "%%%s%%"' % keywords
        if isinstance(keywords, list):
            like = ' or '.join(list('keywords like "%%%s%%"' % keyword for keyword in keywords))
        sql = '''
                select mz_course_course.* from mz_course_course
                inner join mz_common_objtagindex on mz_common_objtagindex.obj_id = mz_course_course.id
                where mz_common_objtagindex.obj_type='COURSE' and (%s)
                ''' % like
        if limit:
            sql = '%s limit %s' % (sql, limit)
        if order_by:
            sql = '%s order by %s' % (sql, order_by)
        return self.db.select(sql)
