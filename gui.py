import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
import sys
from studyPlan import StudyPlan
from plannerIO import PlannerIO
from period import Period
            
class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, courseListFileName):
        
        super(MainWindow, self).__init__()
        
        self.courseListFileName = courseListFileName
        self.plannerIO = PlannerIO()
        self.studyPlan = None
        self.studyPlanner = None
        
        self.setWindowTitle('Study Planner')  
        openFile = QtGui.QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open a study plan')
        openFile.triggered.connect(self.openDialog)
        
        saveFile = QtGui.QAction('Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save the study plan')
        saveFile.triggered.connect(self.saveDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)       
        fileMenu.addAction(saveFile)
        self.show()
        
    def openDialog(self):

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                'studyplan.csv')
        
        self.studyPlan = self.plannerIO.loadStudyPlan(fname)
        self.studyPlan.setAvailableCourses(self.plannerIO.loadCourses(self.courseListFileName))
        self.studyPlanner = StudyPlanner(self.studyPlan)
        self.setCentralWidget(self.studyPlanner)
        
    def saveDialog(self):

        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', 
                'studyplan.csv')
        
        self.plannerIO.saveStudyPlan(fname, self.studyPlan)
        
class CourseButton(QtGui.QPushButton):
  
    def __init__(self, title, parent):
        self.title = title
        self.parent = parent
        super(CourseButton, self).__init__(title, parent)
        year, period = self.parent.studyPlan.getCourse(self.title)
        menu = QtGui.QMenu()
        menu.addAction('Suorita kurssi myohemmin', self.Later)
        if year > 0:
            menu.addAction('Suorita kurssi aiemmin', self.Earlier)
        menu.addAction('Merkitse kurssi suoritetuksi', self.Completed)
        menu.addAction('Poista kurssi aikataulusta', self.Unschedule)
        self.setMenu(menu)
    
    def Later(self):
        year, period = self.parent.studyPlan.getCourse(self.title)
        self.parent.studyPlan.scheduleCourse(self.title, year+1, period)
        self.parent.clearCourses()
        self.parent.drawCourses()  

    def Earlier(self):
        year, period = self.parent.studyPlan.getCourse(self.title)
        self.parent.studyPlan.scheduleCourse(self.title, year-1, period)
        self.parent.clearCourses()
        self.parent.drawCourses()  
        
    def Completed(self):
        year, period = self.parent.studyPlan.getCourse(self.title)
        self.parent.studyPlan.scheduleCourse(self.title, StudyPlan.COMPLETED, period)
        self.parent.clearCourses()
        self.parent.drawCourses()  
        
    def Unschedule(self):
        year, period = self.parent.studyPlan.getCourse(self.title)
        self.parent.studyPlan.scheduleCourse(self.title, StudyPlan.UNSCHEDULED, period)
        self.parent.clearCourses()
        self.parent.drawCourses()  

class StudyPlanner(QtGui.QWidget):
    
    def __init__(self, studyPlan):
        
        super(StudyPlanner, self).__init__()
        
        self.studyPlan = studyPlan
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid) 
        self.drawCourses()
        
        
    def drawCourses(self):
        creditsPerPeriod = self.studyPlan.listCreditsPerPeriod()
        for year in range(0, len(self.studyPlan.schedule)):
            syear = QtGui.QPushButton('Vuosi ' + str(year+1) + ' (' + str(sum(creditsPerPeriod[year])) + 'op)')
            self.grid.addWidget(syear, 0, year*4, 1, 4)
            for i in range(0, 4):
                periodButton = QtGui.QPushButton(Period.ROMANS[i] + ' (' + str(creditsPerPeriod[year][i]) + 'op)')
                if creditsPerPeriod[year][i] > self.studyPlan.maxCreditsPerPeriod:
                    periodButton.setStyleSheet('QPushButton {color: purple}')
                elif creditsPerPeriod[year][i] < self.studyPlan.minCreditsPerPeriod:
                    periodButton.setStyleSheet('QPushButton {color: red}')
                self.grid.addWidget(periodButton, 1, year*4+i)
            for courseName, period in self.studyPlan.schedule[year].iteritems():
                col = year*4+period.begin-1
                button = CourseButton(courseName, self)
                if self.studyPlan.hasSatisfiedPrerequisites(courseName):
                    button.setStyleSheet('QPushButton {color: blue}')
                else:
                    button.setStyleSheet('QPushButton {color: orange}')
                colspan = period.length()
                for row in range(2, self.grid.rowCount()+1):
                    if row == self.grid.rowCount():
                        self.grid.addWidget(button, row, col, 1, colspan)
                        break
                    if self.grid.itemAtPosition(row, col) == None:
                        room = True
                        for i in range(1, colspan):
                            if self.grid.itemAtPosition(row, col+i) != None:
                                room = False
                        if room:
                            self.grid.addWidget(button, row, col, 1, colspan)
                            break
                    
    def clearCourses(self):
        for row in range(0, self.grid.rowCount()):
            for col in range(0, self.grid.columnCount()):
                if self.grid.itemAtPosition(row, col) != None and self.grid.itemAtPosition(row, col).widget() != None:
                    self.grid.itemAtPosition(row, col).widget().setParent(None)
                    
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    window = MainWindow('autcourses.csv') # TODO: Something less hard-coded
    menu = QtGui.QMenu()  
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()