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

class MyCmdBaseRequestHandlerr(StreamRequestHandler):
    def handle(self):
        g_StatusMonitor.set_client_connected(True)
        while True:
            try:
                data = self.request.recv(128)
                print "receive from (%r):%r" % (self.client_address, data)
                if len(data) > 0 :
                    if data.contains("[SF,1]")  :
                        self.server.listener.set_detector_running(True);
                    elif data.contains("[SF,0]"):
                        self.server.listener.set_detector_running(False);
                        break;
                    try:
                        self.server.detector_socket.send(data)
                        response = self.server.detector_socket.recv(128)
                        self.wfile.write(response)
                    except socket.timeout:
                        print "CmdProxy:: detector socket timeout"
                    except:
                        log =  "CmdProxy:: failed of Detector\n"
                        print log
                        self.server.listener.set_trace_info(log)
                elif len(data) == 0:
                    log = "CmdProxy:: get remote socket shutdown\n"
                    print(log)
                    self.server.listener.set_trace_info(log)
                    break;

                if server.stopped:
                    print "CmfProxy:: server.stop flag set\n"
                    break;
            except:
                self.server.detector_socket.close()
                print "CmdProxy:: get exeception in socket handler, quit\n"
                #traceback.print_exc()
                break
            self.server.listener.set_client_connected(False)

class CmdTCPServer(ThreadingTCPServer):
    def __init__(self, service_addr, handler, detector_socket, listener):
        ThreadingTCPServer.__init__(self, service_addr, handler)
        self.detector_socket = detector_socket
        self.stopped = False;
        self.listener = listener;
    def serve_forever(self):
        while not self.stopped:
            self.handle_request()
    def force_stop (self):
        self.stopped = True
        self.server_close()
        self.detector_socket.close ()



class CmdProxy(threading.Thread):
    def __init__(self, detector_ip, detector_cmd_port, service_port, listener):
        threading.Thread.__init__(self, name='CmdProxy')
        self.detector_ip = detector_ip
        self.detector_cmd_port = detector_cmd_port
        self.service_port = service_port
        self.listener = listener
    def connect(self):
        detector_addr = (self.detector_ip, self.detector_cmd_port)
        print "Cmd:proxy addr is " + str(detector_addr)
        self.detector_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.detector_socket.settimeout(2)
            self.detector_socket.connect(detector_addr)

            print "connect successful"
            self.listener.set_detector_connected(True)
        except socket.error, msg:
            print "CmdProxy:: [ERROR] %s\n" % msg[1]
            self.listener.set_detector_connected(False)

    def stop(self):
        server.force_stop()

    def run(self):
        service_addr = ('', self.service_port)

        #start service
        server = CmdTCPServer(service_addr, MyCmdBaseRequestHandlerr, self.detector_socket, self.listener)
        #try:
        server.serve_forever()
        #except KeyboardInterrupt:
        #    server.force_stop()

def start_proxy(detector_ip, detector_cmd_port, service_port,listener):
    try:

        proxy = CmdProxy(detector_ip, detector_cmd_port, service_port,listener)
        proxy.setDaemon(True)
        proxy.connect()
        proxy.start()
        return proxy;
    except Exception, e:
        print "CmdProxy:: error start CmdTCP server  " + str(e)
        traceback.print_exc()
        proxy.stop()
