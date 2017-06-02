import re
import subprocess
def get_uuid(): 
    ss = subprocess.Popen('wmic csproduct get UUID',stdout=subprocess.PIPE)
    out,inp=ss.communicate()
    mt= re.search('UUID[\s\r\n]*([^\s\r\n]+)',out)
    return mt.group(1)

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