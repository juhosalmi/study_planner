'''
Created on 22.4.2013

@author: Juho Salmi
'''
import unittest
from plannerIO import PlannerIO 
from period import Period
from course import Course
from studyPlan import StudyPlan


class Test(unittest.TestCase):


    def test_loadCourses(self):
        plannerIO = PlannerIO()
        courses = plannerIO.loadCourses('courses1.csv')
        self.assertEqual(10, courses['matematiikka 1'].ects, 'wrong number of credits')

    def test_loadAndSaveStudyPlan(self):
        plannerIO = PlannerIO()
        studyPlan = plannerIO.loadStudyPlan('studyplan1.csv')
        year1, period1 = studyPlan.getCourse('matematiikka 2')
        self.assertEqual(0, year1, 'wrong year')
        self.assertEqual(Period(Period.III, Period.IV), period1, 'wrong period')
        year2, period2 = studyPlan.getCourse('puhekurssi')
        self.assertEqual(-1, year2, 'wrong year')
        self.assertEqual(None, period2, 'wrong period')
        year3, period3 = studyPlan.getCourse('kirjoituskurssi')
        self.assertEqual(-2, year3, 'wrong year')
        self.assertEqual(None, period3, 'wrong period')
        plannerIO.saveStudyPlan('outputFile.csv', studyPlan)
        
        
    def test_loadAndSaveStudyPlan2(self):
        plannerIO = PlannerIO()
        studyPlan = plannerIO.loadStudyPlan('outputFile.csv')
        year1, period1 = studyPlan.getCourse('matematiikka 2')
        self.assertEqual(0, year1, 'wrong year')
        self.assertEqual(Period(Period.III, Period.IV), period1, 'wrong period')
        year2, period2 = studyPlan.getCourse('puhekurssi')
        self.assertEqual(-1, year2, 'wrong year')
        self.assertEqual(None, period2, 'wrong period')
        year3, period3 = studyPlan.getCourse('kirjoituskurssi')
        self.assertEqual(-2, year3, 'wrong year')
        self.assertEqual(None, period3, 'wrong period')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIO']
    unittest.main()