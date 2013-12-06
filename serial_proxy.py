#python
import serial

from SocketServer import ThreadingTCPServer, StreamRequestHandler
import socket
import threading
import time
import sys

class MyCmdBaseRequestHandlerr(StreamRequestHandler):
    def handle(self):
        while True:
            try:
                #The command need to remove the \r\n
                data = self.request.recv(128).strip() 
                print "receive from (%r):%r" % (self.client_address, data)
                if len(data) > 0 :
                    if cmp(data, '[close]') == 0 :
                        self.server.shutdown()
                        break;
                    print "goin to write\n"
                    self.server.detector_serial.write(data)
                    self.server.detector_serial.timeout=2
                    print "going to read"
                    #The max length of the return msg is 13 bytes
                    response = self.server.detector_serial.read(13)
                    
                    if len(response) > 0:
                        int_list = [int(i) for i in response]
                        hex_list = [hex(i) for i in int_list]
                        print "return is " + hex_list
                        self.wfile.write(response)
                elif len(data) == 0:
                    break;
                if self.server.stopped:
                    break;
            except:
                self.server.shutdown()
                traceback.print_exc()
                break

class CmdTCPServer(ThreadingTCPServer):
    def __init__(self, service_addr, handler, serial):
        ThreadingTCPServer.__init__(self, service_addr, handler)
        self.detector_serial = serial
        self.stopped = False;   
        
    def serve_forever(self):
        while not self.stopped:
            self.handle_request()
    
    def force_stop (self):
        self.server_close()
        self.stopped = True

class CmdProxy(threading.Thread):
    def __init__(self, service_port ):
        threading.Thread.__init__(self, name='CmdProxy')
        self.service_port = service_port

    def connect(self):
        try:
            self.detector_serial  = serial.Serial("COM2")
            self.detector_serial.timeout = 2
            #self.detector_serial  = serial.Serial('/dev/tty.usbserial-FT20E5D5')
            print self.detector_serial.portstr
            print "serial connect successful"
        except Exception, e:
            print "error open serial port: " + str(e)
    
    def run(self):
        service_addr = ('', self.service_port)
   
        #start service
        try:
            self.server = CmdTCPServer(service_addr, MyCmdBaseRequestHandlerr, self.detector_serial)
            print "run tcp server"
            self.server.serve_forever()
        except Exception,  e:
            print "error start CmdTCP server  " + str(e)
            self.server.shutdown()
        finally: 
            if self.detector_serial:  
                self.detector_serial.close()

def start_proxy ():
    cmd_proxy = CmdProxy(1234);
    cmd_proxy.connect()
    cmd_proxy.start()

if __name__ == '__main__':

    start_proxy()
