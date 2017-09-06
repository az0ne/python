# -*- coding:utf-8 -*-
from rest_framework import serializers
from mz_user.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'nick_name', 'description', 'avatar_url', 'position')


