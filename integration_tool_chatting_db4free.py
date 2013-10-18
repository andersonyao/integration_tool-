#!/usr/bin/python
#coding=utf8

from PyQt4 import QtCore, QtGui
import time,os,sys
import MySQLdb
import ConfigParser
    
class ExtendedQLabel(QtGui.QLabel):
    def __init(self, parent):
        QtGui.QLabel.__init__(self, parent)
    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked(PyQt_PyObject)'), self) 

class Ui_PublicChattingPlatform(QtGui.QFrame):
    def __init__(self,parent=None):
        self.frame_2_list=[]
        self.frame_21_list=[]
        self.label_21_list=[]
        self.label_22_list=[]
        self.label_23_list=[]
        self.frame_22_list=[]
        self.textEdit_2_list=[]
        self.frameY=0
        self.framecount=0
        self.user_messages_count=0
        self.tname="anonymity"
        self.bootdirpath=os.path.join(os.getenv('APPDATA'),'Microsoft\Windows\Start Menu\Programs\Startup')
        self.filedirpath=sys.path[1]
        self.tempr1=os.path.join(self.filedirpath,"Touxiang.jpg")

        self.cf1=ConfigParser.ConfigParser()
        self.cf1.read(os.path.join(self.filedirpath,"User_data.ini"))
        self.cf2=ConfigParser.ConfigParser()
        self.cf2.read(os.path.join(self.filedirpath,"User_photo_data.ini"))
        if (not os.path.exists(os.path.join(self.filedirpath,"User_data.ini"))) or (not os.path.exists(os.path.join(self.filedirpath,"User_photo_data.ini"))):
            if os.getcwd()!=self.bootdirpath:
                self.user_messages_count=1
                if not os.path.exists(os.path.join(self.filedirpath,"User_photo_data.ini")):
                    self.cf2.add_section("User_photo_data")
                self.cf2.set("User_photo_data", "English_Name",self.tname)
                self.cf2.set("User_photo_data", "PhotoPath",self.tempr1)
                self.cf2.write(open(os.path.join(self.filedirpath,"User_photo_data.ini"), "w"))
            else:
                f=open(os.path.join(self.filedirpath,'Error_Log.txt'),'w')
                f.write("您的User_data.ini或User_photo_data.ini文件丢失，请不要从开机启动项中启动！您可以从该软件原程序处启动！")
                f.close()
        else:
            if len(self.cf1.sections())>=1:
                self.user_messages_count=int(self.cf1.sections()[-1][-1])
        self.Photo_English_Name=self.cf2.get("User_photo_data", "English_Name")
        self.PhotoPath=self.cf2.get("User_photo_data", "PhotoPath")
        self.tname=self.Photo_English_Name
        self.tempr1=self.PhotoPath
        
        super(Ui_PublicChattingPlatform, self).__init__(parent)
        self.frame = QtGui.QFrame(parent)
        self.frame.setGeometry(QtCore.QRect(0, 0, 600, 365))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.hide()
        self.tabWidget = QtGui.QTabWidget(self.frame)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 600, 365))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.chat_frame_1 = QtGui.QFrame(self.tab)
        self.chat_frame_1.setGeometry(QtCore.QRect(0, 0, 600, 365))
        self.chat_frame_1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.chat_frame_1.setFrameShadow(QtGui.QFrame.Raised)
        self.chat_frame_1.setObjectName("chat_frame_1")
        self.chat_frame_1.setFrameShadow(QtGui.QFrame.Sunken)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.chat_frame_2 = QtGui.QFrame(self.tab_2)
        self.chat_frame_2.setGeometry(QtCore.QRect(20, 20, 560, 300))
        self.chat_frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.chat_frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.chat_frame_2.setObjectName("chat_frame_2")
        self.chat_frame_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.photo = ExtendedQLabel('photo',self.chat_frame_2)
        self.photo.setGeometry(QtCore.QRect(0, 0, 100, 100))
        self.photo.setMaximumSize(QtCore.QSize(200, 200))
        self.photo.setFrameShape(QtGui.QFrame.StyledPanel)
        self.photo.setText('')
        self.photo.setPixmap(QtGui.QPixmap(self.tempr1))
        self.photo.setAlignment(QtCore.Qt.AlignCenter)
        self.photo.setObjectName("photo") 
        self.photo.setToolTip(u'可以通过点击图片编辑留言人头像！')
        QtCore.QObject.connect(self.photo, QtCore.SIGNAL("clicked(PyQt_PyObject)"), self.Upload_photo)
        author = QtGui.QLabel(u'留言人',self.chat_frame_2)
        title = QtGui.QLabel(u'留言时间',self.chat_frame_2)
        review = QtGui.QLabel(u'消息内容',self.chat_frame_2)
        self.authorEdit = QtGui.QLineEdit(self.chat_frame_2)
        self.authorEdit.setGeometry(QtCore.QRect(100, 0, 80, 50))
        self.authorEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.authorEdit.setObjectName("authorEdit")
        self.authorEdit.setText(self.tname)
        self.authorEdit.setToolTip(u'可以通过输入编辑留言人名！')
        self.timeEdit = QtGui.QLineEdit(self.chat_frame_2)
        self.timeEdit.setGeometry(QtCore.QRect(100, 0, 80, 50))
        self.timeEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.timeEdit.setObjectName("timeEdit")
        temptime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.timeEdit.setText(str(temptime))
        self.timeEdit.setReadOnly(True)
        self.timeEdit.setStyleSheet("background-color:rgba(0,192,192,192)")
        self.timeEdit.setToolTip(u'自动读取，不可以编辑当前时间！')
        self.reviewEdit = QtGui.QTextEdit(self.chat_frame_2)
        self.reviewEdit.setToolTip(u'可以通过输入编辑此次留言内容！')
        pushButton = QtGui.QPushButton(self.chat_frame_2)
        pushButton.setGeometry(QtCore.QRect(350, 5, 70, 20))
        pushButton.setCheckable(False)
        pushButton.setAutoExclusive(False)
        pushButton.setDefault(False)
        pushButton.setFlat(False)
        pushButton.setObjectName("pushButton")
        pushButton.setText("Submit")
        QtCore.QObject.connect(pushButton, QtCore.SIGNAL("clicked()"), self.WriteDatabase)    
        InsertButton = QtGui.QPushButton(self.chat_frame_2)
        InsertButton.setGeometry(QtCore.QRect(270, 5, 70, 20))
        InsertButton.setCheckable(False)
        InsertButton.setAutoExclusive(False)
        InsertButton.setDefault(False)
        InsertButton.setFlat(False)
        InsertButton.setObjectName("InsertButton")
        InsertButton.setText("Insert Image")
        QtCore.QObject.connect(InsertButton, QtCore.SIGNAL("clicked()"), self.InsertImagefun)
        grid = QtGui.QGridLayout(self.chat_frame_2)
        self.frame_button = QtGui.QFrame(self.chat_frame_2)
        self.frame_button.setObjectName("frame_button")
        grid_button = QtGui.QGridLayout(self.frame_button)
        grid_button.setSpacing(10)
        grid_button.addWidget(InsertButton, 1, 0)
        grid_button.addWidget(pushButton, 1, 1)
        grid.setSpacing(10)
        grid.addWidget(self.photo, 1, 0, 2, 2)
        grid.addWidget(author, 1, 2)
        grid.addWidget(self.authorEdit, 1, 3)
        grid.addWidget(title, 2, 2)
        grid.addWidget(self.timeEdit, 2, 3)
        grid.addWidget(review, 3, 0)
        grid.addWidget(self.reviewEdit, 3, 1, 4, 3)
        grid.addWidget(self.frame_button, 7, 2,1,2)
        self.chat_frame_2.setLayout(grid)
        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),  "message board")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "message publish")
        self.frame11 = QtGui.QFrame(self.chat_frame_1)
        self.frame11.setGeometry(QtCore.QRect(0, 0, 600, 20))
        self.frame11.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame11.setFrameShadow(QtGui.QFrame.Plain)
        self.frame11.setObjectName("frame11")
        self.label_11 = QtGui.QLabel(self.frame11)
        self.label_11.setGeometry(QtCore.QRect(0, 0, 180, 20))
        self.label_11.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setText("User Account")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtGui.QLabel(self.frame11)
        self.label_12.setGeometry(QtCore.QRect(180, 0, 420, 20))
        self.label_12.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setText("User Message")
        self.label_12.setObjectName("label_12")
        self.scrollArea = QtGui.QScrollArea(self.chat_frame_1)
        self.scrollArea.setGeometry(QtCore.QRect(0, 20, 600, 345))    
        self.scrollArea.setFrameShadow(QtGui.QFrame.Plain)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 20, 600, 100))    
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)    
        QtCore.QMetaObject.connectSlotsByName(self.frame)
        self.ReadDatabase()
    def Upload_photo(self):
        dlg2 = QtGui.QFileDialog()
        uploadphoto = dlg2.getOpenFileName(self,u"open the text", os.getcwd(), "image files (*.jpeg *.jpg *.gif *.bmp)")
        if not uploadphoto:
            uploadphoto=QtCore.QString(r'C:\Users\Administrator\workspace\Integration_tool\src\Touxiang.jpg')
        self.photo.setPixmap(QtGui.QPixmap(uploadphoto))
        self.tempr1=unicode(uploadphoto,'utf8','ignore')
        self.cf2.set("User_photo_data", "PhotoPath",self.tempr1)
        self.cf2.write(open(os.path.join(self.filedirpath,"User_photo_data.ini"), "w"))
    def InsertImagefun(self):
        dlg1 = QtGui.QFileDialog()
        insertimage = dlg1.getOpenFileName(self,u"open the text", os.getcwd(), "image files (*.jpeg *.jpg *.gif *.bmp)")
        if not insertimage:
            insertimage=QtCore.QString(r'C:\Users\Administrator\workspace\Integration_tool\src\Touxiang.jpg')
        Textbase=self.reviewEdit.toHtml()
        Textbase=Textbase+QtCore.QString("<img src='")+insertimage+QtCore.QString("' />")  
        self.reviewEdit.setHtml(Textbase)
    def addnewFrame(self):
        self.scrollArea.hide() 
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 20, 600, 100+100*self.framecount))
        self.frame_2 = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setGeometry(QtCore.QRect(0, self.frameY, 600, 100))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_2_list.append(self.frame_2)
        self.frame_21 = QtGui.QFrame(self.frame_2)
        self.frame_21.setGeometry(QtCore.QRect(0, 0, 180, 100))
        self.frame_21.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.frame_21_list.append(self.frame_21)
        self.label_21 = QtGui.QLabel(self.frame_21)
        self.label_21.setGeometry(QtCore.QRect(0, 0, 100, 100))
        self.label_21.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_21.setText("")
        self.label_21.setPixmap(self.myphoto) 
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.label_21_list.append(self.label_21)
        self.label_22 = QtGui.QLabel(self.frame_21)
        self.label_22.setGeometry(QtCore.QRect(100, 0, 80, 50))
        self.label_22.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setText(self.tname)
        self.label_22.setObjectName("label_22")
        self.label_22_list.append(self.label_22)
        self.label_23 = QtGui.QLabel(self.frame_21)
        self.label_23.setGeometry(QtCore.QRect(100, 50, 80, 50))
        self.label_23.setWordWrap(1)
        self.label_23.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setText(str(self.tempr2))
        self.label_23.setObjectName("label_23")
        self.label_23_list.append(self.label_23)
        self.frame_22 = QtGui.QFrame(self.frame_2)
        self.frame_22.setGeometry(QtCore.QRect(180, 0, 420, 100))
        self.frame_22.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_22.setObjectName("frame_22")
        self.frame_22_list.append(self.frame_22)
        self.textEdit_2 = QtGui.QTextEdit(self.frame_22)
        self.textEdit_2.setGeometry(QtCore.QRect(0, 0, 405, 100))
        self.textEdit_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setHtml(self.tempr3)
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2_list.append(self.textEdit_2)
        self.frameY+=100
        self.framecount+=1
        self.scrollArea.show()
    def ReadDatabase(self):
        self.frameY=0
        self.framecount=0
        try:
            conn= MySQLdb.connect(host="db4free.net",user="anderson",passwd="qwe123",db="integrationtool", charset="utf8",read_timeout = 2)
            cur0 = conn.cursor()
            cur0.execute("Select um.English_Name,um.Message_datetime,um.Message_Contents,up.PhotoPath from User_Messages as um inner join User_Photos as up on um.English_Name=up.English_Name order by um.Message_datetime")
            row0 = cur0.fetchall()
            if row0:
                for (English_Name,Message_datetime,Message_Contents,User_Photos) in row0:
                    self.tempr1=User_Photos  
                    self.tempr1=self.tempr1.replace("\/","\\")
                    self.tempr1=self.tempr1.decode('utf8')
                    self.tempr1=QtCore.QString(self.tempr1)
                    self.tname=English_Name
                    self.tempr2=Message_datetime
                    self.tempr3=Message_Contents
                    self.tempr3=self.tempr3.decode('hex').decode('utf8')
                    if self.tname!=self.authorEdit.text():
                        self.myphoto=QtGui.QPixmap(os.path.join(self.filedirpath,"Touxiang.jpg"))
                    elif self.tname==self.authorEdit.text():
                        self.myphoto=QtGui.QPixmap(self.tempr1)
                    self.addnewFrame()
            cur0.close()
            conn.close()
        except Exception,e:
            QtGui.QMessageBox.information(self, u'提交提示', str(e)+'\n'+u'读取的信息显示可能有误，请重新启动该软件或者将您的留言记录存放于同目录下的User_data.ini文件中，谢谢~',QtGui.QMessageBox.Ok)
            if len(self.cf1.sections())>=1:
                j=0
                for i in self.cf1.sections():
                    j+=1
                    self.English_Name=self.cf1.get("%s"%i, "English_Name")
                    self.Message_datetime=self.cf1.get("%s"%i, "Message_datetime")
                    self.Message_Contents=self.cf1.get("%s"%i, "Message_Contents")
                    self.tname=self.English_Name
                    self.tempr2=self.Message_datetime
                    self.tempr3=self.Message_Contents
                    self.tempr3=self.tempr3.decode('hex').decode('utf8')
                    self.user_messages_count=j
                    if self.tname!=self.authorEdit.text():
                        self.myphoto=QtGui.QPixmap(os.path.join(self.filedirpath,"Touxiang.jpg"))
                    elif self.tname==self.authorEdit.text():
                        self.myphoto=QtGui.QPixmap(self.tempr1)
                    self.addnewFrame()
    def WriteDatabase(self):
        QtGui.QMessageBox.information(self, u'提交提示', u'因为要连接远程数据库所以需要一些时间，请您关闭提示对话框后等待消息内容输入框内容被清空后再做其它操作，谢谢~',QtGui.QMessageBox.Ok)
        Textbase1=self.reviewEdit.toPlainText()
        Textbase=self.reviewEdit.toHtml() 
        Textbase=unicode(Textbase,'utf8','ignore') 
        if not Textbase1:
            Textbase="No Comments till now ! Please insert what you want to say !"
        temptime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.timeEdit.setText(temptime)
        try:
            conn= MySQLdb.connect(host="db4free.net",user="anderson",passwd="qwe123",db="integrationtool", charset="utf8",read_timeout = 2 )
            curw0 = conn.cursor()
            curw0.execute('''insert into User_Messages(English_Name,Message_datetime,Message_Contents) values(%s,%s,%s)''', (self.authorEdit.text(),self.timeEdit.text(),Textbase.encode('utf8').encode('hex')))
            conn.commit()
            try:
                try:
                    curw0.execute("Select English_Name,PhotoPath from User_Photos where English_Name=%s",self.authorEdit.text())
                except Exception,e:
                    QtGui.QMessageBox.information(self, u'提交提示', str(e)+'\n'+u'提交的信息显示可能有误，请重新填写后再次提交，谢谢~',QtGui.QMessageBox.Ok)
                curw0.execute("update User_Photos set PhotoPath= %s where English_Name=%s", (self.tempr1,self.authorEdit.text()))
            except Exception,e:
                QtGui.QMessageBox.information(self, u'提交提示', str(e)+'\n'+u'提交的信息显示可能有误，请重新填写后再次提交，谢谢~',QtGui.QMessageBox.Ok)
                curw0.execute('''insert into User_Photos(English_Name,PhotoPath) values(%s,%s)''', (self.authorEdit.text(),self.tempr1))
            curw0.close()
            conn.commit()
            conn.close()
        except Exception,e:
            QtGui.QMessageBox.information(self, u'提交提示', str(e)+'\n'+u'提交的信息显示可能有误，请重新填写后再次提交，谢谢~',QtGui.QMessageBox.Ok)
            if self.user_messages_count==0:
                self.user_messages_count=1
            else:
                self.user_messages_count+=1
            self.cf2.set("User_photo_data", "English_Name",self.authorEdit.text())
            self.cf2.set("User_photo_data", "PhotoPath",self.tempr1)
            self.cf2.write(open(os.path.join(self.filedirpath,"User_photo_data.ini"), "w"))
            self.cf1.add_section("User_Messages_data_%s_%d"%(self.authorEdit.text(),self.user_messages_count))
            self.cf1.set("User_Messages_data_%s_%d"%(self.authorEdit.text(),self.user_messages_count), "English_Name",self.authorEdit.text())
            self.cf1.set("User_Messages_data_%s_%d"%(self.authorEdit.text(),self.user_messages_count), "Message_datetime",self.timeEdit.text())
            self.cf1.set("User_Messages_data_%s_%d"%(self.authorEdit.text(),self.user_messages_count), "Message_Contents",Textbase.encode('utf8').encode('hex'))
            self.cf1.write(open(os.path.join(self.filedirpath,"User_data.ini"), "w"))
        self.reviewEdit.setText('')
        self.ReadDatabase()
