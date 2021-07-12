from numpy import save, true_divide
from utils.util import get_sub_folder_path
from utils.converter import convert
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from DB import DB
from UI import Ui_Form
import sys
import threading
from YouTube_ff import YouTube_Search
from YouTube_ff import Downloader
import time
import os
import pygame
from pygame import mixer
from pygame import time as t
import random
pygame.init()

class Youtube_downlader(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        ## making db class
        self.database = DB()
        ### setting default widget
        self.ui.stackedWidget.setCurrentWidget(self.ui.home_page)
    
        ###################Booleans###########################
        self.youtube_searchable = True
        self.show_listing = False
        self.downloaded = False
        self.downloads_showable = True
        self.search_in_active = False
        self.mp3_joinable = True
        ######################################################
        ##################Connectors########################
        self.ui.quitButton.clicked.connect(self.quit)
        self.ui.home_icon.clicked.connect(self.home)
        self.ui.downloads_icon.clicked.connect(self.downloads)
        self.ui.mp3s_icon.clicked.connect(self.mp3s)
        self.ui.settings_icon.clicked.connect(self.settings)
        self.ui.home_download_button.clicked.connect(self.download_video)
        self.ui.settings_save_button.clicked.connect(self.save_data)
        self.ui.settings_save_browse_button.clicked.connect(lambda:self.takeFolderPath(status=0))
        self.ui.settings_mp3_browse_button.clicked.connect(lambda:self.takeFolderPath(status=1))
        self.ui.mp3_save_location_browse_button.clicked.connect(lambda:self.takeFolderPath(status=2))
        self.ui.mp3_file_location_browse_button.clicked.connect(self.takeFileLocation)
        self.ui.downloads_open_button.clicked.connect(self.open_respective_file)
        self.ui.mp3_open_button.clicked.connect(self.open_mp3)
        self.ui.mp3_play_button.clicked.connect(self.play_mp3)
        self.ui.convert_button.clicked.connect(self.converter2)
        ######################################################
        self.ui.progressBar.setValue(0)
        #########################Initilizing data base##########################################
        #Settings
        self.settings_data = self.database.settings.load_data()
        
        if self.settings_data!=[]:
            self.ui.settings_save_location_line_edit.setText(self.settings_data[0])
            
            if self.settings_data[1] == "true":
                self.ui.settings_check_box.setChecked(True)
            else:
                self.ui.settings_check_box.setChecked(False)
            self.ui.settings_save_location_mp3_line_edit.setText(self.settings_data[2])
            self.ui.mp3_save_location_line_edit.setText(self.settings_data[2])
            if self.settings_data[-1]=="Best":
                self.ui.settigns_combobox.setCurrentIndex(1)
            elif self.settings_data[-1]=="Worst":
                self.ui.settigns_combobox.setCurrentIndex(2)
        ## Downloads
        self.downloads_data = self.database.downloads_mp4.load_data()
        if self.downloads_data!="":
            for i in self.downloads_data:
                self.ui.downloads_downloads_list_widget.addItem(i.split("/")[-1])
        ### MP3s
        self.mp3_data = self.database.downloads_mp3.load_data()
        for i in self.mp3_data:
                self.ui.mp3s_list_widget.addItem(i.split("/")[-1])
        ########################Threads#######################
        
        self.search_bar_thread = threading.Thread(target=self.get_search_bar_data)
        self.search_bar_thread.start()

        self.downloads_bar_thread = threading.Thread(target=self.get_download_bar_data)
        self.downloads_bar_thread.start()
        
        ######################################################
        self.videos = ""
    def open_mp3(self):
        data = self.database.downloads_mp3.load_data()
        if data==[]:
            return
        index = self.ui.mp3s_list_widget.currentRow()
        try:
            os.startfile(data[index]+".mp3")
        except:
            from utils.util import rm
            file = rm(data[index].split("/")[-1], get_sub_folder_path(data[index]))
            if file!=None:
                os.startfile(file)
            else:
                self.showdialog(title="File not found", text="File missing", informative_text="File has been deleted or moved to some other location", detailed_text=f'File Missing : {data[index]+".mp3"}')
                files = os.listdir(self.ui.settings_save_location_mp3_line_edit.text())
                current_data = self.database.downloads_mp3.load_data()
                new_data = []
                for i in files:
                    if i.endswith(".mp3"):
                        if os.path.join(self.ui.settings_save_location_mp3_line_edit.text(), (i.replace(".mp3", ""))).replace("\\", "/") in current_data:
                            
                            new_data.append(os.path.join(self.ui.settings_save_location_mp3_line_edit.text(),(i.replace(".mp3", ""))).replace("\\", "/"))

                self.database.downloads_mp3.save_data(new_data)
                self.ui.mp3s_list_widget.clear()
                current_data_refresh = self.database.downloads_mp3.load_data()
                for i in current_data_refresh:
                    self.ui.mp3s_list_widget.addItem(i.split("/")[-1])
    def play_mp3(self):
        isPlaying=False
        from utils.util import rm
        data = self.database.downloads_mp3.load_data()
        if data==[]:
            return
        index = self.ui.mp3s_list_widget.currentRow()
        if os.path.exists(data[index]+".mp3") and self.ui.mp3_play_button.text() == "Play":
            mixer.music.load(data[index]+".mp3")
            mixer.music.play(-1)
            self.ui.mp3_play_button.setText("Stop")

        elif self.ui.mp3_play_button.text() == "Stop":
            mixer.music.stop()
            self.ui.mp3_play_button.setText("Play")
            isPlaying = True

        else:
            file = rm(data[index].split("/")[-1], get_sub_folder_path(data[index]))
            if file!=None:
                if not isPlaying:
                    mixer.music.load(file)
                    mixer.music.play(-1)
                    isPlaying=False
                    self.ui.mp3_play_button.setText("Pause")
                else:
                    mixer.music.unpause()
                    self.ui.mp3_play_button.setText("Play")
            if file!=None and self.ui.mp3_play_button.text() == "Pause":
                isPlaying = True
                mixer.music.pause()
                self.ui.mp3_play_button.setText("Play")
            else:
                self.showdialog(title="File not found", text="File missing", informative_text="File has been deleted or moved to some other location", detailed_text=f'File Missing : {data[index]+".mp3"}')
                files = os.listdir(self.ui.settings_save_location_mp3_line_edit.text())
                current_data = self.database.downloads_mp3.load_data()
                new_data = []
                for i in files:
                    if i.endswith(".mp3"):
                        if os.path.join(self.ui.settings_save_location_mp3_line_edit.text(), (i.replace(".mp3", ""))).replace("\\", "/") in current_data:
                            new_data.append(os.path.join(self.ui.settings_save_location_mp3_line_edit.text(),(i.replace(".mp3", ""))).replace("\\", "/"))

                self.database.downloads_mp3.save_data(new_data)
                self.ui.mp3s_list_widget.clear()
                current_data_refresh = self.database.downloads_mp3.load_data()
                for i in current_data_refresh:
                    self.ui.mp3s_list_widget.addItem(i.split("/")[-1])
    def get_search_bar_data(self):
        previous_text = ""
        while self.youtube_searchable:
            self.search_text = self.ui.home_search_line_edit.text()
            if self.search_text!="":
                self.videos = YouTube_Search(self.search_text).links.get_videos_all()
                if self.search_text.startswith("http"):
                    if self.ui.home_search_line_edit.text() != previous_text:
                        self.ui.home_list_edit.clear()
                        self.ui.home_list_edit.addItem(Downloader(self.search_text).title)
                        previous_text=self.search_text
                        self.link=self.search_text
                elif self.ui.home_search_line_edit.text() != previous_text:
                    previous_text=self.search_text
                    
                    for i in self.videos:
                        if self.ui.home_search_line_edit.text() != previous_text:
                            self.ui.home_list_edit.clear()
                            break
                        else:
                            if not self.show_listing:
                                self.ui.home_list_edit.addItem(i.title)
                            else:
                                break
                         
                

                        
    def home(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.home_page)
    def downloads(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.downloads_page)
    def mp3s(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.mp3_page)
    def settings(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.settings_page)
        
    def download_video(self):
        index = self.ui.home_list_edit.currentRow()
        
        if self.search_text.startswith("http"):
            self.confirmed_link = self.search_text
            download_thread = threading.Thread(target=self.download_vid, args=(self.confirmed_link,))
            download_thread.start()
        else:
            if self.videos:
                self.confirmed_link = self.videos[index].link_ff
                download_thread = threading.Thread(target=self.download_vid, args=(self.confirmed_link,))
                
                download_thread.start()
                download_thread.join()
                if self.downloaded:
                    QTimer.singleShot(1000, lambda:self.change_download_button(status=0))
                    QTimer.singleShot(5000, lambda:self.change_download_button(status=1))
                    self.downloaded=False
                    if self.ui.settings_check_box.isChecked():
                        data = self.database.downloads_mp4.load_data()[-1]
                        time.sleep(2)
                        convert_thread = threading.Thread(target=self.converter, args=(data+".mp4", self.ui.settings_save_location_mp3_line_edit.text() if self.ui.settings_save_location_mp3_line_edit.text()!="" else os.getcwd()))
                        convert_thread.start()

         
    def converter2(self):
        file_loc = self.ui.mp3_file_location_line_edit.text().split(",")
        save_loc = self.ui.mp3_save_location_line_edit.text()
        file_loc.append(save_loc)
        self.database.converting_data.save_data(file_loc)
        self.ui.convert_button.setText("Converting...")
        self.ui.mp3_file_location_browse_button.setDisabled(True)
        self.ui.mp3_save_location_browse_button.setDisabled(True)
        self.ui.convert_button.setDisabled(True)
        self.ui.progressBar.setMaximum(100)
        os.startfile("mp3writer.pyw")
        self.thread_mp3 = threading.Thread(target=self.convert_check, args=(file_loc,) )
        self.thread_mp3.start()
        
    def convert_check(self, file_loc):
        time.sleep(2)
        value = 0
        val = 0
        save_loc = file_loc.pop()
        file_loc_mp3 = []
        file_loc_files = []
        greater = random.randint(40, 80)
        pluser = 1
        while True:
            if self.database.check_in.check()[0] == "wait" and self.mp3_joinable: 
                if value<=greater:
                    self.ui.progressBar.setValue(value)
                    value+=pluser
                    val+=pluser
                if value==greater:
                    greater=random.randint(92, 99)
                    pluser=0.1
                    val = 0
                    
                continue
            if self.database.check_in.check()[0] == "true" and self.mp3_joinable:
                for i in file_loc:
                    file_loc_mp3.append(os.path.join(save_loc, i.replace("\\", "/").split("/")[-1].replace(".mp4", "").split("/")[-1]).replace("\\", '/'))
                    file_loc_files.append(i.replace("\\", "/").split("/")[-1].replace(".mp4", "").split("/")[-1])
                current_data = self.database.downloads_mp3.load_data()
                current_data.extend(file_loc_mp3)
                self.database.downloads_mp3.save_data(current_data)
                self.ui.mp3s_list_widget.addItems(file_loc_files)
                while value<100:
                    value = round(value)
                    if round(value) == 99:
                       self.ui.progressBar.setValue(100)
                       break
                    self.ui.progressBar.setValue(value)
                    time.sleep(0.1)
                    value+=1

                self.ui.convert_button.setText("Converted")
                time.sleep(3)
                self.ui.convert_button.setText("Convert")
                self.ui.mp3_file_location_browse_button.setEnabled(True)
                self.ui.mp3_save_location_browse_button.setEnabled(True)
                self.ui.convert_button.setEnabled(True)

                break

            elif not self.mp3_joinable:
                break

    def converter(self, file_loc, save_loc):
        from utils.converter import convert
        try:
            convert(file_loc, save_loc)
        except Exception:
            from utils.util import get_ex_file
            file_loc = get_ex_file((file_loc.replace("\\", "/").split("/")[-1].replace(".mp4", "")), (file_loc[:file_loc.replace("\\", "/").rindex("/")]))
            convert(file_loc, save_loc)
        self.change_download_button(status=2)
        time.sleep(5)
        self.change_download_button(status=1)
        current_data = self.database.downloads_mp3.load_data()
        current_data.append(os.path.join(save_loc.replace("\\", "/"),file_loc.replace("\\", "/").split("/")[-1].replace(".mp4", "")).replace("\\","/"))
        self.database.downloads_mp3.save_data(current_data)
        self.ui.mp3s_list_widget.addItem(file_loc.replace("\\", "/").split("/")[-1].replace(".mp4", ''))
    
    

    def showdialog(self, title, text, informative_text,type=QMessageBox.Critical, detailed_text="", buttons=QMessageBox.Ok):
        msg = QMessageBox(self)
        msg.setIcon(type)
        msg.setText(text)
        msg.setInformativeText(informative_text)
        msg.setWindowTitle(title)
        if detailed_text!="":
            msg.setDetailedText(detailed_text)
        msg.setStandardButtons(buttons)
        retval = msg.exec_()
    def open_respective_file(self):
        if not self.search_in_active:
            data = self.database.downloads_mp4.load_data()
            if data==[]:
                return
            index = self.ui.downloads_downloads_list_widget.currentRow()
            try:
                os.startfile(data[index]+".mp4")
            except FileNotFoundError:
                from utils.util import rm
                nice_path = rm(data[index].split("/")[-1],data[index][:(data[index].rindex("/"))])
                if nice_path!=None:
                    os.startfile(nice_path)
                else:
                    self.showdialog(title="File not found", text="File missing", informative_text="File has been deleted or moved to some other location", detailed_text=f'File Missing : {data[index]+".mp4"}')
                    files = os.listdir(self.ui.settings_save_location_line_edit.text())
                    current_data = self.database.downloads_mp4.load_data()
                    new_data = []
                    for i in files:
                        if i.endswith(".mp4"):
                            if os.path.join(self.ui.settings_save_location_line_edit.text(), (i.replace(".mp4", ""))).replace("\\", "/") in current_data:
                                
                                new_data.append(os.path.join(self.ui.settings_save_location_line_edit.text(),(i.replace(".mp4", ""))).replace("\\", "/"))

                    self.database.downloads_mp4.save_data(new_data)
                    self.ui.downloads_downloads_list_widget.clear()
                    current_data_refresh = self.database.downloads_mp4.load_data()
                    for i in current_data_refresh:
                        self.ui.downloads_downloads_list_widget.addItem(i.split("/")[-1])

            except Exception:
                pass
        else:
            data_base = self.database.downloads_mp4.load_data()
            if data_base==[]:
                return
            songs_name = self._getName(data_base)
            file = self.ui.downloads_downloads_list_widget.currentItem().text()
            if file in songs_name:
                try:
                    os.startfile(data_base[songs_name.index(file)]+".mp4")
                except FileNotFoundError:
                    from utils.util import rm
                    from utils.util import get_sub_folder_path
                    nice_path_2 = rm(data_base[songs_name.index(file)].split("/")[-1], get_sub_folder_path(data_base[songs_name.index(file)]))
                    if nice_path_2 != None:
                        os.startfile(nice_path_2)
                
                    self.showdialog(title="File not found", text="File missing", informative_text="File has been deleted or moved to some other location", detailed_text=f'File Missing : {data_base[songs_name.index(file)]+".mp4"}')
                    files = os.listdir(self.ui.settings_save_location_line_edit.text())
                    current_data = self.database.downloads_mp4.load_data()
                    new_data = []
                    for i in files:
                        if i.endswith(".mp4"):
                            if os.path.join(self.ui.settings_save_location_line_edit.text(), (i.replace(".mp4", ""))).replace("\\", "/") in current_data:
                                
                                new_data.append(os.path.join(self.ui.settings_save_location_line_edit.text(),(i.replace(".mp4", ""))).replace("\\", "/"))

                    self.database.downloads_mp4.save_data(new_data)
                    self.ui.downloads_downloads_list_widget.clear()
                    current_data_refresh = self.database.downloads_mp4.load_data()
                    for i in current_data_refresh:
                        self.ui.downloads_downloads_list_widget.addItem(i.split("/")[-1])
    def _getName(self, _list):
        _new_list = []
        for _i in _list:
            _new_list.append(_i.split("/")[-1])
        return _new_list

    def get_download_bar_data(self):
        showable_list = []
        cleared = False
        prev = ""
        once = False
        while self.downloads_showable:
            data = self.ui.downloads_search_downloads_line_edit.text()
            dataBase_data = self.database.downloads_mp4.load_data()
            if data!="":
                prev = data
                self.search_in_active=True
                song_names = self._getName(dataBase_data)
                for i in song_names:
                    if data.lower() in i.lower():
                        showable_list.append(i)
                if self.ui.downloads_search_downloads_line_edit.text() == prev:
                    if not once:
                        self.ui.downloads_downloads_list_widget.clear()
                        cleared=True
                        self.ui.downloads_downloads_list_widget.addItems(showable_list)
                        once = True     
                else:
                    
                    self.ui.downloads_downloads_list_widget.clear()
                    cleared = True
                    showable_list = []
                    once = False
            else:
                if cleared:
                    self.ui.downloads_downloads_list_widget.addItems(song_names)
                    cleared=False
    def save_data(self):
        """
        savelocation 
        alwaysmp3
        mp3location
        quality
        """
        
        saveLocation = self.ui.settings_save_location_line_edit.text()
        alwaysmp3 = self.ui.settings_check_box.isChecked()
        if alwaysmp3:
            alwaysmp3 = "true"
        else:
            alwaysmp3 = "false"
        mp3Location = self.ui.settings_save_location_mp3_line_edit.text()
        quality = self.ui.settigns_combobox.currentText()
        if saveLocation=="":
            self.showdialog(title="Save Downloads Location Error", text="Path Empty", informative_text="Please specify a proper path before saving the information")
            return
        if not os.path.exists(saveLocation):
            self.showdialog(title="Save Downloads Location Error", text="Did not specify proper location", informative_text="Please specify a proper path before saving the information")
            return
        if mp3Location=="":
            self.showdialog(title="Save MP3 Location Error", text="Path Empty", informative_text="Please specify a proper path before saving the information")
            return
        if not os.path.exists(mp3Location):
            self.showdialog(title="Save MP3 Location Error", text="Did not specify proper location", informative_text="Please specify a proper path before saving the information")
            return
        if quality=="Select":
            self.showdialog(title="Quality Error", text="No Quality found", informative_text="Please select the quality before saving the information", detailed_text="Please select the quality under settings tab to save the information")
            return

        self.database.settings.save_data([saveLocation, alwaysmp3, mp3Location, quality])
        self.showdialog(title="Success", text="Settings Saved Successfully", informative_text="",type=QMessageBox.Information)
        



    
    def change_download_button(self, status):
        if status==0:
            self.ui.home_download_button.setText("Downloaded")
            self.ui.home_download_button.setStyleSheet("QPushButton {background-color: rgb(0, 195, 0)}")
        elif status==1:
            self.ui.home_download_button.setText("Download")
            self.ui.home_download_button.setStyleSheet("QPushButton {background-color: rgb(255, 35, 252)}")
        elif status==2:
            self.ui.home_download_button.setText("Converted")
            self.ui.home_download_button.setStyleSheet("QPushButton {background-color: rgb(0, 35, 252)}")
        elif status==3:
            self.ui.home_download_button.setText("Converting...")
            self.ui.home_download_button.setStyleSheet("QPushButton {background-color: rgb(255, 35, 252)}")
    def download_vid(self, link):
        if self.ui.settigns_combobox.currentText() == "Best":
            Downloader(link).download_first(self.ui.settings_save_location_line_edit.text() if self.ui.settings_save_location_line_edit.text()!="" else "")
        if self.ui.settigns_combobox.currentText() == "Worst":
            Downloader(link).download_last(self.ui.settings_save_location_line_edit.text() if self.ui.settings_save_location_line_edit.text()!="" else "")
        if self.ui.settigns_combobox.currentText() == "Select":
            self.downloaded=False
            return
        self.downloaded = True
        downloaded_list = self.database.downloads_mp4.load_data()
        downloaded_list.append(os.path.join(self.ui.settings_save_location_line_edit.text() if self.ui.settings_save_location_line_edit.text()!="" else os.getcwd(), Downloader(link).title).replace("\\", "/"))
        self.database.downloads_mp4.save_data(downloaded_list)
        self.ui.downloads_downloads_list_widget.addItem(Downloader(link).title) 
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileNames(self,"MP4 Files","","MP4 Files (*.mp4)", options=options)
        return fileName
    def selectFolderDialog(self):
        dialog = QFileDialog()
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        dialog.setWindowTitle("Folder Choose")
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilter("Folder Choose")
        dialog.setFileMode(QFileDialog.Directory)
        if dialog.exec_() == QFileDialog.Accepted:
            return(dialog.selectedFiles()[0])
            
        else:
            return None
    def takeFileLocation(self):
        path = self.saveFileDialog()
        if path!=None:
            if len(path)==1:
                self.ui.mp3_file_location_line_edit.setText(path[0])
            elif len(path)>1:
                path = ",".join(path)
                self.ui.mp3_file_location_line_edit.setText(path)
    def takeFolderPath(self,status):
        path = self.selectFolderDialog()

        if path != None:
            
            if status==0:
                self.ui.settings_save_location_line_edit.setText(path)
            elif status==1:
                self.ui.settings_save_location_mp3_line_edit.setText(path)
            elif status==2:
                self.ui.mp3_save_location_line_edit.setText(path)
            elif status==3:
                self.ui.mp3_file_location_line_edit.setText(path)
    def quit(self):
        ##############Thread enders#########################
        self.youtube_searchable = False
        self.show_listing = True
        self.downloads_showable = False
        self.mp3_joinable = False
        self.search_bar_thread.join()
        self.downloads_bar_thread.join()
        try:
            self.thread_mp3.join()
        except:
            pass

        #####################################################
        sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Youtube_downlader()
    window.show()
    while mixer.music.get_busy():
        t.Clock().tick(10)
    sys.exit(app.exec_())
    
