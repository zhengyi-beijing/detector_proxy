from PyQt4.QtDeclarative import QDeclarativeView

from PyQt4 import QtGui,  QtCore
import sys
import detector_proxy,  serial_proxy
from proxy_monitor import ProxyMonitor 


        
class MonitorWindow (QDeclarativeView,  ProxyMonitor):
    def __init__ (self,  parent = None):
        super(MonitorWindow,  self).__init__(parent)
        self.setWindowFlags (QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)
        self.setStyleSheet ('''background-color:cyan;''')
        
    def showMaxsized (self):
        desktop = QtGui.QApplication.desktop()
        rect = desktop.availableGeometry()
        self.setGeometry(rect)
        self.show()
    
    
    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
             #here accept the event and do something
            print event.key()
            if event.key() == QtCore.Qt.Key_Escape:
                self.close()
            event.accept()
        else:
            event.ignore()
            
    def set_xray_battery_level(self,  level):
        self.rootObject.set_xray_battery_level (level)
        
    def set_scanner_battery_level(self,  level):
        self.rootObject.set_scanner_battery_level (level)
        
    def set_detector_running (self,  running):
        self.rootObject.set_detector_running(running)
            
    def  set_detector_connected(self,  connected):
        self.rootObject.set_detector_connected(connected)
    
    def set_client_connected(self,  connected): 
        self.rootObject.set_client_connected (connected)
    
    def set_trace_info(msg) :
        print "msg: "+ msg
    
if __name__ == "__main__":

    print "ui start"
    app = QtGui.QApplication([])

    view = MonitorWindow()
    #detector_proxy.start_proxy(view)
    serial_proxy.start_proxy()

    view.setSource(QtCore.QUrl("MonitorWindow.qml"))
    view.setResizeMode(QDeclarativeView.SizeRootObjectToView) 

    view.show()
    
    
    
    #view.showMaximized()
    #rootObj = view.rootObject()
    #rootObj.setProperty("height",  view.height)
    #rootObj.setProperty("width",  view.width)
    #view.showFullScreen()
    app.exec_()
