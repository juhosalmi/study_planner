import sys
from PyQt4 import QtGui, QtCore
from studyPlan import StudyPlan
from plannerIO import PlannerIO

class CourseButton(QtGui.QPushButton):
  
    def __init__(self, title, parent):
        super(CourseButton, self).__init__(title, parent)

    def mousePressEvent(self, e):
      
        QtGui.QPushButton.mousePressEvent(self, e)
        if e.button() == QtCore.Qt.LeftButton:
            print 'press'
        elif e.button() == QtCore.Qt.RightButton:
            print 'right press'
            
class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, studyPlan):
        
        super(MainWindow, self).__init__()
        
        self.studyPlan = studyPlan
        self.statusBar()
        studyPlanner = StudyPlanner(studyPlan)
        self.setCentralWidget(studyPlanner)
        self.setWindowTitle('Study Planner')    
        self.show()
        
    def keyPressEvent(self, e):
        
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        
    

class StudyPlanner(QtGui.QWidget):
    
    def __init__(self, studyPlan):
        
        super(StudyPlanner, self).__init__()
        
        self.studyPlan = studyPlan
        self.initUI()
        
    def initUI(self):
        
        grid = QtGui.QGridLayout()
        
        for year in range(0, len(self.studyPlan.schedule)):
            syear = QtGui.QPushButton(str(year+1))
            grid.addWidget(syear, 0, year*4, 1, 4)
            I = QtGui.QPushButton('I')
            II = QtGui.QPushButton('II')
            III = QtGui.QPushButton('III')
            IV = QtGui.QPushButton('IV')
            grid.addWidget(I, 1, year*4)
            grid.addWidget(II, 1, year*4+1)
            grid.addWidget(III, 1, year*4+2)
            grid.addWidget(IV, 1, year*4+3)
            for courseName, period in self.studyPlan.schedule[year].iteritems():
                col = year*4+period.begin-1
                button = CourseButton(courseName, self)
                button.clicked.connect(self.buttonClicked)
                colspan = period.end - period.begin + 1
                for row in range(2, grid.rowCount()+1):
                    if row == grid.rowCount():
                        grid.addWidget(button, row, col, 1, colspan)
                        break
                    if grid.itemAtPosition(row, col) == None:
                        grid.addWidget(button, row, col, 1, colspan)
                        break
        self.setLayout(grid) 
        
            
    def buttonClicked(self):
      
        sender = self.sender()
        year, period = self.studyPlan.getCourse(sender.text())
        self.studyPlan.scheduleCourse(sender.text(), year+1, period)
        print sender.text() + ' was pressed'
        
def main():
    
    plannerIO = PlannerIO()
    studyPlan = plannerIO.loadStudyPlan('aut.csv')
    studyPlan.setAvailableCourses(plannerIO.loadCourses('autcourses.csv'))
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow(studyPlan)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()