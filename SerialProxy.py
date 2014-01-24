#python
import serial

import socket
import threading
import time
import sys
import tcp_serial_redirect as TcpRedirector

SerialServicePort=1234
COM = "COM2"

class NoBlockingSerialProxy(threading.Thread):
    def __init__(self, service_port, listener):
        threading.Thread.__init__(self)
        self.port = service_port
        self.listener = listener
        self.Alive = True
        self.setupSerial()
        self.daemon = True
        self.redirector = None

    def setupSerial(self):
        self.ser = serial.Serial()
        self.ser.port     = "COM2"
        self.ser.timeout  = 1     # required so that the reader thread can exit

    def open(self):
        try:
            self.ser.open()
            return True
        except serial.SerialException, e:
            sys.stderr.write("Could not open serial port %s: %s\n" % (self.ser.portstr, e))
            return False

    def run(self):

        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.bind( ('', self.port) )
        srv.listen(1)
        while self.Alive:
            try:
                print "SerialProxy waiting for connection on %s ...\n"%self.port
                connection, addr = srv.accept()
                print "Connected by %s\n"%(addr,)
                self.redirector = TcpRedirector.Redirector(
                    self.ser,
                    connection,
                    spy = True
                )
                print "Redirector shortcut"
                self.redirector.shortcut()
                print "SerialProxy Disconnected\n"
                connection.close()
            except socket.error, msg:
                sys.stderr.write('ERROR: %s\n' % msg)

    def stop(self):
        if (self.redirector):
            self.redirector.stop()
        self.Alive = False

        print "Redirector stopped"



def start_proxy (listener = None):

    proxy = NoBlockingSerialProxy(SerialServicePort, listener);
    if proxy.open():
        proxy.start()
        return proxy
    else:
        return None




if __name__ == '__main__':

    start_proxy()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(1)
