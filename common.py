import uuid
import logging


msg_list= []

def get_mac_address(): 
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
    return ":".join([mac[e:e+2] for e in range(0,11,2)])


class FrontHandler(logging.Handler):
    def emit(self,record):
        global msg_list
        msg_list.append({'key':'msg','value':record.getMessage()})
    
def fetch_state():
    global msg_list
    rt_state=list(msg_list)
    del msg_list[:]    
    return rt_state

front_log=logging.getLogger('front')
front_log.addHandler(FrontHandler(level='INFO'))
front_log.setLevel('INFO')

from logging.handlers import RotatingFileHandler

back_log=logging.getLogger('back')
back_log.addHandler(RotatingFileHandler('./temp/inst_log.txt',maxBytes='1024*1024',backupCount=2))
back_log.setLevel('INFO')

class Mystd(object): 
    def write(self, output_stream):
        back_log.info(output_stream)     