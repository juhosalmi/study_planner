'''
Created on 22.3.2013

@author: jtsalmi
'''

from course import Course
from period import Period

class StudyPlan(object):
    
    '''
    StudyPlan has the information on the schedule of the picked courses and the
    algorithms to make good study plans.
    '''
    
    COMPLETED = -1 # Enum return value for completedCourses course
    UNSCHEDULED = -2 # Enum return value for unscheduled course

    def __init__(self): 
        self.schedule = [] # List of dictionaries of scheduled course names and periods for each year. [0] is current year etc.
        self.unscheduledCourses = set() # Set of unscheduled course names
        self.completedCourses = set()  # Set of completed courses
        
        
    def addCompletedCourse(self, courseName):
        self.removeCourse(courseName)
        self.completedCourses.add(courseName)
        
    def addCourse(self, courseName):
        self.removeCourse(courseName)
        self.unscheduledCourses.add(courseName)
    
    def scheduleCourse(self, courseName, year, period):
        self.removeCourse(courseName)
        if len(self.schedule) < year+1:
            for i in range(len(self.schedule), year+1):
                self.schedule.append({})
        self.schedule[year][courseName] = period
        
    def getCourse(self, courseName):
        year = None # Returns None if course is not in the study plan
        period = None 
        if courseName in self.completedCourses:
            year = self.COMPLETED
        elif courseName in self.unscheduledCourses:
            year = self.UNSCHEDULED
        else:
            for i in range(0, len(self.schedule)):
                if courseName in self.schedule[i]:
                    year = i
                    period = self.schedule[i][courseName]
                    break
        return year, period
    
    def removeCourse(self, courseName):
        self.completedCourses.discard(courseName)
        self.unscheduledCourses.discard(courseName)
        for i in range(0, len(self.schedule)):
            if courseName in self.schedule[i]:
                del self.schedule[i][courseName]
                return
    
    