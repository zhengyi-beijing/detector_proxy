from PyQt4.QtDeclarative import QDeclarativeView

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, traceback
import NoBlockingProxy as detector_server
import SerialProxy
from proxy_monitor import ProxyMonitor 
import threading
import reg
        
class MonitorWindow (QDeclarativeView,  ProxyMonitor):
    signalRunning = pyqtSignal(bool)
    signalXrayBatteryLevel = pyqtSignal(int)
    signalXrayConnection = pyqtSignal(bool)
    signalDetectorBatteryLevel = pyqtSignal(int)
    signalDetectorConnected = pyqtSignal(bool)
    signalSpeakerStatus = pyqtSignal(bool)
    signalStopStatus = pyqtSignal(bool)
    signalTraceInfo = pyqtSignal(str)
    singalDetectorSpeed = pyqtSignal(str)

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
        self.signalTraceInfo.connect (self.slot_trace_info, Qt.QueuedConnection)
        self.singalDetectorSpeed.connect(self.slot_detector_speed, Qt.QueuedConnection)
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
    
    #PyQt4.QtCore.pyqtSlot(string)
    def slot_detector_speed(self, speed):
        print "qml call speed is " + speed
        self.rootObject().set_detector_speed(speed)
    def set_detector_speed(self, speed):
        print "speed is " + speed
        self.singalDetectorSpeed.emit(speed)

if __name__ == "__main__":
    detector_ip = "192.168.2.2"
    #detector_ip = "127.0.0.1"
    cmd_port = 3000;
    img_port = 4001;
    print "ui start"
    app = QApplication([])
    view = MonitorWindow()

    try:
        view.setSource(QUrl("MonitorWindow.qml"))
        view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        view.show()
       # view.showFullScreen()
        serialProxy = SerialProxy.start_proxy(view)
        server = detector_server.DetectorServer("detector", "192.168.1.25", 3000,4001,3000,4001, view)
        server.start()
        app.exec_()
    except Exception, e:
        print "star proxy failed"
        print e
        traceback.print_exc()
    #app.exec_()
    #if serialProxy:
    #    serialProxy.stop()
    if server:
        server.stop()

