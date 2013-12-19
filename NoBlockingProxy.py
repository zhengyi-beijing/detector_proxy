#!/usr/bin/env python
# -*- coding: utf-8 -*-

import select
import socket
import Queue
import threading
import time
import NoBlockingSocket as NS

class ChannelProxy(object, NS.Monitor):
    def __init__(self, name, detector_ip, detector_port, service_port, listener=None):
        self.input_queue = Queue.Queue()
        self.output_queue = Queue.Queue()
        self.detector_thread  = NS.SocketClientThread(name+"_detector", (detector_ip, service_port), self.input_queue, self.output_queue)
        self.proxy_thread  = NS.ProxyThread(name+"_proxy", service_port, self.input_queue, self.output_queue)

    def start(self):
        self.detector_thread.start()
        self.proxy_thread.start()

    def stop(self):
        self.detector_thread.stop()
        self.proxy_thread.stop()

class ImgProxy (ChannelProxy):
    totalbytes = 0
    def __init__(self, name, detector_ip, detector_port, service_port, listener=None):
        ChannelProxy.__init__(self, name, detector_ip, detector_port, service_port, listener)

    def pre_process_data(self, cmd):
        pass

    def post_process_data(self, cmd):
        #caculate the image bandwidth here
        totalbytes += len(cmd)
        pass

    def set_clear_flag(self):
        self.detector_thread.set_clear_flag()
        self.proxy_thread.set_clear_flag()

class CmdProxy (ChannelProxy):
    def __init__(self, name, detector_ip, detector_port, service_port, listener=None):
        ChannelProxy.__init__(self, name, detector_ip, detector_port, service_port, listener)
        self.img_proxy =None

    def set_img_proxy (self, img_proxy):
        self.img_proxy = img_proxy

    def pre_process_data(self, cmd):
        if "SDR" in cmd:#setup start grab status
            if "1" in cmd:
                pass
            elif "0" in cmd:
                pass
        if "SDC" in cmd: #setup detector connection:
            if "1" in cmd:
                pass
            elif "0" in cmd:
                pass
        if "SDB" in cmd:  #setup battery info
            pass

        if "SDS" in cmd:#setup detector speed
            pass

        if "SSR" in cmd:#setup speaker status
            if "1" in cmd:
                pass
            elif "0" in cmd:
                pass

        if "SES" in cmd:#setup stop button status
            if "1" in cmd:
                pass
            elif "0" in cmd:
                pass

        if "STI" in cmd: #setup the display info: warning msg error etc
            pass

    def post_process_data(self, cmd):
        if "[SF,0]" in cmd:
            print "CmdChannel get SF,0"
            time.sleep(0.5)
            #Not sure do I need to call clear buf on proxy side.
            #according to the xview code, the xview should clear all remain data in socket pipe in 250 ms
            self.img_channel_proxy.set_clear_flag()

        if "ST,W" in cmd:
            pass

class DetectorServer():
    def __init__(self, name, detector_ip, cmd_port, img_port, service_cmd_port, service_img_port, listener = None):
        self.cmd_proxy = CmdProxy("CmdProxy", detector_ip, cmd_port, service_cmd_port, listener)
        self.img_proxy = ImgProxy("ImgProxy", detector_ip, img_port, service_img_port, listener)
        self.cmd_proxy.set_img_proxy(self.img_proxy)

    def start(self):
        self.cmd_proxy.start()
        self.img_proxy.start()
        
    def stop(self):
        self.cmd_proxy.stop()
        self.img_proxy.stop()

if __name__ == "__main__":
    #server = start_server("imgServer", "192.168.2.2", 4001, 4001)
    try:
        server = DetectorServer("127.0.0.1", 3000, 4001, 3001,4002)
        server.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "get key"
        stop_server(server)
