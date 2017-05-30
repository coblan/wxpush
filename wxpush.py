# encoding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
import json
import sys
from wxbot.wxbot import WXBot
import time

import logging
front_log=logging.getLogger('front')

        
class MyWXBot(WXBot,object):
    
    def init(self):
        url = self.base_uri + '/webwxinit?r=%i&lang=en_US&pass_ticket=%s' % (int(time.time()), self.pass_ticket)
        params = {
            'BaseRequest': self.base_request
        }
        r = self.session.post(url, data=json.dumps(params))
        r.encoding = 'utf-8'
        dic = json.loads(r.text)
        self.get_ex_group_list(dic.get('ContactList',[]))
        self.sync_key = dic['SyncKey']
        self.my_account = dic['User']
        self.sync_key_str = '|'.join([str(keyVal['Key']) + '_' + str(keyVal['Val'])
                                      for keyVal in self.sync_key['List']])
        return dic['BaseResponse']['Ret'] == 0
    
    def get_ex_group_list(self,contact_list):
        self.ex_group_list=[]
        for contact in contact_list:
            if contact['UserName'].find('@@') != -1:  # 群聊
                self.ex_group_list.append(contact)
    
    def __init__(self,state,operations):
        super(MyWXBot,self).__init__()
        self.state=state
        self.operations=operations
        #sys.stdout=Mystd(self.state)
           
    
    def proc_msg(self):
        front_log.info('登陆成功')
        self.state.append({'key':'login','value':True})
        self.test_sync_check()
        self.status = 'loginsuccess'  #WxbotManage使用
        
        group_list=self.ex_group_list + self.group_list
        self.state.append({'key':'contact_list','value':self.contact_list})
        self.state.append({'key':'group_list','value':group_list})
        self.state.append({'key':'my_account','value':self.my_account})
        
        
        while True:
            if self.status == 'wait4loginout':  #WxbotManage使用
                break 
            
            #while len(self.operations > 0):
                #operation = self.operations.popleft() # 还没弄
                #if operation['func']
                
            check_time = time.time()
            try:
                [retcode, selector] = self.sync_check()
                # print '[DEBUG] sync_check:', retcode, selector
                if retcode == '1100':  # 从微信客户端上登出
                    self.state.append({'key':'msg','value':'从微信客户端上登出'})
                    break
                elif retcode == '1101':  # 从其它设备上登了网页微信
                    self.state.append({'key':'msg','value':'从其它设备上登了网页微信'})
                    break
                elif retcode == '0':
                    if selector == '2':  # 有新消息
                        r = self.sync()
                        if r is not None:
                            self.handle_msg(r)
                    elif selector == '3':  # 未知
                        r = self.sync()
                        if r is not None:
                            self.handle_msg(r)
                    elif selector == '4':  # 通讯录更新
                        r = self.sync()
                        if r is not None:
                            self.get_contact()
                    elif selector == '6':  # 可能是红包
                        r = self.sync()
                        if r is not None:
                            self.handle_msg(r)
                    elif selector == '7':  # 在手机上操作了微信
                        r = self.sync()
                        if r is not None:
                            self.handle_msg(r)
                    elif selector == '0':  # 无事件
                        pass
                    else:
                        print '[DEBUG] sync_check:', retcode, selector
                        r = self.sync()
                        if r is not None:
                            self.handle_msg(r)
                else:
                    print '[DEBUG] sync_check:', retcode, selector
                    time.sleep(10)
                self.schedule()
            except:
                print '[ERROR] Except in proc_msg'
                print format_exc()
            check_time = time.time() - check_time
            if check_time < 0.8:
                time.sleep(1 - check_time)

    
    def handle_msg_all(self, msg):
        pass
        #if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            #self.send_msg_by_uid(u'hi', msg['user']['id'])
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
    #bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()
    front_log.info('上次用户监听循环退出/用户退出成功')


if __name__ == '__main__':
    main()
