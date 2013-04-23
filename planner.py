'''
Created on 22.3.2013

@author: jtsalmi
'''

class Planner(object):
    '''
    classdocs
    '''


    def __init__(self, courses, studyPlan):
        self.courses = courses
        self.studyPlan = studyPlan
        
    def scheduleUnscheduledCourses(self):
        