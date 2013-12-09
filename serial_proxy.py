#python
import serial

from SocketServer import ThreadingTCPServer, StreamRequestHandler
import socket
import threading
import time
import sys

SerialServicePort=1234
COM = "COM2"
class MyCmdBaseRequestHandlerr(StreamRequestHandler):
    def handle(self):
        while True:
            try:
                #The command need to remove the \r\n
                data = self.request.recv(128).strip() 
                if len(data) == 0:
                    break;
                print "receive from (%r):%r" % (self.client_address, data)
                if len(data) > 0 :
                    if cmp(data, '[close]') == 0 :
                        self.server.shutdown()
                        break;
                    elif cmp(data, '[on]') == 0 :
                        self.server.listener.set_detector_running(True)
                    elif cmp(data, '[off]') == 0 :
                        print "call off"
                        self.server.listener.set__detector_running(False)
                        print "call end"
                    elif cmp(data, '[sp_on]') == 0:
                        self.server.listener.set_speaker_status (True);
                    elif cmp(data, '[sp_off]') == 0:
                        self.server.listener.set_speaker_status (False);

                    elif cmp(data, '[e_on]') == 0:
                        self.server.listener.set_stop_status (True);
                    elif cmp(data, '[e_off]') == 0:
                        self.server.listener.set_stop_status (False);
                    else:
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
                            if response[0] == 0xaa:
                                self.server.listener.set_trace_info ("ok")
                            else:
                                self.server.listener.set_trace_info ("error")

                if self.server.stopped:
                    break;
            except:
                self.server.shutdown()
                traceback.print_exc()
                break

class CmdTCPServer(ThreadingTCPServer):
    def __init__(self, service_addr, handler, serial, listener):
        ThreadingTCPServer.__init__(self, service_addr, handler)
        self.detector_serial = serial
        self.stopped = False
        self.listener = listener
        
    def serve_forever(self):
        while not self.stopped:
            self.handle_request()
    
    def force_stop (self):
        self.server_close()
        self.stopped = True

class CmdProxy(threading.Thread):
    def __init__(self, service_port, listener):
        threading.Thread.__init__(self, name='CmdProxy')
        self.service_port = service_port
        self.listener = listener
        self.detector_serial = None

    def connect(self):
        try:
            self.detector_serial  = serial.Serial(COM)
            self.detector_serial.timeout = 2
            #self.detector_serial  = serial.Serial('/dev/tty.usbserial-FT20E5D5')
            print self.detector_serial.portstr
            print "serial connect successful"
        except Exception, e:
            print "error open serial port: " + str(e)
    def stop():
        self.server.force_stop()

    def run(self):
        service_addr = ('', self.service_port)
        #start service
        try:
            self.server = CmdTCPServer(service_addr, MyCmdBaseRequestHandlerr, self.detector_serial, self.listener)
            print "run tcp server"
            self.server.serve_forever()
        except Exception,  e:
            print "error start CmdTCP server  " + str(e)
            self.server.shutdown()
        finally: 
            if self.detector_serial is not None:
                self.detector_serial.close()

def start_proxy (listener = None):
     try:
        cmd_proxy = CmdProxy(SerialServicePort, listener);
        cmd_proxy.connect()
        cmd_proxy.start()
     except Exception, e:
        print "error start CmdTCP server  " + str(e)

def stop():
    cmd_proxy.stop()

#if __name__ == '__main__':

#    start_proxy()
