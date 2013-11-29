# producer_consumer_queue

from SocketServer import ThreadingTCPServer, StreamRequestHandler
import traceback
import socket

from Queue import Queue
import random
import threading
import time
import sys getopt

#
class MyCmdBaseRequestHandlerr(StreamRequestHandler):
    def handle(self):
        while True:
            try:
                data = self.request.recv(128).strip 
                print "receive from (%r):%r" % (self.client_address, data)
                if len(data) > 0 :
                    if cmp(data, '[close]') == 0 :
                        server.stopped = True; 
                        break;
                    self.server.detector_socket.send(data)
                    response = self.server.detector_socket.recv(128)
                    self.wfile.write(response)
                if server.stopped:
                    break;
            except:
                self.server.detector_socket.close()
                #traceback.print_exc()
                exit()
                break

class CmdTCPServer(ThreadingTCPServer):
    def __init__(self, service_addr, handler, detector_socket):
        ThreadingTCPServer.__init__(self, service_addr, handler)
        self.detector_socket = detector_socket
        self.stopped = False;
    def serve_forever(self):
        while not self.stopped:
            self.handle_request()
    def force_stop (self):
        self.server_close()
        self.detector_socket.close () 
        self.stopped = True


class CmdProxy(threading.Thread):
    def __init__(self, detector_ip, detector_cmd_port, service_port):
        threading.Thread.__init__(self, name='CmdProxy')
        self.detector_ip = detector_ip
        self.detector_cmd_port = detector_cmd_port
        self.service_port = service_port

    def connect(self):
        detector_addr = (self.detector_ip, self.detector_cmd_port)
        self.detector_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.detector_socket.connect(detector_addr)
            print "connect successful"
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            exit()
    
    def run(self):
        service_addr = ('127.0.0.1', self.service_port)
   
        #start service
        server = CmdTCPServer(service_addr, MyCmdStreamRequestHandlerr, self.detector_socket)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.force_stop()

#current implement tation for image channel just support one client
class MyImgStreamRequestHandlerr(StreamRequestHandler):
    def handle(self):
        while True:
            try:
                data = self.server.detector_socket.recv(1024)
                self.wfile.write(data)
                if server.stopped:
                    break;
            except:
                traceback.print_exc()
                break

class ImgTCPServer(ThreadingTCPServer):
    def __init__(self, service_addr, handler, detector_socket):
        ThreadingTCPServer.__init__(self, service_addr, handler)
        self.detector_socket = detector_socket
    def serve_forever(self):
        while not self.stopped:
            self.handle_request()
    def force_stop (self):
        self.server_close()
        self.detector_socket.close () 
        self.stopped = True

class ImgProxy(threading.Thread):
    def __init__(self, detector_ip, detector_img_port, service_port):
        threading.Thread.__init__(self, name='CmdProxy')
        self.detector_ip = detector_ip
        self.detector_img_port = detector_img_port
        self.service_port = service_port

    def connect(self):
        detector_addr = (self.detector_ip, self.detector_img_port)
        self.detector_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.detector_socket.connect(detector_addr)
            print "connect successful"
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            exit()
    def run(self):
        service_addr = ('127.0.0.1', self.service_port)
   
        #start service
        server = ImgTCPServer(service_addr, MyImgStreamRequestHandlerr, self.detector_socket)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
#            server.shutdown()
            server.force_quit()
            

#Main thread
def usage ()
    print "detector_proxy.py usage "
    print "-h print help message"
    print "-d detector ip address"
    print "-c detector cmd port number"
    print "-i detector img port number"

#The way to setup the recv buffer
   # [HKEY_LOCAL_MACHINE \SYSTEM \CurrentControlSet \Services \Afd \Parameters]
   # DefaultReceiveWindow = 16384
   # DefaultSendWindow = 16384
#    int a = 65535;
#    if (setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &a, sizeof(int)) == -1) {
#            fprintf(stderr, "Error setting socket opts: %s\n", strerror(errno));
 #   }

def main():

    opt, args = getopt.getopt(sys.argv[1:], "hd:c:i:")
    detector_ip = ""
    cmd_port = 9000;
    img_port = 8888;
    for op,value in opts
        if op == "-h":
            usage()
            sys.exit(1)
        if op == "-d":
            detector_ip = value
        if op == "-c":
            try:
                cmd_port = int(value)
            except ValueError:
                print "cmd_port should be an integer, set to default value"
                cmd_port = 9000;
        if op == "-i"
            try:
                img_port = int(value)
            except ValueError:
                print "img_port should be an integer, set to default value"
                img_port = 8888;

    #cmd_proxy = CmdProxy("10.211.55.4", 9000, 9000)
    cmd_proxy = CmdProxy(detector_ip, cmd_port, cmd_port)
    cmd_proxy.setDaemon(True)
    cmd_proxy.connect()
    cmd_proxy.start()

    #img_proxy = ImgProxy("10.211.55.4", 8888, 8888)
    img_proxy = ImgProxy(detctor_ip, img_port, img_port)
    img_proxy.setDaemon(True)
    img_proxy.connect()
    img_proxy.start()

    #proxies = [];
    #proxies.append (cmd_proxy)
    #proxies.append (img_proxy)
    #interrupEvent = Threading.Event()
    #while True:
    #    try:
    #        alive = False
    #        for proxy in proxies:
    #            alive = alive or proxy.isAlive()
    #        if not alive:
    #            break;
    #    except KeyboardInterrupt:
    #        interruptEvent.set()
            

    cmd_proxy.join()
    img_proxy.join()

    print 'All threads terminate!'

if __name__ == '__main__':

    main()


