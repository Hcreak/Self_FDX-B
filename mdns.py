# coding=utf-8

from zeroconf import Zeroconf
import socket
 
class Listener:
 
    def add_service(self, zeroconf, serviceType, name):
 
        info = zeroconf.get_service_info(serviceType, name)
 
        print "Address: " + str(socket.inet_ntoa(info.address))
        print "Port: " + str(info.port)
        print "Service Name: " + info.name
        print "Server: " + info.server
        print "Properties: " + str(info.properties)
    
 
zconf = Zeroconf()
 
serviceListener = Listener()
 
zconf.add_service_listener("_fdx-b._tcp.local.", serviceListener)
 
raw_input("Press enter to close... \n")
zconf.close()