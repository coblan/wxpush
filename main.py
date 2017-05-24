import sys
import os
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl,QObject,pyqtSlot, pyqtProperty
from PyQt4.QtWebKit import QWebView

if __name__ =='__main__':
    app = QApplication(sys.argv)
    win =QWebView()
    win.load( QUrl('http://127.0.0.1:28289/html/main.html'))
    win.show()
    sys.exit(app.exec_())    