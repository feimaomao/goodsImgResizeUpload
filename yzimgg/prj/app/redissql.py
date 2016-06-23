# -*- coding: utf-8 -*-

import redis, json
rs = redis.Redis(host='127.0.0.1', port=6379, db=5)


def updatespgood(spinfo):
    spcode = spinfo["spcode"]    
    rs.set(spcode, json.dumps(spinfo))
    

def getthespdata(spcode):    
    spdata = rs.get(spcode)    
    if spdata:        
        return json.loads(spdata)
    else:
        return spdata
           


