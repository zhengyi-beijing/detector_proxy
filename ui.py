from PyQt4.QtDeclarative import QDeclarativeView

from PyQt4 import QtGui,  QtCore
import sys
import detector_proxy,  serial_proxy
#class DetectorWindow (QtGui.QMainWindow):
class DetectorWindow (QDeclarativeView):
    def __init__ (self,  parent = None):
        super(DetectorWindow,  self).__init__(parent)
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
            
if __name__ == "__main__":
    detector_proxy.start_proxy()
    serial_proxy.start_proxy()
    print "ui start"
    app = QtGui.QApplication([])

    view = DetectorWindow()


    view.setSource(QtCore.QUrl("demo.qml"))
    view.setResizeMode(QDeclarativeView.SizeRootObjectToView) 

    view.show()
    
    
    #view.showMaximized()
    #rootObj = view.rootObject()
    #rootObj.setProperty("height",  view.height)
    #rootObj.setProperty("width",  view.width)
    #view.showFullScreen()
    app.exec_()
