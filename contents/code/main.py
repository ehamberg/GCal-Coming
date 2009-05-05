from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.kdecore import KUrl

class HelloWorldApplet(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

    def init(self):
        self.setHasConfigurationInterface(False)

        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)

        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
        webView = Plasma.WebView(self.applet)
        webView.setUrl(KUrl("http://google.com/calendar/m"))
        self.layout.addItem(webView)
        self.setLayout(self.layout)
        self.resize(300,400)

def CreateApplet(parent):
    return HelloWorldApplet(parent)
