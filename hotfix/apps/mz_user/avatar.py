# -*- coding: utf-8 -*-

"""
@version: 2016/5/19
@author: Jackie
@contact: jackie@maiziedu.com
@file: avatar.py.py
@time: 2016/5/19 16:06
@note:  ??
"""

# import os
# import django
# from core.common.utils.decorators import timecost
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
# django.setup()
import os

from django.conf import settings
from core.common.upload.local import upload
import StringIO

try:
    from PIL import ImageFile, Image
except:
    import ImageFile, Image


def avatar_upload(file_data):
    """
    头像原始文件上传
    :param file_data:
    :return:文件URL,,,不包括前面的MEDIA_URL
    """
    if file_data.size / 1024 > settings.AVATAR_SIZE_LIMIT:
        return False, u"头像大小超过" + str(settings.AVATAR_SIZE_LIMIT) + u"KB限制"
        # 判断图片格式
    if settings.AVATAR_SUFFIX_LIMIT.find(file_data.name.split(".")[-1]) == -1:
        return False, u"头像必须为GIF/JPG/PNG/BMP格式"

    parser = ImageFile.Parser()
    data = file_data.read()
    parser.feed(data)
    img = parser.close()
    width, height = img.size
    if img.mode != "RGB":
        img = img.convert("RGB")

    io = StringIO.StringIO()
    img.save(io, 'jpeg', quality=100)
    io.name = file_data.name
    io.seek(0)
    src_url = upload(io, 'temp')
    del io
    return True, dict(img_url=settings.MEDIA_URL + src_url, width=width, height=height)


def avatar_crop(src_img_url, **kwargs):
    """
    头像剪切
    :param src_img_url:原始文件的地址
    :param kwargs:
    :return:
    """
    picwidth = kwargs.pop('picwidth')
    picheight = kwargs.pop('picheight')
    width = kwargs.pop('width')
    height = kwargs.pop('height')
    left = kwargs.pop('left')
    top = kwargs.pop('top')

    src_img_path = os.path.join(settings.MEDIA_ROOT, src_img_url[len(settings.MEDIA_URL):])
    buff = StringIO.StringIO()
    f = Image.open(src_img_path)
    f.resize((picwidth, picheight), Image.ANTIALIAS).save(buff, 'jpeg', quality=100)

    parser = ImageFile.Parser()
    buff.seek(0)
    parser.feed(buff.read())
    del buff

    ft = parser.close()

    box = (left, top, left + width, top + height)
    result = {}

    def _inner(name, w):
        io2save = StringIO.StringIO()
        io2save.name = 'temp.jpg'

        ft.crop(box).resize((w, w), Image.ANTIALIAS).save(io2save, 'jpeg', quality=100)
        io2save.seek(0)
        result[name] = upload(io2save, 'avatar')
        del io2save

    tmp = [('big', 220), ('middle', 104), ('small', 70)]
    for name, w in tmp:
        _inner(name, w)
    return result


def test():
    # avatar_upload(open(u'D:/qie.jpg', 'rb'))
    print avatar_crop(
        'temp/2016/05/19/b71447d187f84dfbba0f0f5b51bbe47c.jpg',
        **dict(top=109,
               left=83,
               width=100,
               height=100,
               picwidth=350,
               picheight=263)
    )


def test2():
    for i in xrange(100):
        test()


if __name__ == '__main__':
    test2()
