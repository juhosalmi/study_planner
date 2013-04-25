

import sys
from PyQt4 import QtGui
from studyPlan import StudyPlan
from plannerIO import PlannerIO


class Example(QtGui.QWidget):
    
    def __init__(self, studyPlan):
        super(Example, self).__init__()
        
        self.studyPlan = studyPlan
        self.initUI()
        self.center()
        
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
                button = QtGui.QPushButton(courseName)
                colspan = period.end - period.begin + 1
                for row in range(2, grid.rowCount()+1):
                    if row == grid.rowCount():
                        grid.addWidget(button, row, col, 1, colspan)
                        break
                    if grid.itemAtPosition(row, col) == None:
                        grid.addWidget(button, row, col, 1, colspan)
                        break
        
        self.setLayout(grid) 
        self.setWindowTitle('Study Planner')    
        self.show()
        
    def center(self):
    
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
def main():
    
    plannerIO = PlannerIO()
    studyPlan = plannerIO.loadStudyPlan('aut.csv')
    studyPlan.setAvailableCourses(plannerIO.loadCourses('autcourses.csv'))
    app = QtGui.QApplication(sys.argv)
    ex = Example(studyPlan)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()