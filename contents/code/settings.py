from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kio import *
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from settingsform import Ui_gcal_settings

class Settings(QWidget, Ui_gcal_settings):
    def __init__(self, parent):
        QWidget.__init__(self)

        self.parent = parent

        self.setupUi(self)
        self.wallet = KWallet.Wallet.openWallet(KWallet.Wallet.LocalWallet(), 0)#, 1)

        if self.wallet <> None:
            self.wallet.setFolder("gcal-plasmoid")

            if  not self.wallet.entryList().isEmpty():
                username = str(self.wallet.entryList().first())
                password = QString()
                self.wallet.readPassword(username, password)
                self.le_email.setText(username)
                self.le_password.setText(str(password))
        else:
            print(":(")

    def getSettings(self):
        return {'username': str(self.le_email.text()),
                'password': str(self.le_password.text())}
