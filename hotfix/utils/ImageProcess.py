#coding:utf-8
'''
    python图片处理
    @author:fc_lamp
    @blog:http://fc-lamp.blog.163.com/
'''
import PIL.Image as image
from PIL import Image, ImageFilter


class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)

#等比例压缩图片
def resizeImg(**args):
    args_key = {'ori_img':'','dst_img':'','dst_w':'','dst_h':'','save_q':75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]
        
    im = image.open(arg['ori_img'])
    ori_w,ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1
    if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
        if arg['dst_w'] and ori_w > arg['dst_w']:
            widthRatio = float(arg['dst_w']) / ori_w #正确获取小数的方式
        if arg['dst_h'] and ori_h > arg['dst_h']:
            heightRatio = float(arg['dst_h']) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio
            
        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h
        
    im.resize((newWidth,newHeight),image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])

    '''
    image.ANTIALIAS还有如下值：
    NEAREST: use nearest neighbour
    BILINEAR: linear interpolation in a 2x2 environment
    BICUBIC:cubic spline interpolation in a 4x4 environment
    ANTIALIAS:best down-sizing filter
    '''

#裁剪压缩图片
def clipResizeImg(**args):
    
    args_key = {'ori_img':'','dst_img':'','dst_w':'','dst_h':'','save_q':75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]
        
    im = image.open(arg['ori_img'])
    ori_w,ori_h = im.size

    dst_scale = float(arg['dst_h']) / arg['dst_w'] #目标高宽比
    ori_scale = float(ori_h) / ori_w #原高宽比

    if ori_scale >= dst_scale:
        #过高
        width = ori_w
        height = int(width*dst_scale)

        x = 0
        y = (ori_h - height) / 3
        
    else:
        #过宽
        height = ori_h
        width = int(height*dst_scale)

        x = (ori_w - width) / 2
        y = 0

    #裁剪
    box = (x,y,width+x,height+y)
    #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    #所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = im.crop(box)
    im = None

    #压缩
    ratio = float(arg['dst_w']) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    newIm.resize((newWidth,newHeight),image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])
    

#水印(这里仅为图片水印)
def waterMark(**args):
    args_key = {'ori_img':'','dst_img':'','mark_img':'','water_opt':''}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]
        
    im = image.open(arg['ori_img'])
    ori_w,ori_h = im.size

    mark_im = image.open(arg['mark_img'])
    mark_w,mark_h = mark_im.size
    option ={'leftup':(0,0),'rightup':(ori_w-mark_w,0),'leftlow':(0,ori_h-mark_h),
             'rightlow':(ori_w-mark_w,ori_h-mark_h)
             }
    

    im.paste(mark_im,option[arg['water_opt']],mark_im.convert('RGBA'))
    im.save(arg['dst_img'])
    


if __name__ == "__main__":
    simg = 'test.jpg'
    dimg = 'test2.jpg'
    image = Image.open(simg)
    image = image.filter(MyGaussianBlur(radius=30))
    image.save(dimg)
    print dimg, 'success'

    # #Demon
    # #源图片
    # ori_img = 'test.jpg'
    # #水印标
    # mark_img = 'test.png'
    # #水印位置(右下)
    # water_opt = 'rightlow'
    # #目标图片
    # dst_img = 'test2.jpg'
    # #目标图片大小
    # dst_w = 400
    # dst_h = 300
    # #保存的图片质量
    # save_q = 35
    # #裁剪压缩
    # clipResizeImg(ori_img=ori_img,dst_img=dst_img,dst_w=dst_w,dst_h=dst_h,save_q = save_q)
    #等比例压缩
    #resizeImg(ori_img=ori_img,dst_img=dst_img,dst_w=dst_w,dst_h=dst_h,save_q=save_q)
    #水印
    #waterMark(ori_img=ori_img,dst_img=dst_img,mark_img=mark_img,water_opt=water_opt)
    #该代码片段来自于: http://www.sharejs.com/codes/python/5927