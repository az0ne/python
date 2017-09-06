# -*- coding: utf-8 -*-
__author__ = 'qxoo'

from django import forms
from mz_course.models import Stage, Discounted, CareerCourse


class StageForm(forms.ModelForm):
    error_messages = {
        'image_error': '试学设置错误',
    }

    class Meta:
        model = Stage

    def clean(self):
        # 限制章节试学添加章节
        career_course = self.cleaned_data['career_course']
        lps_version = self.cleaned_data['lps_version']
        is_try = self.cleaned_data['is_try']
        obj = self.instance
        if is_try == True:
            stage_list = Stage.objects.xall().filter(career_course=career_course, lps_version=lps_version).order_by('index')
            for stage in stage_list:
                if stage == obj:
                    break
                if stage.is_try == False:
                    raise forms.ValidationError(
                        self.error_messages['image_error'],
                        code='image_error'
                    )
            return self.cleaned_data
        else:
            return self.cleaned_data


class DiscountedForm(forms.ModelForm):
    error_messages = {
        'discount_error': '优惠折扣范围为0-40，表示用户享受全款最多40%的优惠，合同价为全款的60%',
        'cash_error': '优惠金额范围为正整数',
    }

    class Meta:
        model = Discounted

    def clean(self):
        # 限制章节试学添加章节
        content = self.cleaned_data.get('content')
        type = self.cleaned_data.get('type')
        if type == '1':
            if not (0 <= content <= 40):
                raise forms.ValidationError(
                    self.error_messages['discount_error'],
                    code='discount_error'
                )
        if type == '2':
            if content < 0:
                raise forms.ValidationError(
                    self.error_messages['cash_error'],
                    code='cash_error'
                )
        return self.cleaned_data


class CareerCourseForm(forms.ModelForm):
    error_messages = {
        'try_price_error': '试学价格<官网价格',
        'discounted_price_error': '优惠金额不能大于等于全款价格',
    }

    class Meta:
        model = CareerCourse

    def clean(self):
        # 限制章节试学添加章节
        try_price = self.cleaned_data.get('try_price')
        net_price = self.cleaned_data.get('net_price')
        discounted = self.cleaned_data.get('discounted')
        if try_price == None or net_price == None:
            return self.cleaned_data
        if discounted and discounted.type == '2' and discounted.content >= net_price:
            raise forms.ValidationError(
                self.error_messages['discounted_price_error'],
                code='discounted_price_error'
            )
        if try_price >= net_price:
            raise forms.ValidationError(
                self.error_messages['try_price_error'],
                code='try_price_error'
            )
        return self.cleaned_data
