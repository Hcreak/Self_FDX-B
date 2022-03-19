# coding=utf-8

from zeroconf import Zeroconf
from socket import *
 
import time

connect_target = ()

class Listener:
 
    def add_service(self, zeroconf, serviceType, name):
 
        info = zeroconf.get_service_info(serviceType, name)
 
        print "Address: " + str(inet_ntoa(info.address))
        print "Port: " + str(info.port)
        print "Service Name: " + info.name
        print "Server: " + info.server
        print "Properties: " + str(info.properties)

        global connect_target
        connect_target = (str(inet_ntoa(info.address)), int(info.port))
 
zconf = Zeroconf()
 
serviceListener = Listener()
 
zconf.add_service_listener("_fdx-b._tcp.local.", serviceListener)

print "mDNS listening, Wait Ready ...."

while not connect_target:
    print "."
    time.sleep(5)

s = socket(AF_INET,SOCK_STREAM)
s.connect(connect_target)
s.setblocking(False)

print "TCP connected, mDNS Exit."
zconf.close()

while True:
    try:
        print s.recv(1024)
    except:
        pass