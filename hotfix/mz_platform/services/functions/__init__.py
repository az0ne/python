# -*- coding: utf-8 -*-

"""
server接口的定义和引用应遵守如下规则：

1. 针对实体定义服务，实体间的关系，拆分到实体服务之内。例如
   Course 和 CareerCourse 为两个实体，因此分别有CourseService 和 CareerCourseService
   Course 和 CareerCourse 有关联关系，如，Course 可能属于多个CareerCourse, 而CareerCurse 可能包含多个Course
   通过Course查找相关的CareerCourse的服务接口，应定义在CourseService内，反之，应定义在CareerCourseService内。
   即，对于两个实体，A 和 B，两者有关联关系，则，由A找B的服务接口定义在A内，由B找A的服务接口定义在B内

2. 对于多实体的关联查询，如由A,B两个实体查找C, 则将服务定义在CService内。例如：
   course_service内，名为get_course_by_career_tag的服务接口。该服务接口通过Career和tag的id查找相关的Course.

3. 对于多实体查找多实体的服务，目前尚未定义，有待讨论。例如
   通过A，B 实体查找C，D实体的相关信息

4. 对于过程，如LPS系统，将服务接口定义于自身的服务内，不再拆分关系。如与LPS相关的服务接口，全部定义与LPSService内。例如：
   获取某个用户报名的企业直通班列表的服务接口，位于LPSService内，而非UserService内。

5. 更为未尽问题需要更多讨论。
"""

__author__ = 'changfu'

