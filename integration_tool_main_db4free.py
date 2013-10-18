#!/usr/bin/python
#coding=utf8

from PyQt4 import QtCore
from PyQt4 import QtGui
import sys,os
import random
import time
import ConfigParser
import ctypes
# import winshell
import smtplib
# import socket
from integration_tool_chatting_db4free import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
    
class IntegrationToolMain(QtGui.QMainWindow):  
    def __init__(self):
        super(IntegrationToolMain, self).__init__()
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint) #CustomizeWindowHint,WindowSystemMenuHint
        self.setObjectName("Integration Tool Main")
        self.setWindowTitle("Integration Tool Main")
        self.resize(620, 425)
        self.setMinimumSize(QtCore.QSize(620, 425))
        self.setMaximumSize(QtCore.QSize(620, 425))
        self.statusBar()
        self.main_frame = QtGui.QFrame(self)
        self.main_frame.setGeometry(QtCore.QRect(10, 40, 600, 365))
        self.main_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.main_frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame = QtGui.QFrame(self.main_frame)
        self.frame.setGeometry(QtCore.QRect(0, 0, 600, 365))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.show()
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 600, 365))
        self.label.setPixmap(QtGui.QPixmap("youlechang1.jpg"))
        
        self.main_filedirpath=sys.path[1]
        exit = QtGui.QAction(QtGui.QIcon(os.path.join(self.main_filedirpath,"exit.ico")), 'hide or exit', self)
        exit.setShortcut('Ctrl+0')
        exit.setStatusTip(u'hide or exit tool   快捷键切换：Ctrl+0')
        exit.setToolTip(u'hide or exit tool   快捷键切换：Ctrl+0')
        self.connect(exit, QtCore.SIGNAL('triggered()'), self.close)
        self.main_tool_remindertool = QtGui.QAction(QtGui.QIcon(os.path.join(self.main_filedirpath,"main_tool_remindertool.ico")), 'reminder tool', self)
        self.main_tool_remindertool.setShortcut('Ctrl+1')
        self.main_tool_remindertool.setStatusTip(u'reminder tool   快捷键切换：Ctrl+1')
        self.main_tool_remindertool.setToolTip(u'reminder tool   快捷键切换：Ctrl+1')
        
        self.connect(self.main_tool_remindertool, QtCore.SIGNAL('triggered()'), self.main_tool_remindertool_show)        
        self.main_tool_chatting= QtGui.QAction(QtGui.QIcon(os.path.join(self.main_filedirpath,"main_tool_chatting.ico")), 'message board', self)
        self.main_tool_chatting.setShortcut('Ctrl+2')
        self.main_tool_chatting.setStatusTip(u'message board   快捷键切换：Ctrl+2')
        self.main_tool_chatting.setToolTip(u'message board   快捷键切换：Ctrl+2')
        self.connect(self.main_tool_chatting, QtCore.SIGNAL('triggered()'), self.main_tool_chatting_show)
        
        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(self.main_tool_remindertool)
        self.toolbar.addAction(self.main_tool_chatting)
        self.toolbar.addAction(exit)

        main_icon = QtGui.QIcon(os.path.join(self.main_filedirpath,"168.ico"))     
        self.setWindowIcon(main_icon)
        self.isTopLevel()
        self.main_trayIcon = QtGui.QSystemTrayIcon(self)
        self.main_trayIcon.setIcon(main_icon)
        self.main_trayIcon.show()
        self.main_trayIcon.activated.connect(self.main_trayClick) 
        self.main_trayIcon.setToolTip(u"Integration Tool Main") 
        self.main_Menu()

    def main_Menu(self):
        self.main_minimizeAction = QtGui.QAction(u"最小化窗口", self,triggered=self.main_hide_event)
        self.main_restoreAction = QtGui.QAction(u"恢复窗口", self,triggered=self.main_shownormal_event)
        self.main_quitAction = QtGui.QAction(u"退出软件", self,triggered=self.close)
        self.main_trayIconMenu = QtGui.QMenu(self)
        self.main_trayIconMenu.addAction(self.main_minimizeAction)
        self.main_trayIconMenu.addAction(self.main_restoreAction)
        self.main_trayIconMenu.addSeparator()
        self.main_trayIconMenu.addAction(self.main_quitAction)
        self.main_trayIcon.setContextMenu(self.main_trayIconMenu)

    def main_trayClick(self,reason):
        if reason==QtGui.QSystemTrayIcon.DoubleClick: 
            self.main_shownormal_event()
            self.main_showMessage()

    def main_hide_event(self):
        self.hide()
        myalarm.hide_flag=1

    def main_shownormal_event(self):
        self.showNormal()
        myalarm.hide_flag=0

    def main_showMessage(self):
        main_icon=QtGui.QSystemTrayIcon.Information
        self.main_trayIcon.showMessage(u"Integration Tool Main",u"双击激活窗口，右击选择退出",main_icon)

    def main_tool_remindertool_show(self):
        global tools_dict
        if tools_dict[1].isHidden():
            for key in tools_dict:
                if key==1:
                    tools_dict[1].show()
                    tools_dict[1].frame.show()
                    self.frame.hide()
                    continue;
                tools_dict[key].hide()
                tools_dict[key].frame.hide()
        else:
            self.frame.show()
            tools_dict[1].hide()
            tools_dict[1].frame.hide()
            
    def main_tool_chatting_show(self):
        global tools_dict
        if tools_dict[2].isHidden():
            for key in tools_dict:
                if key==2:
                    tools_dict[2].show()
                    tools_dict[2].frame.show()
                    tools_dict[2].chat_frame_1.show()
                    self.frame.hide()
                    continue;
                tools_dict[key].hide()
                tools_dict[key].frame.hide()
        else:
            self.frame.show()
            tools_dict[2].hide()
            tools_dict[2].frame.hide()

    def closeEvent(self,event):
        if self.main_trayIcon.isVisible() and self.isVisible():
            self.main_hide_event()
            event.ignore()
        else:
            myalarm.timerreminder.stop()
            if myalarm.total_workingtimes>=myalarm.total_times:
                myalarm.total_timelogaccumulation+='第%d次休息时间：\n'%(myalarm.total_workingtimes)+str(time.strftime("%H:%M:%S", time.localtime()))+'\n'+'此次共休息%s\n\n'%myalarm.time_calculate(myalarm.last_resttimeduration)+'忙碌的一天终于结束了！下班啦，呼呼 ~\n将在你点击Close按钮关闭对话框后关闭软件。'
                MessageBox(title='Notes',message=_fromUtf8(myalarm.total_timelogaccumulation))
            else:
                myalarm.total_timelogaccumulation+='第%d次工作时间：\n'%(myalarm.total_workingtimes)+str(time.strftime("%H:%M:%S", time.localtime()))+'\n\n'+'忙碌的一天终于结束了！下班啦，呼呼 ~\n将在你点击Close按钮关闭对话框后关闭软件。'
                MessageBox(title='Notes',message=_fromUtf8(myalarm.total_timelogaccumulation))
            myalarm.plainTextEdit.setPlainText(_fromUtf8(myalarm.total_timelogaccumulation))
            f=open(os.path.join(myalarm.filedirpath,'daily_restTime_recording_in_%s.txt'%str(time.strftime("%Y_%m_%d", time.localtime()))),'w')
            f.write(str(myalarm.total_timelogaccumulation))
            f.close()
#             ipaddress=socket.gethostbyname(socket.gethostname())
#             myalarm.total_timelogaccumulation+='\nIP address: %s \n rest_reminder工具已经启动过了~'%ipaddress
            sender = 'integration_tool@163.com'
            mailto = 'integration_tool@163.com'
            smtp = smtplib.SMTP()    
            smtp.connect( 'smtp.163.com' )
            smtp.login(sender, 'qwe123')
            smtp.sendmail(sender, mailto, str(myalarm.total_timelogaccumulation))
            smtp.quit()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
            
class ProgressStart(QtGui.QSplashScreen):
    def __init__(self, parent=None):
        super(ProgressStart, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal) 
        self.resize(620, 425)
        self.setMinimumSize(QtCore.QSize(620, 425))
        self.setMaximumSize(QtCore.QSize(620, 425))
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        self.pbar = QtGui.QProgressBar(self)
        self.pbar.setGeometry(80, 380, 200, 25)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerfun)
        self.step = 0
        self.count=0
        self.start_time=random.randint(1, 90)
        self.end_time=random.randint(self.start_time,100)
        self.timer.start(10)
    def timerfun(self):
        global splash
        if self.step >= 100:
            global integration_tool_main
            self.timer.stop()
            splash.close()
            integration_tool_main.show()
            return 0
        splash.show()
        self.step = self.step + 1
        self.pbar.setValue(self.step)
        while (self.step>=self.start_time) and (self.step<=self.end_time) and (self.count<self.end_time-self.start_time):
            self.timer.stop()
            time.sleep(0.01)
            self.count+=1
        self.timer.start(10)

class MessageBox(QtGui.QWidget):
    def __init__(self, parent=None,title='message box',message="What do you want to mention ?"):
        QtGui.QWidget.__init__(self, parent)
        self.title=title
        self.message=message
        self.setGeometry(300, 300, 300, 180)
        self.setWindowTitle(title)
        reply = QtGui.QMessageBox.warning(self,self.title,self.message,QtGui.QMessageBox.Close)
        if reply == QtGui.QMessageBox.Close:
            self.close()        

class Ui_ReminderAlarm(QtGui.QFrame): 
    def __init__(self,parent=None):      
        self.bootdirpath=os.path.join(os.getenv('APPDATA'),'Microsoft\Windows\Start Menu\Programs\Startup')
        self.filedirpath=sys.path[1]
        init_flag=0
        self.cf=ConfigParser.ConfigParser()
        self.cf.read(os.path.join(self.filedirpath,"reminderalarm_config.ini"))
        if not os.path.exists(os.path.join(self.filedirpath,"reminderalarm_config.ini")):
            if os.getcwd()!=self.bootdirpath:
                self.opentimes=1
                self.startday=time.localtime()[7]
                self.currentday=self.startday
                self.lastday=self.currentday
                self.filedirpath=sys.path[1]
                self.cf.add_section("main")
#                 pa=os.path.join(self.filedirpath,'rest_reminder_forQQ.exe')
#                 winshell.CreateShortcut(Path = os.path.join(os.getenv('APPDATA'),r'Microsoft\Windows\Start Menu\Programs\Startup\rest_reminder_forQQ.lnk'), Target = pa, Icon=(pa, 0), Description='shortcut')
            else:
                self.filedirpath=sys.path[1]
                init_flag=1
                if not os.path.exists(os.path.join(self.filedirpath,"reminderalarm_config.ini")):
                    f=open(os.path.join(self.filedirpath,'Error_Log.txt'),'w')
                    f.write("您的reminderalarm_config.ini文件丢失，请不要从开机启动项中启动！您可以从该软件原程序处启动！")
                    f.close()
        else:
            self.filedirpath=self.cf.get("main", "filedirpath")
            init_flag=1
        if init_flag==1:
            self.opentimes=int(self.cf.get("main", "opentimes"))
            self.opentimes+=1
            self.currentday=int(time.localtime()[7])
            self.lastday=int(self.cf.get("main", "lastday"))
            self.startday=int(self.cf.get("main", "startday"))
            divday=self.currentday-self.lastday
            if divday>=2:
                MessageBox(title='Notes',message=_fromUtf8('\n您已经超过%d天没有启动休息提醒软件了，记住，拥有健康的身体才是人生中最重要的！\n'%divday))
            self.lastday=self.currentday
        self.cf.set("main", "opentimes", str(self.opentimes))
        self.cf.set("main", "startday", str(self.startday))
        self.cf.set("main", "filedirpath", self.filedirpath)
        self.cf.set("main", "bootdirpath", self.bootdirpath)
        self.cf.set("main", "lastday", str(self.lastday))
        self.cf.set("main", "currentday", str(self.currentday))
        self.cf.write(open(os.path.join(self.filedirpath,"reminderalarm_config.ini"), "w"))
        
        super(Ui_ReminderAlarm, self).__init__(parent)
        self.total_times=0
        self.total_workingtimes=0
        self.last_workingtimes=0
        self.last_time=0
        self.total_timelogaccumulation=''
        self.total_worktimeduration=0
        self.total_resttimeduration=0
        self.last_resttimeduration=0
        self.last_total_worktimeduration=0
        self.count=0
        self.maintimer_flag=0
        self.delay_count=0
        self.hide_flag=0

        self.start = time.time()
        self.dynamictime=QtCore.QTimer()
        self.dynamictime.singleShot(1000,self.refreshing)
        self.timerreminder=QtCore.QTimer()
        self.timerreminder.timeout.connect(self.remindernotes)
        self.timerreminder.start(1000000)  #5400000
        self.locktimerreminder=QtCore.QTimer()
        self.locktimerreminder.timeout.connect(self.lockscreen)

        self.frame = QtGui.QFrame(parent)
        self.frame.setGeometry(QtCore.QRect(0, 0, 600, 365))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.hide()
        self.frame_1 = QtGui.QFrame(self.frame)
        self.frame_1.setGeometry(QtCore.QRect(0, 0, 300, 360))
        self.frame_1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_1.setObjectName(_fromUtf8("frame_1"))
        self.label_11 = QtGui.QLabel(self.frame_1)
        self.label_11.setGeometry(QtCore.QRect(100, 0, 100, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.frame_11 = QtGui.QFrame(self.frame_1)
        self.frame_11.setGeometry(QtCore.QRect(10, 20, 280, 310))
        self.frame_11.setFrameShape(QtGui.QFrame.Box)
        self.frame_11.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_11.setObjectName(_fromUtf8("frame_11"))
        self.label_12 = QtGui.QLabel(self.frame_1)
        self.label_12.setGeometry(QtCore.QRect(20, 341, 120, 12))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.lineEdit12 = QtGui.QLineEdit(self.frame_1)
        self.lineEdit12.setGeometry(QtCore.QRect(150, 337, 130, 20))
        self.lineEdit12.setObjectName(_fromUtf8("lineEdit12"))
        self.lineEdit12.setReadOnly(True)
        self.lineEdit12.setText(_fromUtf8(str(self.time_calculate(self.count))))
        self.lineEdit12.setStatusTip(_fromUtf8('这里显示的是你当前所处工作或休息状态的动态时间，可以查看你截止此刻共休息或工作的时长~'))
        self.frame_2 = QtGui.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(300, 0, 300, 365))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.frame_21 = QtGui.QFrame(self.frame_2)
        self.frame_21.setGeometry(QtCore.QRect(0, 0, 300, 180))
        self.frame_21.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_21.setObjectName(_fromUtf8("frame_21"))
        self.label_211 = QtGui.QLabel(self.frame_21)
        self.label_211.setGeometry(QtCore.QRect(100, 0, 100, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_211.setFont(font)
        self.label_211.setAlignment(QtCore.Qt.AlignCenter)
        self.label_211.setObjectName(_fromUtf8("label_211"))
        self.frame_211 = QtGui.QFrame(self.frame_21)
        self.frame_211.setGeometry(QtCore.QRect(10, 20, 280, 150))
        self.frame_211.setFrameShape(QtGui.QFrame.Box)
        self.frame_211.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_211.setObjectName(_fromUtf8("frame_211"))
        self.label_2111 = QtGui.QLabel(self.frame_211)
        self.label_2111.setGeometry(QtCore.QRect(10, 15, 100, 12))
        self.label_2111.setObjectName(_fromUtf8("label_2111"))
        self.lineEdit2111 = QtGui.QLineEdit(self.frame_211)
        self.lineEdit2111.setGeometry(QtCore.QRect(120, 11, 150, 20))
        self.lineEdit2111.setObjectName(_fromUtf8("lineEdit2111"))
        self.lineEdit2111.setReadOnly(True)
        self.lineEdit2111.setText(_fromUtf8(str(self.total_worktimeduration)))
        self.lineEdit2111.setStatusTip(_fromUtf8('这里显示的是总共累计工作的总时间，别太多哟~'))
        self.lineEdit2112 = QtGui.QLineEdit(self.frame_211)
        self.lineEdit2112.setGeometry(QtCore.QRect(120, 38, 150, 20))
        self.lineEdit2112.setObjectName(_fromUtf8("lineEdit2112"))
        self.lineEdit2112.setReadOnly(True)
        self.lineEdit2112.setText(_fromUtf8(str(self.total_resttimeduration)))
        self.lineEdit2112.setStatusTip(_fromUtf8('这里显示的是总共累计休息的总时间，别太少哟~'))
        self.label_2112 = QtGui.QLabel(self.frame_211)
        self.label_2112.setGeometry(QtCore.QRect(10, 42, 100, 12))
        self.label_2112.setObjectName(_fromUtf8("label_2112"))
        self.lineEdit2113 = QtGui.QLineEdit(self.frame_211)
        self.lineEdit2113.setGeometry(QtCore.QRect(120, 65, 150, 20))
        self.lineEdit2113.setObjectName(_fromUtf8("lineEdit2113"))
        self.lineEdit2113.setReadOnly(True)
        self.lineEdit2113.setText(_fromUtf8(str(self.last_time)))
        self.lineEdit2113.setStatusTip(_fromUtf8('这里显示的是总共累计休息的总次数，别太少哟~'))
        self.label_2113 = QtGui.QLabel(self.frame_211)
        self.label_2113.setGeometry(QtCore.QRect(10, 69, 100, 12))
        self.label_2113.setObjectName(_fromUtf8("label_2113"))
        self.lineEdit2114 = QtGui.QLineEdit(self.frame_211)
        self.lineEdit2114.setGeometry(QtCore.QRect(120, 92, 150, 20))
        self.lineEdit2114.setObjectName(_fromUtf8("lineEdit2114"))
        self.lineEdit2114.setReadOnly(True)
        self.lineEdit2114.setText(_fromUtf8(str(self.last_resttimeduration)))
        self.lineEdit2114.setStatusTip(_fromUtf8('这里显示的是最近一次你休息的时刻，别离上一次休息时刻太远哟~'))
        self.label_2114 = QtGui.QLabel(self.frame_211)
        self.label_2114.setGeometry(QtCore.QRect(10, 96, 100, 12))
        self.label_2114.setObjectName(_fromUtf8("label_2114"))
        self.label_2115 = QtGui.QLabel(self.frame_211)
        self.label_2115.setGeometry(QtCore.QRect(10, 123, 100, 12))
        self.label_2115.setObjectName(_fromUtf8("label_2115"))
        self.lineEdit2115 = QtGui.QLineEdit(self.frame_211)
        self.lineEdit2115.setGeometry(QtCore.QRect(120, 119, 150, 20))
        self.lineEdit2115.setObjectName(_fromUtf8("lineEdit2115"))
        self.lineEdit2115.setReadOnly(True)
        self.lineEdit2115.setText(_fromUtf8(str(self.last_resttimeduration)))
        self.lineEdit2115.setStatusTip(_fromUtf8('这里显示的是最近一次你休息的时长，一次可别太短了哟~'))
        self.frame_22 = QtGui.QFrame(self.frame_2)
        self.frame_22.setGeometry(QtCore.QRect(0, 175, 300, 195))
        self.frame_22.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_22.setObjectName(_fromUtf8("frame_22"))
        self.plainTextEdit = QtGui.QPlainTextEdit(self.frame_22)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 20, 280, 135))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.plainTextEdit.setReadOnly(True)
        self.total_timelogaccumulation='忙碌的一天开始啦！\n请每隔最多1个半小时休息一次哟亲！\n\n第1次工作时间：\n'+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+'\n'
        self.plainTextEdit.setPlainText(_fromUtf8(self.total_timelogaccumulation))
        self.plainTextEdit.setStatusTip(_fromUtf8('这里显示的是你休息和工作的详细时间和时长记录，好好把握你的工作节奏哟~'))
        self.pushButton_221 = QtGui.QPushButton(self.frame_22)
        self.pushButton_221.setGeometry(QtCore.QRect(10, 160, 80, 25))
        self.pushButton_221.setObjectName(_fromUtf8("pushButton_221"))
        self.pushButton_221.setStatusTip(_fromUtf8('点击此按钮可以进入提前休息模式哟~'))
        QtCore.QObject.connect(self.pushButton_221, QtCore.SIGNAL("clicked()"),self.restinadvance)
        self.pushButton_223 = QtGui.QPushButton(self.frame_22)
        self.pushButton_223.setGeometry(QtCore.QRect(100, 160, 100, 25))
        self.pushButton_223.setObjectName(_fromUtf8("pushButton_223"))
        self.pushButton_223.setStatusTip(_fromUtf8('点击此按钮可以暂时停止休息提醒，再次点击按钮可以恢复提醒模式~'))
        QtCore.QObject.connect(self.pushButton_223, QtCore.SIGNAL("clicked()"),self.pauseorresume_reminder)
        self.pushButton_222 = QtGui.QPushButton(self.frame_22)
        self.pushButton_222.setGeometry(QtCore.QRect(210, 160, 80, 25))
        self.pushButton_222.setObjectName(_fromUtf8("pushButton_222"))
        self.pushButton_222.setStatusTip(_fromUtf8('点击此按钮可以一次延迟休息一个半小时时间~'))
        QtCore.QObject.connect(self.pushButton_222, QtCore.SIGNAL("clicked()"),self.restdelay)
        self.label_221 = QtGui.QLabel(self.frame_22)
        self.label_221.setGeometry(QtCore.QRect(100, 0, 100, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_221.setFont(font)
        self.label_221.setAlignment(QtCore.Qt.AlignCenter)
        self.label_221.setObjectName(_fromUtf8("label_221"))
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
    def retranslateUi(self):
        self.setWindowTitle(_translate("ReminderAlarm", "ReminderAlarm", None))
        self.label_11.setText(_translate("ReminderAlarm", "时钟表", None))
        self.label_211.setText(_translate("ReminderAlarm", "休息情况详细统计", None))
        self.label_2111.setText(_translate("ReminderAlarm", "总共累计工作时长", None))
        self.label_2112.setText(_translate("ReminderAlarm", "总共累计休息时长", None))
        self.label_2113.setText(_translate("ReminderAlarm", "总共累计休息次数", None))
        self.label_2114.setText(_translate("ReminderAlarm", "最近一次休息时间", None))
        self.label_2115.setText(_translate("ReminderAlarm", "最近一次休息时长", None))
        self.label_221.setText(_translate("ReminderAlarm", "休息时间详细记录", None))
        self.pushButton_221.setText(_translate("ReminderAlarm", "我要提前休息", None))
        self.pushButton_222.setText(_translate("ReminderAlarm", "一次延时休息", None))
        self.pushButton_223.setText(_translate("ReminderAlarm", "暂停或继续提醒", None))
        self.label_12.setText(_translate("ReminderAlarm", "显示此次工作动态计时", None))

    def refreshing(self):
        self.count+=1
        self.dynamictimecount=str(self.time_calculate(self.count))
        self.lineEdit12.setText(_fromUtf8(self.dynamictimecount))
        self.dynamictime.singleShot(1000,self.refreshing)
    def lockscreen(self):
        if self.maintimer_flag!=3:
            self.dll = ctypes.WinDLL('user32.dll')
            self.dll.LockWorkStation()
            self.maintimer_flag=3
    def time_calculate(self,end_time=0,start_time=0,divtime=0):
        self.elapsed =  end_time - start_time-divtime
        self.hours=self.elapsed/3600
        self.minutes=(self.elapsed-int(self.hours)*3600)/60
        self.seconds=self.elapsed-(int(self.hours)*3600+int(self.minutes)*60)
        self.standardtime=str(int(self.hours))+'小时'+str(int(self.minutes))+'分'+str(int(self.seconds))+'秒'
        return self.standardtime
    def remindernotes(self):
        if self.maintimer_flag!=3:
            self.label_12.setText(_translate("ReminderAlarm", "显示此次休息动态计时", None))
            self.tempflag=self.maintimer_flag
            self.timerreminder.stop()
            self.locktimerreminder.start(30000)
            self.count=0
            self.total_worktimeduration=str(self.time_calculate(time.time(),self.start,self.total_resttimeduration))
            self.last_workingtimes=time.time()-self.start-self.total_resttimeduration-self.last_total_worktimeduration
            self.lineEdit2111.setText(_fromUtf8(self.total_worktimeduration))
            gettime=time.time()
            self.total_times+=1
            self.total_workingtimes=self.total_times+1
            self.last_time=time.strftime("%H:%M:%S", time.localtime())
            self.lineEdit2114.setText(_fromUtf8(str(self.last_time)))
            self.total_timelogaccumulation+='第%d次休息时间：\n'%self.total_times+str(time.strftime("%H:%M:%S", time.localtime()))+'\n' 
            self.plainTextEdit.setPlainText(_fromUtf8(self.total_timelogaccumulation)) 
            integration_tool_main.showNormal()
            MessageBox(title='Notes',message=_fromUtf8("宝贝儿，该休息了！\n30秒后电脑将自动锁屏，请站起来扭扭腰动动腿喝喝水，休息下眼睛脑袋，再上上厕所等，在你休息完回来后解锁屏幕，直到你点击下面这个‘close’按钮关闭这个提示框之前都会计算你的休息时间，在点击关闭后你将重新进入工作模式，直到下一次的定时提醒休息框弹出！"))
            if self.hide_flag==1:
                integration_tool_main.hide()
            self.label_12.setText(_translate("ReminderAlarm", "显示此次工作动态计时", None))
            self.maintimer_flag=self.tempflag
            self.locktimerreminder.stop()
            self.last_resttimeduration = time.time() - gettime
            self.total_timelogaccumulation+='此次共休息%s\n\n'%self.time_calculate(self.last_resttimeduration)
            self.plainTextEdit.setPlainText(_fromUtf8(self.total_timelogaccumulation))    
            self.total_resttimeduration+=self.last_resttimeduration
            self.lineEdit2115.setText(_fromUtf8(str(self.time_calculate(self.last_resttimeduration))))
            self.lineEdit2112.setText(_fromUtf8(str(self.time_calculate(self.total_resttimeduration))))
            self.lineEdit2113.setText(_fromUtf8(str(self.total_times)))
            self.total_timelogaccumulation+='第%d次工作时间：\n'%self.total_workingtimes+str(time.strftime("%H:%M:%S", time.localtime()))+'\n此次共工作%s\n\n'%self.time_calculate(self.last_workingtimes)
            self.plainTextEdit.setPlainText(_fromUtf8(self.total_timelogaccumulation))
            self.count=0
            self.last_total_worktimeduration=time.time()-self.start-self.total_resttimeduration
            if self.maintimer_flag==0:
                self.timerreminder.start(1000000)   #5400000
    def pauseorresume_reminder(self):
        if self.maintimer_flag!=3:
            self.tempflag=self.maintimer_flag
        if self.timerreminder.isActive():
            self.timerreminder.stop()
            self.total_timelogaccumulation+='\n这次你可能由于太忙或不想休息暂停了休息提醒呢，你男人表示很囧的！(@.@)\n'
            self.plainTextEdit.setPlainText(_fromUtf8(self.total_timelogaccumulation))
            self.maintimer_flag=3
        else:
            self.delay_count=0
            if self.maintimer_flag==3:
                self.maintimer_flag=self.tempflag
            if self.maintimer_flag==0:
                self.timerreminder.start(1000000)   #5400000
            self.count=0
            self.total_timelogaccumulation+='\n太好了，又开始休息提醒了！你男人表示很欣慰！呼呼~\n'
            self.plainTextEdit.setPlainText(_fromUtf8(self.total_timelogaccumulation))
    def restinadvance(self):
        self.delay_count=0
        self.total_timelogaccumulation+='\n这次你是提前休息的呢，不错哟！^ . ^\n'
        if self.maintimer_flag!=3:
            self.plainTextEdit.setPlainText(_fromUtf8(self.total_timelogaccumulation))
        else:
            self.total_timelogaccumulation+='\n您还处于暂停提醒模式，请再次点击暂停或继续提醒按钮后再点击此按钮提前休息！\n'
            self.plainTextEdit.setPlainText(_fromUtf8(self.total_timelogaccumulation))
            MessageBox(title='Notes',message=_fromUtf8('\n您还处于暂停提醒模式，请再次点击"暂停或继续提醒"按钮后再点击此按钮提前休息！\n'))
            return 0
        if self.timerreminder.isActive():
            self.timerreminder.stop()
            self.timerreminder.start(0)
    def restdelay(self):
        self.delay_count+=1
        if self.timerreminder.isActive():
            self.timerreminder.stop()
        self.timerreminder.start(1000000)   #5400000
        self.maintimer_flag=0
        self.total_timelogaccumulation+='\n这次你延迟了1个半小时休息时间呢，你男人表示很囧的！希望你忙完后点击提前休息按钮的！(*.*)\n\n'
        self.plainTextEdit.setPlainText(_fromUtf8(self.total_timelogaccumulation))
        if self.delay_count>=2:
            MessageBox(title='Warning',message=_fromUtf8('\n您已经第%d次延迟休息了，这样对亲的健康会造成严重影响，为了亲的健康请再忙也放下手中的事儿休息片刻，请点击提前休息按钮！*——* \n'%self.delay_count))
    def closeEvent(self,event):
        event.ignore()
                 
class clockForm(QtGui.QFrame):
    def __init__(self,parent=None):
        super(clockForm,self).__init__(parent)
        self.setGeometry(QtCore.QRect(5, -6, 270, 320))
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.update) 
        self.timer.start(1000)
    def paintEvent(self,event):
        painter=QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        font=QtGui.QFont("Times",6)
        fm=QtGui.QFontMetrics(font)
        fontRect=fm.boundingRect("99")
        minPoints=[QtCore.QPointF(50,25),QtCore.QPointF(48,50),QtCore.QPointF(52,50)]
        hourPoints=[QtCore.QPointF(50,35),QtCore.QPointF(48,50),QtCore.QPointF(52,50)]
        side=min(self.width(),self.height())
        painter.setViewport((self.width()-side)/2,(self.height()-side)/2,side,side)
        painter.setWindow(0,0,100,100)
        niceBlue=QtGui.QColor(150,150,200)
        haloGrident=QtGui.QRadialGradient(50,50,50,50,50)
        haloGrident.setColorAt(0.0,QtCore.Qt.lightGray)
        haloGrident.setColorAt(0.5,QtCore.Qt.darkGray)
        haloGrident.setColorAt(0.9,QtCore.Qt.white)
        haloGrident.setColorAt(1.0,niceBlue)
        painter.setBrush(haloGrident)
        painter.setPen(QtGui.QPen(QtCore.Qt.darkGray,1))
        painter.drawEllipse(0,0,100,100)
        transform=QtGui.QTransform()
        painter.setPen(QtGui.QPen(QtCore.Qt.black,1.5))
        fontRect.moveCenter(QtCore.QPoint(50,10+fontRect.height()/2))
        painter.setFont(font)
        painter.drawLine(50,2,50,8)
        painter.drawText(QtCore.QRectF(fontRect),QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop,"12")
        for i in range(1,12,1):
            transform.translate(50, 50)
            transform.rotate(30)
            transform.translate(-50,-50)          
            painter.setWorldTransform(transform)
            painter.drawLine(50,2,50,8)
            painter.drawText(QtCore.QRectF(fontRect),QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop,"%d" % i)
        transform.reset()
        painter.setPen(QtGui.QPen(QtCore.Qt.blue,1))
        for i in range(1,60): 
            transform.translate(50,50)
            transform.rotate(6)
            transform.translate(-50,-50)
            if i%5!=0:
                painter.setWorldTransform(transform)
                painter.drawLine(50,2,50,5)
        transform.reset()
        currentTime=QtCore.QTime().currentTime()
        hour=currentTime.hour() if currentTime.hour()<12 else currentTime.hour()-12
        minite=currentTime.minute()
        second=currentTime.second()
        hour_angle=hour*30.0+(minite/60.0)*30.0
        minite_angle=(minite/60.0)*360.0
        second_angle=second*6.0
        transform.translate(50,50)
        transform.rotate(hour_angle)
        transform.translate(-50,-50)
        painter.setWorldTransform(transform)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(QtCore.Qt.darkRed))
        painter.drawPolygon(QtGui.QPolygonF(hourPoints))
        transform.reset()
        transform.translate(50,50)
        transform.rotate(minite_angle)
        transform.translate(-50,-50)
        painter.setWorldTransform(transform)
        painter.setBrush(QtGui.QBrush(QtCore.Qt.darkGreen))
        painter.drawPolygon(QtGui.QPolygonF(minPoints))
        transform.reset()
        transform.translate(50,50)
        transform.rotate(second_angle)
        transform.translate(-50,-50)
        painter.setWorldTransform(transform)
        painter.setPen(QtGui.QPen(QtCore.Qt.darkCyan,1))
        painter.drawLine(50,50,50,20)


if __name__=='__main__':       
    app = QtGui.QApplication(sys.argv)
    splash=ProgressStart(QtGui.QPixmap("youlechang.jpg"))
    splash.show()
    app.processEvents() 
    integration_tool_main = IntegrationToolMain() 
    splash.finish(integration_tool_main)
    myalarm = Ui_ReminderAlarm(integration_tool_main.main_frame) 
    myalarm.hide()
    clock=clockForm(myalarm.frame_11)
    clock.show()
    chat = Ui_PublicChattingPlatform(integration_tool_main.main_frame)
    chat.hide()

    tools_dict={}
    tools_dict[1]=myalarm
    tools_dict[2]=chat
    
    sys.exit(app.exec_())
    
