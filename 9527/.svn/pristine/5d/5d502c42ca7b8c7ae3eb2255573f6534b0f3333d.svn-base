# -*- coding: UTF-8 -*-
__author__ = 'lee'

class UploadResult(object):

#
# 得到上传文件所对应的各个参数,数组结构
# array(
#     "state" => "",          //上传状态，上传成功时必须返回"SUCCESS"
#     "url" => "",            //返回的地址
#     "title" => "",          //新文件名
#     "original" => "",       //原始文件名
#     "type" => ""            //文件类型
#     "size" => "",           //文件大小
# )
#

    def __init__(self,ret,url="",title="",original="",type="",size=0):
        self.ret = ret

        state = "SUCCESS"
        if(ret == False):
            state = ""
        self.info = "{\"state\":\"%s\",\"url\":\"%s\",\"title\":\"%s\",\"original\":\"%s\",\"type\":\"%s\",\"size\":%s}" % (state,url,title,original,type,str(size))
        print(self.info)