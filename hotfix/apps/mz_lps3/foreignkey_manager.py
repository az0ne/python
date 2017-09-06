# -*- coding: utf-8 -*-
__author__ = 'qxoo'

from django.db import router, models
import exceptions


class CustomManagerForeignKey(models.ForeignKey):
    '''
    定制外键manager路由
    '''
    def __init__(self, *args, **kwargs):
        if 'manager' in kwargs:
            self.customManager = kwargs['manager']()
            del kwargs['manager']
        else:
            self.customManager = None
        super(CustomManagerForeignKey, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        field = super(CustomManagerForeignKey, self).formfield(**kwargs)
        if self.customManager:
            field.queryset = self.customManager
        return field

    def validate(self, value, model_instance):
        if self.rel.parent_link:
            return
        super(models.ForeignKey, self).validate(value, model_instance)
        if value is None:
            return
        if self.customManager:
            manager = self.customManager
        else:
            using = router.db_for_read(model_instance.__class__, instance=model_instance)
            manager = self.rel.to._default_manager.using(using)
        qs = manager.filter(**{self.rel.field_name: value})
        qs = qs.complex_filter(self.rel.limit_choices_to)
        if not qs.exists():
            raise exceptions.ValidationError(self.error_messages['invalid'] % {'model': self.rel.to._meta.verbose_name, 'pk': value})