# -*- coding: UTF-8 -*-

from db.api.upload.upload_result import UploadResult
from db.api.upload.upload_config import UploadConfig
from utils import tool

class Uploader(object):
    @staticmethod
    def get_config():
        try:
            with open(UploadConfig.UPLOAD_CONFIG_PATH, 'r') as f:
                config = f.read().decode("utf-8")
            return config
        except Exception,e:
            #写日志
            return ""

    #filetype:uploadimage,uploadfile,uploadvideo
    @staticmethod
    def upload(file,filetype = "uploadimage"):
        if(file == None):
            print("上传资源为空.")
            return UploadResult(False)
        old_filename = file.name#.decode('utf-8')
        filesize = file.size
        fileext = old_filename.split('.')[-1]
        new_filename = str(tool.generate_random(18,1)) +'.'+ fileext#tool.getRandom() + "." + fileext
        local_path = ""
        if_download = False
        if filetype == "uploadimage":
            if_download = False
            local_path = UploadConfig.UPLOAD_IMG_PATH
            if not fileext.lower() in ('jpg', 'jpeg', 'bmp', 'gif', 'png'):
                print("图片格式不合法.")
                return UploadResult(False)


        if filetype == "uploadfile" :
            if_download = True
            local_path = UploadConfig.UPLOAD_FILE_PATH
            if not fileext.lower() in ("rar", "zip", "tar", "gz", "7z", "bz2", "cab", "iso",
                                       "doc", "docx", "xls", "xlsx", "ppt", "pptx", "pdf", "txt", "md", "xml"):
                print("附件格式不合法.")
                return UploadResult(False)

        if filetype == "uploadvideo" :
            if_download = False
            local_path = UploadConfig.UPLOAD_VIDEO_PATH
            if not fileext.lower() in ("flv", "swf", "mkv", "avi", "rm", "rmvb", "mpeg", "mpg",
                                       "ogg", "ogv", "mov", "wmv", "mp4", "webm", "mp3", "wav", "mid"):
                print("多媒体格式不合法.")
                return UploadResult(False)

        try:
            destination = open(local_path + new_filename, 'wb+')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()

            #转存七牛
            #result = CurrentStorage.upload_file(new_filename,local_path + new_filename,False,if_download)


        except  Exception,e:
            print("资源写入失败.")
            return UploadResult(False)

        url = "/" + local_path + new_filename;
        return UploadResult(True,url,new_filename,old_filename,"."+fileext,filesize)
