import xadmin
from models import *


class RecommendKeywordsAdmin(object):
    list_display = ('name', 'index', 'id')
    search_fields = ['name', 'id']
    list_editable = ['index','name','url']
    ordering = ('index',)

class AdAdmin(object):
    list_display = ('title', 'image', 'back_image', 'url', 'index', 'id')
    search_fields = ['title', 'id']
    list_editable = ['index','title','url']
    ordering = ('index',)

class RecommendPointAdmin(object):
    list_display = ('title', 'image', 'url', 'index', 'id')
    search_fields = ['title', 'id']
    list_editable = ['index','title','url']
    ordering = ('index',)

class NewsAdmin(object):
    list_display = ('title', 'url', 'type', 'index', 'id')
    search_fields = ['title', 'id']
    list_editable = ['index','title','url']
    list_filter = ('type',)
    ordering = ('index',)

class LiveStudyAdmin(object):
    list_display = ('title', 'image', 'original_price', 'current_price', 'lecturer', 'limit_count', 'real_count',
                    'url', 'index', 'id')
    search_fields = ['title', 'id', 'lecturer']
    list_editable = ['index','title','url']
    ordering = ('index',)

class CourseInfoAdmin(object):
    list_display = ('title', 'image','url', 'type', 'studying_count', 'lesson_count', 'lecturer', 'index', 'id')
    search_fields = ['title', 'id', 'lecturer']
    list_editable = ['index','title','url']
    list_filter = ('type',)
    ordering = ('index',)

class CareerPathAdmin(object):
    list_display = ('name', 'image', 'url', 'monthly_salary', 'description', 'index', 'id')
    search_fields = ['name', 'id']
    list_editable = ['index','name','url']
    ordering = ('index',)

class GoldLecturerAdmin(object):
    list_display = ('name', 'image', 'url', 'index', 'id')
    search_fields = ['name', 'id']
    list_editable = ['index','name','url']
    ordering = ('index',)

class CooperationAdmin(object):
    list_display = ('name', 'image', 'url', 'type', 'index', 'id')
    search_fields = ['name', 'id']
    list_editable = ['index','name','url']
    list_filter = ('type',)
    ordering = ('index',)

class AdImageAdmin(object):
    list_display = ('title', 'image', 'url', 'type', 'id')
    search_fields = ['title', 'id']
    list_filter = ('type',)
    list_editable = ['title','url']

# Register your models here.
xadmin.site.register(RecommendKeywords, RecommendKeywordsAdmin)
xadmin.site.register(Ad, AdAdmin)
xadmin.site.register(RecommendPoint, RecommendPointAdmin)
xadmin.site.register(News, NewsAdmin)
xadmin.site.register(LiveStudy, LiveStudyAdmin)
xadmin.site.register(CourseInfo, CourseInfoAdmin)
xadmin.site.register(CareerPath, CareerPathAdmin)
xadmin.site.register(GoldLecturer, GoldLecturerAdmin)
xadmin.site.register(Cooperation, CooperationAdmin)
xadmin.site.register(AdImage, AdImageAdmin)

