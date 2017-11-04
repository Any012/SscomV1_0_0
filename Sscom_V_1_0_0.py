import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QComboBox, QCheckBox, 
                             QLineEdit, QPlainTextEdit, QGroupBox, 
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QMainWindow, QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

class MySscomUI(QWidget):
# class MySscom(QWidget):
    def __init__(self):
        super().__init__()
        self.CreateItems()
        self.CreateLayout()
        self.CreateSignalSolt()
        self.refreshCom()
        self.setGeometry(300, 300, 800, 550)
        self.setWindowTitle('串口调试助手')
        self.show()

    def CreateItems(self):
        self.com = QSerialPort()

        self.lblPort = QLabel('串  口')
        self.lblBaud = QLabel('波特率')
        self.lblParity = QLabel('校验位')
        self.lblWordLen = QLabel('数据位')
        self.lblStopBits = QLabel('停止位')

        self.cmbPort = QComboBox()
        self.cmbBaud = QComboBox()
        self.cmbParity = QComboBox()
        self.cmbWordLen = QComboBox()
        self.cmbStopBits = QComboBox()

        self.btnOpenPort = QPushButton('打开串口')
        self.btnClosePort = QPushButton('关闭串口')
        # self.btnOpenPort.setFont(QFont('Arial', 15))
        self.btnOpenPort.setFixedHeight(35)
        self.btnClosePort.setFixedHeight(35)
        font = QFont()
        font.setPixelSize(15)
        self.btnOpenPort.setFont(font)
        self.btnClosePort.setFont(font)
        self.btnClosePort.setEnabled(False)

        self.chcHexRecv = QCheckBox('十六进制接收')
        self.chcWrap = QCheckBox('自动换行')
        self.chcAutoClear = QCheckBox('自动清空')
        self.chcAutoSave = QCheckBox('自动保存')

        self.btnClear = QPushButton('清空')

        self.lblAddr = QLabel('地址')
        self.txtAddr = QLineEdit()
        self.btnSaveAs = QPushButton('选择...')

        self.chcHexSend = QCheckBox('十六进制发送')
        self.chcAutoSend = QCheckBox('自动发送')
        self.txtAutoSend = QLineEdit()
        self.lblAutoSend = QLabel('秒')

        self.txtRecv = QPlainTextEdit()
        
        self.txtSend = QPlainTextEdit()
        self.btnSend = QPushButton('发送')
        self.txtSend.setFixedHeight(100)
        self.btnSend.setFixedHeight(35)
    
    def CreateLayout(self):
        hboxMain = QHBoxLayout()
        vboxMainSet = QVBoxLayout()
        vboxDisp = QVBoxLayout()

        gboxPortSet = QGroupBox('串口设置')
        gboxRecvSet = QGroupBox('接收设置')
        gboxSendSet = QGroupBox('发送设置')

        vboxPortSet = QVBoxLayout()
        vboxRecvSet = QVBoxLayout()
        vboxSendSet = QVBoxLayout()
        
        gridPortSet = QGridLayout()
        hboxOpenClosePort = QHBoxLayout()
        gridRecvSet = QGridLayout()
        hboxAddrSet = QHBoxLayout()
        hboxAutoSend = QHBoxLayout()

        hboxSend = QHBoxLayout()

        hboxMain.addLayout(vboxMainSet)
        hboxMain.addLayout(vboxDisp)
        hboxMain.setStretchFactor(vboxMainSet, 0)
        hboxMain.setStretchFactor(vboxDisp, 1)

        vboxMainSet.addWidget(gboxPortSet)
        vboxMainSet.addWidget(gboxRecvSet)
        vboxMainSet.addWidget(gboxSendSet)
        vboxMainSet.addStretch()

        gboxPortSet.setLayout(vboxPortSet)
        gboxRecvSet.setLayout(vboxRecvSet)
        gboxSendSet.setLayout(vboxSendSet)

        vboxPortSet.addLayout(gridPortSet)
        vboxPortSet.addLayout(hboxOpenClosePort)

        vboxRecvSet.addLayout(gridRecvSet)
        vboxRecvSet.addLayout(hboxAddrSet)

        gridPortSet.addWidget(self.lblPort, 0, 0)
        gridPortSet.addWidget(self.cmbPort, 0, 1)
        gridPortSet.addWidget(self.lblBaud, 1, 0)
        gridPortSet.addWidget(self.cmbBaud, 1, 1)
        gridPortSet.addWidget(self.lblParity, 2, 0)
        gridPortSet.addWidget(self.cmbParity, 2, 1)
        gridPortSet.addWidget(self.lblWordLen, 3, 0)
        gridPortSet.addWidget(self.cmbWordLen, 3, 1)
        gridPortSet.addWidget(self.lblStopBits, 4, 0)
        gridPortSet.addWidget(self.cmbStopBits, 4, 1)

        gridPortSet.setColumnStretch(0, 1)
        gridPortSet.setColumnStretch(1, 3)

        hboxOpenClosePort.addWidget(self.btnOpenPort)
        hboxOpenClosePort.addWidget(self.btnClosePort)

        gridRecvSet.addWidget(self.chcHexRecv, 0, 0)
        gridRecvSet.addWidget(self.chcWrap, 0, 1)
        gridRecvSet.addWidget(self.chcAutoClear)
        gridRecvSet.addWidget(self.btnClear)
        gridRecvSet.addWidget(self.chcAutoSave )

        hboxAddrSet.addWidget(self.lblAddr)
        hboxAddrSet.addWidget(self.txtAddr)
        hboxAddrSet.addWidget(self.btnSaveAs)

        vboxSendSet.addWidget(self.chcHexSend)
        vboxSendSet.addLayout(hboxAutoSend)

        hboxAutoSend.addWidget(self.chcAutoSend)
        hboxAutoSend.addWidget(self.txtAutoSend)
        hboxAutoSend.addWidget(self.lblAutoSend)

        vboxDisp.addWidget(self.txtRecv)
        vboxDisp.addLayout(hboxSend)
        vboxDisp.setStretchFactor(self.txtRecv, 1)
        vboxDisp.setStretchFactor(hboxSend, 0)

        hboxSend.addWidget(self.txtSend)
        hboxSend.addWidget(self.btnSend)

        self.setLayout(hboxMain)

    def CreateSignalSolt(self):
        self.btnOpenPort.clicked.connect(self.openSerial)
        self.btnClosePort.clicked.connect(self.closeSerial)

    def refreshCom(self):
        self.cmbPort.clear()
        for info in QSerialPortInfo.availablePorts():
            # self.com.setPort(info)
            self.cmbPort.addItem(info.portName())
        for info in QSerialPortInfo.standardBaudRates():
            self.cmbBaud.addItem(str(info))

        if (self.cmbBaud.findText('9600') != -1):
            self.cmbBaud.setCurrentIndex(self.cmbBaud.findText('9600'))
        elif(slef.cmbBaud.findText('19200') != -1):
            self.cmbBaud.setCurrentIndex(self.cmbBaud.findText('19200'))
        else:
            slef.cmbBaud.setCurrentIndex(0)

    def openSerial(self):
        comName = self.cmbPort.currentText()
        comBaud = int(self.cmbBaud.currentText())
        self.com.setPortName(comName)

        try:
            if self.com.open(QSerialPort.ReadWrite) == False:
                QMessageBox.critecla(self, '串口打开失败')
                return
        except:
            QMessageBox.critical(self, '串口打开失败')

        self.com.setBaudRate(comBaud)

        self.btnOpenPort.setEnabled(False)
        self.btnClosePort.setEnabled(True)

    def closeSerial(self):
        self.com.close()
        self.btnClosePort.setEnabled(False)
        self.btnOpenPort.setEnabled(True)
class MySscomMain(QMainWindow):
    def __init__(self):
        super().__init__()

        statusBar = self.statusBar().showMessage('Ready')
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('文件(&F)')
        helpMenu = menuBar.addMenu('帮助(&H)')

        mySscomUI = MySscomUI()
        self.setCentralWidget(mySscomUI)
        
        self.setGeometry(300, 300, 800, 550)
        self.setWindowTitle('串口调试助手')
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MySscomMain()
    sys.exit(app.exec_())