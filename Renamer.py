import sys,os
import ctypes
from PySide2 import QtCore, QtWidgets,QtUiTools

CURRENT_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
SCREEN_SIZE=ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1),
WINDOW_SIZE=SCREEN_SIZE[0]/2,SCREEN_SIZE[1]/2
WINDOW_POSITION=SCREEN_SIZE[0]/4,SCREEN_SIZE[1]/6

class UIWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(UIWindow, self).__init__(parent)
        self.ui = QtUiTools.QUiLoader().load(os.path.join(CURRENT_PATH, 'Renamer.ui'))
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Renamer")
        self.setAcceptDrops(True)
        self.setGeometry(WINDOW_POSITION[0], WINDOW_POSITION[1], WINDOW_SIZE[0], WINDOW_SIZE[1])
        #Initialize Model
        self.modelFile=QtCore.QStringListModel()
        #Signal
        self.ui.pushButtonExit.clicked.connect(self.clickExit)
        self.ui.pushButtonPrefix.clicked.connect(self.renamePrefix)
        self.ui.pushButtonSuffix.clicked.connect(self.renameSuffix)
        self.ui.pushButtonReplace.clicked.connect(self.renameReplace)
        self.ui.pushButtonRenameBasic.clicked.connect(self.renameBasic)
        self.ui.pushButtonPre.clicked.connect(self.shavePre)
        self.ui.pushButtonPost.clicked.connect(self.shavePost)
    def clickExit(self):
        self.close()
    def dropEvent(self, event):
        print('Dorp file!')
        drop_str=event.mimeData().text().replace("file:///","")
        drop_str=drop_str.replace('/','\\')
        self.ui.file_list=drop_str.split('\n')
        if len(self.ui.file_list)>1:
            self.ui.file_list.pop()
        self.makeStructure()
    def makeStructure(self):
        self.ui.file_structure=[]
        for i in self.ui.file_list:
            path_name,file_name_ext=os.path.split(i)
            file_name,file_ext=os.path.splitext(file_name_ext)
            row_list=[path_name,file_name,file_ext]
            self.ui.file_structure.append(row_list)
        view_list=[]
        for i in self.ui.file_structure:
            view_list.append(i[1])
        self.modelFile.setStringList(view_list)
        self.ui.listViewFile.setModel(self.modelFile)
    def renamePrefix(self):
        print('Prefix!')
        prefix_word=self.ui.lineEditPrefix.text()
        i=0
        for structure in self.ui.file_structure:
            new_path=structure[0]+'\\'+prefix_word+structure[1]+structure[2]
            os.rename(self.ui.file_list[i],new_path)
            # Suffix Execute
            self.ui.file_list[i] = new_path
            i+=1
        self.makeStructure()
    def renameSuffix(self):
        print('Suffix!')
        suffix_word=self.ui.lineEditSuffix.text()
        i=0
        for structure in self.ui.file_structure:
            new_path=structure[0]+'\\'+structure[1]+suffix_word+structure[2]
            os.rename(self.ui.file_list[i],new_path)
            # Suffix Execute
            self.ui.file_list[i] = new_path
            i+=1
        self.makeStructure()
    def renameReplace(self):
        print('Replace!')
        i=0
        for structure in self.ui.file_structure:
            new_name=structure[1].replace(self.ui.lineEditReplaceBefore.text(),self.ui.lineEditReplaceAfter.text())
            new_path=structure[0]+'\\'+new_name+structure[2]
            os.rename(self.ui.file_list[i], new_path)
            #Suffix Execute
            self.ui.file_list[i] = new_path
            i += 1
        self.makeStructure()
    def renameBasic(self):
        print('Rename!')
        format_str='{0:0'+str(self.ui.spinBoxRenameFormat.value())+'d}'
        new_word=self.ui.lineEditRenameBasic.text()
        print(new_word)
        i=0
        print(str('{0:02d}'.format(i)))
        for structure in self.ui.file_structure:
            new_path = structure[0] + '\\' + new_word+str(format_str.format(i))+ structure[2]
            os.rename(self.ui.file_list[i], new_path)
            # Suffix Execute
            self.ui.file_list[i]=new_path
            i += 1
        #self.resetList()
        self.makeStructure()
    def shavePre(self):
        print('ShavePre!')
        shave_num=self.ui.spinBoxPre.value()
        i=0
        for structure in self.ui.file_structure:
            new_name=structure[1][shave_num:]
            new_path=structure[0]+'\\'+new_name+structure[2]
            os.rename(self.ui.file_list[i], new_path)
            self.ui.file_list[i] = new_path
            i += 1
        self.makeStructure()
    def shavePost(self):
        print('ShavePost!')
        shave_num=self.ui.spinBoxPost.value()
        #print(self.ui.file_structure[0][1][:-shave_num])
        i=0
        for structure in self.ui.file_structure:
            new_name=structure[1][:-shave_num]
            new_path=structure[0]+'\\'+new_name+structure[2]
            os.rename(self.ui.file_list[i], new_path)
            self.ui.file_list[i] = new_path
            i += 1
        self.makeStructure()
    def resetList(self):
        print('Reset list!')
        view_list=[]
        self.modelFile.setStringList(view_list)
        self.ui.listViewFile.setModel(self.modelFile)
    def dragEnterEvent(self, event):
        mime=event.mimeData()
        if mime.hasUrls()==True:
            event.accept()
        else:
            event.ignore()
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Window = UIWindow()
    try:
        with open('..\CSS\DawnTheme.css','r')as f:
            Window.setStyleSheet(''.join(f.readlines()))
    except:
        print('No CSS File!')
    Window.show()
    sys.exit(app.exec_())