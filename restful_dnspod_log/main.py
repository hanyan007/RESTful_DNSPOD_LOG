#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @Date    : 2017-03-08
# @Author  : hanyan_news
import base64
import random
import time
import json
import sys
import urllib
import urllib2
from datetime import datetime, timedelta
from flask import Flask, request, make_response, render_template

reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)
oauth_redirect_uri = []
resp= {}


ACCESS = {
    'test': '666666',
    'xf.shen': 'test8899'
}

def info_response(info,status='0',state='failed'):
    resp={'status':status,'state':state,'info':info}
    res = json.dumps(resp)
    return res

@app.route('/oauth/access_token', methods=['POST', 'GET'])
def access_token():
   # if request.method == 'POST' and request.args.get('appid'):
     if request.args.get('appid') and request.args.get('appsecret'):
        id = request.args.get('appid')
        ct = request.args.get('appsecret')
     	if ACCESS.has_key(id) and ACCESS.get(id) == request.args.get('appsecret'):
        #return  'id=%s,ct=%s,aid=%s,act=%s' % (id,ct,aid,act)
     		return gen_token(id,ct)
	else:
    	#	resp={'status':'0','state':'create failed','info':'appid or appsecret value is wrong.'}
	#	res = json.dumps(resp)
	#	return res
		return info_response('appid or appsecret value is wrong.')
     else:
	  return info_response('appid or appsecret args name required,or  not correct.')	

def gen_token(appid,appsecret):
    token = base64.b64encode(':'.join([str(appid), str(random.random()), str(appsecret),str(time.time() + 7200)]))
    #ACCESS[appid].append(token)
    resp={'status':'1','info':'create successful','access_token':token,'expires_time':'7200s'}
    res = json.dumps(resp)
    return res
   # return token

def verify_token(token):
    try:
    	_token = base64.b64decode(token)
    except (ValueError,TypeError),e:
	print  "token may be is wrong,Please check."
	#return 2 
    else:
    	key =  ACCESS.get(_token.split(':')[0])
	value =  ACCESS.get(_token.split(':')[2])
	times = float(_token.split(':')[-1])
    	if  key in ACCESS:
       		return "verify token keys error: %s" %  token
	if times >= time.time():
        	return 1
	else:
        	return 0

@app.route('/swjoy', methods=['POST', 'GET'])
def swjoy_dnspod():
        lt= []
        if request.args.get('token'):
            token = request.args.get('token')
            posturl = 'https://dnsapi.cn/Domain.Log'
            postdata = {'login_token':'yourID,yourToken','format':'json','domain':'test.com','length':'30'}
            req = urllib2.Request(posturl)
            data = urllib.urlencode(postdata)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            response = opener.open(req,data)
            result = response.read()
            list = eval(result)
            for i in list['log']:
                log= i.decode("unicode_escape")
                lt.append(log)
            ret = verify_token(token)
            if verify_token(token) == 1:
                return render_template('index_swjoy.html', var1 = lt)
	    else:
            	return info_response('The token may be wrong,Please check...')
        else:
            return info_response('require token args, or not correct.')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8080)

