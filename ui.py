from PyQt4.QtDeclarative import QDeclarativeView

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import detector_proxy,  serial_proxy
from proxy_monitor import ProxyMonitor 


        
class MonitorWindow (QDeclarativeView,  ProxyMonitor):

    signalRunning = pyqtSignal(bool)
    def __init__ (self,  parent = None):
        super(MonitorWindow,  self).__init__(parent)
        self.setWindowFlags (Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setStyleSheet ('''background-color:cyan;''')


        self.connectSignalSlot()
        
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
                serial_proxy.stop()
                self.close()
            event.accept()
        else:
            event.ignore()



    def connectSignalSlot(self):
        self.signalRunning.connect(self.slot_running_signal, Qt.QueuedConnection)

    def set_xray_battery_level(self,  level):
        self.rootObject().set_xray_battery_level (level)
        
    def set_scanner_battery_level(self,  level):
        self.rootObject().set_scanner_battery_level (level)
        

    #@PyQt4.QtCore.pyqtSlot(bool)
    def slot_running_signal (self, running):
        print "get signal running " +running
        self.rootObject().set_detector_running(running)

    def set_detector_running (self,  running):
        print "get detetector running " +running
        signalRunning.emit(running)

            
    def  set_detector_connected(self,  connected):
        self.rootObject().set_detector_connected(connected)
    
    def set_xray_connected(self,  connected):
        self.rootObject().set_xray_connected (connected)
    
    def set_speaker_status (self, on):
        self.rootObject().set_speaker_status (on)

    def set_stop_status (self, stopped):
        self.rootObject().set_stop_status (stopped)

    def set_trace_info(msg) :
        self.rootObejct().set_trace_info (msg)
    
if __name__ == "__main__":

    print "ui start"
    app = QApplication([])

    view = MonitorWindow()
    #detector_proxy.start_proxy(view)
    serial_proxy.start_proxy(view)

    view.setSource(QUrl("MonitorWindow.qml"))
    view.setResizeMode(QDeclarativeView.SizeRootObjectToView) 

    view.show()
    
    
    
    #view.showMaximized()
    #rootObj = view.rootObject()
    #rootObj.setProperty("height",  view.height)
    #rootObj.setProperty("width",  view.width)
    #view.showFullScreen()
    app.exec_()
