import sys
import time
from ctypes import *


class halconpy():
    def __init__(self):
        self.halcon_module = cdll.LoadLibrary('./halconc.dll')

    #1读图像
    #InPut:     路径
    #OutPut:    图像的指针
    def Read_Image(self, path):
        value=c_long(0)
        image=pointer(value)
        cpath=c_char_p(bytes(str(path), 'utf-8'))
        self.halcon_module.gen_empty_obj(byref(image))
        self.halcon_module.read_image(byref(image), cpath)
        return image

    #2转灰度
    # InPut:    图像
    # Output:   图像    
    def Rgb1_To_Gray(self, image):
        value=c_long(0)
        cimage=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cimage))
        self.halcon_module.rgb1_to_gray(image, byref(cimage))
        return cimage

    #3获取图像长宽
    #InPut:     图像
    #OutPut:    [height, width]
    def Get_Image_Size(self, image):
        cheight=c_long(0)
        cwidth=c_long(0)
        self.halcon_module.get_image_size(image, byref(cheight), byref(cwidth))
        height=cheight.value
        width=cwidth.value
        return [height,width]

    #4阈值分割
    #InPut:     图像，低阈值，高阈值
    #OutPut:    区域
    def Threshold(self, image, mingray, maxgray):        
        value=c_long(0)
        region=pointer(value)
        self.halcon_module.threshold(image, byref(region), c_double(mingray), c_double(maxgray))
        return region
    
    #5连通处理
    #InPut:     区域
    #OutPut:    区域集合
    def Connection(self, region):
        value=c_long(0)
        cregion=pointer(value)
        # self.halcon_module.gen_empty_obj(byref(cregion))
        # self.halcon_module.clear_obj(cregion)
        self.halcon_module.connection.argtypes=[POINTER(c_long), POINTER(POINTER(c_long))]
        self.halcon_module.connection.restype=None
        self.halcon_module.connection(region, byref(cregion))
        return cregion

    #6统计对象
    #InPut:     区域
    #OutPut:    个数
    def Count_Obj(self, region):
        num=c_long(0)
        self.halcon_module.count_obj(region, byref(num))
        return num.value
    
    #7过滤对象
    #Input:     区域,过滤项，选项, 低过滤值, 高过滤值
    #OutPut；   区域
    def Select_Shape(self, region, features, operation, min, max):
        value=c_long(0)
        cregion=pointer(value)
        cfeatures=c_char_p(bytes(str(features), 'utf-8'))
        coperation=c_char_p(bytes(str(operation), 'utf-8'))
        self.halcon_module.gen_empty_obj(byref(cregion))
        self.halcon_module.clear_obj(cregion)
        self.halcon_module.select_shape(region, byref(cregion), cfeatures, coperation, c_double(min), c_double(max))
        return cregion
    
    #8获取图像通道
    #InPut:     图像
    #OutPut:    通道数
    def Count_Channels(self, image):
        num=c_long(0)
        self.halcon_module.count_channels(image, byref(num))
        return num.value

    #9保存区域
    #InPut:     区域, path
    #OutPut:    None
    def Write_Region(self, region, name):
        cname=c_char_p(bytes(str(name), 'utf-8'))
        self.halcon_module.write_region(region,cname)
    
    #10保存图片
    #InPut:     
    def Write_Image(self, image, formatd, fillcolor, filename):
        cformat=c_char_p(bytes(str(formatd), 'utf-8'))
        cfilename=c_char_p(bytes(str(filename), 'utf-8'))
        self.halcon_module.write_image(image, cformat, c_long(fillcolor), cfilename)

    #11区域中心
    #InPut:     图像或者区域
    #OutPut:    面积，中心点
    def Area_Center(self, region):
        area=c_long(0)
        row=c_double(0)
        column=c_double(0)
        self.halcon_module.area_center(region, byref(area), byref(row), byref(column))
        return [area.value, row.value, column.value]

    #12剪切图片
    #InPut:     图像，区域
    #OutPut:    图像
    def Reduce_Domain(self, image, region):
        value=c_long(0)
        cimage=pointer(value)
        self.halcon_module.reduce_domain(image, region, byref(cimage))
        return cimage

    #13矩形膨胀
    #Input:     区域，长，宽
    #OutPut:    区域
    def Dilation_Rectangle1(self, region, width, height):
        value=c_long(0)
        cregion=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cregion))
        self.halcon_module.clear_obj(cregion)
        self.halcon_module.dilation_rectangle1(region, byref(cregion), c_long(width), c_long(height))
        return cregion

    #14圆形膨胀
    #InPut:     区域，半径
    #OutPut:    区域
    def Dilation_Circle(self, region, radius):
        value=c_long(0)
        cregion=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cregion))
        self.halcon_module.clear_obj(cregion)
        self.halcon_module.dilation_circle(region, byref(cregion), c_double(radius))
        return cregion

    #15矩形腐蚀
    #InPut:     区域，长，宽
    #OutPut:    区域
    def Erosion_Rectangle1(self, region, width, height):
        value=c_long(0)
        cregion=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cregion))
        self.halcon_module.clear_obj(cregion)
        self.halcon_module.erosion_rectangle1(region, byref(cregion), c_long(width), c_long(height))
        return cregion
    
    #16圆形腐蚀
    #InPut；    区域，半径
    #OutPut:    区域
    def Erosion_Circle(self, region, radius):
        value=c_long(0)
        cregion=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cregion))
        self.halcon_module.clear_obj(cregion)
        self.halcon_module.erosion_circle(region, byref(cregion), c_double(radius))
        return cregion

    #17矩形开运算
    #InPut:     区域，宽，长
    #OutPut:    区域
    def Opening_Rectangle1(self, region, width, height):
        value=c_long(0)
        cregion=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cregion))
        self.halcon_module.clear_obj(cregion)
        self.halcon_module.opening_rectangle1(region, byref(cregion), c_long(width), c_long(height))
        return cregion

    #18圆形开运算
    #InPut:     区域，宽，长
    #OutPut:    区域
    def Opening_Circle(self, region, radius):
        value=c_long(0)
        cregion=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cregion))
        self.halcon_module.clear_obj(cregion)
        self.halcon_module.opening_circle(region, byref(cregion), c_double(radius))
        return cregion
    
    #19 图像快速傅里叶变换
    #InPut:     图像
    #OutPut:    图像(傅里叶变换)
    def FFT_Image(self, image):
        value=c_long(0)
        cimage=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cimage))
        self.halcon_module.clear_obj(cimage)
        self.halcon_module.fft_Image(image, byref(cimage))
        return cimage
    
    #20 图像转二维傅里叶变换
    #InPut:     图像,变换方向，。。，输出类型，宽
    #OutPut:    图像(二维傅里叶变换)
    def RFT_Generic(self, image, direction, norm, resultType, width):
        cdirection=c_char_p(bytes(str(direction), 'utf-8'))
        cnorm=c_char_p(bytes(str(norm), 'utf-8'))
        cresultType=c_char_p(bytes(str(resultType), 'utf-8'))
        cwidth=c_long(0)
        value=c_long(0)
        cimage=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cimage))
        self.halcon_module.clear_obj(cimage)
        self.halcon_module.rft_generic(image, byref(cimage), cdirection, cnorm, cresultType, cwidth)
        return cimage

    #21 生成高斯过滤器
    #InPut:     横向sigma,纵向sigma,角度，none,高斯核类型,宽，高
    #OutPut:    图像(高斯过滤器)
    def Gen_Gauss_Filter(self, sigma1, sigma2, phi, norm, mode, width, height):
        value=c_long(0)
        cimage=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cimage))
        self.halcon_module.clear_obj(cimage)
        csigma1=c_double(sigma1)
        csigma2=c_double(sigma2)
        cphi=c_double(phi)
        cnorm=c_char_p(bytes(str(norm), 'utf-8'))
        cmode=c_char_p(bytes(str(mode), 'utf-8'))
        cwidth=c_long(width)
        cheight=c_long(height)
        self.halcon_module.gen_gauss_filter(byref(cimage), csigma1, csigma2, cphi, cnorm, cmode, cwidth, cheight)
        return cimage

    #22 傅里叶卷积运算
    #InPut:     傅里叶图像， 过滤器
    #OutPut:    图像(傅里叶)
    def Convol_FFT(self, fftimage, filter):
        value=c_long(0)
        cimage=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cimage))
        self.halcon_module.clear_obj(cimage)
        self.halcon_module.convol_fft(fftimage, filter, byref(cimage))
        return cimage

    #23 图像相减
    #InPut:     图像1，图像2， 相乘数， 相加数
    #OutPut:    图像
    def Sub_Image(self, image1, image2, mult, add):
        value=c_long(0)
        cimage=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cimage))
        self.halcon_module.clear_obj(cimage)
        cmult=c_double(mult)
        cadd=c_double(add)
        self.halcon_module.sub_image(image1, image2, byref(cimage), cmult, cadd)
        return cimage

    #24 对比度增强
    #InPut:     图像，宽，高，因子
    #OutPut:    图像
    def Emphasize(self, image, maskwidth, maskheight, factor):
        value=c_long(0)
        cimage=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cimage))
        self.halcon_module.clear_obj(cimage)
        cmaskwidth=c_long(maskwidth)
        cmaskheight=c_long(maskheight)
        cfactor=c_double(factor)
        self.halcon_module.emphasize(image, byref(cimage), cmaskwidth, cmaskheight, cfactor)
        return cimage

    #25 均值滤波
    #Input:     图像，宽，高
    #OutPut:    图像
    def Mean_Image(self, image, maskwidth, maskheight):
        value=c_long(0)
        cimage=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cimage))
        self.halcon_module.clear_obj(cimage)
        cmaskwidth=c_long(maskwidth)
        cmaskheight=c_long(maskheight)
        self.halcon_module.mean_image(self, image, byref(cimage), cmaskwidth, cmaskheight)
        return cimage

    #26 中值滤波
    #InPut:     图像，过滤形状，大小，幅度
    #OutPut:    图像
    def Median_Image(self, image, masktype, radius, margin):
        value=c_long(0)
        cimage=pointer(value)
        self.halcon_module.gen_empty_obj(byref(cimage))
        self.halcon_module.clear_obj(cimage)
        cmasktype=c_char_p(bytes(str(masktype), 'utf-8'))
        cradius=c_long(radius)
        cmargin=c_char_p(bytes(str(margin), 'utf-8'))
        self.halcon_module.median_image(image, byref(cimage), cmasktype, cradius, cmargin)
        return cimage

    #27 获取区域
    #Input:     图像
    #OutPut:    区域
    def Get_Domain(self, image):
        value=c_long(0)
        region=pointer(value)
        self.halcon_module.get_domain(image, byref(region))
        return region
    
    #28 获取XLD的长度
    #InPut:     XLD
    #OutPut:    长度
    def Length_XLD(self, XLD):
        clength=c_double(0)
        self.halcon_module.length_xld(XLD, byref(clength))
        return clength