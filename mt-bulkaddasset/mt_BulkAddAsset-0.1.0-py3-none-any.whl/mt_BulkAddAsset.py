from PyQt5 import QtWidgets, QtCore, QtGui, uic

import winreg
import sys

import mt_FileMan
import mt_UI
import mt_ODBC

#==============================================================
#==============================================================
#==============================================================
class MainUI(QtWidgets.QFrame):

    closed = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent) # Call init for inherited class

        uiPath = mt_FileMan.resource_path('UI/MaxTrack_Main.ui')
        uic.loadUi(uiPath, self) # Load .ui
        self.stayAlive = False
        
        self.tabs = self.findChild(QtWidgets.QTabWidget, 'tabWidget')

        #self.ini_tab = self.tabs.findChild(QtWidgets.QWidget, 'set_ini_tab')
        #self.ini_tab_main_layout = QtWidgets.QVBoxLayout(self)
        #self.ini_tab.setLayout(self.ini_tab_main_layout)

        #ini_UI = mt_SetFile.MainUI()
        #self.ini_tab_main_layout.addWidget(ini_UI)
        #self.ini_tab_label01 = QtWidgets.QLabel('HeyWo!')
        #self.ini_tab_main_layout.addWidget(self.ini_tab_label01)

        
        
        print(self.findChildren(QtWidgets.QLineEdit))
        
        # Make pointers we need to manipulate widgets
        # Line Edit Widgets
        self.customerLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'custNum_lineEdit')
        self.mfgLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'mfg_lineEdit')
        self.snPrefixLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'snPre_lineEdit')
        self.snStartLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'snStart_lineEdit')
        self.snEndLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'snEnd_lineEdit')
        self.controlNumLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'controlNumStart_lineEdit')
        self.idPrefixLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'idPre_lineEdit')
        self.idStartLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'idStart_lineEdit')
        self.idEndLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'idEnd_lineEdit')
        self.altNameLineEdit = self.tabs.findChild(QtWidgets.QLineEdit, 'nameToAppear_lineEdit')
        # Push Button Widgets
        self.beginPushButt = self.tabs.findChild(QtWidgets.QPushButton, 'start_pushButton')
        self.beginPushButt.clicked.connect(self.beginButtPressed)
        self.beginPushButt = self.tabs.findChild(QtWidgets.QPushButton, 'model_pushButton')
        self.beginPushButt.clicked.connect(self.modelButtPressed)
       # Combo Box Widgets
        #self.modelComboBox = self.tabs.findChild(QtWidgets.QComboBox, 'model_comboBox')
        self.dsnComboBox = self.tabs.findChild(QtWidgets.QComboBox, 'dsn_comboBox')
        self.searchComboBox = mt_UI.ExtendedCombo()
       #Layout Widgets that we need to manipulate later
        self.modelHLayout = self.findChild(QtWidgets.QHBoxLayout, 'horizontalLayout_3')
        #self.searchComboBox = ExtendedCombo()
        
        #Set the variables to read to ODBC sources with winreg 
        root = winreg.HKEY_LOCAL_MACHINE
        key = winreg.OpenKey(root, "SOFTWARE\WOW6432Node\ODBC\ODBC.INI")
        #Create a list to hold the ODBC sources
        self.connList = []
        #Query the registry key set earlier, and add ODBC sources to list
        for i in range(0, winreg.QueryInfoKey(key)[0]):
            #Get the source name
            skey_name = winreg.EnumKey(key, i)
            #print(skey_name) #Verbose output
            #Add source name to list
            self.connList.append(skey_name)
            #If we needed sub-values (which we don't here)
            #skey = winreg.OpenKey(key, skey_name)
        key.Close()
                
        print(self.connList)
            
        for x in self.connList:
            self.dsnComboBox.addItem(x)
        
        self.show() # Show yourself
#==============================================================
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.closed.emit()
        #self.parent.setWindowOpacity(1.)
#==============================================================     
    def modelButtPressed(self):
        print('pressed the model button...')
        cur = self.mtConnect()
        if not cur:
            print('no connection')
            sys.exit()
        sql = "SELECT DISTINCT(i4203) FROM mt.inventory"
        
        try:
            result = mt_ODBC.execQuery(cur, sql, True)
        except pyodbc.Error as err:
            result = "%s Failed to Execute: \n %s" % (err)
        #print(result)
        resultList = []
        for x in result:
            resultList.append(str(x[0]))
            
        #result = sorted(resultList, key=lambda item: (int(item.partition(' ')[0])
        #                       if item[0].isdigit() else float('inf'), item))
        result = ioMan.sorted_nicely(resultList)
        #sprint(result)
        #for x in result:
        #    self.modelComboBox.addItem(x)
        cur.close()
        
        model = QtGui.QStandardItemModel()
        for i,word in enumerate(result):
            item = QtGui.QStandardItem(word)
            model.setItem(i, 0, item)
            
        self.searchComboBox.setModel(model)
        self.searchComboBox.setModelColumn(0)
        self.modelHLayout.addWidget(self.searchComboBox)
#==============================================================
    def beginButtPressed(self):
        print('pressed the start button...')
        #con = conDB('DSN=Playground;UID=mt;PWD=mt')

        tmpD = self.getFieldData()
        
        requiredValues = ['customer number', 'manufacturer',
            'Serial# start value', 'Serial# end value', 'model']

        if False in mt_UI.validateInput(requiredValues, tmpD):
            return
        
        [print(i+' : '+x) for i, x in self.infoDict.items()]

        self.con = self.mtConnect()
        if not self.con:
            print('no connection')
            return
        
        self.getModelInfo()
        
        sql = "SELECT ktag FROM customers WHERE K4601 = '"+tmpD['customer number']+"'"
        while True:
            try:
                result = mt_ODBC.execQuery(self.con, sql, True).fetchone()
            except:
                result = "Failed to Execute"
            if result:
                print('Result: {}'.format(result))#debug#
                self.infoDict['ktag'] = result[0]
                break
            else:
                err_msg = 'Failed to retrieve KTAG from customer number: {}\nRetry?'.format(
                    tmpD['customer number'])
                print(err_msg)
                reply = mt_UI.msgBox(message=err_msg)
                if reply == QTYES:
                    continue
                else:
                    return
        if len(self.infoDict['Control# start'])<1:
            self.infoDict['Control# start'] = self.infoDict['customer number']+\
                                        self.infoDict['Serial# start value']
        [print(i+' : '+x) for i, x in self.infoDict.items()]
        for i, x in self.infoDict.items():
            try:
                msgDetails = msgDetails+'\n'+i+' : '+x
            except:
                msgDetails = i+' : '+x
        numberOfAssets = int(tmpD['Serial# end value'])-int(tmpD['Serial# start value'])+1
        counter = 0
        confMsg = 'Are you sure you want to create '+str(numberOfAssets)+' assets?'
        reply = mt_UI.msgBox(message=confMsg, details=msgDetails)
        if reply == QtWidgets.QMessageBox.No:
            print('action cancelled by user\n')
            return
        while counter<numberOfAssets:
            #serialNum = int(tmpD['Serial# start value'])
            serialNum = int(tmpD['Serial# start value']) + counter
            serialNumber = tmpD['Serial# Prefix'] + str(serialNum)
            #controlNumber = tmpD['Control# start'] + str(counter)
            
            controlNumber = tmpD['customer number'] + str(serialNum)
            idNumber = ''
            sql = """INSERT INTO mt.Inventory (I4201, I4202, I4203, I4204, I4206,
                I4207, I4210, I4215, I4218, I4222, I4224, I4228, I4229, I4231, I4246,
                idsrc, ktag) VALUES('"""+controlNumber+"', '"+tmpD['manufacturer']+ \
                "', '"+tmpD['model']+"', '"+tmpD['description']+"', '"+ \
                serialNumber+"', '"+idNumber+"', '', '1', '"+tmpD['cert code']+ \
                "', '"+tmpD['cert cost']+"', '"+today+"', 'M', '12', '"+tmpD['Name to appear on cert']+ \
                "', '"+tmpD['department']+"', 'MAX', '"+tmpD['ktag']+"')"
            print(sql)
            try:
                mt_ODBC.execQuery(self.con, sql, True)
            except:
                result = "Failed to Execute"
            counter = counter + 1
        
        self.con.close()
        return
#==============================================================
    def getModelInfo(self):
        sql = '''
        SELECT 
        data1 as descr,
        data2 as dept,
        data6 as code,
        data9 as cost
        FROM VALLINKDATA 
        WHERE ROOTDATA = \'{}\''''.format(self.infoDict['model'])
        try:
            result = mt_ODBC.execQuery(self.con, sql, True)
        except:
            result = "Failed to Execute"
        resultList = []
        for x in result:
            resultList.append(x)
        print(resultList)
        result = list(resultList[0])
        print(result)
        self.infoDict['description'] = result.pop(0)
        self.infoDict['department'] = result.pop(0)
        self.infoDict['cert code'] = result.pop(0)
        self.infoDict['cert cost'] = result.pop(0)

        return 0
#==============================================================        
    def getFieldData(self):
        custNum = self.customerLineEdit.text()
        mfgName = self.mfgLineEdit.text()
        snPrefix = self.snPrefixLineEdit.text()
        snStart = self.snStartLineEdit.text()
        snEnd = self.snEndLineEdit.text()
        idPrefix = self.idPrefixLineEdit.text()
        idStart = self.idStartLineEdit.text()
        idEnd = self.idEndLineEdit.text()
        controlNumStart = self.controlNumLineEdit.text()
        altName = self.altNameLineEdit.text()
        #this wasn't working right. my function needs work (ExtendedCombo.currentData)
        #modelNumber = self.searchComboBox.currentData()
        modelNumber = self.searchComboBox.currentText()
        
        self.infoDict = {'customer number': custNum, 'manufacturer': mfgName,
            'Serial# start value': snStart, 'Serial# end value': snEnd,
            'Serial# Prefix': snPrefix, 'ID# prefix': idPrefix,
            'ID# start': idStart, 'ID# end': idEnd,
            'Control# start': controlNumStart,
            'Name to appear on cert': altName, 'model': modelNumber}

        return self.infoDict
#==============================================================        
    def mtConnect(self):
        dsn = self.dsnComboBox.currentText()
        try:
            con = mt_ODBC.conDB('DSN='+dsn+';UID=mt;PWD=mt')
        except:
            print('could not connect to '+dsn)
            return None
        return con
#==============================================================
#==============================================================
#==============================================================
def main():
    from datetime import datetime
    import os

    theCurrentDatetime = datetime.now()
#    today = theCurrentDatetime.strftime('%m/%d/%y')
    today = theCurrentDatetime.strftime('%Y-%m-%d')
    print('Today is: {}'.format(today))
    
    logFile = ioMan.startLog(ioMan)
    
    QtCore.pyqtRemoveInputHook()
    app = QtWidgets.QApplication(sys.argv) # Create QApplication instance
    #window = MainUI() # Create MainUI instance
    window = MainUI()
    sys.exit(app.exec_()) # Start the app
if __name__ == '__main__':
    ioMan = mt_FileMan.mtIOMan
    main()
