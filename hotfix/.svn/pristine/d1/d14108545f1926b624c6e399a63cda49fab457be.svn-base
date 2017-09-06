# -*- coding: utf-8 -*-
"""
homepage 的复杂　service.　比如首页的文章，涉及到复杂的sql语句，并且无法清晰归类到实体service
"""

__author__ = 'changfu'

from mz_platform.services.functions.mz_service import MZService

class HomePageService(MZService):
    """

    """
    def __init__(self):
        """

        @return:
        """
        super(HomePageService, self).__init__()

    def get_home_page_article(self, type_id):
        """
        按type_id获取首页的文章，以及与文章关联的career_course的名字，如果无关联的career_course，则返回麦子分享

        @param type_id:
        @return:
        """
        sql = '''
            select distinct na.id, na.title, na.title_image, (case when cc.name is null then '麦子分享' else cc.name end) as name
            from mz_common_newarticle as na
            left join mz_common_careerobjrelation as cor
            on cor.obj_id = na.id and cor.obj_type='ARTICLE' and cor.is_actived = 1
            left join mz_course_careercourse as cc on cor.career_id = cc.id
            where na.article_type_id = %s order by na.publish_date desc limit 6
            ''' % type_id
        return self.execute(sql)




