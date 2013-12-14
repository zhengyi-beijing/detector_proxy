#!/usr/bin/env python
# -*- coding: utf-8 -*-

import select
import socket
import Queue
import threading
import time

def clearQueue(queue):
    while not queue.empty():
        queue.get()

def empty_socket(sock):
    """remove the data present on the socket"""
    input = [sock]
    while 1:
        inputready, o, e = select.select(input,[],[], 0.0)
        if len(inputready)==0: break
        for s in inputready: s.recv(1)


class NoBlockingProxy(threading.Thread):
    def __init__(self, name, detector_ip, detector_port, service_port, max_clients_num=1, listener=None):
        threading.Thread.__init__(self)
        self.name = name
        self.detector_addr = (detector_ip, detector_port)
        self.server_addr = ("", service_port);
        self.listener = listener
        self.detector_queue = Queue.Queue()
        self.client_queue = Queue.Queue()
        self.Alive = True;
        self.max_clients_num = max_clients_num
        self.daemon = True
        self.clearBuf = False

    def init(self):
        #create listener socket
        #Only allow one connection
        #When new connection come, recreate the detector connection a
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.server_addr)
        print "%s listening \n"%self.name
        self.server.listen(self.max_clients_num)

        self.inputs = [self.server]
        self.timeout = 10

        self.detector = None;


    def open_detector(self):

        if not self.detector is None:
            self.detector.close()
            time.sleep(1)
            self.detector = None
        clearQueue (self.detector_queue)
        self.detector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.detector.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192*4)
        try:
            self.detector.setblocking(False)
            print self.name+"::"
            print "open_detector Tring connect to ", self.detector_addr
            self.detector.connect(self.detector_addr)
            print "open_detector connected  "
            #self.detector.setblocking(False)

            return True;
        except socket.error, msg:
            print msg
        self.inputs.append(self.detector)

        return True

    def close_detector(self):
        self.detector.close()
        while not self.detector_queue.empty():
            self.detector_queue.get()
        self.inputs.remove(self.detector)
        self.detector = None;


    def on_new_client_comming(self, s):
        connection, client_addr = s.accept()
        print "%s on_new_client_comming"%self.name
        print "connection from ", client_addr
        connection.setblocking(False)

        self.inputs.append(connection)
#        if self.max_clients_num ==1:
#            self.close_detector()
        self.open_detector()


    def on_detector_data_comming(self,s):
        try:
            data = s.recv(4096)
            if data :
        #        print "on_detector_data_comming: received data:", data
                self.detector_queue.put(data)
            else:
                print "detector close the socket:\n"
                self.close_detector()
        except:
            print "detector recv exception happen:\n"
            self.close_detector()

    def pre_process_cmd (self, cmd):
        pass

    def post_process_cmd(self, cmd):
        pass

    def remove_socket (self, s):
        if s in self.inputs:
            print "**** Remove socket***"
            #self.inputs.remove(s)
            self.inputs = [ i for i in self.inputs if i!=s]
            s.close()

    def on_client_data_comming(self, s):
        try:
            print "on_client_data_comming\n"
            data = s.recv(128)
            self.pre_process_cmd(data)
            if data:
                self.client_queue.put(data)
            else:
                print "*************closing client\n"
                print " ********* There is %d sockets in inputs"%len(self.inputs)
                self.remove_socket(s)
                self.remove_socket(self.detector)
                print " ********* There is %d sockets in inputs"%len(self.inputs)
        except socket.error, e:
                print "error is no blocking"


    def on_detector_writable(self,s):
        while not self.client_queue.empty():

            data = self.client_queue.get()
            try:
                print "on_detector_writable:: write %s\n"%data
                self.detector.send(data)
                self.post_process_cmd(data)
            except socket.error, msg:
                print "detector send data error%s\n"% msg[1]

    def on_client_writable(self,s):
        while not self.detector_queue.empty():
            data = self.detector_queue.get()
            try:
                #print "on_client_writable:: write %s\n"%data
                s.send(data)
            except socket.error, msg:
                print "detector send data error%s\n"% msg[1]

    def set_clear_flag(self):
        self.clearBuf = True

    def process(self):
        print "start process"
        
        while self.Alive:
            if self.clearBuf:
                empty_socket(self.detector)
                clearQueue(self.detector_queue)
                self.clearBuf = False
            readable, writable, exceptional = select.select (self.inputs, self.inputs, self.inputs, self.timeout)
            for s in readable:
                if s is self.server:
                    #there is new connect request
                    self.on_new_client_comming (s)
                else:
                    #data comming from detector
                    if s is self.detector:
                        self.on_detector_data_comming (s)
                    else:
                        #data comming from client
                        self.on_client_data_comming (s)
            for s in writable:
                if s is self.detector:
                    self.on_detector_writable(s)
                else:
                    self.on_client_writable(s)

        print "quit process\n"
    def run(self):
        print "detector server run\n"
        self.init()
        self.process()
        print "DetectorServer q%suit" % self.name

    def stop(self):
        print "get interrupt stop"
        self.Alive = False

class CmdChannelProxy (NoBlockingProxy):
    def __init__(self, name, detector_ip, detector_port, service_port, max_clients_num, listener=None):
        NoBlockingProxy.__init__(self, name, detector_ip, detector_port, service_port, max_clients_num, listener);
        self.img_channel_proxy =None

    def set_img_channel_proxy (self, proxy):
        self.img_channel_proxy = proxy


    def pre_process_cmd(self, cmd):
        if cmd:
            return
        else:
            #shutdown the detector cmd and img channel because cmd client shut down
            pass

    def post_process_cmd(self, cmd):
        if "[SF,0]" in cmd:
            print "CmdChannel get SF,0"
            time.sleep(0.5)
            #Not sure do I need to call clear buf on proxy side.
            #according to the xview code, the xview should clear all remain data in socket pipe in 250 ms
            self.img_channel_proxy.set_clear_flag()

        if "ST,W" in cmd:
            pass

class DetectorServer():
    def __init__(self):
        self.cmd_proxy = None
        self.img_proxy = None

    def start(self, name, detector_ip, cmd_port, img_port, service_cmd_port, service_img_port, listener = None):
        print "detector server start\n"
        self.cmd_proxy = CmdChannelProxy("CmdPrxory", detector_ip, cmd_port, service_cmd_port, 1, listener);
        self.img_proxy = NoBlockingProxy("ImgProxy", detector_ip, img_port, service_img_port, 1, listener)
        self.cmd_proxy.set_img_channel_proxy(self.img_proxy)

        self.cmd_proxy.start()
        self.img_proxy.start()
        

    def stop(self):
        self.cmd_proxy.stop()
        self.img_proxy.stop()

if __name__ == "__main__":
    #server = start_server("imgServer", "192.168.2.2", 4001, 4001)
    try:
        server = DetectorServer()
        server.start("Server", "127.0.0.1", 3000, 4001, 3001,4002)

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "get key"
        stop_server(server)
