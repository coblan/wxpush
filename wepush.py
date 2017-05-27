# encoding:utf-8
from __future__ import unicode_literals
import os
import sys
os.environ["path"] += os.path.join(os.getcwd(), "dll")
sys.path.append(os.path.join(os.getcwd(), "dll"))

from PyQt4.QtGui import QApplication,QWidget,QIcon
from PyQt4.QtCore import QUrl,QObject,pyqtSlot, pyqtProperty
from PyQt4.QtWebKit import QWebView
import thread
import server
os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.getcwd(), "cacert.pem")


if __name__ =='__main__':
    app = QApplication(sys.argv)
    thread.start_new_thread (server.start_server,(28289,))
    win =QWebView()
    win.setWindowIcon(QIcon( './html/wechat.ico'))
    win.setMinimumSize(1200,900)
    win.setWindowTitle('微信群发工具V1.0')
    win.load( QUrl('http://127.0.0.1:28289/html/main.html'))
    win.show()
    sys.exit(app.exec_())    