# -*- coding: utf-8 -*-

__author__ = 'changfu'

import datetime

from mz_platform.services.functions.mz_service import MZService, Orm2Str
from mz_platform.orms.mz_common import Discuss

# 新架构需要的接口
import db

class DiscussService(MZService):
    """课程service

    """

    factory_functions = dict(discuss=Discuss)

    def __init__(self):
        """
        :return:
        """
        super(DiscussService, self).__init__()

    def new_discuss(self, object_id, user_id, parent_id, object_type='LESSON', comment='', nick_name=u'匿名',
                    head='', create_date=None):
        """
        @brief 添加新的评论

        @param object_id: 关联的对象id
        @param user_id: 用户id
        @param parent_id: 父评论id
        @param object_type: 关联对象类型, 默认为lesson
        @param comment: 评论内容
        @param nick_name: 用户昵称，默认为匿名
        @param head: 用户头像，默认为''
        @param create_date: 创建时间，默认为当前时间
        @return:

        @note: 一个典型的用法如下：
               discuss_service.new_discuss(dict(object_id=2, object_type='LESSON', comment='just for test测试哈哈哈',
                                                user_id=8, nick_name='我是QA', head='temp/temp/2.img',
                                                create_date=datetime.datetime.now(),parent_id=8))
        """
        # data = Orm2Str.orm2str(op_type='insert', where=Discuss,
        #                        values=dict(object_id=object_id, user_id=user_id, parent_id=parent_id,
        #                                    object_type=object_type, comment=comment, nick_name=nick_name, head=head,
        #                                    create_date=create_date if create_date else datetime.datetime.now()))
        # return self.db.insert(**data)
        sql = '''
            insert into mz_common_newdiscuss
            (object_id, object_type, comment, user_id, nick_name, head, create_date, parent_id)
            values
            (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
        new_id = self.execute_insert(sql, (object_id, object_type, comment, user_id, nick_name, head, create_date, parent_id))
        if object_type.upper() == 'ARTICLE':  # 讨论的类型为文章
            db.api.article.article.add_count(object_id, 'replay_count')
        return new_id
