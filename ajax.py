from __future__ import unicode_literals
from __future__ import absolute_import
import wxpush
import thread
import md5
from collections import deque


def get_global():
    return globals()

state=[]
operations=deque([])

def start():
    global state
    thread.start_new_thread (wxpush.main,(state,operations))
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