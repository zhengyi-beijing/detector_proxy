# producer_consumer_queue

from SocketServer import ThreadingTCPServer, StreamRequestHandler
import traceback
import socket

from Queue import Queue
import random
import threading
import time
import sys

#
class MyCmdBaseRequestHandlerr(StreamRequestHandler):
    def handle(self):
        while True:
            try:
                data = self.request.recv(128).strip 
                print "receive from (%r):%r" % (self.client_address, data)
                if len(data) > 0 :
                    if cmp(data, '[close]') == 0 :
                        exit()
                        break;
                    self.server.detector_socket.send(data)
                    response = self.server.detector_socket.recv(128)
                    self.wfile.write(response)
            except:
                self.server.detector_socket.close()
                traceback.print_exc()
                exit()
                break
class CmdTCPServer(ThreadingTCPServer):
    def __init__(self, service_addr, handler, detector_socket):
        ThreadingTCPServer.__init__(self, service_addr, handler)
        self.detector_socket = detector_socket

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
        server.serve_forever()

#current implement tation for image channel just support one client
class MyImgStreamRequestHandlerr(StreamRequestHandler):
    def handle(self):
        while True:
            try:
                data = self.server.detector_socket.recv(1024)
                self.wfile.write(data)
            except:
                traceback.print_exc()
                break

class ImgTCPServer(ThreadingTCPServer):
    def __init__(self, service_addr, handler, detector_socket):
        ThreadingTCPServer.__init__(self, service_addr, handler)
        self.detector_socket = detector_socket

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
        server.serve_forever()
#Producer thread
class Producer(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data=queue

    def run(self):
        for i in range(5):
            print "%s: %s is producing %d to the queue!/n" %(time.ctime(), self.getName(), i)
            self.data.put(i)
            time.sleep(random.randrange(10)/5)
        print "%s: %s finished!" %(time.ctime(), self.getName())

 

#Consumer thread

class Consumer(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data=queue

    def run(self):
        for i in range(5):
            val = self.data.get()
            print "%s: %s is consuming. %d in the queue is consumed!/n" %(time.ctime(), self.getName(), val)
            time.sleep(random.randrange(10))
        print "%s: %s finished!" %(time.ctime(), self.getName())

 

#Main thread

def main():

    #queue = Queue()

    #producer = Producer('Pro.', queue)


    #producer.start()

    #consumer.start()

    #producer.join()

    #consumer.join()

    cmd_proxy = CmdProxy("10.211.55.4", 9000, 9000)
    cmd_proxy.setDaemon(True)
    cmd_proxy.connect()
    cmd_proxy.start()

    img_proxy = ImgProxy("10.211.55.4", 8888, 8888)
    img_proxy.setDaemon(True)
    img_proxy.connect()
    img_proxy.start()

    cmd_proxy.join()
    img_proxy.join()

    print 'All threads terminate!'

if __name__ == '__main__':

    main()


