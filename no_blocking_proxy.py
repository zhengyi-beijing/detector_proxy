#!/usr/bin/env python
# -*- coding: utf-8 -*-

import select
import socket
import Queue
import threading
import time

class NoBlockingProxy(threading.Thread):
    def __init__(self, name, detector_ip, detector_port, service_port, max_clients_num, listener=None):
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

    def init(self):
        #create listener socket
        #Only allow one connection
        #When new connection come, recreate the detector connection a
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.server_addr)
        self.server.listen(self.max_clients_num)

        self.inputs = [self.server]
        self.timeout = 10

        self.detector = None;

    def open_detector(self):
        if not self.detector is None:
            self.detector.close()
            self.detector = None
        self.detector_queue.clear()
        self.detector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.detector.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192*4)
        try:
            self.detector.setblocking(False)
#            self.detector.settimeout(2)
            self.detector.connect(self.detector_addr)
            self.inputs.append(self.detector)
            return True;
        except socket.error, msg:
            print  ":: detector connect failed:[ERROR] %s\n" % msg[1]
            return False

    def close_detector(self):
        self.detector.close()
        self.detector_queue.clear()
        self.inputs.remove(self.detector)
        self.detector = None;


    def on_new_client_comming(self, s):
        connection, client_addr = s.accept()
        print "connection from ", client_addr
        connection.setblocking(False)
        #connection.setblocking(True)
        #connection.settimeout(2)

        self.inputs.append(connection)
#        if self.max_clients_num ==1:
#            self.close_detector()
        self.open_detector()


    def on_detector_data_comming(self):
        try:
            data = self.detector.recv(4096)
            if data :
                print "received data:", data
                self.detector_queue.put(data)
            else:
                print "detector close the socket:\n"
                self.close_detector()
        except:
            print "detector recv exception happen:\n"
            self.detector.close()
            self.detector_queue.clear()

    def process_cmd (self, cmd):
        print "data is " + data
        pass

    def on_client_data_comming(self, s):
        try:
            data = self.s.recv(128)
            if data:

                self.process_cmd()
                self.client_queue.put(data)
            else:
                print "closing client"
                if s in inputs:
                    inputs.remove(s)
                    s.close()

        except socket.error, e:
                print "error is no blocking"


    def on_detector_writable(self):
        while not self.client_queue.empty():
            data = self.client_queue.get()
            try:
                self.detector.send(data)
            except socket.error, msg:
                print "detector send data error%s\n"% msg[1]

    def on_client_writable(self):
        while not self.detector_queue.empty():
            data = self.detector_queue.get()
            try:
                self.detector.send(data)
            except socket.error, msg:
                print "detector send data error%s\n"% msg[1]


    def process(self):
        print "start process"
        while self.Alive:

            readable, writable, exceptional = select.select (self.inputs, self.inputs, self.inputs, self.timeout)
            for s in readable:
                if s is self.server:
                    #there is new connect request
                    self.on_new_client_comming (s)
                else:
                    #data comming from detector
                    if s is self.detector:
                        self.on_detector_data_comming ()
                    else:
                        #data comming from client
                        self.on_client_data_comming (s)
            for s in writable:
                if s is self.detector:
                    self.on_detector_writable()
                else:
                    self.on_client_writable()

        print "quit process"
    def run(self):
        print "detector server run"
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

    def set_img_channel_proxy (proxy):
        self.img_channel_proxy = proxy

    def process_cmd(self, cmd):
        if cmp(cmd,[SF,1]):
            print "CmdChannel get SF,1"
            img_channel_proxy.open_detector()
        elif cmp(cmd,[SF,0]):
            print "CmdChannel get SF,0"
            img_channel_proxy.close_detector()




def start_server(name, detector_ip, cmd_port_, img_port, service_cmd_port, service_img_port, listener = None):
    cmd_proxy = CmdChannelProxy("name", detector_ip, cmd_port, service_cmd_port, 1, listener);
    server.daemon = True
    img_proxy server = NoBlockingProxy("name", detector_ip, img_port, service_img_port, 1, listener);
    cmd_proxy.set_img_channel_proxy(img_proxy)

    cmd_proxy.start()
    img_proxy.start()
    return True

if __name__ == "__main__":
    #server = start_server("imgServer", "192.168.2.2", 4001, 4001)
    try:
        server = start_server("imgServer", "127.0.0.1", 1234, 4001)
        server.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "get key"
        server.stop()
        server.join()
