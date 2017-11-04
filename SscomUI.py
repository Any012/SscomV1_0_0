import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QComboBox, QCheckBox, 
                             QLineEdit, QTextEdit, QPlainTextEdit, QGroupBox, 
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QScrollBar, QMainWindow, QApplication)
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import QTimer

class MySscomUI(QWidget):
    def __init__(self):
        super().__init__()
        self.CreateItems()
        self.CreateLayout()
        self.setGeometry(300, 300, 800, 550)
        self.setWindowTitle('串口调试助手')
        self.show()

    def CreateItems(self):
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

        self.chcHexRecv = QCheckBox('十六进制接收')
        self.chcWrap = QCheckBox('自动换行')
        self.chcAutoClear = QCheckBox('自动清空')
        self.chcAutoSave = QCheckBox('自动保存')

        self.btnClear = QPushButton('清空')

        self.lblAddr = QLabel('地址:')
        self.txtAddr = QLineEdit()
        self.btnSaveAs = QPushButton('选择...')

        self.chcHexSend = QCheckBox('十六进制发送')
        self.chcAutoSend = QCheckBox('自动发送')
        self.txtAutoSend = QLineEdit()
        self.lblAutoSend = QLabel('秒')
        intValidAutoSend = QIntValidator(0, 999, self)
        self.txtAutoSend.setValidator(intValidAutoSend)

        self.txtRecv = QPlainTextEdit()
        # self.txtRecv.verticalScrollBar().setValue(self.txtRecv.verticalScrollBar().maximum())
        self.vscrlRecv = self.txtRecv.verticalScrollBar()
        # print(vscrlRecv.maximum())
        
        self.txtSend = QPlainTextEdit()
        self.btnSend = QPushButton('发送')
        self.txtSend.setFixedHeight(100)
        self.btnSend.setFixedHeight(35)

        self.tmrSend = QTimer()
    
    def CreateLayout(self):
        hboxMain = QHBoxLayout()
        vboxMainSet = QVBoxLayout()
        vboxDisp = QVBoxLayout()

        self.gboxPortSet = QGroupBox('串口设置')
        self.gboxRecvSet = QGroupBox('接收设置')
        self.gboxSendSet = QGroupBox('发送设置')

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

        vboxMainSet.addWidget(self.gboxPortSet)
        vboxMainSet.addWidget(self.gboxRecvSet)
        vboxMainSet.addWidget(self.gboxSendSet)
        vboxMainSet.addStretch()

        self.gboxPortSet.setLayout(vboxPortSet)
        self.gboxRecvSet.setLayout(vboxRecvSet)
        self.gboxSendSet.setLayout(vboxSendSet)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MySscomUI()
    sys.exit(app.exec_())