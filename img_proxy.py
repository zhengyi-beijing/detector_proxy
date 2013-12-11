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

class Receiver(threading.Thread):
    def __init__(self, t_name, queue, addr):
        threading.Thread.__init__(self, name= t_name)
        self.queue = queue
        #self.socket = socket
        self.alive =True
        self.addr = addr

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
        try:
            self.socket.connect(self.addr)
            print "ImgProxy:: detector connect successful"
            #self.listener.set_detector_connected(True)
            return True

        except socket.error, msg:
            print "ImgProxy:: detector connect failed:[ERROR] %s\n" % msg[1]
            #self.listener.set_detector_connected(False)
            return False

    def disconnect(self):
        self.socket.close()

    def run(self):
        if self.connect():
            while self.alive:
                try:
                    data = self.socket.recv(1024)
                    self.queue.put(data)
                except:
                    traceback.print_exc()
                    break
            self.disconnect()
            print "Receiveer quit\n"

    def stop(self):
        self.alive = False;

class MyImgBaseRequestHandlerr(StreamRequestHandler):
    def handle(self):
        receiver = Receiver("receiver", self.server.queue, self.server.detector_addr)
        receiver.start()

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
        receiver.stop()
        receiver.join()

class ImgTCPServer(ThreadingTCPServer):
    def __init__(self, service_addr, handler, listener, queue, detector_addr):
        ThreadingTCPServer.__init__(self, service_addr, handler)
        self.stopped = False
        self.listener = listener
        self.queue = queue
        self.detector_addr = detector_addr

    def serve_forever(self):
        while not self.stopped:
            self.handle_request()

    def force_stop (self):
        print "ImgTCPServer force quit"
        self.queue.put(None)
        self.stopped = True
        self.socket.close()
        self.server_close()

class ImgProxy(threading.Thread):
    def __init__(self, detector_ip, detector_img_port, service_port, listener):
        threading.Thread.__init__(self, name='Proxy')
        self.detector_ip = detector_ip
        self.detector_img_port = detector_img_port
        self.service_port = service_port
        self.listener = listener
        self.queue = Queue()



    def run(self):
        service_addr = ('', self.service_port)
        detector_addr = (self.detector_ip, self.detector_img_port)
        #start service
        self.server = ImgTCPServer(service_addr, MyImgBaseRequestHandlerr, self.listener, self.queue, detector_addr)
        self.server.serve_forever()

    def stop(self):
        #close socket should cause exception on the receiver
        #self.detector_socket.close()
        self.server.force_stop()

def start_proxy(detector_ip, detector_cmd_port, service_port,listener):
    try:

        proxy = ImgProxy(detector_ip, detector_cmd_port, service_port,listener)
        proxy.setDaemon(True)
#        proxy.connect()
        proxy.start()
        return proxy;
    except Exception, e:
        print "error start ImgTCP server  " + str(e)
        traceback.print_exc()
        proxy.stop()
