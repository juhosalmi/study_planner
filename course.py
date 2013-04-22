'''
Created on 22.3.2013

@author: jtsalmi
'''

from period import Period

class Course(object):

    def __init__(self, name, ects, periods, description, prerequisites):
        
        self.name = name # Name of the course
        self.ects = ects # Number of credits
        self.periods = periods # List of Periods in which the course will be held
        self.description = description # Course description
        self.prerequisites = prerequisites # WHich courses should the student have completed before attending this course
        
        
        