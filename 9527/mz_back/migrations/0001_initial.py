# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u59d3\u540d')),
                ('password', models.CharField(max_length=100, verbose_name='\u5bc6\u7801')),
            ],
            options={
                'verbose_name': '\u540e\u53f0\u7528\u6237\u8868',
                'verbose_name_plural': '\u540e\u53f0\u7528\u6237\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdminRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField(verbose_name='\u7528\u6237id')),
                ('role_id', models.IntegerField(verbose_name='\u89d2\u8272id')),
            ],
            options={
                'verbose_name': '\u540e\u53f0\u7528\u6237\u89d2\u8272\u8868',
                'verbose_name_plural': '\u540e\u53f0\u7528\u6237\u89d2\u8272\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u83dc\u5355\u540d\u5b57')),
                ('url', models.URLField(null=True, verbose_name='\u83dc\u5355url', blank=True)),
            ],
            options={
                'verbose_name': '\u6743\u9650\u8868',
                'verbose_name_plural': '\u6743\u9650\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u7528\u6237\u89d2\u8272')),
            ],
            options={
                'verbose_name': '\u89d2\u8272\u8868',
                'verbose_name_plural': '\u89d2\u8272\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoleMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role_id', models.IntegerField(verbose_name='\u89d2\u8272id')),
                ('menu_id', models.IntegerField(verbose_name='\u83dc\u5355id')),
            ],
            options={
                'verbose_name': '\u89d2\u8272\u6743\u9650\u8868',
                'verbose_name_plural': '\u89d2\u8272\u6743\u9650\u8868',
            },
            bases=(models.Model,),
        ),
    ]
