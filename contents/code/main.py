import urllib
import re

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from PyKDE4.kio import *

from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
#from PyKDE4.kdecore import KUrl

from settings import Settings

class GCalApplet(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)
        self.parent = parent

    def init(self):
        self.settings = {}
        self.setHasConfigurationInterface(False)
        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)

        self.wallet = KWallet.Wallet.openWallet(KWallet.Wallet.LocalWallet(), 0)
        self.timer = QTimer(self)

        if self.wallet <> None:
            if not self.wallet.hasFolder("gcal-plasmoid"):
                self.wallet.createFolder("gcal-plasmoid")

            self.wallet.setFolder("gcal-plasmoid")
            if self.wallet.entryList().isEmpty():
                src = """
                <div style="text-align: center">
                <img src="http://calendar.google.com/googlecalendar/images/calendar_sm2_en.gif" />
                <p>
                Click the wrench to configure the Google Calendar widget.
                </p>
                </div>
                """
                #self.showConfigurationInterface()
            else:
                username = str(self.wallet.entryList().first())

                password = QString()
                self.wallet.readPassword(username, password)

                self.storeUserAndDomain(username, str(password))
                src = self.getSrc()

        else:
            self.storeUserAndDomain("", "")
            src = self.getSrc()

        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
        self.webview = Plasma.WebView(self.applet)

        # google's ugly 1995 gifs destroys the beauty of transparency :(
        #palette = self.webview.palette()
        #palette.setBrush(QPalette.Base, Qt.transparent)
        #self.webview.page().setPalette(palette)
        #self.webview.setAttribute(Qt.WA_OpaquePaintEvent, False)

        self.webview.setHtml(src)
        self.layout.addItem(self.webview)
        self.setLayout(self.layout)
        self.resize(300,400)

    def createConfigurationInterface(self, parent):
        self.gcalsettings = Settings(self)
        p = parent.addPage(self.gcalsettings, i18n("Google Calendar Settings") )

        self.connect(parent, SIGNAL("okClicked()"), self.configAccepted)
        self.connect(parent, SIGNAL("cancelClicked()"), self.configDenied)

    def showConfigurationInterface(self):
        dialog = KPageDialog()
        dialog.setFaceType(KPageDialog.Plain)
        dialog.setButtons( KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel) )
        self.createConfigurationInterface(dialog)
        dialog.resize(400,300)
        dialog.exec_()

    def configDenied(self):
        pass

    def configAccepted(self):
        self.settings = self.gcalsettings.getSettings()
        self.storeUserAndDomain(self.settings['username'], self.settings['password'])
        wallet = KWallet.Wallet.openWallet(KWallet.Wallet.LocalWallet(), 0)
        if wallet <> None:
            wallet.setFolder("gcal-plasmoid")
            for e in wallet.entryList():
                wallet.removeEntry(e)
            wallet.writePassword(QString(self.settings['username']),
                    QString(self.settings['password']))
            wallet = None

        self.webview.setHtml(self.getSrc())

    def storeUserAndDomain(self, username, password):
        re_email = re.compile('@(.+)')
        m = re_email.search(username)

        # if username is an email address with a domain name other than
        # gmail.com, assume it's a Google Apps for your Domain thingie and
        # change the url
        if m <> None and m.group(1) <> "gmail.com":
            self.url = "http://google.com/calendar/hosted/" + m.group(1) + "/m"
            username = re_email.sub('', username)
        else:
            self.url = "http://google.com/calendar/m"

        self.settings['username'] = username
        self.settings['password'] = password

    def getSrc(self):
        try:
            webFile = urllib.urlopen(self.url)
            src = webFile.read()
            webFile.close()

            if self.timer.isActive():
                self.timer.stop()
        except IOError, e:
            # NOTE: It appears that the Solid.Networking.notifier() function has
            # not be included in pyKDE4 as of now. This should be used when it
            # is included. For now, lets try every 5 seconds...
            if not self.timer.isActive():
                self.timer.setInterval(5000)
                self.connect(self.timer, SIGNAL("timeout()"),
                        self.connectionCheck)
                self.timer.start()

            src = """
            <div style="text-align: center; color: #ee2222;">
            <p>
            Network error: Could not connect to Google Calendar.
            </p>
            </div>
            """

        if self.settings['username']:
            src = src.replace("id=\"Email\"",
                    "id=\"Email\" value=\""+self.settings['username']+"\"")
            src = src.replace("id=\"Passwd\"",
                    "id=\"Passwd\" value=\""+self.settings['password']+"\"")
            src = src.replace("id=\"gaia_loginform\"",
                    "id=\"gaia_loginform\" name=\"gaia_loginform\"")
            src = src.replace("</body>",
                    "<script>document.gaia_loginform.submit()</script></body>")

        return src

    def connectionCheck(self):
        self.webview.setHtml(self.getSrc())
        pass


def CreateApplet(parent):
    return GCalApplet(parent)
