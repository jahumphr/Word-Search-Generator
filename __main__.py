# =============================================================================
# Word Search Generator Main
# Created by Josh Humphries May 2020
# 
# GUI for WordSearch.py 
# Created in PyQt5
# =============================================================================

from PyQt5 import QtCore, QtGui, QtWidgets
from WordSearch import WordSearch

ws = WordSearch()        

# =============================================================================
# startWindow displays on program start, allows user to enter size of word search
# =============================================================================
        
class startWindow(object):
    def setupUi(self, MainWindow):
        """initiate start window"""
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(250, 100)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1096, 26))
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        
        #Text box for user to enter size of word search
        self.size = QtWidgets.QLineEdit(self.centralwidget)
        self.size.setGeometry(QtCore.QRect(20, 30, 113, 22))

        #OK button to generate word search once user has entered size
        self.generate = QtWidgets.QPushButton(self.centralwidget)
        self.generate.setGeometry(QtCore.QRect(140, 30, 71, 21))
        self.generate.clicked.connect(self.start)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 221, 21))
        
        #Error message - displays if user enters invalid size
        self.error = QtWidgets.QLabel(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        
    def start(self):
        """Called when user clicks OK button on start window to generate word search. 
        Checks that user entered a valid size. If size is valid, creates playWindow to 
        display word search."""
        
        #If size is invalid, display error message
        if (not self.size.text().isdigit() or int(self.size.text()) < 10 
            or int(self.size.text()) > 55):
            self.error.setGeometry(QtCore.QRect(20, 50, 221, 21))
            self.error.setText("Size must be between 10 and 55")
            palette = self.error.palette()
            color = QtGui.QColor('red')
            palette.setColor(QtGui.QPalette.Foreground, color)
            self.error.setPalette(palette)
            self.error.show()
            return 0
        
        #If size is valid, playWindow is displayed with word search
        self.error.close()
        self.playWindow = playWindow(int(self.size.text()))
        self.playWindow.show()      

        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.generate.setText(_translate("MainWindow", "OK"))
        self.label.setText(_translate("MainWindow", "Enter a size between 10 and 55:"))
        

# =============================================================================
# playWindow is the main window operating the word search. After user enters a size
# in the start window, playWindow displays generated word search and hidden word bank.
# =============================================================================

class playWindow(QtWidgets.QWidget):
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.coordsToCheck = [] #stores currently selected letters to check if winning word
        self.initUI()
    
    def initUI(self):
        """Generates word search and displays in new window"""
        
        self.setWindowTitle('Word Search')
        
        ws.buildArray(self.size) #Builds sizexsize matrix of hidden words
        
        #Create tableWidget to store letter matrix with hidden words
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setColumnCount(self.size)
        self.tableWidget.setRowCount(self.size)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.setFixedWidth(2 + 19*self.size)
        self.tableWidget.setFixedHeight(2 + 17*self.size)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        #Populate tableWidget with generated word search matrix
        for row in range(self.size):
            for col in range(self.size):
                item = QtWidgets.QTableWidgetItem(ws.letterArray[row][col])
                item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                item.setBackground(QtGui.QColor('white'))
                self.tableWidget.setItem(row, col, item)
                self.tableWidget.setColumnWidth(col, 19)
                self.tableWidget.setRowHeight(row, 17)

        #Word bank widget to display hidden words
        self.wordsToFind = QtWidgets.QTextBrowser()
        self.wordsToFind.setText('\n'.join(ws.wordsAdded))
        self.wordsToFind.setFont(QtGui.QFont("Calibri", 10))
        self.wordsToFind.setFixedWidth(len(max(ws.wordsAdded,key=len))*13)
        
        #Button to clear all selected letters that aren't part of winning words
        self.clearButton = QtWidgets.QPushButton()
        self.clearButton.clicked.connect(self.clearSelectedText)
        self.clearButton.setText("Clear")
        
       
        self.vBox = QtWidgets.QVBoxLayout()
        self.vBox.addWidget(self.wordsToFind)
        self.vBox.addWidget(self.clearButton)
       
        #Main widget that other widgets are added to
        self.centralWidget = QtWidgets.QGridLayout()
        self.centralWidget.addLayout(self.vBox, 0, 0)
        self.centralWidget.addWidget(self.tableWidget, 0, 1)
        
        self.setLayout(self.centralWidget)
      
        self.show()
        
        self.tableWidget.cellClicked.connect(self.leftClickLetter)
        
        
    def leftClickLetter(self, row, col):
        """Called whenever a letter is clicked in tableWidget. Changes background
        color of letter cell to indicate it's been selected, or changes background
        color back to normal if letter has been clicked again to de-select.
        Checks for winning word each time a new letter is selected."""
               
        item = self.tableWidget.item(row, col)
        
        if (item.background() == QtGui.QColor('white')):
            item.setBackground(QtGui.QColor(51,153,255))
            self.coordsToCheck.append((row,col)) #adds selection to list to check for win
        
        elif (item.background() == QtGui.QColor(51,153,255)):
            item.setBackground(QtGui.QColor('white'))
            self.coordsToCheck.remove((row,col)) #removes selection from list if user de-selects
            
        elif (item.background() == QtGui.QColor('lightgreen')):
            item.setBackground(QtGui.QColor(0,204,204))
            self.coordsToCheck.append((row,col))
            
        elif (item.background() == QtGui.QColor(0,204,204)):
            item.setBackground(QtGui.QColor('lightgreen'))
            self.coordsToCheck.remove((row,col))

        #If coordinates in coordsToCheck are a winning word, the
        #word is highlighted green
        if self.wordFoundCheck(self.coordsToCheck):
            for coordPair in self.coordsToCheck:
                item = self.tableWidget.item(coordPair[0], coordPair[1])
                item.setBackground(QtGui.QColor('lightGreen'))
            self.coordsToCheck = []
            
        self.tableWidget.clearSelection()
        
        
    def wordFoundCheck(self, coordsToCheck):
        """Checks for win, comparing coordinates in coordsToCheck with
        coordinates stored in WordSearch.wordLocations. If there's a win,
        returns True and word is removed from word bank."""
        
        for word in ws.wordLocations:
            if sorted(ws.wordLocations[word]) == sorted(self.coordsToCheck):
                ws.wordsAdded.remove(word)
                self.wordsToFind.setText('\n'.join(ws.wordsAdded))
                self.wordsToFind.show()
                return True
        return False
    
    
    def clearSelectedText(self):
        """Called when user clicks clear button. All selected letters that
        are not part of a winning word are cleared on Word Search table"""
    
        for coordPair in self.coordsToCheck:
            item = self.tableWidget.item(coordPair[0], coordPair[1])
            if item.background() == QtGui.QColor(0,204,204):
                item.setBackground(QtGui.QColor('lightGreen'))
            else:
                item.setBackground(QtGui.QColor('white'))
    
        self.coordsToCheck = [] #selected letters removed from coordsToCheck
        



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = startWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
