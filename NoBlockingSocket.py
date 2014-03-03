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

def empty_noblocking_socket(sock):
    """remove the data present on the socket"""
    input = [sock]
    while True:
        inputready, o, e = select.select(input,[],[], 0.0)
        if len(inputready)==0:
            break
        for s in inputready: s.recv(1)

class Monitor:
    def pre_process_data(data):
        pass
    def post_process_data(data):
        pass

class SocketClientThread(threading.Thread):
    def __init__(self, name, addr, input_queue, output_queue, monitor = None):
        threading.Thread.__init__(self)
        self.name = name
        self.output_queue = output_queue
        self.input_queue = input_queue
        self.timeout = 1
        self.addr = addr
        self.daemon = True
        self.sockets = []
        self.monitor = None
        self.Alive =True
        self.clearBuf = False
        self.connected = False
        self.open()
        self.pingFlag = False

            

    def ping(self):
        cmd = "[PI]"
        if(self.input_queue.empty()):
            self.pingFlag = True            
            self.input_queue.put(cmd)                
        
    def setMonitor(self, monitor):
        self.monitor = monitor

    def open(self):
        clearQueue(self.input_queue)
        clearQueue(self.output_queue)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
        try:
            self.socket.setblocking(False)
            print self.name+"::"
            print "open_detector Tring connect to ", self.addr
            self.socket.connect(self.addr)
			
            print "open_detector connected  "

        except socket.error, msg:
            print socket.error, msg
        if not (self.socket in self.sockets):
            self.sockets.append(self.socket)
        return True

    def _close(self):
        clearQueue(self.input_queue)
        clearQueue(self.output_queue)
        self.connected = False
        if not self.socket:
            return
        self.socket.close()
        #self.sockets.remove(self.socket)
        self.socket = None;


    def on_socket_readable(self, s):
        try:
            data = s.recv(4096)
            if data :
        #        print "on_detector_data_comming: received data:", data
                if(self.pingFlag):
                    self.pingFlag = False;
                    print "get ping return" + data
                else:
                    self.output_queue.put(data)
                return True
            else:
                print "detector close the socket:\n"
                self.connected = False
                return False
        except socket.error, e:
            (err_no, err_msg) = e
            print "error is %s"%err_msg
            print "errornumber is %d"%err_no

            return False

    def on_socket_writable(self,s):
        if self.connected == False:
            print "Socket became writable, connected is true"
            self.connected = True
        if  not self.input_queue.empty():
            data = self.input_queue.get()
            try:
                self.socket.send(data)
                
            except socket.error, e:
                (err_no, err_msg) = e
                print "error is %s"%err_msg
                print "errornumber is %d"%err_no
                return False
        return True
        
    def run(self):
        print "start client thread"
        while self.Alive:
            if self.clearBuf:
                empty_noblocking_socket(self.socket)
                clearQueue(self.queue)
                self.clearBuf = False
            try:
                readable, writable, exceptional = select.select (self.sockets, self.sockets, [], self.timeout)
            except Exception as e:
                print "socket select exception happen:\n"
                print e
                self.sockets = []
                self.socket.close()
                self.connected = False
            #    break
            for s in writable:
                if s is self.socket:
                    if not self.on_socket_writable(s):
                        print "Client Thread Write Error "
                        self.sockets.remove(s)
                        s.close()
                        self.connected = False
                        break;
            for s in readable:
                if s is self.socket:
                    if not self.on_socket_readable (s):
                        print "Client Thread Read Error "
                        self.sockets.remove(s)
                        s.close()
                        self.connected = False

                        break;



        self._close()
        print "quit Socket Client Thread"

    def set_clear_flag(self):
        self.clearBuf = True

    def stop(self):
        self.Alive = False


class ProxyThread (threading.Thread):
    def __init__(self, name, service_port, input_queue, output_queue, monitor = None):
        threading.Thread.__init__(self)
        self.name = name
        self.server_addr = ("", service_port);
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.Alive = True;
        self.daemon = True
        self.clearBuf = False
        self.monitor = monitor
        self.timeout = 0.1
        self._open()

    def setMonitor(self, monitor):
        self.monitor = monitor

    def _open(self):
        #create listener socket
        #Only allow one connection
        #When new connection come, recreate the detector connection a
        self._close()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.server_addr)
        print "%s listening \n"%self.name
        self.server.listen(1)
        self.inputs = [self.server]

    def _close(self):
        clearQueue(self.input_queue)
        clearQueue(self.output_queue)
        if hasattr(self, 'inputs'):
            for socket in self.inputs:
                socket.close()
                self.inputs.remove(socket)


    def on_new_client_comming(self, s):
        connection, client_addr = s.accept()
        print "%s on_new_client_comming"%self.name
        print "connection from ", client_addr
        connection.setblocking(False)
        self.inputs.append(connection)

    def remove_socket (self, s):
        if s in self.inputs:
            print "**** Remove socket***"
            self.inputs.remove(s)
        s.close()

    def on_client_readable(self, s):
        try:
            print "on_client_data_comming\n"
            data = s.recv(128)
            if data:
                print "Proxy get data %s\n"% data
                send = True
                if self.monitor:
                    print "call pre_processs_data"
                    send = self.monitor.pre_process_data(data)
                if (send):
                    self.input_queue.put(data)
            else:
                print "*************closing client\n"
                print " ********* There is %d sockets in inputs"%len(self.inputs)
                self.remove_socket(s)
                print " ********* There is %d sockets in inputs"%len(self.inputs)
        except socket.error, e:
            (err_no, err_msg) = e
            print "error is %s"%err_msg
            print "errornumber is %d"%err_no
            if(err_no == 10054):
                self.remove_socket(s)


    def on_client_writable(self,s):
        if  not self.output_queue.empty():
            data = self.output_queue.get()
            try:
                #print "on_client_writable:: write %s\n"%data
                s.send(data)
            except socket.error, e:
                (err_no, err_msg) = e
                print "error is %s"%err_msg
                print "errornumber is %d"%err_no
                if(err_no == 10054):
                    self.remove_socket(s)

    def process(self):
        print "start process"
        while self.Alive:
            readable, writable, exceptional = select.select (self.inputs, self.inputs, self.inputs, self.timeout)
            for s in readable:
                if s is self.server:
                    #there is new connect request
                    self.on_new_client_comming (s)
                        
                else:
                    #data comming from client
                    self.on_client_readable(s)
                        #Something wrong happen 
                                                
            for s in writable:
                if s is not self.server:
                    self.on_client_writable(s)

        print "quit proxy process\n"
        for s in self.inputs:
            s.close()

    def run(self):
        print "detector server run\n"
        self.process()
        print "DetectorServer proxy q%suit" % self.name
        self._close()

    def stop(self):
        print "get interrupt stop"
        self.Alive = False
