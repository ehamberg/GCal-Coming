from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kio import *
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from settingsform import Ui_gcal_settings

class Settings(QWidget, Ui_gcal_settings):
    def __init__(self, parent, settings):
        QWidget.__init__(self)

        self.wallet = KWallet.Wallet.openWallet(KWallet.Wallet.LocalWallet(), 0)#, 1)
        if self.wallet <> None:
            self.connect(self.wallet, SIGNAL("walletOpened(bool)"), self.walletOpened)
        else:
            print(":(")
            # KWallet service is disabled
            #self.checkMail()
            #self.timer.start(self.settings["pollinterval"] * 60000)

        self.setupUi(self)

    def walletOpened(self, success):
        if success:
            print "Wallet opened"
            # Get passwords from wallet
            self.wallet.setFolder("gcal-plasmoid")

            passwd = QString()
            self.wallet.readPassword(self.settings["username"], passwd)
            print(str(passwd))
            self.settings["password"] = str(passwd)
