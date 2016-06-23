# -*- coding: utf-8 -*-
#from geom import pnosql

#conn = pnosql.conn
import requests, json
#获取商品资料信息

def gettheSpdata(spcode,depart,comp):
    p = {"item":'spcode','value': spcode}
    cookie = {"depart":str(depart),"comp":str(comp)}
    r = requests.post("http://127.0.0.1:5002/gemo/gettheSpdata", data=p,cookies=cookie)
    spdata = r.json()
    return spdata

def updateSp(sp):
#     "operator": spinfo["depart"],"imgPath":result,"_id":spinfo["_id"],"comp",spinfo["comp"]
# result = {'0': '/2/126/upload/0/000911.jpg'}, {'r': '/2/126/upload/r/000911.jpg'}, {'c': '/2/126/upload/c/000911.jpg'}, {'d': '/2/126/upload/d/000911.jpg'}, {'b': '/2/126/upload/b/000911.jpg'}, {'imgDir': 'D:/img'}
    print sp
    r = requests.post("http://127.0.0.1:5002/gemo/updateSpinfo", json.dumps(sp))
    result = r.json()
    return result

if __name__ == '__main__':
    print gettheSpdata("2213221411121123", "103", "2")


def gettheTextdata(textcode):
    try:
        p = {"item":'spcode','value': textcode,  "company":"x"}
        r = requests.post("http://127.0.0.1:5002/gemo/gettheTKdata", data=p)
        #print str(r)
        TKdata = r.json()
        
        
        return TKdata
    except:        
        TKdata = {
        "barcode":'text001',
        "spcode":'text001',
        "width": 110,
        "height": 200,
        "thickness":'1'
        }
        return TKdata

