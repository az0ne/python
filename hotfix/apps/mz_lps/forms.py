# -*- coding: utf-8 -*-
__author__ = 'qxoo'

from django import forms
from models import Quiz


class QuizForm(forms.ModelForm):
    error_messages = {
        'image_error': "试卷题目不能添加超过20个",
        }

    class Meta:
        model = Quiz

    def clean_paper(self):
        """
        限制试卷题目不能超过20个
        :return:
        """
        if self.cleaned_data['paper'].quiz_set.count() >= 20:
            raise forms.ValidationError(
                self.error_messages['image_error'],
                code='image_error'
            )
        else:
            return self.cleaned_data['paper']