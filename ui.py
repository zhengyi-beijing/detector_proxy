from PyQt4.QtDeclarative import QDeclarativeView

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import cmd_proxy,  serial_proxy, img_proxy
from proxy_monitor import ProxyMonitor 
import threading
import reg
"""
class TestThread(threading.Thread,QObject):
    #Signal define
    signalRunning = pyqtSignal(bool)
    def __init__(self):
        threading.Thread.__init__(self, name='TestThread')
        super(QObject, self).__init__()

        self.flag = 1
        self.alive =True
        self.changed = False
        pass
    def run(self):
        print "Thread start\n"
        while self.alive:
            if self.changed:
                print "Firing  signal %d"% self.flag
                #self.signalRunning.emit(self.flag)
                self.listener.set_detector_running(self.flag)
                self.changed =False
        print "thread end\n"

    def startSignal(self):
        print "######Start Signal"
        print "flag is "+ str(self.flag)
        if self.flag == 1:
            self.changed = False
        else:
            self.flag = 1
            self.changed = True
        print "changed is " + str(self.changed)



    def stopSignal(self):
        print "*****Stop Sginal"
        print "flag is "+ str(self.flag)
        if self.flag == 0:
            self.changed = False
        else:
            self.flag = 0
            print "         self. flag is %d"%self.flag
            self.changed = True

        print "changed is " + str(self.changed)

    def stop(self):
        self.alive = False

    def setListener (self, view):
        self.listener = view
"""


        
class MonitorWindow (QDeclarativeView,  ProxyMonitor):
    signalRunning = pyqtSignal(bool)
    signalXrayBatteryLevel = pyqtSignal(int)
    signalXrayConnection = pyqtSignal(bool)
    signalDetectorBatteryLevel = pyqtSignal(int)
    signalDetectorConnected = pyqtSignal(bool)
    signalSpeakerStatus = pyqtSignal(bool)
    signalStopStatus = pyqtSignal(bool)
    signalTraceInfo = pyqtSignal(str)

    def __init__ (self,  parent = None):
        super(MonitorWindow,  self).__init__(parent)
        self.setWindowFlags (Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setStyleSheet ('''background-color:cyan;''')


        self.connectSignalSlot()

        shortcut = QShortcut(QKeySequence("Ctrl+S"), self, None, self.hotkeypress)
        
    def showMaxsized (self):
        desktop = QtGui.QApplication.desktop()
        rect = desktop.availableGeometry()
        self.setGeometry(rect)
        self.show()
    
    
    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
             #here accept the event and do something

            print event.key()
            if event.key() == Qt.Key_Escape:

                self.close()

            elif event.key() == Qt.Key_R:
                if(event.modifiers() & Qt.AltModifier):
                    print "Get Alt+F1 Restore explore\n"
                    reg.restoreShell()
            elif event.key() == Qt.Key_S:
                if(event.modifiers() & Qt.AltModifier):
                    print "Get Alt+F2 Setup the shell appons\n"
                    reg.setupShell()
                #self.slot_running_signal ( False)

            #event.accept()
        else:
            event.ignore()
    def hotkeypress(self):
        print "get hot key"


    def connectSignalSlot(self):

        self.signalRunning.connect(self.slot_running_signal, Qt.QueuedConnection)
        self.signalDetectorConnected.connect(self.slot_detector_connected, Qt.QueuedConnection)
        self.signalTraceInfo.connect (self.slot_trace_info, Qt.QueuedConnection)
        #testThread.signalRunning.connect(self.slot_running_signal,Qt.QueuedConnection)

    #@PyQt4.QtCore.pyqtSlot(int)
    def slot_xray_battery_level(self, level):
        self.rootObject().set_xray_battery_level (level)
    def set_xray_battery_level(self,  level):
        self.signalXrayBatteryLevel.emit(level)

    #@PyQt4.QtCore.pyqtSlot(int)
    def slot_scanner_battery_level(self, level):
        self.rootObject().set_scanner_battery_level (level)
    def set_scanner_battery_level(self,  level):
        self.signalScannerBatteryLevel.emit(level)
        

    #@PyQt4.QtCore.pyqtSlot(bool)
    def slot_running_signal (self, running):
        print "get signal running \n" +str(running)
        self.rootObject().set_detector_running(running)
    def set_detector_running (self,  running):
        print "get detetector running " +str(running)
        self.signalRunning.emit(running)

    #@PyQt4.QtCore.pyqtSlot(bool)
    def slot_detector_connected (self, connected):
        print "Slot detector connected is "+str(connected)
        self.rootObject().set_detector_connected(connected)
    def set_detector_connected(self,  connected):
        print "Set detector connected is "+str(connected)
        self.signalDetectorConnected.emit(connected)
    
    #@PyQt4.QtCore.pyqtSlot(bool)
    def slot_xray_connected(self, connected):
        self.rootObject().set_xray_connected (connected)
    def set_xray_connected(self,  connected):
        self.signalXrayConnected.emit(connected);
    
    #PyQt4.QtCore.pyqtSlot(bool)
    def slot_speaker_status(self, on):
        self.rootObject().set_speaker_status(on)
    def set_speaker_status (self, on):
        self.signalSpeakerStatus.emit(on)

    #PyQt4.QtCore.pyqtSlot(bool)
    def slot_stop_status(self, stopped):
        self.rootObject().set_stop_status (stopped)
    def set_stop_status (self, stopped):
        self.signalStopStatus.emit(stopped)

    #PyQt4.QtCore.pyqtSlot(string)
    def slot_trace_info(self, msg):
        self.rootObject().set_trace_info (msg)
    def set_trace_info(self, msg) :
        self.signalTraceInfo.emit(msg)
    
if __name__ == "__main__":
    detector_ip = "192.168.2.2"
    cmd_port = 3000;
    img_port = 4001;
    print "ui start"
    app = QApplication([])
    view = MonitorWindow()

    try:
        view.setSource(QUrl("MonitorWindow.qml"))
        view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        view.show()

        serialProxy = serial_proxy.start_proxy(view)
        cmdProxy = cmd_proxy.start_proxy(detector_ip, cmd_port, cmd_port,view)
        imgProxy = img_proxy.start_proxy(detector_ip, img_port, img_port,view)

        view.showFullScreen()
        app.exec_()
    except:
        print "star proxy failed"


    serialProxy.stop()
    cmdProxy.stop()
    imgProxy.stop()

