from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtNetwork
from PyQt5.QtWebKitWidgets import QWebView , QWebPage


class PDFViewer(QtWebKit.QWebView):
    pdf_viewer_page = 'res/pdf-viewer.html'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QtWebKit.QWebSettings.globalSettings()
        self.settings.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessFileUrls, True )
        self.settings.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True )
        self.settings.setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True )
        nam = QtNetwork.QNetworkAccessManager()
        page = QtWebKit.QWebPage(self)
        page.setNetworkAccessManager(nam)
        self.setPage(page)
        self.loadFinished.connect(self.onLoadFinish)
        self.setUrl(QtCore.QUrl(self.pdf_viewer_page))

    def onLoadFinish(self, success):
        if success:
            self.page().mainFrame().evaluateJavaScript("init();")


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    viewer = PDFViewer(parent=None)
    viewer.show()
    sys.exit(app.exec_())