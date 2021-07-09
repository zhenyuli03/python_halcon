import sys
import time
from PythonHalcon import *

if __name__=='__main__':
    pyhalcon=halconpy()
    image=pyhalcon.Read_Image("1.bmp")

    image=pyhalcon.Rgb1_To_Gray(image)
    region=pyhalcon.Threshold(image,10,255)
    area,row,column=pyhalcon.Area_Center(region)
    region=pyhalcon.Connection(region)
    region=pyhalcon.Select_Shape(region,"area","and",0,1000)
    num=pyhalcon.Count_Obj(region)
    print(num)

