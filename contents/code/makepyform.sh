python /usr/share/kde4/apps/pykde4/pykdeuic4.py -o settingsform.py settings.ui
sed -i 's/fonTextFont = KComboBox/fonTextFont = kdeui.KFontComboBox/' settingsform.py
pyrcc4 -o settings_rc.py settings.qrc
