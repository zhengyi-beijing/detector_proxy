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
                data = self.request.recv(128).strip 
                print "receive from (%r):%r" % (self.client_address, data)
                if len(data) > 0 :
                    if cmp(data, '[close]') == 0 :
                        self.server.shutdown()
                        break;

                    self.detector_serial.write(data)
                    response = self.detector_serial.read(128)
                    self.wfile.write(response)
            except:
                self.server.detector_socket.close()
                traceback.print_exc()
                break

class CmdTCPServer(ThreadingTCPServer):
    def __init__(self, service_addr, handler, serial):
        ThreadingTCPServer.__init__(self, service_addr, handler)
        self.detector_serial = serial

class CmdProxy(threading.Thread):
    def __init__(self, service_port ):
        threading.Thread.__init__(self, name='CmdProxy')
        self.service_port = service_port

    def connect(self):
        try:
            #self.detector_serial  = serial.Serial(0)
            self.detector_serial  = serial.Serial('/dev/tty.usbserial-FT20E5D5')
            print self.detector_serial.portstr
            print "connect successful"
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            exit()
    
    def run(self):
        service_addr = ('127.0.0.1', self.service_port)
        #service_addr = ('192.168.1.102', self.service_port)
   
        #start service
        server = CmdTCPServer(service_addr, MyCmdBaseRequestHandlerr, self.detector_serial)
        server.serve_forever()

        server.detector_serial.close()

def main ():
    cmd_proxy = CmdProxy(1234);
    cmd_proxy.connect()
    cmd_proxy.start()
    cmd_proxy.join()

if __name__ == '__main__':

    main()
