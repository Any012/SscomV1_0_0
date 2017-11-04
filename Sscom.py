import sys
import binascii
import re

from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QAction, QMessageBox, QMainWindow, QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.Qt import Qt
from SscomUI import MySscomUI

class MySscom(MySscomUI):
    def __init__(self):
        super().__init__()
        self.com = QSerialPort()
        
        self.Layout()
        self.CreateSignalSolt()
        self.RefreshCom()

        self.encoding = 'utf-8'
        self.recvCount = 0
        self.sendCount = 0
   
    def Layout(self):
        self.chcHexRecv.setChecked(True)
        self.chcWrap.setChecked(True)
        self.btnClosePort.setEnabled(False)
        self.gboxRecvSet.setEnabled(False)
        self.gboxSendSet.setEnabled(False)
        self.chcHexSend.setChecked(True)
        self.txtAutoSend.setText('1')

    def CreateSignalSolt(self):
        self.btnOpenPort.clicked.connect(self.OpenSerial)
        self.btnClosePort.clicked.connect(self.CloseSerial)
        self.btnSend.clicked.connect(self.SendData)
        self.com.readyRead.connect(self.RecvData)
        self.btnClear.clicked.connect(self.ClearRecv)
        self.chcAutoSend.clicked.connect(self.AutoSend)
        self.tmrSend.timeout.connect(self.SendData)

    def RefreshCom(self):
        self.cmbPort.clear()
        for info in QSerialPortInfo.availablePorts():
            self.cmbPort.addItem(info.portName())
            # self.cmbPort.addItem(info.portName()+info.description())
            # print(info.description())
            # print(info.manufacturer())
            # print(info.serialNumber())
        for info in QSerialPortInfo.standardBaudRates():
            self.cmbBaud.addItem(str(info))

        if (self.cmbBaud.findText('9600') != -1):
            self.cmbBaud.setCurrentIndex(self.cmbBaud.findText('9600'))
        elif(self.cmbBaud.findText('19200') != -1):
            self.cmbBaud.setCurrentIndex(self.cmbBaud.findText('19200'))
        else:
            self.cmbBaud.setCurrentIndex(0)

        self.cmbParity.addItems(['None', 'Even', 'Odd', 'Mark', 'Space'])
        self.cmbWordLen.addItems(['5', '6', '7', '8'])
        self.cmbStopBits.addItems(['1', '1.5', '2'])
        

    def OpenSerial(self):
        comName = self.cmbPort.currentText()
        comBaud = int(self.cmbBaud.currentText())
        self.com.setPortName(comName)

        try:
            if self.com.open(QSerialPort.ReadWrite) == False:
                QMessageBox.critecla(self, '打开失败', '该串口不存在或已被占用')
                return
        except:
            QMessageBox.critical(self, '打开失败', '该串口不存在或已被占用')
            return

        self.com.setBaudRate(comBaud)

        self.btnOpenPort.setEnabled(False)
        self.btnOpenPort.setFocus(False)
        self.btnClosePort.setEnabled(True)
        self.gboxRecvSet.setEnabled(True)
        self.gboxSendSet.setEnabled(True)
        self.cmbPort.setEnabled(False)
        self.cmbBaud.setEnabled(False)
        self.cmbParity.setEnabled(False)
        self.cmbWordLen.setEnabled(False)
        self.cmbStopBits.setEnabled(False)

    def CloseSerial(self):
        if(self.com.isOpen()):
            self.com.close()
        self.btnClosePort.setEnabled(False)
        self.btnOpenPort.setEnabled(True)
        self.gboxRecvSet.setEnabled(False)
        self.gboxSendSet.setEnabled(False)
        self.cmbPort.setEnabled(True)
        self.cmbBaud.setEnabled(True)
        self.cmbParity.setEnabled(True)
        self.cmbWordLen.setEnabled(True)
        self.cmbStopBits.setEnabled(True)

    def RecvData(self):
        try:
            recvData = bytes(self.com.readAll())
        except:
            QMessageBox.critical(self, '错误', '串口接收错误')
        
        if len(recvData) > 0:
            self.recvCount += len(recvData)
            if self.chcHexRecv.isChecked() == False:
                recvData = recvData.decode(self.encoding, 'ignore')
                self.txtRecv.insertPlainText(recvData)
            else:
                # data = ' '.join('%02X' % i for i in recvData) + ' '
                # self.txtRecv.insertPlainText(data.upper())
                data = binascii.b2a_hex(recvData).decode('ascii')
                pattern = re.compile('.{2,2}')
                hexStr = ' '.join(pattern.findall(data)) + ' '
                self.txtRecv.insertPlainText(hexStr.upper())
            if self.chcWrap.isChecked() == True:
                self.txtRecv.insertPlainText('\r\n')
            
            self.vscrlRecv.setValue(self.vscrlRecv.maximum())

    def SendData(self):
        sendData = self.txtSend.toPlainText()
        if len(sendData) == 0:
            return
        if self.chcHexSend.isChecked():
            s = sendData.replace(' ', '')
            if len(s) % 2 == 1:
                QMessageBox.critical(self, '错误', '十六进制数不是偶数个')
                return
            if not s.isalnum():
                QMessageBox.critical(self, '错误', '包含非十六进制数')
                return
            try:
                hexData = binascii.a2b_hex(s)
            except:
                QMessageBox.critical(self, '错误', '转换编码错误')
                return
            try:
                n = self.com.write(hexData)
            except:
                QMessageBox.critical(self, '异常', '十六进制发送错误')
        else:
            n = self.com.write(sendData.encode(self.encoding, 'ignore'))
        self.sendCount += n

    def ClearRecv(self):
        self.txtRecv.clear()
        self.recvCount = 0
        self.sendCount = 0

    def AutoSend(self):
        if self.com.isOpen():
            if self.chcAutoSend.isChecked():
                # if self.txtAutoSend.text()
                self.tmrSend.start(int(self.txtAutoSend.text()) * 1000)
            else:
                self.tmrSend.stop()
        

class MySscomFrame(QMainWindow):
    def __init__(self):
        super().__init__()

        mySscom = MySscom()
        self.setCentralWidget(mySscom)

        statusBar = self.statusBar()
        lblStatus1 = QLabel('status1')
        lblStatus1.setAlignment(Qt.AlignCenter)
        lblStatus2 = QLabel('接收 ' + str(mySscom.recvCount) + ' 字节')
        lblStatus2.setAlignment(Qt.AlignCenter)
        lblStatus3 = QLabel('发送 ' + str(mySscom.sendCount) + ' 字节')
        lblStatus3.setAlignment(Qt.AlignCenter)
        lblStatus4 = QLabel('status4')
        lblStatus4.setAlignment(Qt.AlignCenter)
        statusBar.addWidget(lblStatus1, 1)
        statusBar.addWidget(lblStatus2, 1)
        statusBar.addWidget(lblStatus3, 1)
        statusBar.addWidget(lblStatus4, 1)
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('文件(&F)')
        helpMenu = menuBar.addMenu('帮助(&H)')

        self.exitAct = QAction('退出', self)
        self.exitAct.triggered.connect(self.close)
        fileMenu.addAction(self.exitAct)
        self.aboutAct = QAction('关于', self)
        self.aboutAct.triggered.connect(self.about)
        helpMenu.addAction(self.aboutAct)

        # mySscom.recvCount.changed.connect(self.StatusRecv)
        # mySscom.recvCount

        self.setGeometry(300, 300, 800, 550)
        self.setWindowTitle('串口调试助手')
        self.show()

    def StatusRecv(self):
        pass
        
    def about(self):
        QMessageBox.about(self, 'About Serialport Assistor', '串口调试助手'  
            '\r\nVersion:')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MySscomFrame()
    sys.exit(app.exec_())