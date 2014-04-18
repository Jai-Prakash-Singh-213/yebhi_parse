import base64
from random import choice
import subprocess
import sys
import os
import time

#f = open("/home/desktop/proxy5")
#f = open("/home/user/Desktop/proxy5")
f = open("/home/desktop/proxy_http_auth.txt")

ip_list = f.read().strip().split("\n")
f.close()


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        #ip_port = choice(ip_list).strip()
        ip_port = choice(ip_list).strip().split("@")
        
        print "*"*145
        print "myproxy: ", str(ip_port)

        request.meta['proxy'] = "http://"+ip_port[1]
        #proxy_user_pass = user_pass = "vinku:india123"
        proxy_user_pass = user_pass = ip_port[0]

        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
