import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
import sys
from studyPlan import StudyPlan
from plannerIO import PlannerIO
            
class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, studyPlan):
        
        super(MainWindow, self).__init__()
        
        self.setWindowTitle('Study Planner')  
        self.studyPlan = studyPlan
        self.studyPlanner = StudyPlanner(self.studyPlan)
        self.setCentralWidget(self.studyPlanner)
        self.show()
        
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
        for year in range(0, len(self.studyPlan.schedule)):
            syear = QtGui.QPushButton(str(year+1))
            self.grid.addWidget(syear, 0, year*4, 1, 4)
            I = QtGui.QPushButton('I')
            II = QtGui.QPushButton('II')
            III = QtGui.QPushButton('III')
            IV = QtGui.QPushButton('IV')
            self.grid.addWidget(I, 1, year*4)
            self.grid.addWidget(II, 1, year*4+1)
            self.grid.addWidget(III, 1, year*4+2)
            self.grid.addWidget(IV, 1, year*4+3)
            for courseName, period in self.studyPlan.schedule[year].iteritems():
                col = year*4+period.begin-1
                button = CourseButton(courseName, self)
                colspan = period.end - period.begin + 1
                for row in range(2, self.grid.rowCount()+1):
                    if row == self.grid.rowCount():
                        self.grid.addWidget(button, row, col, 1, colspan)
                        break
                    if self.grid.itemAtPosition(row, col) == None:
                        self.grid.addWidget(button, row, col, 1, colspan)
                        break
                    
    def clearCourses(self):
        for row in range(0, self.grid.rowCount()):
            for col in range(0, self.grid.columnCount()):
                if self.grid.itemAtPosition(row, col) != None and self.grid.itemAtPosition(row, col).widget() != None:
                    self.grid.itemAtPosition(row, col).widget().setParent(None)
                    
        
def main():
    
    plannerIO = PlannerIO()
    studyPlan = plannerIO.loadStudyPlan('aut.csv')
    studyPlan.setAvailableCourses(plannerIO.loadCourses('autcourses.csv'))
    app = QtGui.QApplication(sys.argv)
    window = MainWindow(studyPlan)
    menu = QtGui.QMenu()  
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()