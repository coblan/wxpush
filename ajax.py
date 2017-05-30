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
import time
import logging
import common

front_log=logging.getLogger('front')

hula='http://wxpush.enjoyst.com'

def get_global():
    return globals()

state=[]
common.msg_list=state

operations=deque([])

#sys.stdout=wxpush.Mystd(state)

def start():
    global state
    thread.start_new_thread (wxpush.main,(state,operations))
    front_log.info('启动成功，请扫描新的二维码登陆')
    return {'status':'success'}

def get_state():
    
    rt_state=common.fetch_state()
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
    names= os.listdir('./data')
    for contact in contact_list:
        name = random.choice(names)
        myfile=os.path.join('./data',name)
        dc={
            'file_name':name,
            'nickname':contact['NickName'],
        }
        if myfile.endswith('txt'):
            with open(myfile,'rb') as f:
                raw = f.read()
                try:
                    txt= raw.decode('gbk')
                except UnicodeDecodeError:
                    txt=raw.decode('utf-8')
                tm = time.time()
                if wxpush.bot.send_msg_by_uid(txt,contact['UserName']):
                    dc['timespan']=time.time()-tm
                    front_log.info('向%(nickname)s发送 %(file_name)s 成功,耗费时间%(timespan)s秒'%dc)
                else:
                    front_log.error('向%(nickname)s发送 %(file_name)s [不成功]'%dc)
        elif myfile.lower().endswith(('jpg','png','gif')):
            tm = time.time()
            if wxpush.bot.send_img_msg_by_uid(myfile,contact['UserName']):
                dc['timespan']=time.time()-tm
                front_log.info('向%(nickname)s发送 %(file_name)s 成功,耗费时间%(timespan)s秒'%dc)
            else:
                front_log.error('向%(nickname)s发送 %(file_name)s [不成功]'%dc)
        else:
            front_log.warn('[ERROR] 文件类型不合要求 %s'%name)
        time.sleep(0.5)
    front_log.info('发送完毕')
    return {'status':'success'}

def end_last_bot():
    if wxpush.bot:
        front_log.info('发出退出命令')
        wxpush.bot.status = 'wait4loginout'
        wxpush.bot=None
    else:
        front_log.info('没有登陆的账号')
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