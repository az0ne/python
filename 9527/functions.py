# -*- coding:utf-8-*-

from mz_course.models import *
from mz_common.models import *
#获取分页数据
def get_page_data(Model,currentPage,pageSize):
      if currentPage > 0 and pageSize > 0:
            #获取总的数目
            try:
                  totalCounts = Model.objects.all().count()
                  if totalCounts % pageSize == 0: #计算总页数
                      totalPages = totalCounts / pageSize
                  else:
                      totalPages = (totalCounts / pageSize) + 1
                  # 根据当前页和每页的数量获取对应的数据
                  startNumber = (currentPage - 1) * pageSize
                  endNumber = currentPage * pageSize
                  data = Model.objects.all()[startNumber:endNumber]
                  output = {'data': data, 'totalCounts': totalCounts, 'totalPages': totalPages}
            except:
                  raise
      return output


def get_obj_name(obj_type,obj_id):
      if obj_type=='COURSE':
            return Course.objects.get(id=obj_id).name
      elif obj_type =='ARTICLE':
            return NewArticle.objects.get(id=obj_id).title
      elif obj_type == 'TEACHER':
            pass
      elif obj_type == 'LESSON':
            pass


def sha1(str):
    import hashlib
    m = hashlib.sha1()
    m.update(str)
    return m.hexdigest()
