# encoding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
import wxpush
import thread
import md5
from collections import deque
import time
import sys
from common import get_mac_address
import requests
import json
import base64
import random
import os

hula='http://wxpush.enjoyst.com'

def get_global():
    return globals()

state=[]
operations=deque([])

sys.stdout=wxpush.Mystd(state)

def start():
    global state
    thread.start_new_thread (wxpush.main,(state,operations))
    print('启动成功，请扫描新的二维码登陆')
    return {'status':'success'}

def get_state():
    global state
    rt_state=list(state)
    del state[:]
    rt_state.append({'key':'md5','value':get_png_md5()})
    rt_state.append({'key':'bot','value':bool(wxpush.bot)})
    if rt_state:
        return rt_state
    else:
        return {'msg':'bot is null'}

def get_png_md5():
    md = md5.new()
    with open('temp/wxqr.png','rb') as f:
        md.update(f.read())
    md5code = md.hexdigest()
    return md5code

def send(contact_list):
    files = [os.path.join('./data',name) for name in os.listdir('./data')] 
    for contact in contact_list:
        myfile = random.choice(files)
        if myfile.endswith('txt'):
            with open(myfile,'rb') as f:
                raw = f.read()
                try:
                    txt= raw.decode('gbk')
                except UnicodeDecodeError:
                    txt=raw.decode('utf-8')
                wxpush.bot.send_msg_by_uid(txt,contact['UserName'])
                print('向(%s)发送 文字消息 成功'%contact['NickName'])
        elif myfile.lower().endswith(('jpg','png','gif')):
            wxpush.bot.send_img_msg_by_uid(myfile,contact['UserName'])
            print('向(%s)发送 图片消息 成功'%contact['NickName'])
        else:
            print('[ERROR] 文件类型不合要求 %s'%myfile)
        #wxpush.bot.send_msg_by_uid('hi', contact['UserName'])
        time.sleep(0.8)
    print('发送完毕')
    return {'status':'success'}

def end_last_bot():
    if wxpush.bot:
        print('发出退出命令')
        wxpush.bot.status = 'wait4loginout'
        wxpush.bot=None
    else:
        print('没有登陆的账号')
    return {'status':'success'}

def check(checkstring=''):
    try:
        mac=get_mac_address()
        dc={}
        if checkstring:
            rt = requests.get(hula+'/bj?wx=%(wx)s&bj=%(bj)s'%{'wx':base64.b64encode(mac),'bj':base64.b64encode( checkstring)})
        else:
            rt = requests.get(hula+'/wx?wx='+base64.b64encode(mac))
        return json.loads(rt.content)
    except:
        return {'status':'fail'}