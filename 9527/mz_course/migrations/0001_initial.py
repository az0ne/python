# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CareerCatagory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u4e13\u4e1a\u65b9\u5411')),
            ],
            options={
                'verbose_name': '\u4e13\u4e1a\u65b9\u5411',
                'verbose_name_plural': '\u4e13\u4e1a\u65b9\u5411',
            },
            bases=(models.Model,),
        ),
    ]
