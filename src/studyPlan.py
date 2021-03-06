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
    
    # TODO: add error handling
    
    COMPLETED = -1 # Enumeration for completedCourses course
    UNSCHEDULED = -2 # Enumeration for unscheduled course

    def __init__(self): 
        self.schedule = [] # List of dictionaries of scheduled course names and periods for each year. [0] is current year etc.
        self.unscheduledCourses = set() # Set of unscheduled course names
        self.completedCourses = set()  # Set of completed courses
        self.courses = {} # Dictionary of all available courses accessed by name
        self.minCreditsPerPeriod = 12.0 # How many credits the student wants to study per period at minimum, initially 12
        self.maxCreditsPerPeriod = 18.0 # How many credits the student wants to study per period at maximum, initially 18
    
    
    '''
    COURSE METHODS
    '''
    
    '''
    addCompletedCourse
    '''
    def addCompletedCourse(self, courseName):
        self.removeCourse(courseName)
        self.completedCourses.add(courseName)
        
    '''
    addCourse
    '''
    def addCourse(self, courseName):
        self.removeCourse(courseName)
        self.unscheduledCourses.add(courseName)
    
    '''
    scheduleCourse
    '''
    def scheduleCourse(self, courseName, year, period):
        courseName = str(courseName).strip()
        self.removeCourse(courseName)
        if len(self.schedule) < year+1:
            for i in range(len(self.schedule), year+1):
                self.schedule.append({})
        if year == self.COMPLETED:
            self.addCompletedCourse(courseName)
        elif year == self.UNSCHEDULED:
            self.addCourse(courseName)
        else:
            self.schedule[year][courseName] = period
        
    '''
    getCourse 
    '''
    def getCourse(self, courseName):
        year = None # Returns None if course is not in the study plan
        period = None 
        courseName = str(courseName)
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
    
    '''
    removeCourse removes a course from the studyPlan if course with such name exists in it
    '''
    def removeCourse(self, courseName):
        self.completedCourses.discard(courseName)
        self.unscheduledCourses.discard(courseName)
        for i in range(0, len(self.schedule)):
            if courseName in self.schedule[i]:
                del self.schedule[i][courseName]
                return
    
    
    '''
    PLANNING METHODS AND ALGORITHMS
    '''
    
    '''
    setAvailableCourses 
    '''
    def setAvailableCourses(self, courses):
        self.courses = courses
        
    '''
    setMinCreditsPerPeriod
    '''
    def setMinCreditsPerPeriod(self, minCreditsPerPeriod):
        self.minCreditsPerPeriod = minCreditsPerPeriod
        
    '''
    setMaxCreditsPerPeriod
    '''
    def setMaxCreditsPerPeriod(self, maxCreditsPerPeriod):
        self.maxCreditsPerPeriod = maxCreditsPerPeriod
    
    '''
    hasSatisfiedPrerequisites
    '''
    def hasSatisfiedPrerequisites(self, courseName):
        prerequisites = self.courses[courseName].prerequisites
        year, period = self.getCourse(courseName)
        for prerequisite in prerequisites:
            yearp, periodp = self.getCourse(prerequisite)
            if yearp == self.UNSCHEDULED or yearp > year or yearp == None:
                return False
            elif yearp == year:
                if periodp >= period:
                    return False
        return True
    
    '''
    listCourseNamesWithDissatisfiedPrerequisites
    '''
    def listCourseNamesWithDissatisfiedPrerequisites(self):
        courseNames = []
        for each in self.schedule:
            for courseName in each.iterkeys():
                if not self.hasSatisfiedPrerequisites(courseName):
                    courseNames.append(courseName)
        return courseNames
        
    def listCreditsPerPeriod(self):
        creditsPerPeriod = [] # list of list of periodic credits
        for year in range(0, len(self.schedule)):
            creditsPerPeriod.append([0.0, 0.0, 0.0, 0.0])
            for courseName in self.schedule[year]:
                course = self.courses[courseName]
                courseLength = course.courseLength()
                for i in range(course.period.begin-1, course.period.end):
                    creditsPerPeriod[year][i] = creditsPerPeriod[year][i] + (float(course.ects)/courseLength)
        return creditsPerPeriod
            
    
    