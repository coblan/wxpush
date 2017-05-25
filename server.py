# encoding:utf-8
import os
import urlparse
import json
import ajax
from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import wxpush
import urlparse

class HybirdServer(BaseHTTPRequestHandler):  
    def do_GET(self):  
  
        o=urlparse.urlparse(self.path)
        args=dict(urlparse.parse_qsl(o.query))
        data=''
        path = o.path
        self.protocal_version = 'HTTP/1.1'
        self.send_response(200)  
        self.send_header("Welcome", "Contect") 
        
        data=''
        
        if path=='/proxy':
            print('proxy')
            img_url = urlparse.unquote(args['url'])
            rt=wxpush.bot.session.get('https://wx2.qq.com'+img_url)
            for k,v in rt.headers.items():
                self.send_header(k,v)
            data=rt.content
        else:
            if path.endswith('png'):
                self.send_header('content-type','image/png') 
            with open('.'+path,'rb') as f:
                data=f.read()        
        self.end_headers()  
        
        self.wfile.write(data)
        
    
    def do_POST(self):

        self.protocal_version = 'HTTP/1.1'
        self.send_response(200)  
        self.send_header("Welcome", "Contect")     
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('content-type','application/json')
        self.end_headers()  
        
        varLen = int(self.headers['Content-Length'])
        
        if varLen:
            body=self.rfile.read(varLen)
        else:
            body=self.rfile.read()
        call_list=json.loads(body)
        for call_item in call_list:
            fun_name=call_item.pop('fun')
            fun_dc=ajax.get_global()
            rt =fun_dc[fun_name](**call_item)
        self.wfile.write(json.dumps(rt))
         

        
  
def start_server(port):  
    http_server = HTTPServer(('127.0.0.1', int(port)), HybirdServer)  
    http_server.serve_forever() #设置一直监听并接收请求



def get_files(path):
    ls = os.listdir(path)
    return ls
   

def get_img():
    
    return r'D:\work\coloring_backend\media\pool\1_pool_cover.png'

if __name__=='__main__':
    start_server(28289)