#coding:utf-8

# ��ôʹ�� api �ӿ�
#
# ���� app_key, app_secret, �� callback_url ����һ��url 
#   �������ʷ����̵�Ȩ�޷�����
# 
# �ȱ���Ȩ�޷�������ַΪ 
# https://api.shanbay.com/oauth2/authorize/?
# display=default&
# redirect_uri=http%3A//www.pinmingjiadanci//call.com&
# response_type=code&
# client_id=05623ce286a180e4e8c1

# ���Ȩ������Ļ�������ת�� �ص���ַ
# http://www.pinmingjiadanci//call.com?
# code=unSqYMkQgk1XTN1kjDyOxVNSotsIfy

# �ص���ַ�е� code �����������������Ҫ�� CODE
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# ��������������������Ϊ������Ӧ�õ�ʱ�򣬷������ṩ���˺ź�����
# �ص���ַ �� ����������Ȩ�����Ƶ�ʱ�����ַ
APP_KEY = "05623ce286a180e4e8c1"
# APP_KEY = "a40e6b12f395da55a88b"
APP_SECRET = "e1417f6b92924e20f0a57da61c68aa1c2d6f33fc"
# APP_SECRET = "5feaab8faecb3cab596fb9808e1c8b7b61ac78c1"
CALLBACK_URL = 'http://www.pinmingjiadanci//call.com'
# CALLBACK_URL = 'https://api.shanbay.com/oauth2/auth/success/'

# 1. ������Ȩ
# ��վ
domain='api.shanbay.com'
# ��վȨ�޷�������ַ
auth_url = 'https://%s/oauth2/' % domain

# ����Ȩ�޵�ַ
# ʾ��
# https://api.shanbay.com/oauth2/authorize/?
# client_id=CLIENT_ID&
# response_type=code&
# state=123
CLIENT_ID = "05623ce286a180e4e8c1"
response_type = 'code'
state = 123

authorize_url = auth_url + 'authorize/?' + 'client_id=05623ce286a180e4e8c1&response_type=code&state=123'
# client_id ����,����Ӧ��ʱ�����App key
# response_type ���룬����Ϊcode����token����һ��
# state ��ѡ����������ڷ����������ͬ��stateֵ���ظ��ͻ��ˣ����ڱ���״̬
# ʾ�� 
# https://api.shanbay.com/oauth2/authorize/?client_id=05623ce286a180e4e8c1&response_type=code&state=123 
# ����ʽ GET
# RbIFjf3UzwkKLDIL5IY429LkgW6LoV 
CODE = 'oWeUPSOAOA3qO6SLA1OjxjElYD5KUY'

# 2. ��ȡtoken
# ��ַ https://api.shanbay.com/oauth2/token/
# ����ʽ POST
# 
auth_token_url = 'https://%s/oauth2/token/' % domain
# ����Ĳ�����
# client_id         ����,����Ӧ��ʱ�����App key
# client_secret     ����,����Ӧ��ʱ�����App secret
# grant_type        ���룬ֵΪauthorization_code
# code              ���룬��һ����ȡ��CODE
# redirect_uri      ����,��Ҫ�ʹ���Ӧ��ʱ��д�Ļص���ַ��ͬ
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
# ���ؽ����ʾ��
# print (resp.read())
# b'{"access_token": "n2h9evwQrUcAog16sQBf5R1ZKy0pS3",
# "token_type": "Bearer", 
# "expires_in": 2592000, 
# "refresh_token": "PaiMJRK9swpmQpxBYdvdYlamKYZayC", 
# "scope": "read write"}
# ��Ҫ�õ�����Ȩ�� access_token
# print (resp['access_token'])
# print (resp['expires_in'])
# print (resp.read())

# �ӱ�json�������ð�����
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


# 3. �� token ȥ������Դ
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