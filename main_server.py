#coding=utf-8  
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import datetime
import time
import json
from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler
import random




define("port", default=1213, type=int)

class ChatHandler(WebSocketHandler):

    #建立websocket连接
    def open(self):
        self.write_message("connected")
        print("new websocket guest connected")
        pass

    def create_mock_data(self):
        test_array=[]
        for i in range(0,10):
            test_array.append(repr(random.random()*100))
            i = i+1
        return test_array

    #websocket接受信息
    def on_message(self, message):
        if(message=="go" or message =="connected"):
            res=self.create_mock_data()
            info = ' '.join(res)
            self.on_send(info)
        else:
            pass
    
    def on_send(self,message):
        self.write_message(message)

    #关闭websocket    
    def on_close(self):
        print('connection closed')
        pass

    #允许跨域请求
    def check_origin(self, origin):
        return True  

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r"/chat", ChatHandler)],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__), "template"),
        debug = True
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
