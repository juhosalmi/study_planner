'''
Created on 22.4.2013

@author: Juho Salmi
'''
import unittest
from plannerIO import PlannerIO 


class Test(unittest.TestCase):


    def test_IO(self):
        plannerIO = PlannerIO()
        courses = plannerIO.loadCourses('courses1.csv')
        print courses['matematiikka 1']
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIO']
    unittest.main()