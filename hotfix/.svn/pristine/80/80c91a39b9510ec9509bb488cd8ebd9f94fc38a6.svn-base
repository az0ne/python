#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import urllib, urllib2, json
from datetime import datetime
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"/..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
import django
django.setup()
from maiziedu_website import settings
from mz_lps2.models import ClassMeetingTaskVideo510,ClassMeetingTaskVideo,LiveRoom
from mz_lps3.models import ClassMeetingVideo,ClassMeetingRelation,LiveRoom as LPS3LiveRoom
import db.api.onevone.meeting



#包含 lps2.0 和lps 3.0班会直播历史记录获取获取
class ClassMeetingUrl(object):

    def __init__(self,start_time,end_time):
        start_datetime = start_time.strftime("%Y-%m-%d %H:%M:%S")
        finish_datetime = end_time.strftime("%Y-%m-%d %H:%M:%S")
        self.data_list510=self.get_liveroom_info(settings.LIVE_ROOM_GET_API510,start_datetime,finish_datetime)
        self.data_list=self.get_liveroom_info(settings.LIVE_ROOM_GET_API,start_datetime,finish_datetime)

    def get_liveroom_info(self,url,start_datetime,finish_datetime):
        values = {
                'loginName':settings.LIVE_ROOM_USERNAME,
                'password':settings.LIVE_ROOM_PASSWORD,
                'sec':'true',
                'startTime':start_datetime,
                "endTime":finish_datetime,
                "pageNo":1
                }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result = json.loads(response.read())
        data_list = result.get('list',[])
        return data_list

    def get_url510(self):
        for data in self.data_list510:
            start_time = data.get('recordStartTime')
            end_time = data.get('recordEndTime')
            create_time = data.get('createdTime')
            play_id = data.get('id','')
            room_id = data.get('roomId','')
            start_time = datetime.fromtimestamp(start_time/1000.0)
            end_time = datetime.fromtimestamp(end_time/1000.0)
            create_time = datetime.fromtimestamp(create_time/1000.0)
            creator = data.get('creator','')
            size = data.get('size',0)
            name = data.get('name',0)

            live_room = None
            live_rooms = LiveRoom.objects.filter(live_id=room_id)
            if live_rooms:
                live_room = live_rooms[0]
                print start_time,end_time,room_id,end_time-start_time
                if not ClassMeetingTaskVideo510.objects.filter(play_id=play_id).count():
                    ClassMeetingTaskVideo510(live_room=live_room,play_id=play_id,create_time=create_time,
                                          creator=creator,size=size,name=name,record_start_time=start_time,record_end_time=end_time).save()

    def get_url511(self):
        for data in self.data_list:
            # start_time = data.get('recordStartTime')
            # end_time = data.get('recordEndTime')
            create_time = data.get('createdTime')
            play_id = data.get('id','')
            room_id = data.get('roomId','')
            # start_time = datetime.fromtimestamp(start_time/1000.0)
            # end_time = datetime.fromtimestamp(end_time/1000.0)
            create_time = datetime.fromtimestamp(create_time/1000.0)
            subject = data.get('subject','')
            token = data.get('token','')
            play_url = data.get('url','')
            creator = data.get('creator','')
            description = data.get('description','')
            number = data.get('number','')
            record_id = data.get('recordId','')

            live_room = None
            live_rooms = LiveRoom.objects.filter(live_id=room_id)
            if live_rooms:
                live_room = live_rooms[0]
                if not ClassMeetingTaskVideo.objects.filter(play_id=play_id).count():
                    details = ClassMeetingTaskVideo510.objects.filter(play_id=record_id)
                    if details:
                        if (details[0].record_end_time -details[0].record_start_time).seconds >= 60:
                            ClassMeetingTaskVideo(live_room=live_room,play_id=play_id,create_time=create_time,url=play_url,
                                                  creator=creator,description=description,number=number,
                                                  token=token,play_subject=subject,record_id=record_id).save()

    def delete_2week_video(self):
        two_week_ago = datetime.now() - datetime.timedelta(days=14)
        date_from = datetime(two_week_ago.year,two_week_ago.month,two_week_ago.day,0,0,0)
        class_videos = ClassMeetingTaskVideo.objects.filter(record_start_time__lte=date_from)
        for class_video in class_videos:
            url = settings.LIVE_ROOM_DELETE_API
            play_id = class_video.play_id
            values = {
                'loginName':settings.LIVE_ROOM_USERNAME,
                'password':settings.LIVE_ROOM_PASSWORD,
                'sec':'true',
                'coursewareId':play_id,
            }

            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            result = json.loads(response.read())
            if result.get('code',-1) == 1:
                class_video.delete()

    def update_lps3video(self):
        """更新lps 产生的视频信息"""
        record_dict={}#保持视频的记录信息
        for data in self.data_list510:
            start_time = data.get('recordStartTime')
            end_time = data.get('recordEndTime')
            # create_time = data.get('createdTime')
            play_id = data.get('id','')
            # room_id = data.get('roomId','')
            start_time = datetime.fromtimestamp(start_time/1000.0)
            end_time = datetime.fromtimestamp(end_time/1000.0)
            # create_time = datetime.fromtimestamp(create_time/1000.0)
            # creator = data.get('creator','')
            # size = data.get('size',0)
            # name = data.get('name',0)
            record_dict[play_id]=[start_time,end_time]

        #获取视频信息
        for data in self.data_list:
            create_time = data.get('createdTime')
            play_id = data.get('id','')
            room_id = data.get('roomId','')
            create_time = datetime.fromtimestamp(create_time/1000.0)
            subject = data.get('subject','')
            token = data.get('token','')
            play_url = data.get('url','')
            creator = data.get('creator','')
            description = data.get('description','')
            number = data.get('number','')
            record_id = data.get('recordId','')
            #录取的时间必须超过60秒
            time_lst=record_dict.get(record_id)
            if time_lst and (time_lst[1] -time_lst[0]).seconds >= 60:
                print time_lst,room_id
                #记录ID信息没有收录入班会视频
                if ClassMeetingVideo.objects.filter(play_id=play_id).count() == 0:
                    liveroom=LPS3LiveRoom.objects.filter(live_id=room_id)
                    if liveroom:
                        class_meeting_relation_lst=ClassMeetingRelation.objects.filter(class_meeting=liveroom[0].class_meeting)
                        for class_meeting_relation in class_meeting_relation_lst:
                            ClassMeetingVideo(class_id=class_meeting_relation.class_id,live_id=room_id,play_id=play_id,
                                                create_time=create_time,url=play_url,
                                                creator=creator,description=description,number=number,
                                                token=token,play_subject=subject).save()
                # 4.0 1v1直播
                db.api.onevone.meeting.save_video_record(room_id, play_url, token)
if __name__ == '__main__':
    now_time = datetime.now()
    # search_start = datetime(2015, 12, 5, 0, 0, 0)
    # search_end = datetime(2015, 7, 15, 23, 59, 59)
    search_start = datetime(now_time.year, now_time.month, now_time.day, 0, 0, 0)
    search_end = datetime(now_time.year, now_time.month, now_time.day, 23, 59, 59)
    class_meeting_url = ClassMeetingUrl(search_start,search_end)

    # class_meeting_url.get_url510()
    # class_meeting_url.get_url511()
    class_meeting_url.update_lps3video()