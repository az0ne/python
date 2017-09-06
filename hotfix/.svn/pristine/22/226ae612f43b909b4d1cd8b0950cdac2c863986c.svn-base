#!/usr/bin/env python
# -*- coding: utf8 -*-

from mz_platform.objects.sql_result_wrapper import SqlResultWrapper
from mz_platform.services.functions.mz_service import MZService


class CareerCourse(SqlResultWrapper):
    """
    @brief      CareerCourse

    支持以下属性:
    id,
    name,
    short_name,
    image,
    description,
    student_count,
    market_page_url,
    course_color,
    discount,
    click_count,
    index,
    seo_description,
    seo_keyword,
    seo_title,
    app_image,
    course_scope,
    balance_product_id,
    product_id,
    status,
    app_career_image,
    guide_line_page,
    qq,
    qq_key,
    is_hot,
    brief_intro,
    institute_id,
    course_color_px,
    description_px,
    id_53kf,
    image_px,
    image_px_2,
    seo_description_px,
    seo_keyword_px,
    seo_title_px,
    lps3_guide_task_id,
    contract_price,
    discounted_id,
    net_price,
    try_price

    """

    @property
    def course_total(self):
        temp_sql = """select count(c.id) as total
                      from mz_common_careerobjrelation as  ccr
                      inner join mz_course_course c on ccr.obj_id = c.id
                      where ccr.obj_type = 'COURSE' and ccr.career_id = {};"""
        data = MZService.execute_select(temp_sql.format(self.id))
        return data[0]['total'] if data and 'total' in data[0] else 0

    @property
    def need_days(self):
        temp_sql = """select sum(c.need_days) as total
                      from mz_common_careerobjrelation ccr
                      inner join mz_course_course c on ccr.obj_id = c.id
                      where ccr.obj_type = 'COURSE' and ccr.career_id = {};"""
        data = MZService.execute_select(temp_sql.format(self.id))
        return (data[0]['total'] if data and 'total' in data[0]
                                         and data[0]['total'] else 0)
