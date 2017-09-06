# -*- coding: utf-8 -*-
__author__ = 'qxoo'

from mz_lps.models import Class, ClassStudents
from mz_user.models import UserProfile
from mz_course.models import CareerCourse, Institute
from mz_lps2.models import CourseUserTask
from mz_lps3.models import ClassRank, ClassMeetingRelation, ClassMeetingAttendance
from mz_pay.models import UserPurchase
from django.http import HttpResponse
import xlwt
from mz_usercenter.student.interface_study import get_study_base
from mz_usercenter.student.interface_job_info import get_job_info_by_class_student
from django.shortcuts import get_object_or_404


class StudentClassRank(object):
    '''
    获取课程班级排名
    '''

    def __init__(self, user_id, careercourse_id):
        self.user_id = user_id
        self.careercourse_id = careercourse_id
        clazz = Class.objects.xall().filter(students=self.user_id, career_course=self.careercourse_id)
        if not clazz:
            self.clazz = None
            self.is_lps3 = None
        else:
            self.clazz = clazz[0]
            self.is_lps3 = True if clazz[0].lps_version == '3.0' else False

    def get_lps2_rank(self):
        from mz_common.views import current_user_ranking, all_stu_ranking

        user = UserProfile.objects.get(id=self.user_id)
        careercourse = CareerCourse.objects.get(id=self.careercourse_id)

        curren_stu_ranking = current_user_ranking(careercourse, user)
        course_lists = CourseUserTask.objects.filter( \
            user=user, user_class=self.clazz, status=2).order_by("-id")
        # if curren_stu_ranking !="NotSignUp":
        if len(course_lists) > 0 and self.clazz.is_normal():
            all_stu = all_stu_ranking(careercourse, user)
            if course_lists[0].rank_in_class:
                # print course_lists[0].rank_in_class
                return str(course_lists[0].rank_in_class) + '/' + str(len(all_stu))
            else:
                return '--/' + str(len(all_stu))
        elif curren_stu_ranking != "NotSignUp" and self.clazz.is_normal():
            return '--/--'
        else:
            return '未报名'

    def get_lps3_rank(self):
        '''
        get lps3 student rank
        :return:
        '''
        if Class.objects.xall().get(id=self.clazz.id).is_experience():
            return '未报名'
        class_rank = ClassRank.objects.filter(class_id=self.clazz.id, student_id=self.user_id).order_by('-id').first()
        try:
            class_students = ClassStudents.objects.get(student_class=self.clazz, user_id=self.user_id)
        except Exception:
            return '未报名'
        student_total = str(self.clazz.current_student_count)
        return str(class_rank.rank) + '/' + student_total if class_rank else '--/--'

    def get_rank(self):
        '''
        获取排名
        '''
        if self.clazz:
            if self.is_lps3:
                return self.get_lps3_rank()
            else:
                return self.get_lps2_rank()
        else:
            return '未报名'


def pretty_format(dt):
    tmp = (u'周一', u'周二', u'周三', u'周四', u'周五', u'周六', u'周日')
    date = dt.date()
    return u"%s %s %s" % (date.isoformat(), tmp[date.weekday()], dt.time().strftime('%H:%M'))


class ExportStudentInfo(object):
    '''
    导出学生学籍信息
    '''

    def __init__(self, **kwargs):
        '''
        初始化数据
        :param k:
        :return: None
        '''
        self.student_id = kwargs.get('student_id', '')
        self.class_id = kwargs.get('class_id', '')

        if not self.student_id or not self.class_id:
            raise KeyError()
            #
            # cls = Class.objects.xall().get(id=self.class_id)
            # self.domain_name = self._get_course_domain(cls.career_course.institute_id)

    def export_excel_for_studentinfo(self):
        '''
        导出学生学籍信息为excel
        :return:
        '''
        self.info = self.student_info()

        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet((u"%s-学籍信息" % self.info['name']).encode('utf-8'))

        font_bold = xlwt.Font()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        font_bold.bold = True
        style_bold = xlwt.XFStyle()
        style_title = xlwt.XFStyle()
        style_bold.font = font_bold
        style_title.font = font_bold
        style_title.alignment = alignment

        sheet.write_merge(0, 1, 0, 7, '%s' % self.info['name'], style=style_title)

        sheet.write_merge(2, 3, 0, 7, '基础信息', style=style_bold)

        sheet.write_merge(4, 4, 0, 1, '性别 : %s' % str(self.info['sex']))
        sheet.write_merge(4, 4, 2, 3, '年龄 : %s' % str(self.info['age']))
        sheet.write_merge(4, 4, 4, 7, 'QQ : %s' % str(self.info['qq']))
        sheet.write_merge(5, 5, 0, 3, '电话 : %s' % str(self.info['mobile']))
        sheet.write_merge(5, 5, 4, 7, '邮箱 : %s' % str(self.info['mail']))
        sheet.write_merge(6, 6, 0, 7, '麦子账号 : %s' % str(self.info['account']))

        sheet.write_merge(7, 7, 0, 3, '意向就业城市 : %s' % str(self.info['intention_job_city']))
        sheet.write_merge(7, 7, 4, 7, '毕业院校 : %s' % str(self.info['graduate_institution']))
        sheet.write_merge(8, 8, 0, 3, '在职与否 : %s' % str(self.info['in_service']))
        sheet.write_merge(8, 8, 4, 7, '工作年限 : %s' % str(self.info['service_year']))
        sheet.write_merge(9, 9, 0, 7, '身份证号 : %s' % str(self.info['id_number']))

        sheet.write_merge(10, 10, 0, 7, '地址 : %s' % str(self.info['address']))
        sheet.write_merge(11, 11, 0, 7, '自我评价 : %s' % str(self.info['description']))

        sheet.write_merge(12, 12, 0, 7, '学习信息', style=style_bold)

        sheet.write_merge(13, 13, 0, 3, '入学时间 : %s' % str(self.info['start_study_time']))
        sheet.write_merge(13, 13, 4, 7, '学历 : %s' % str(self.info['education']))

        if self.info['study_goal']:
            sheet.write_merge(14, 14, 0, 3, '学习目标 : %s' % str(self.info['study_goal']))
        else:
            sheet.write_merge(14, 14, 0, 3, '学习目标 : %s' % str(self.info['user_study_goal']))

        sheet.write_merge(14, 14, 4, 7, '学习基础 : %s' % str(self.info['study_base']))

        sheet.write_merge(15, 15, 0, 3, '带班老师 : %s' % str(self.info['teacher_name']))
        sheet.write_merge(15, 15, 4, 7, '教务老师 : %s' % str(self.info['eduadmin_name']))

        row_index = 15
        i = 0
        for study_base in self.info['user_study_base_list']:
            if i % 2 == 0:
                row_index = row_index + 1
                sheet.write_merge(row_index, row_index, 0, 3, '%s : %s' % (study_base['name'], study_base['level']))
            else:
                sheet.write_merge(row_index, row_index, 4, 7, '%s : %s' % (study_base['name'], study_base['level']))
            i = i + 1

        row_index = row_index + 1
        sheet.write_merge(row_index, row_index, 0, 7, '支付信息', style=style_bold)

        row_index1 = row_index + 1
        row_index2 = row_index + 2
        row_index3 = row_index + 3
        row_index4 = row_index + 4
        for i, pay_info in enumerate(self.info['pay']):
            sheet.write_merge(row_index1 + i * 4, row_index + i * 4, 0, 7, '订单%s:' % str(i + 1))
            sheet.write_merge(row_index2 + i * 4, row_index + i * 4, 0, 3, '支付课程 : %s' % str(pay_info['pay_course']))
            sheet.write_merge(row_index2 + i * 4, row_index + i * 4, 4, 7, '支付金额 : %s' % str(pay_info['pay_amount']))
            sheet.write_merge(row_index3 + i * 4, row_index + i * 4, 0, 3, '支付类型 : %s' % str(pay_info['pay_type']))
            sheet.write_merge(row_index3 + i * 4, row_index + i * 4, 4, 7, '支付方式 : %s' % str(pay_info['pay_way']))
            sheet.write_merge(row_index4 + i * 4, row_index + i * 4, 0, 3, '订单号 : %s' % str(pay_info['pay_no']))
            sheet.write_merge(row_index4 + i * 4, row_index + i * 4, 4, 7,
                              '交易号 : %s' % str(pay_info['pay_complete_no']))

        row_index = row_index1 + len(self.info['pay']) * 4 + 1
        sheet.write_merge(row_index, row_index, 0, 7, u'班会考勤', style=style_bold)
        sheet.write_merge(row_index + 1, row_index + 1, 0, 2, u'班会时间', style=style_bold)
        sheet.write_merge(row_index + 1, row_index + 1, 3, 5, u'班会主题', style=style_bold)
        sheet.write_merge(row_index + 1, row_index + 1, 6, 7, u'考勤', style=style_bold)

        for i, att in enumerate(self.info['attendances']):
            sheet.write_merge(row_index + 2 + i, row_index + 2 + i, 0, 2, att[0])
            sheet.write_merge(row_index + 2 + i, row_index + 2 + i, 3, 5, att[1])
            sheet.write_merge(row_index + 2 + i, row_index + 2 + i, 6, 7, att[2])

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = (u'attachment; filename=%s-学籍信息.xls' % self.info['name']).encode('utf-8')

        book.save(response)
        return response

    def _load_attendance(self):
        objs1 = ClassMeetingRelation.objects.filter(
            class_id=self.class_id,
            class_meeting__status=1,  # 已结束
        ).values('class_meeting__id', 'class_meeting__startline', 'class_meeting__content').order_by(
            'class_meeting__id')
        tmp1 = list(obj['class_meeting__id'] for obj in objs1)
        objs2 = ClassMeetingAttendance.objects.filter(
            student_id=self.student_id,
            class_meeting_id__in=tmp1
        )
        tmp2 = dict((obj.class_meeting_id, obj) for obj in objs2)
        ret = list()
        for m in objs1:
            dt = m['class_meeting__startline']
            att = tmp2.get(m['class_meeting__id'])
            ret.append(
                (pretty_format(dt),
                 m['class_meeting__content'],
                 att.status_text if att else u"缺勤")
            )
        return ret

    # def _get_course_domain(self, institute_id):
    #     institutes = Institute.objects.filter(id=institute_id)
    #     if not institutes:
    #         return '技术类'
    #     institute_name = institutes[0].name
    #     if '软件开发' == institute_name or '智能硬件' == institute_name:
    #         return '技术类'
    #     elif '设计' == institute_name:
    #         return '设计类'
    #     elif '产品运营' == institute_name:
    #         return '产品运营'
    #
    # def _get_user_study_base(self):
    #     user_skills = UserProfessionalSkill.objects.filter(skill__domain=self.domain_name,
    #                                                        user_id=self.student_id)
    #     study_base_list = []
    #
    #     if user_skills:
    #         for s in user_skills:
    #             study_base_list.append(dict(id=s.skill.id, name=s.skill.skill,
    #                                         level=UserProfessionalSkill.LEVEL_CHOICES[s.level]))
    #     return study_base_list

    # def _get_user_study_goal(self):
    #     cls = Class.objects.xall().get(id=self.class_id)
    #     study_goals = UserStudyGoal.objects.filter(user_id=self.student_id,
    #                                                career_course_id=cls.career_course.id)
    #     user_study_goal = ''
    #     if study_goals:
    #         user_study_goal = UserStudyGoal.GOAL_CHOICES[study_goals[0].goal]
    #
    #     return user_study_goal

    def student_info(self):
        '''
        获取学生学籍信息
        :return:
        '''
        user = UserProfile.objects.get(id=self.student_id)
        class_student = ClassStudents.objects.get(student_class__id=self.class_id, user=user)
        user_purchase_list = UserPurchase.objects.filter(pay_status=1, user=user,
                                                         pay_careercourse=class_student.student_class.career_course)
        cls = class_student.student_class
        eduadmin = cls.edu_admin

        job_info = get_job_info_by_class_student(class_student)
        info = {'teacher_name': cls.teacher_name,
                'eduadmin_name': eduadmin.staff_name if eduadmin else '',
                'name': user.real_name if user.real_name else user.nick_name,
                'sex': user.get_gender_display() if user.get_gender_display() else '',
                'age': user.get_user_age() if user.get_user_age() else '',
                'qq': user.qq if user.qq else '',
                'mobile': user.mobile if user.mobile else '',
                'mail': user.email if user.email else '',
                'account': user.username if user.username else '',
                'address': user.address if user.address else '',
                'description': user.description if user.description else '',
                'start_study_time': class_student.created.strftime("%Y-%m-%d") if class_student.created else '',
                'education': job_info.get('degree', ''),
                'study_goal': user.study_goal if user.study_goal else '',
                'study_base': user.study_base if user.study_base else '',
                'intention_job_city': job_info.get('intention_job_city', ''),
                'graduate_institution': job_info.get('graduate_institution', ''),
                'in_service': job_info.get('in_service', ''),
                'service_year': job_info.get('service_year', ''),
                'id_number': user.id_number if user.id_number else '暂无',
                'pay': [
                    {
                        'num': '订单%s' % str(i + 1),
                        'pay_course': user_purchase.pay_careercourse.name if user_purchase.pay_careercourse.name else '',
                        'pay_amount': user_purchase.pay_money if user_purchase.pay_money is not None else '',
                        'pay_type': user_purchase.get_pay_type_display() if user_purchase.get_pay_type_display() else '',
                        'pay_way': user_purchase.get_pay_way_display() if user_purchase.get_pay_way_display() else '',
                        'pay_no': user_purchase.order_no if user_purchase.order_no else '',
                        'pay_complete_no': user_purchase.trade_no if user_purchase.trade_no else ''
                    }
                    for i, user_purchase in enumerate(user_purchase_list)
                    ],
                'attendances': self._load_attendance(),
                'position': job_info.get('position', ''),
                'industry': job_info.get('industry', ''),
                'to_industry': job_info.get('to_industry', ''),
                'user_study_goal': job_info.get('study_goal', ''),
                'user_study_base_list': get_study_base(user.id,
                    get_object_or_404(Institute, id=cls.career_course.institute_id).name),
                }

        return info


def testExportStudentInfo__student_info(class_id, student_id):
    print ExportStudentInfo(class_id=class_id, student_id=student_id).student_info()


def testExportStudentInfo(info):
    print ExportStudentInfo(info=info).export_excel_for_studentinfo()


def testClassRank(userid, careercourseid):
    print StudentClassRank(userid, careercourseid).get_rank()
