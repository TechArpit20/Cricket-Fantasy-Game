# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'evaluate.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3


class Ui_Form(object):

    def __init__(self):
        self.playerList=[]
        self.selectMatchList=[]
        self.selectTeamList=[]
        self.allpoints=[]
        self.playerAndTeam=[]
        self.bow=0
        self.economyRate=0
        self.score=0

    # Displaying the players in a Team
    def showTeam_Match(self):
        cricket=sqlite3.connect('fantasycricket.db')
        objcricket=cricket.cursor()
        objcricket.execute('Select Name from Teams')
        for i in objcricket.fetchall():
            if i[0] not in self.selectTeamList:
                self.Select_Team.addItem(i[0])
                self.selectTeamList.append(i[0])

        objcricket.execute('Select Matches from Match')
        for i in objcricket.fetchall():
            if i[0] not in self.selectMatchList:
                self.Select_Match.addItem(i[0])
                self.selectMatchList.append(i[0])


    # message box
    def messagebox(self,title,message):
        mess=QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.setIcon(QtWidgets.QMessageBox.Information)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setWeight(12)
        mess.setFont(font)
        mess.exec_()

    # calculating the Scores of the Team
    def calculateScore(self):
        self.players_list.clear()
        self.points_list.clear()
        self.playerList=[]
        self.allpoints=[]
        self.playerAndTeam=[]
        self.score=0
        cricket=sqlite3.connect('fantasycricket.db')
        objcricket=cricket.cursor()
        objcricket.execute('Select Players,Name from Teams') 
        for i in objcricket.fetchall():
            self.playerAndTeam.append(i)
        objcricket.execute('select * from Match')
        self.players_list.clear()
        self.points_list.clear()
        
        if "Match no."==self.Select_Match.currentText() and "Select Team" == self.Select_Team.currentText():
            self.messagebox('INFO','Please Select Team and Match')
        elif "Select Team" == self.Select_Team.currentText() and "Match no."!=self.Select_Match.currentText(): 
            self.messagebox('INFO','Please Select Team')
        elif "Match no."==self.Select_Match.currentText() and "Select Team"!=self.Select_Team.currentText():
            self.messagebox('INFO','Please Select Match')
        else:
            for i in objcricket.fetchall():
                for k in self.playerAndTeam:
                    self.points=0
                    self.economyRate=0
                    self.bow=0
                    if k[1] == self.Select_Team.currentText() and i[12]==self.Select_Match.currentText():
                        if i[0] == k[0]:
                            self.players_list.addItem(i[0])
                            if i[1]%2==0:
                                self.points+=(i[1]/2)
                                if i[1]>=50:
                                    self.points+=5
                                    if i[1]>=100:
                                        self.points+=10
                            else:
                                self.points+=(i[1]-1)/2
                                if i[1]>=50:
                                    self.points+=5
                                    if i[1]>=100:
                                        self.points+=10
                            if i[2] >80 and i[2] < 100:
                                self.points+=2
                                if i[2]>100:
                                    self.points+=4
                            self.points+=i[3]
                            self.points+=i[4]*2
                            if i[5]>0:
                                self.bow=i[5]/6
                                self.economyRate=i[7]/self.bow
                                if self.economyRate>3.5 and self.economyRate<=4.5:
                                    self.points+=4
                                elif self.economyRate>2 and self.economyRate<3.5:
                                    self.points+=7
                                elif self.economyRate<2:
                                    self.points+=10
                            self.points+=i[8]*10
                            if i[8]>=3:
                                self.points+=5
                            if i[8]>=5:
                                self.points+=10
                            self.points+=i[9]*10
                            self.points+=i[10]*10
                            self.points+=i[11]*10
                            self.points_list.addItem(str(self.points))
                            self.allpoints.append(self.points)
            for i in self.allpoints:
                self.score+=i
            self.total_points.setText(str(self.score))


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(552, 379)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r"icons/logo.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("background-color: rgb(201, 255, 175);\n""font: 75 9pt \"Arial\";")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.players_label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.players_label.setFont(font)
        self.players_label.setObjectName("players_label")
        self.horizontalLayout_4.addWidget(self.players_label)
        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.points_label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.points_label.setFont(font)
        self.points_label.setObjectName("points_label")
        self.horizontalLayout_2.addWidget(self.points_label)
        self.total_points = QtWidgets.QLabel(Form)
        self.total_points.setText("")
        self.total_points.setObjectName("total_points")
        self.horizontalLayout_2.addWidget(self.total_points)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.players_list = QtWidgets.QListWidget(Form)
        self.players_list.setStyleSheet("background-color:rgb(252, 207, 255)")
        self.players_list.setObjectName("players_list")
        self.horizontalLayout.addWidget(self.players_list)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.points_list = QtWidgets.QListWidget(Form)
        self.points_list.setStyleSheet("background-color:rgb(252, 207, 255)")
        self.points_list.setObjectName("points_list")
        self.horizontalLayout.addWidget(self.points_list)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.calculate = QtWidgets.QPushButton(Form)
        self.calculate.setIconSize(QtCore.QSize(14, 12))
        self.calculate.setAutoDefault(False)
        self.calculate.setFlat(False)
        self.calculate.setObjectName("calculate")
        self.horizontalLayout_6.addWidget(self.calculate)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.gridLayout.addLayout(self.horizontalLayout_6, 6, 0, 1, 2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        self.evl_headingLabel = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(9)
        self.evl_headingLabel.setFont(font)
        self.evl_headingLabel.setObjectName("evl_headingLabel")
        self.horizontalLayout_5.addWidget(self.evl_headingLabel)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem7)
        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 0, 1, 2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Select_Team = QtWidgets.QComboBox(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.Select_Team.setFont(font)
        self.Select_Team.setEditable(False)
        self.Select_Team.setObjectName("Select_Team")
        self.Select_Team.addItem("")
        self.Select_Team.setItemText(0, "Select Team")
        # self.Select_Team.addItem("")
        # self.Select_Team.addItem("")
        self.horizontalLayout_3.addWidget(self.Select_Team)
        spacerItem8 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.Select_Match = QtWidgets.QComboBox(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.Select_Match.setFont(font)
        self.Select_Match.setObjectName("Select_Match")
        self.Select_Match.addItem("")
        self.horizontalLayout_3.addWidget(self.Select_Match)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 2)

        self.showTeam_Match()
        self.calculate.clicked.connect(self.calculateScore)


        self.retranslateUi(Form)
        self.calculate.clicked.connect(self.points_label.show)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Cricket League 2020"))
        self.players_label.setText(_translate("Form", "Players"))
        self.points_label.setText(_translate("Form", "Points :"))
        self.calculate.setText(_translate("Form", "Calculate Score"))
        self.evl_headingLabel.setText(_translate("Form", "Evaluate the Performance of Your Fantasy Team"))
        # self.Select_Team.setItemText(1, _translate("Form", "LOL"))
        # self.Select_Team.setItemText(2, _translate("Form", "fd"))
        self.Select_Match.setItemText(0, _translate("Form", "Match no."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
