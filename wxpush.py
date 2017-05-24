# encoding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
import json
import sys
from wxbot.wxbot import WXBot

class Mystd(object):
    
    def __init__(self,msg):
        self.msg=msg
        
    def write(self, output_stream):
        self.msg.append({'key':'msg','value':output_stream})
        
class MyWXBot(WXBot,object):
    def __init__(self,state,operations):
        super(MyWXBot,self).__init__()
        self.state=state
        self.operations=operations
        sys.stdout=Mystd(self.state)
        
    def proc_msg(self):
        self.state.append({'key':'contact_list','value':self.contact_list})
        while True:
            while len(self.operations > 0):
                operation = self.operations.popleft()
                pass
    
    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            self.send_msg_by_uid(u'hi', msg['user']['id'])
            #self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            #self.send_file_msg_by_uid("img/1.png", msg['user']['id'])
'''
    def schedule(self):
        self.send_msg(u'张三', u'测试')
        time.sleep(1)
'''
bot=None

def main(state,operations):
    global bot
    bot = MyWXBot(state,operations)
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()
