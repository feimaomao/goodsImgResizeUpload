#coding:utf-8
import os
from PIL import Image
from PIL import ImageEnhance
IMGDIR = "D:\\img"
BAISHU = 0.5   #放大比例



def procimg(spcode,depart,comp, side,gemo):
# gemo = {"width":, "height":, "thickness":}

    srcimgpath,srcimgpathSave = getsrcimgpath(spcode, side, depart, comp, "upload")
    if srcimgpath:
        picWH=getpicWH(gemo, side)
        width = picWH['width']
        height = picWH['height']
        #picWH ={"width":, "height":}

        targetImg = fmImg(srcimgpath, width, height)
        targetimgpath,targetimgpathSave = getsrcimgpath(spcode, side, depart, comp, "sp2")
        targetImg.save(targetimgpath, "JPEG")
        return {side:targetimgpathSave}
        # return {"error": "", "spcode": spcode, "side": side, "success": True}

    elif side =="r":
        srcimgpath,targetimgpathSave = getsrcimgpath(spcode, "0", depart, comp, "sp2")
        if os.path.exists(srcimgpath):
            srcimg = Image.open(srcimgpath)
            angle = 90

            targetImg = srcimg.rotate(angle)
            targetimgpath, targetimgpathSave = getsrcimgpath(spcode, side, depart, comp, "sp2")
            targetImg.save(targetimgpath, "JPEG")
            return {"r": targetimgpathSave}
            # return {"error": "", "spcode": spcode, "side": side, "success": True}

    return {side: None}


def getsrcimgpath(spcode, side, depart, comp, pos):
    if pos == "upload":
        for g in [ "jpg", "png","gif"]:
            srcimgpathSave = "/{comp}/{depart}/upload/{side}/{spcode}.{g}".format(comp=comp,depart=depart,side=side,spcode=spcode,g=g)
            srcimgpath = IMGDIR+srcimgpathSave
            if os.path.exists(srcimgpath):
                return srcimgpath,srcimgpathSave

    elif pos == "sp2":
        # srcimgpath = "{imgdir}/{comp}/{depart}/sp2/{side}/{spcode}.jpg".format(imgdir=IMGDIR,comp=comp,depart=depart,side=side,spcode=spcode)
        srcimgpath = IMGDIR + "/{comp}/{depart}/sp2/{side}".format(comp=comp,depart=depart,side=side)
        if not os.path.exists(srcimgpath):
            os.makedirs(srcimgpath)
        srcimgpath = srcimgpath+"/{spcode}.jpg".format(spcode=spcode)
        srcimgpathSave = "/{comp}/{depart}/upload/{side}/{spcode}.jpg".format(comp=comp,depart=depart,side=side,spcode=spcode)
        return srcimgpath,srcimgpathSave

    elif pos=="back":
        srcimgDir = "{imgdir}/{comp}/{depart}/back/{side}".format(imgdir=IMGDIR, comp=comp, depart=depart, side=side)
        if not os.path.exists(srcimgDir):
            os.makedirs(srcimgDir)
        srcimgpath = srcimgDir + "/{spcode}.jpg".format(spcode=spcode)
        return srcimgpath

    return False,False


def getpicWH(gemo, side):
    #gemo = {"width":, "height":, "thickness":}
    picwh = {"width":0, "height":0}

    if side=="c":
        picwh["height"] = int(gemo["height"] * BAISHU)  #0.5        侧面
        picwh["width"] = int(gemo["thickness"] * BAISHU)  #0.5　　　侧面

    elif side== "b":
        picwh["height"] = int(gemo["height"] * BAISHU)  # 0.5      背面
        picwh["width"] = int(gemo["width"] * BAISHU)  # 0.5　　　背面

    elif side=="d":
        picwh["height"] = int(gemo["thickness"] * BAISHU)  # 0.5          底面
        picwh["width"] = int(gemo["width"] * BAISHU)  # 0.5　　　底面

    elif side=="0":
        picwh["height"] = int(gemo['height'] *BAISHU)  # 0.5      有图商品
        picwh["width"] = int(gemo['width'] * BAISHU)  # 0.5　　　有图商品
    return picwh


def fmImg(imgPath,picwidth,picheight):
    targetImg = Image.open(imgPath)
    targetImg = transformpic(targetImg)
    targetImg = targetImg.resize((picwidth, picheight), Image.ANTIALIAS)
    return targetImg


def transformpic(img):
    enc2 = ImageEnhance.Contrast(img)
    img = enc2.enhance(1.3)
    enc = ImageEnhance.Sharpness(img)
    img = enc.enhance(1.3)
    return img

def getSpcodeSide(yzfilename):
    imgname = yzfilename.split(".")[0]
    side = imgname[-1]
    if side.isalpha():
        spcode = imgname[0:-1]
    else:
        side = '0'
        spcode = imgname
    return spcode,side


# if __name__ == "__main__":
#     print procimg("000911","126","2","0",{"width": 200, "height": 200, "thickness": 200})
# if __name__ == "__main__":
    # print getsrcimgpath("222","c",103,2,"upload")
    # print getsrcimgpath("222","d",103,2,"dispose")
    # print getsrcimgpath("222","0",103,2,"sp2")
    # print getpicWH({"width":71, "height":106, "thickness":71},"c")

    # fm = fmImg("D:/img/2/103/upload/0/111.jpg",400,100)
    # fm.save("D:/img/2/103/sp2/0/222.jpg", "JPEG")
    # procimg("111",103,2,"c",{"width":71, "height":106, "thickness":80})