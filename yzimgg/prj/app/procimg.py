#coding:utf-8
from PIL import Image
from PIL import ImageEnhance

import shutil, os

import goodsinterface,redissql

from procSpImg import procimg
from procSpImg import IMGDIR
import goodsinterface



def procImg(spcode, depart, comp,height,width,thickness):
    sides = ["0", "r", "c", "d", "b"]
    result = [procimg(spcode, depart, comp, side, {"width": width, "height": height, "thickness": thickness}) for
              side in sides]
    result.append({"imgDir":IMGDIR})
    # result = [{'0': '/2/126/upload/0/000911.jpg'}, {'r': '/2/126/upload/r/000911.jpg'}, {'c': '/2/126/upload/c/000911.jpg'}, {'d': '/2/126/upload/d/000911.jpg'}, {'b': '/2/126/upload/b/000911.jpg'}, {'imgDir': 'D:/img'}]
    return result

if __name__ == "__main__":
    print procImg("000911","126","2",200,200,200)
#     print resizeImg(222,103,2)


# #删除图片
# def delimg(spcode,depart,comp, side=""):
#     imgdir = 'd:/img/%s/%s/upload/%s/%s.jpg' % (comp,depart,side,spcode)
#     if os.path.exists(imgdir):
#         os.remove(imgdir)

#     if side == "":
#         side = "r"
#         delimg(spcode, side,depart,comp)
# #上传图片后图片的处理
# def proc(img,depart,comp):
#     imgname = img.split(".")[0]
#     imgformat = 'jpg'                 #图像文件必须是jpg格式
#
#     side = imgname[-1]
#
#     if side.isalpha():
#         spcode = imgname[0:-1]
#     else:
#         side = ''
#         spcode = imgname
#     #获取商品资料
#     spinfo = getspinfo(spcode)
#     #print str(spinfo)
#
#     if spinfo  == None:
#         return {"error":"能上传,但没有相应的商品资料处理失败", "spcode":spcode, "side":side, "success":False}
#     else:
#         if side == "":
#             result = procspimg_zr(spcode,depart,comp)
#         elif side == "c":
#             result = procspimg_c(spcode,depart,comp)
#         elif side == "d":
#             result = procspimg_d(spcode,depart,comp)
#         elif side == "b":
#             result = procspimg_b(spcode,depart,comp)
#         else:
#             return {"error":"能上传,处理失败", "spcode":spcode, "side":side, "success":False}
#
#         return result
UPLOAD_PATH = 'd:/fmapp/yzimgg/prj/static/test/'
SAVE_PATH = 'd:/fmapp/yzimgg/prj/static/test_save/'
def copyimg(img):
    imgdir = UPLOAD_PATH + img
    imgdir2 = SAVE_PATH  + img

    shutil.copy(imgdir,  imgdir2)

    return {"success":True}
