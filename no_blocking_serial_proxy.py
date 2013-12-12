#!/usr/bin/env python
# -*- coding: utf-8 -*-

import select
import socket
import Queue
import threading
import time

class NoBlockingSerialProxy(threading.Thread):
    def __init__(self, name, detector_ip, detector_port, service_port, max_clients_num, listener=None):
        threading.Thread.__init__(self)
        self.name = name
        self.detector_addr = (detector_ip, detector_port)
        self.server_addr = ("", service_port);
        self.listener = listener
        self.serial_queue = Queue.Queue()
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

    def open_serial(self):


    def close_serial(self):


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
        while not self.serial_queue.empty():
            data = self.serial_queue.get()
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
