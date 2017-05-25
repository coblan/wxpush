# encoding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
import wxpush
import thread
import md5
from collections import deque
import time
import sys
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
    for contact in contact_list:
        wxpush.bot.send_msg_by_uid('hi', contact['UserName'])
        time.sleep(0.8)
    print('发送成功')
    return {'status':'success'}

def end_last_bot():
    if wxpush.bot:
        wxpush.bot.status = 'wait4loginout'
        print('退出成功')
        wxpush.bot=None
    else:
        print('没有登陆的账号')
    return {'status':'success'}