#!/usr/bin/env python
# -*- coding: utf-8 -*-
from SocketServer import ThreadingTCPServer, StreamRequestHandler
import traceback
import socket

from Queue import Queue
import random
import threading
import time
import sys,  getopt

#current implement tation for image channel just support one client
DataReady = threading.Condition()

class Receiver(threading.Thread):
    def __init__(self, t_name, socket, queue):
        threading.Thread.__init__(self, name= t_name)
        self.queue = queue
        self.socket = socket
    def run():
        while True:
            try:
                data = self.socket.recv(1024)
                self.server.queue.put(data)
            except:
                traceback.print_exc()
                break

class MyImgBaseRequestHandlerr(StreamRequestHandler):
    def handle(self):

        while True:
            try:
                data = self.server.queue.get()
                if data == None:
                    print "Img Sender data is None quit\n"
                    break
                self.request.send(data)
                #print "#"
                if self.server.stopped:
                    break;
            except:
                traceback.print_exc()
                break

class ImgTCPServer(ThreadingTCPServer):
    def __init__(self, service_addr, handler, listener, queue):
        ThreadingTCPServer.__init__(self, service_addr, handler)
        self.stopped = False
        self.listener = listener
        self.queue = queue

    def serve_forever(self):
        while not self.stopped:
            self.handle_request()

    def force_stop (self):
        print "ImgTCPServer force quit"
        self.queue.put(None)
        self.stopped = True
        self.detector_socket.close ()
        self.server_close()

class ImgProxy(threading.Thread):
    def __init__(self, detector_ip, detector_img_port, service_port, listener):
        threading.Thread.__init__(self, name='CmdProxy')
        self.detector_ip = detector_ip
        self.detector_img_port = detector_img_port
        self.service_port = service_port
        self.listener = listener
        self.queue = Queue()

    def connect(self):
        detector_addr = (self.detector_ip, self.detector_img_port)
        self.detector_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.detector_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096*8192)
        #self.detector_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
        #self.detector_socket.settimeout(4)
        bufsize = self.detector_socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF);
        print "ImgProxy:: recv buf size is %d \n" % bufsize
        try:
            #import pdb
            #pdb.set_trace()
            self.detector_socket.connect(detector_addr)
            print "ImgProxy:: detector connect successful"
            self.listener.set_detector_connected(True)
            self.receiver = Receiver("receiver", self.detector_socket, self.queue)

        except socket.error, msg:

            print "ImgProxy:: detector connect failed:[ERROR] %s\n" % msg[1]
            self.listener.set_detector_connected(False)

    def run(self):
        service_addr = ('', self.service_port)

        #start service
        self.server = ImgTCPServer(service_addr, MyImgBaseRequestHandlerr, self.detector_socket, self.listener, self.queue)
        self.server.serve_forever()

    def stop(self):
        #close socket should cause exception on the receiver
        self.detector_socket.close()
        self.server.force_stop()

def start_proxy(detector_ip, detector_cmd_port, service_port,listener):
    try:

        proxy = ImgProxy(detector_ip, detector_cmd_port, service_port,listener)
        proxy.setDaemon(True)
        proxy.connect()
        proxy.start()
        return proxy;
    except Exception, e:
        print "error start ImgTCP server  " + str(e)
        traceback.print_exc()
        proxy.stop()
