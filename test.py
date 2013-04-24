'''
Created on 22.3.2013

@author: jtsalmi
'''
import unittest
from course import Course
from period import Period
from studyPlan import StudyPlan
from plannerIO import PlannerIO



class Test(unittest.TestCase):


    def test_simpleStuff(self):
        
        self.study_plan = StudyPlan()
        self.study_plan.addCompletedCourse("completed course")
        self.study_plan.addCourse("course")
        self.study_plan.scheduleCourse("course", 1, Period(Period.I, Period.II))
        year1, period1 = self.study_plan.getCourse("course")
        self.assertEqual(1, year1, "Wrong year")
        self.assertEqual(Period(Period.I, Period.II), period1, "Wrong period")
        year2, period2 = self.study_plan.getCourse("completed course")
        self.assertEqual(StudyPlan.COMPLETED, year2, "Wrong year")
        self.assertEqual(None, period2, "Wrong period")
        year3, period3 = self.study_plan.getCourse("inexisting")
        self.assertEqual(None, year3, "wrong year")
        self.assertEqual(None, period3, "Wrong period")
        self.study_plan.removeCourse("course")
        year1, period1 = self.study_plan.getCourse("course")
        self.assertEqual(None, year1, "Wrong year")
        self.assertEqual(None, period1, "Wrong period")
        self.study_plan.addCourse("course")
        year1, period1 = self.study_plan.getCourse("course")
        self.assertEqual(StudyPlan.UNSCHEDULED, year1, "Wrong year")
        self.assertEqual(None, period1, "Wrong period")
        
    def test_prerequisites(self):
        plannerIO = PlannerIO()
        studyPlan = plannerIO.loadStudyPlan('studyplan2.csv')
        studyPlan.setAvailableCourses(plannerIO.loadCourses('courses1.csv'))
        dissatisfied = studyPlan.listCourseNamesWithDissatisfiedPrerequisites()
        self.assertTrue('fysiikka 2' in dissatisfied, 'something wrong with dissatisfied prerequisites')
        self.assertTrue('matematiikka 3' in dissatisfied, 'something wrong with dissatisfied prerequisites')



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()