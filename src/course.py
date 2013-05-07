'''
Created on 22.3.2013

@author: jtsalmi
'''

from period import Period

class Course(object):

    def __init__(self, name, ects, period, description, prerequisites):
        
        self.name = name # Name of the course
        self.ects = int(ects) # Number of credits
        self.period = period # The periods in which the course will be held
        self.description = description # Course description
        self.prerequisites = prerequisites # WHich courses should the student have completed before attending this course
        
    def courseLength(self):
        return self.period.length()
        
    def __str__(self):
        # TODO: add period tostring
        string = self.name + ': ' + self.ects + 'op, ' + self.period.__str__() + ', ' + self.description + ', Esitiedot: ' 
        for each in self.prerequisites:
            string = string + each + ', '
        return string
        