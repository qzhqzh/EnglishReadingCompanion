#coding:utf-8

# 怎么使用 api 接口
#
# 利用 app_key, app_secret, 和 callback_url 构造一个url 
#   用来访问服务商的权限服务器
# 
# 扇贝的权限服务器地址为 
# https://api.shanbay.com/oauth2/authorize/?
# display=default&
# redirect_uri=http%3A//www.pinmingjiadanci//call.com&
# response_type=code&
# client_id=05623ce286a180e4e8c1

# 如果权限允许的话，会跳转到 回调地址
# http://www.pinmingjiadanci//call.com?
# code=unSqYMkQgk1XTN1kjDyOxVNSotsIfy

# 回调地址中的 code 后面的数字是我们需要的 CODE
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# 这里的三个变量是申请成为第三方应用的时候，服务商提供的账号和密码
# 回调地址 是 服务器给你权限令牌的时候的网址
APP_KEY = "05623ce286a180e4e8c1"
# APP_KEY = "a40e6b12f395da55a88b"
APP_SECRET = "e1417f6b92924e20f0a57da61c68aa1c2d6f33fc"
# APP_SECRET = "5feaab8faecb3cab596fb9808e1c8b7b61ac78c1"
CALLBACK_URL = 'http://www.pinmingjiadanci//call.com'
# CALLBACK_URL = 'https://api.shanbay.com/oauth2/auth/success/'

# 1. 请求授权
# 网站
domain='api.shanbay.com'
# 网站权限服务器地址
auth_url = 'https://%s/oauth2/' % domain

# 申请权限地址
# 示例
# https://api.shanbay.com/oauth2/authorize/?
# client_id=CLIENT_ID&
# response_type=code&
# state=123
CLIENT_ID = "05623ce286a180e4e8c1"
response_type = 'code'
state = 123

authorize_url = auth_url + 'authorize/?' + 'client_id=05623ce286a180e4e8c1&response_type=code&state=123'
# client_id 必须,创建应用时分配的App key
# response_type 必须，必须为code或者token其中一个
# state 可选，如果传递在服务器会把相同的state值传回给客户端，用于保存状态
# 示例 
# https://api.shanbay.com/oauth2/authorize/?client_id=05623ce286a180e4e8c1&response_type=code&state=123 
# 请求方式 GET
# RbIFjf3UzwkKLDIL5IY429LkgW6LoV 
CODE = 'oWeUPSOAOA3qO6SLA1OjxjElYD5KUY'

# 2. 获取token
# 网址 https://api.shanbay.com/oauth2/token/
# 请求方式 POST
# 
auth_token_url = 'https://%s/oauth2/token/' % domain
# 申请的参数有
# client_id         必须,创建应用时分配的App key
# client_secret     必须,创建应用时分配的App secret
# grant_type        必须，值为authorization_code
# code              必须，上一步获取的CODE
# redirect_uri      必须,需要和创建应用时填写的回调地址相同
http_body = 'code='+CODE+\
            '&client_id='+APP_KEY+\
            '&redirect_uri=http%3A//www.pinmingjiadanci//call.com'\
            '&grant_type=authorization_code'+\
            '&client_secret='+APP_SECRET
            # '&redirect_uri='+CALLBACK_URL
# print (http_body)
            
# python3 
import urllib.request

r = urllib.request.Request(auth_token_url, data=http_body.encode('utf-8'))

resp = urllib.request.urlopen(r)
# 返回结果的示例
# print (resp.read())
# b'{"access_token": "n2h9evwQrUcAog16sQBf5R1ZKy0pS3",
# "token_type": "Bearer", 
# "expires_in": 2592000, 
# "refresh_token": "PaiMJRK9swpmQpxBYdvdYlamKYZayC", 
# "scope": "read write"}
# 主要拿到了授权码 access_token
# print (resp['access_token'])
# print (resp['expires_in'])
# print (resp.read())

# 坑比json，还是用包算了
# def read_json(s):
    # # b'{"access_token": "n2h9evwQrUcAog16sQBf5R1ZKy0pS3", "token_type": "Bearer", "expires_in": 2592000, "refresh_token": "PaiMJRK9swpmQpxBYdvdYlamKYZayC", "scope": "read write"}'
    # # s = '{"access_token": "n2h9evwQrUcAog16sQBf5R1ZKy0pS3", "token_type": "Bearer", "expires_in": 2592000, "refresh_token": "PaiMJRK9swpmQpxBYdvdYlamKYZayC", "scope": "read write"}'
    # # print (s)
    # # print (s.decode('utf-8').lstrip('{"').rstrip('"}'))
    # s = s.decode('utf-8').lstrip('{"').rstrip('"}')
    # # s = s.decode('utf-8')
    # # print (s)
    # # s = s.lstrip('b\'\{"').rstrip('"}')
    # li = s.split('", "')
    # # print (li)
    # d = {}
    # for i in li:
        # li2 = i.split('": "')
        # d[ li2[0] ] = li2[1]
    # return d
    
# print (resp.read())
# print (type(resp.read()))

import json

def _obj_hook(pairs):
    '''
    convert json object to python object.
    '''
    o = JsonObject()
    for k, v in pairs.items():
        o[str(k)] = v
    return o
class JsonObject(dict):
    '''
    general json object that can bind any fields but also act as a dict.
    '''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

access_token = json.loads(resp.read().decode('utf-8'), object_hook=_obj_hook)['access_token']


# 3. 用 token 去申请资源
# test 
test_url = "https://api.shanbay.com/account/"
req = urllib.request.Request(test_url, data=None)
req.add_header('Authorization', 'Bearer %s' % access_token)
resp = urllib.request.urlopen(req)
print (resp.read())

# test2
test_url = "https://api.shanbay.com/bdc/search/?word=big"
req = urllib.request.Request(test_url, data=None)
req.add_header('Authorization', 'Bearer %s' % access_token)
resp = urllib.request.urlopen(req)
s = resp.read()
print (s.decode('cp936'))
print (json.loads(s.decode('utf-8'), object_hook=_obj_hook).keys())
word_id = json.loads(s.decode('utf-8'), object_hook=_obj_hook)['data']['id']

# # test3
test_url = "https://api.shanbay.com/bdc/learning/"
test_body = "id="+str(word_id)
print (test_body)
req = urllib.request.Request(test_url, data=test_body.encode('utf-8'))
req.add_header('Authorization', 'Bearer %s' % access_token)
resp = urllib.request.urlopen(req)
print (resp.read())

# test 4 - PUT -DELETE
##PUT
# import urllib2

# request = urllib2.Request('http://example.org', data='your_put_data')

# request.add_header('Content-Type', 'your/contenttype')
# request.get_method = lambda: 'PUT'
# response = urllib2.urlopen(request)


# #DELETE
# import urllib2

# request = urllib2.Request(uri)
# request.get_method = lambda: 'DELETE'
# response = urllib2.urlopen(request)