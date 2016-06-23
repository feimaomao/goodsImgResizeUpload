# coding:utf-8
import json
import os
import os.path
import shutil
import sys
import time

from flask import current_app, Flask, jsonify, render_template, request
from flask.views import MethodView
from procSpImg import IMGDIR,getSpcodeSide,getsrcimgpath,getsrcimgpath
import requests
from goodsinterface import gettheSpdata,updateSp
import procimg
import shutil
from procimg import procImg
# Meta
##################
__version__ = '0.1.0'

# Config
##################
DEBUG = True
SECRET_KEY = 'development key'

BASE_DIR = os.path.dirname(__file__)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
UPLOAD_DIRECTORY = os.path.join(MEDIA_ROOT, 'upload')
CHUNKS_DIRECTORY = os.path.join(MEDIA_ROOT, 'chunks')

app = Flask(__name__)
app.config.from_object(__name__)
from flask.ext.cors import CORS
CORS(app)


# Utils
##################
def make_response(status=200, content=None):
    """ Construct a response to an upload request.
Success is indicated by a status of 200 and { "success": true }
contained in the content.

Also, content-type is text/plain by default since IE9 and below chokes
on application/json. For CORS environments and IE9 and below, the
content-type needs to be text/html.
"""
    return current_app.response_class(json.dumps(content,
                                                 indent=None if request.is_xhr else 2), mimetype='text/plain')


def validate(attrs):
    """ No-op function which will validate the client-side data.
Werkzeug will throw an exception if you try to access an
attribute that does not have a key for a MultiDict.
"""
    try:
        # required_attributes = ('qquuid', 'qqfilename')
        # [attrs.get(k) for k,v in attrs.items()]
        return True
    except Exception, e:
        return False


# 删除图片
def handle_delete(uuid):
    """ Handles a filesystem delete based on UUID."""
    location = os.path.join(app.config['UPLOAD_DIRECTORY'], uuid)
    shutil.rmtree(location)

def disposeImg(spcode,side, depart, comp, pos):
    srcimgpath,srcimgpathSave = getsrcimgpath(spcode, side, depart, comp, "upload")
    if os.path.exists(srcimgpath):
        if pos=="upload":
            targetimgpath, targetimgpathSave = getsrcimgpath(spcode, side, depart, comp, "back")
            shutil.copy(srcimgpath,targetimgpath)
        os.remove(srcimgpath)

        srcimgpath, srcimgpathSave = getsrcimgpath(spcode, side, depart, comp, "sp2")
        os.remove(srcimgpath)
        if side == "0":
            side = "r"
            srcimgpath, srcimgpathSave = getsrcimgpath(spcode, side, depart, comp, "sp2")
            os.remove(srcimgpath)
        return True
    else:
        return False

def handle_upload(f, attrs,depart,comp):
    """ Handle a chunked or non-chunked upload.
"""
    try:
        yzfilename = attrs['img']
        uploadtype = 'fine-upload'
    except:
        yzfilename = f.filename
        uploadtype = 'jupload--ajaxupload'

    spcode,side = getSpcodeSide(yzfilename)

    targetImgSave = "/{comp}/{depart}/upload/{side}/{spcode}.jpg".format(comp=comp,depart=depart,side=side,spcode=spcode)
    targetImg = IMGDIR +targetImgSave
    save_upload(f, targetImg)

    result = disposeImg(spcode, depart, comp, uploadtype, side)
    # {'spcode': ', 'side': , 'success': , 'error': }
    result["name"] = yzfilename
    return result


# 保存图片
def save_upload(f, path):
    """ Save an upload.
Uploads are stored in media/uploads
"""
    print str(path)
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'wb+') as destination:
        destination.write(f.read())


# Views
##################
@app.route("/")
def index():
    """ The 'home' page. Returns an HTML page with Fine Uploader code
ready to upload. This HTML page should contain your client-side code
for instatiating and modifying Fine Uploader.
"""
    return render_template('fine_uploader/index2.html')


@app.route("/set")
def set():
    code = request.args.get('code', '')
    width = request.args.get('width', '')
    height = request.args.get('height', '')
    content = request.args.get('content', '')
    return render_template('fine_uploader/index.html', code=code, width=width, height=height, content=content)


@app.route("/uploadinfo", methods=["POST"])
def uploadinfo():
    code = request.form['code']
    filename = request.form['filename']

    requests.post("http://127.0.0.1:5002/gemo/updataTK",
                  data={"key": json.dumps({"spcode": code}), "setvalue": json.dumps({"filename": filename})})
    return 'ok'


# 调整图片尺寸
@app.route("/resizeimg", methods=["POST"])
def resizeimg():
    spcode = request.form['spcode']
    depart = request.cookies.get('depart')
    comp = request.cookies.get('comp')
    height = int(request.form["height"])
    width = int(request.form["width"])
    thickness = int(request.form["thickness"])
    result = procImg(spcode,depart,comp,height,width,thickness)
    return json.dumps(result)


# 删除图片
@app.route("/delspimg", methods=["POST"])
def delspimg():
    spcode = request.form["spcode"]
    side = request.form["side"]
    depart  = "111"
    comp = "1"
    disposeImg(spcode,side, depart, comp, "upload")

    return '删除商品图像成功'


# 跳转上传图片的类
class UploadAPI(MethodView):
    """ View which will handle all upload requests sent by Fine Uploader.

Handles POST and DELETE requests.
"""
    def post(self):
        """A POST request. Validate the form and then handle the upload
based ont the POSTed data. Does not handle extra parameters yet.
"""
        print request.form,111,request.files['qqfile']
        if validate(request.form):
            # 调用上传图片函数
            depart = "111"
            comp = "1"
            result = handle_upload(request.files['qqfile'], request.form,depart,comp)
            # if result:
            #     return make_response(200, {"success": True})  # for fine_upload
            # else:
            #     return json.dumps([result])  # for jupload
            return jsonify(success=True)
        else:
            return make_response(400, {"error", "Invalid request"})

    def delete(self, uuid):
        """A DELETE request. If found, deletes a file with the corresponding
UUID from the server's filesystem.
"""
        try:
            handle_delete(uuid)
            return make_response(200, {"success": True})
        except Exception, e:
            return make_response(400, {"success": False, "error": e.message})


upload_view = UploadAPI.as_view('upload_view')
app.add_url_rule('/upload', view_func=upload_view, methods=['POST', ])
app.add_url_rule('/upload/<uuid>', view_func=upload_view, methods=['DELETE', ])

@app.route('/test')
def test():
    return render_template("test.html")

from redis import Redis
redi = Redis()
from io import BytesIO
import base64
import os
import re
from flask import send_file
@app.route('/photoDispose')
def img_dispose():
    #解析传入字符，判断是否有样式
    photo_string = request.args.get('img')
    style_list = photo_string.split('|')[0]
    try:
        photoPath = style_list.split('@')[0]
        style = style_list.split('@')[1]
        is_photo =0
    except:
        photoPath = style_list.split('@')[0]
        is_photo = 1
    photo = IMGDIR+photoPath
    if not redi.get(photoPath):
        if is_photo:
            with  open(photo,'rb') as img:
                redi.set(photo, base64.b64encode(img.read()))
        else:
            dic = photoDispose(photo,style)
            photo = dic['photo']
            if os.path.exists(photo):
                with  open(photo, 'rb') as img:
                    redi.set(photoPath, base64.b64encode(img.read()))
                os.remove(photo,)#打开文件后，不关闭文件是没法删除的
            else:
                photo ="D:\\img\\1\\111\\sp2\\0\\0.jpg"
                with  open(photo, 'rb') as img:
                    redi.set(photoPath, base64.b64encode(img.read()))
    ls_f = redi.get(photo)
    ls_f1 = base64.b64decode(ls_f)
    #将字符流写入BytesIO(主要用于读取缓存中的数据)
    by = BytesIO(ls_f1)
    return send_file(by, mimetype='image/png')
# F:\VCM\yzapp\yzimgg\prj\app>convert -rotate 50 phtoto\change222.jpg phtoto\change222.jpg
# 传参数到.bat
def photoDispose(imgPath,style):
    dic={}
    #解析字符串
    print imgPath
    photo = re.search(r'[a-zA-Z0-9]+.jpg',imgPath).group()
    change_photo = 'change'+photo
    #photo 222.jpg   imgPath  D:\img\1\111\sp2\0\123\222.jpg   style 1e_1c_0_50w_50r.src
    os.system('%s %s %s %s %s' % ('image_dispose.bat', imgPath, '100%', '-resize',change_photo))
    style = style.split("|")[0].split('&')[0]
    #获取宽度
    width = re.search(r'[0-9]+w',style)
    #获取高度
    height= re.search(r'[0-9]+h',style)
    #可以对处理后的图片进行按顺时针旋转,默认值 ：0(表示不旋转),[0, 360]
    rotate = re.search(r'[0-9]+r',style)
    #按比例缩放   1-1000
    proportion = re.search(r'[0-9]+p', style)
    if width:
        dic['width'] = width.group()[:-1]
        os.system('%s %s %s %s %s' % ('image_dispose.bat', change_photo,dic['width'], '-resize', change_photo))
    if height:
        dic['height'] = height.group()[:-1]
        os.system('%s %s %s %s %s' % ('image_dispose.bat', change_photo,'x'+ dic['height'], '-resize', change_photo))
    if width and height:
        if dic['width'] <dic['height']:
            os.system('%s %s %s %s %s' % ('image_dispose.bat', change_photo,dic['width'], '-resize',change_photo))
    if rotate:
        dic['rotate'] = rotate.group()[:-1]
        os.system('%s %s %s %s %s' % ('image_dispose.bat', change_photo, dic['rotate'], '-rotate',change_photo))
    if proportion:
        dic['proportion'] = proportion.group()[:-1]
        os.system('%s %s %s %s %s' % ('image_dispose.bat',change_photo, dic['proportion']+'%', '-resize',change_photo))
    # os.rename('phtoto\%s'%change_photo,'phtoto\%s')
    # 返回的为字典，change_photo为change加图片名称
    dic['photo'] = change_photo
    return dic

# Main
##################
# def main():
# app.run('0.0.0.0')
# return 0

if __name__ == '__main__':
    app.run(debug=True, port=5003)
