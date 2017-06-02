import re
import subprocess
def get_uuid(): 
    ss = subprocess.Popen('wmic csproduct get UUID',stdout=subprocess.PIPE)
    out,inp=ss.communicate()
    mt= re.search('UUID[\s\r\n]*([^\s\r\n]+)',out)
    return mt.group(1)