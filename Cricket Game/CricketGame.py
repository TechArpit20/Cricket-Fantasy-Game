from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QInputDialog
import sqlite3
import match

class Ui_MainWindow(object):
    def __init__(self):
        self.initial_counts=1000
        self.bow_count_value=0
        self.ar_count_value=0
        self.bat_count_value=0
        self.wk_count_value=0
        self.no_of_players=0
        self.final_team_name=''
        self.already_in_selected_player_list=set()
        self.already_in_selected_player_list_for_edit=set()
        self.new_click_list=set()
        self.final_team_list=[]
        self.in_wk_present=set()
        self.open_player_name=set()
        self.open_player_value=0
        self.already_team=set()
        self.all_team=set()
        self.total_count_value=0
   
    def showDialog(self,title,message):     # message box
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.exec()
 
    def func_for_new(self):
        import faulthandler
        faulthandler.enable()
        name, ok=QtWidgets.QInputDialog.getText(MainWindow, "Team Name", "Enter name of team:")
        if ok==True:
            if name!='':
                self.final_team_name=name.upper()
                self.team_name.setText(name.upper())
                self.bow_count_value=0
                self.ar_count_value=0
                self.total_count_value=0
                self.bat_count_value=0
                self.wk_count_value=0
                self.open_player_value=0
                self.initial_counts=1000
                self.used_count=0
                self.no_of_players=0
                self.bat_count.setText('0')
                self.total_count.setText('0')
                self.bow_count.setText('0')
                self.ar_count.setText('0')
                self.wk_count.setText('0')
                self.points_used_count.setText('0')
                self.points_avail_count.setText('1000')
                self.already_in_selected_player_list.clear()
                self.already_in_selected_player_list_for_edit.clear()
                self.new_click_list.clear()
                self.in_wk_present.clear()
                self.open_player_name.clear()
                self.already_team.clear()
                self.bat_radio.setEnabled(True)
                self.bow_radio.setEnabled(True)
                self.ar_radio.setEnabled(True)
                self.wk_radio.setEnabled(True)

                cricket=sqlite3.connect('fantasycricket.db')
                objcricket=cricket.cursor()
                objcricket.execute('Select Name from Teams')
                rows= objcricket.fetchall()
                for row in rows:
                    self.already_team.add(row[0])
                if self.final_team_name not in self.already_team:

                    self.players_list.clear()
                    self.selected_players.clear()
                    self.points_used_count.setText('0')
                    cricket=sqlite3.connect('fantasycricket.db')
                    objcricket=cricket.cursor()
                    objcricket.execute('Select Players from Stats')
                    rows= objcricket.fetchall()
                    for row in rows:
                        if row[0] not in self.new_click_list:
                            self.players_list.addItem(row[0])
                            self.new_click_list.add(row[0])
                else:
                    self.showDialog('Error','Team already present!!!\n Please enter another team name')
                    self.func_for_new()
            else:
                self.showDialog('Error','Please Enter the name of the team....\n')
                self.func_for_new()
        else:
            pass
        
    def func_for_open(self):
        self.teams=set()
        cricket=sqlite3.connect('fantasycricket.db')
        objcricket=cricket.cursor()
        objcricket.execute('Select Name from Teams')
        rows= objcricket.fetchall()
        for row in rows:
            self.teams.add(row[0])

        team, ok=QtWidgets.QInputDialog.getItem(MainWindow,"Open","Choose A Team",self.teams,0,False)
        if ok==True:
            self.showDialog('Message','Successfully opened!!!\n You can also edit your team')
            self.selected_players.clear()
            self.players_list.clear()
            self.bow_count_value=0
            self.ar_count_value=0
            self.total_count_value=0
            self.bat_count_value=0
            self.wk_count_value=0
            self.open_player_value=0
            self.no_of_players=0
            self.total_count.setText('0')
            self.bat_count.setText('0')
            self.bow_count.setText('0')
            self.ar_count.setText('0')
            self.wk_count.setText('0')
            self.points_used_count.setText('0')
            self.points_avail_count.setText('0')
            self.already_in_selected_player_list.clear()
            self.already_in_selected_player_list_for_edit.clear()
            self.new_click_list.clear()
            self.in_wk_present.clear()
            self.open_player_name.clear()         
            self.team_name.setText(f'{team}')
            objcricket.execute(f'Select Players from Teams where Name=="{team}" ')
            rows=objcricket.fetchall()
            for row in rows:
                self.selected_players.addItem(row[0])
                self.already_in_selected_player_list_for_edit.add(row[0])
                self.open_player_name.add(row[0])
            for names in self.open_player_name:
                objcricket.execute(f'Select Players,ctg,value from Stats where Players=="{names}" ')
                rows=objcricket.fetchall()
                for row in rows:
                    self.open_player_value+=row[2]
                self.category_for_count_incr(row[1])
                self.points_used_count.setText(str(self.open_player_value))
                self.initial_counts=1000-self.open_player_value
                self.points_avail_count.setText(str(self.initial_counts))
                self.bat_radio.setEnabled(True)
                self.bow_radio.setEnabled(True)
                self.ar_radio.setEnabled(True)
                self.wk_radio.setEnabled(True)
        else:
            pass

    def open_evaluate(self):
        self.window=QtWidgets.QWidget()
        self.ui= match.Ui_Form()
        self.ui.setupUi(self.window)
        self.window.show()

    def func_for_one_wk(self):      ##selecting the wicket players
        cricket=sqlite3.connect('fantasycricket.db')
        objcricket=cricket.cursor()
        objcricket.execute('Select Players from Stats where ctg=="WK" ')
        rows= objcricket.fetchall()
        for row in rows:
            self.in_wk_present.append(row[0])


    def player_type_selected(self,value):
        self.players_list.clear()
        x=value
        if x=='BAT':
            a= 'bat_radio'
        elif x=='WK':
            a= 'wk_radio'
        elif x=='BWL':
            a= 'bow_radio'
        elif x=='AR':
            a= 'ar_radio'
        lists=['bat_radio','bow_radio','ar_radio','wk_radio']
        category=['BAT','BWL','AR','WK']
        for index,player_type in enumerate(lists):
            if player_type==a:
                cricket=sqlite3.connect('fantasycricket.db')
                objcricket=cricket.cursor()
                objcricket.execute(f'Select Players,ctg from Stats where ctg=="{category[index]}"')
                rows= objcricket.fetchall()
                for row in rows:
                    if row[0] not in self.already_in_selected_player_list and row[0] not in self.already_in_selected_player_list_for_edit:
                        self.players_list.addItem(row[0])

    def remove_player(self,item):           # Removing from players list and adding to selected list
        self.players_list.takeItem(self.players_list.row(item)) 
        cricket=sqlite3.connect('fantasycricket.db')
        objcricket=cricket.cursor()
        objcricket.execute(f'Select Players,value,ctg from Stats where Players=="{item.text()}"')
        rows=objcricket.fetchone()
        name,score,category=rows
 
        if category!='WK':
            if item.text() not in self.already_in_selected_player_list or item.text() not in self.already_in_selected_player_list_for_edit:
                if self.initial_counts>=score:
                    self.selected_players.addItem(item.text())
                    self.already_in_selected_player_list.add(item.text())
                    self.already_in_selected_player_list_for_edit.add(item.text())
                    self.initial_counts-= score
                    self.points_avail_count.setText(str(self.initial_counts))
                    self.used_count+= score
                    self.points_used_count.setText(str(self.used_count))
                    self.category_for_count_incr(category)
                else:
                    self.showDialog('Limit Exceeded','Sorry!! You have exceeded your limit')
        elif category=='WK':
            if item.text() not in self.already_in_selected_player_list or item.text() not in self.already_in_selected_player_list_for_edit:
                if self.wk_count_value<1:
                    if self.initial_counts>=score:
                        self.selected_players.addItem(item.text())
                        self.already_in_selected_player_list.add(item.text())
                        self.already_in_selected_player_list_for_edit.add(item.text())
                        self.initial_counts-= score
                        self.points_avail_count.setText(f'{self.initial_counts}')
                        self.used_count+= score
                        self.points_used_count.setText(f'{self.used_count}')
                        self.category_for_count_incr(category)
                    else:
                        self.showDialog('Limit Exceeded','Sorry!! You have exceeded your limit')
                else:
                    self.showDialog('Error','Sorry you cannot add more than one wicket keeper!!!')
            
    def remove_selected_player(self,item):          # Removing from selected players list and addding to players list
        self.initial_counts=int(self.points_avail_count.text())
        self.used_count=int(self.points_used_count.text())
        self.selected_players.takeItem(self.selected_players.row(item))
        if item.text() in self.already_in_selected_player_list or item.text() in self.already_in_selected_player_list_for_edit:
            self.already_in_selected_player_list.discard(item.text())
            self.already_in_selected_player_list_for_edit.discard(item.text())
        
        cricket=sqlite3.connect('fantasycricket.db')
        objcricket=cricket.cursor()
        objcricket.execute(f'Select Players,value,ctg from Stats where Players=="{item.text()}"')
        rows=objcricket.fetchone()
        name,score,category=rows
        self.used_count-= score
        self.points_used_count.setText(f'{self.used_count}')
        self.initial_counts+= score
        self.points_avail_count.setText(f'{self.initial_counts}')
        self.category_for_count_decr(category)

    def category_for_count_incr(self,cat):
        if cat=='BAT':
            self.bat_count_value+=1
            self.bat_count.setText(f'{self.bat_count_value}')
            self.total_count_value+=1
            self.total_count.setText(f'{self.total_count_value}')
        elif cat=='BWL':
            self.bow_count_value+=1
            self.bow_count.setText(f'{self.bow_count_value}')
            self.total_count_value+=1
            self.total_count.setText(f'{self.total_count_value}')
        elif cat=='AR':
            self.ar_count_value+=1
            self.ar_count.setText(f'{self.ar_count_value}')
            self.total_count_value+=1
            self.total_count.setText(f'{self.total_count_value}')
        elif cat=='WK':
            self.wk_count_value+=1
            self.wk_count.setText(f'{self.wk_count_value}')
            self.total_count_value+=1
            self.total_count.setText(f'{self.total_count_value}')
        self.no_of_players+=1
  
    def category_for_count_decr(self,cat):
        if cat=='BAT':
            self.bat_count_value-=1
            self.bat_count.setText(f'{self.bat_count_value}')
            self.total_count_value-=1
            self.total_count.setText(f'{self.total_count_value}')
        elif cat=='BWL':
            self.bow_count_value-=1
            self.bow_count.setText(f'{self.bow_count_value}')
            self.total_count_value-=1
            self.total_count.setText(f'{self.total_count_value}')
        elif cat=='AR':
            self.ar_count_value-=1
            self.ar_count.setText(f'{self.ar_count_value}')
            self.total_count_value-=1
            self.total_count.setText(f'{self.total_count_value}')
        elif cat=='WK':
            self.wk_count_value-=1
            self.wk_count.setText(f'{self.wk_count_value}')
            self.total_count_value-=1
            self.total_count.setText(f'{self.total_count_value}')
        self.no_of_players-=1

    def func_for_save(self):
        if self.no_of_players>=11:
            cricket=sqlite3.connect('fantasycricket.db')
            objcricket=cricket.cursor()
            objcricket.execute('Select Name from Teams')
            rows= objcricket.fetchall()
            for row in rows:
                self.all_team.add(row[0])
            self.list_for_save_team=[]    
            self.list_for_save_team.append(self.team_name.text())
            if self.team_name.text() not in self.all_team:
                if self.selected_players.count()!=0:
                    for names in self.already_in_selected_player_list:
                        cricket=sqlite3.connect('fantasycricket.db')
                        objcricket=cricket.cursor()
                        objcricket.execute(f'Select Players,value from Stats where Players=="{names}"')
                        rows=objcricket.fetchone()
                        self.final_team_list.append(rows)
                    for one_data in self.final_team_list:
                        name,value=one_data
                        objcricket.execute(f'Insert into Teams Values("{name}","{self.final_team_name}","{value}");')
                        cricket.commit()
                    self.showDialog('Success','You have sucessfully created your team...')
                    self.selected_players.clear()
                    self.players_list.clear()
                    self.total_count.setText('0')
                    self.bat_count.setText('0')
                    self.bow_count.setText('0')
                    self.ar_count.setText('0')
                    self.wk_count.setText('0')
                    self.points_avail_count.setText('0')
                    self.points_used_count.setText('0')
                    self.team_name.setText('No team selected yet')
                    self.already_in_selected_player_list.clear()
                else:
                    self.showDialog('Error','Please Insert players name to add the data')
            else:
                self.store, ok=QtWidgets.QInputDialog.getItem(MainWindow,"IMPORTANT","The team already exists!!!\n This will delete your team previous data:",self.list_for_save_team,0,False)
                if ok==True:
                    if self.selected_players.count()!=0:
                        objcricket.execute(f'Delete from Teams where Name=="{self.team_name.text()}"')
                        cricket.commit()
                        for names in self.already_in_selected_player_list_for_edit:
                            objcricket.execute(f'Select Players,value from Stats where Players=="{names}"')
                            rows=objcricket.fetchone()
                            self.final_team_list.append(rows)
                        for one_data in self.final_team_list:
                            name,value=one_data
                            objcricket.execute(f'Insert into Teams Values("{name}","{self.team_name.text()}","{value}");')
                            cricket.commit()
                        self.showDialog('Success','You have sucessfully edited your team...')
                        self.selected_players.clear()
                        self.players_list.clear()
                        self.total_count.setText('0')
                        self.bat_count.setText('0')
                        self.bow_count.setText('0')
                        self.ar_count.setText('0')
                        self.wk_count.setText('0')
                        self.points_avail_count.setText('0')
                        self.points_used_count.setText('0')
                        self.team_name.setText('No team selected yet')
                        self.already_in_selected_player_list.clear()
                        self.already_in_selected_player_list_for_edit.clear()
                        self.list_for_save_team.clear()
                    else:
                        self.showDialog('Error','Please Insert players name to add the data')
                else:
                    pass
        else:
            self.showDialog('ERROR','Please add atleast 11 players!!!')    

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 450)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r"icons/logo.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(255, 235, 235)")
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 8, 7, 1, 2)
        self.bat_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calisto MT")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.bat_label.setFont(font)
        self.bat_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.bat_label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.bat_label.setObjectName("bat_label")
        self.gridLayout.addWidget(self.bat_label, 2, 11, 1, 1)
        self.bow_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calisto MT")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.bow_label.setFont(font)
        self.bow_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.bow_label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.bow_label.setObjectName("bow_label")
        self.gridLayout.addWidget(self.bow_label, 2, 0, 1, 1)
        self.bow_count = QtWidgets.QLabel(self.centralwidget)
        self.bow_count.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.bow_count.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bow_count.setText("")
        self.bow_count.setObjectName("bow_count")
        self.gridLayout.addWidget(self.bow_count, 2, 1, 1, 1)
        self.points_used_count = QtWidgets.QLabel(self.centralwidget)
        self.points_used_count.setFrameShape(QtWidgets.QFrame.Box)
        self.points_used_count.setFrameShadow(QtWidgets.QFrame.Raised)
        self.points_used_count.setText("")
        self.points_used_count.setObjectName("points_used_count")
        self.gridLayout.addWidget(self.points_used_count, 6, 14, 1, 3)
        self.bat_count = QtWidgets.QLabel(self.centralwidget)
        self.bat_count.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.bat_count.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bat_count.setText("")
        self.bat_count.setObjectName("bat_count")
        self.gridLayout.addWidget(self.bat_count, 2, 12, 1, 1)
        self.your_select = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.your_select.setFont(font)
        self.your_select.setObjectName("your_select")
        self.gridLayout.addWidget(self.your_select, 0, 0, 1, 3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        ##########################
        # self.gridLayout.addWidget(self.selected_players, 2, 12, 2, 1)
        # self.total_count = QtWidgets.QLabel(self.centralwidget)
        # self.total_count.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.total_count.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.total_count.setText("")
        # self.total_count.setObjectName("wk_count")
        ##################################
        self.team_name_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.team_name_label.setFont(font)
        self.team_name_label.setObjectName("team_name_label")
        self.horizontalLayout_2.addWidget(self.team_name_label)
        self.team_name = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.team_name.setFont(font)
        self.team_name.setObjectName("team_name")
        self.horizontalLayout_2.addWidget(self.team_name)
        self.gridLayout.addLayout(self.horizontalLayout_2, 7, 11, 1, 6)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 8, 5, 1, 1)
        self.selected_players = QtWidgets.QListWidget(self.centralwidget)
        self.selected_players.setStyleSheet("font: 75 9pt \"Arial\";")
        self.selected_players.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.selected_players.setObjectName("selected_players")
        self.gridLayout.addWidget(self.selected_players, 8, 11, 1, 6)
        self.wk_count = QtWidgets.QLabel(self.centralwidget)
        self.wk_count.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.wk_count.setFrameShadow(QtWidgets.QFrame.Raised)
        self.wk_count.setText("")
        self.wk_count.setObjectName("wk_count")
        self.gridLayout.addWidget(self.wk_count, 2, 16, 1, 1)
        self.wk_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calisto MT")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.wk_label.setFont(font)
        self.wk_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.wk_label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.wk_label.setObjectName("wk_label")
        self.gridLayout.addWidget(self.wk_label, 2, 14, 1, 2)
        self.Direction = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.Direction.setFont(font)
        self.Direction.setObjectName("Direction")
        self.gridLayout.addWidget(self.Direction, 8, 6, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.wk_radio = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.wk_radio.setFont(font)
        self.wk_radio.setObjectName("wk_radio")
        self.horizontalLayout.addWidget(self.wk_radio)
        self.bat_radio = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.bat_radio.setFont(font)
        self.bat_radio.setObjectName("bat_radio")
        self.horizontalLayout.addWidget(self.bat_radio)
        self.bow_radio = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.bow_radio.setFont(font)
        self.bow_radio.setObjectName("bow_radio")
        self.horizontalLayout.addWidget(self.bow_radio)
        self.ar_radio = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.ar_radio.setFont(font)
        self.ar_radio.setObjectName("ar_radio")
        self.horizontalLayout.addWidget(self.ar_radio)
        self.gridLayout.addLayout(self.horizontalLayout, 7, 0, 1, 5)
        self.points_used_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.points_used_label.setFont(font)
        self.points_used_label.setObjectName("points_used_label")
        self.gridLayout.addWidget(self.points_used_label, 6, 11, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 2, 13, 1, 1)
        self.players_list = QtWidgets.QListWidget(self.centralwidget)
        self.players_list.setStyleSheet("font: 75 9pt \"Arial\";\n""")
        self.players_list.setObjectName("players_list")
        self.gridLayout.addWidget(self.players_list, 8, 0, 1, 5)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 8, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 5, 0, 1, 16)
        self.ar_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calisto MT")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.ar_label.setFont(font)
        self.ar_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ar_label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.ar_label.setObjectName("ar_label")
        self.gridLayout.addWidget(self.ar_label, 2, 3, 1, 2)
        self.points_avail_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.points_avail_label.setFont(font)
        self.points_avail_label.setObjectName("points_avail_label")
        self.gridLayout.addWidget(self.points_avail_label, 6, 0, 1, 2)
        self.points_avail_count = QtWidgets.QLabel(self.centralwidget)
        self.points_avail_count.setFrameShape(QtWidgets.QFrame.Box)
        self.points_avail_count.setFrameShadow(QtWidgets.QFrame.Raised)
        self.points_avail_count.setText("")
        self.points_avail_count.setObjectName("points_avail_count")
        self.gridLayout.addWidget(self.points_avail_count, 6, 2, 1, 3)
        self.ar_count = QtWidgets.QLabel(self.centralwidget)
        self.ar_count.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ar_count.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ar_count.setText("")
        self.ar_count.setObjectName("ar_count")
        self.gridLayout.addWidget(self.ar_count, 2, 5, 1, 2)
        #################################
        self.total_count = QtWidgets.QLabel(self.centralwidget)
        self.total_count.setObjectName("label")
        self.gridLayout.addWidget(self.total_count, 0, 1, 1, 1)
        ##################################
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 586, 21))
        self.menubar.setObjectName("menubar")
        self.menuManage_Team = QtWidgets.QMenu(self.menubar)
        self.menuManage_Team.setObjectName("menuManage_Team")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_new = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(r"icons/new.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.action_new.setIcon(icon1)
        self.action_new.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.action_new.setShortcutVisibleInContextMenu(True)
        self.action_new.setObjectName("action_new")
        self.action_open = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(r"icons/open.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.action_open.setIcon(icon2)
        self.action_open.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.action_open.setObjectName("action_open")
        self.action_save = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(r"icons/save.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.action_save.setIcon(icon3)
        self.action_save.setObjectName("action_save")
        self.action_evaluate = QtWidgets.QAction(MainWindow)
        icon4=QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(r"icons/evaluate.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.action_evaluate.setIcon(icon4)
        self.action_evaluate.setObjectName("action_evaluate")
        self.action_quit = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(r"icons/exit.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.action_quit.setIcon(icon5)
        self.action_quit.setObjectName("action_quit")
        self.menuManage_Team.addAction(self.action_new)
        self.menuManage_Team.addAction(self.action_open)
        self.menuManage_Team.addAction(self.action_save)
        self.menuManage_Team.addAction(self.action_evaluate)
        self.menuManage_Team.addAction(self.action_quit)
        self.menubar.addAction(self.menuManage_Team.menuAction())
        self.points_avail_count.setText('1000')
        self.initial_counts=int(self.points_avail_count.text())
        self.points_used_count.setText('0')
        self.used_count= int(self.points_used_count.text())
        self.bat_radio.setEnabled(False)
        self.bow_radio.setEnabled(False)
        self.ar_radio.setEnabled(False)
        self.wk_radio.setEnabled(False)             
        self.players_list.itemDoubleClicked.connect(self.remove_player)
        self.selected_players.itemDoubleClicked.connect(self.remove_selected_player)
        self.bat_radio.clicked.connect(lambda : self.player_type_selected('BAT'))
        self.wk_radio.clicked.connect(lambda : self.player_type_selected('WK'))
        self.bow_radio.clicked.connect(lambda : self.player_type_selected('BWL'))
        self.ar_radio.clicked.connect(lambda : self.player_type_selected('AR'))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.wk_radio, self.bat_radio)
        MainWindow.setTabOrder(self.bat_radio, self.ar_radio)
        MainWindow.setTabOrder(self.ar_radio, self.bow_radio)

        self.action_new.triggered.connect(self.func_for_new)
        self.action_new.setShortcut('Ctrl+N')
        self.action_open.triggered.connect(self.func_for_open)
        self.action_open.setShortcut('Ctrl+O')
        self.action_evaluate.triggered.connect(self.open_evaluate)
        self.action_evaluate.setShortcut('Ctrl+E')
        self.action_save.triggered.connect(self.func_for_save)
        self.action_save.setShortcut('Ctrl+S')
        self.action_quit.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.action_quit.setShortcut('Ctrl+Q')
      
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cricket Fantasy Game"))
        self.bat_label.setText(_translate("MainWindow", "Batsman(BAT)"))
        self.bow_label.setText(_translate("MainWindow", "Bowlers(BOW)"))
        self.your_select.setText(_translate("MainWindow", "Total Selected:"))
        self.team_name_label.setText(_translate("MainWindow", "Team Name :"))
        self.team_name.setText(_translate("MainWindow", "No Team selected yet"))
        self.wk_label.setText(_translate("MainWindow", "Wicket-keeper(WK)"))
        self.Direction.setText(_translate("MainWindow", ">"))
        self.wk_radio.setText(_translate("MainWindow", "WK"))
        self.bat_radio.setText(_translate("MainWindow", "BAT"))
        self.bow_radio.setText(_translate("MainWindow", "BOW"))
        self.ar_radio.setText(_translate("MainWindow", "AR"))
        self.points_used_label.setText(_translate("MainWindow", "Points Used :"))
        self.ar_label.setText(_translate("MainWindow", "AllRounders(AR)"))
        self.points_avail_label.setText(_translate("MainWindow", "Points Available :"))
        self.menuManage_Team.setTitle(_translate("MainWindow", "Manage Team"))
        self.action_new.setText(_translate("MainWindow", "New Team"))
        self.action_new.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.action_open.setText(_translate("MainWindow", "Open Team"))
        self.action_open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_save.setText(_translate("MainWindow", "Save Team"))
        self.action_save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_evaluate.setText(_translate("MainWindow", "Evaluate Team"))
        self.action_evaluate.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.action_quit.setText(_translate("MainWindow", "Quit"))
        self.action_quit.setShortcut(_translate("MainWindow", "Ctrl+Q"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
