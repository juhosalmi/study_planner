'''
Created on 22.4.2013

@author: Juho Salmi
'''

import csv

from course import Course
from period import Period

class PlannerIO(object):
    '''
    classdocs
    '''


    def loadCourses(self, inputFile):
        with open(inputFile, 'rb') as csvfile:
            courseReader = csv.reader(csvfile, delimiter=';')
            courses = {}
            for row in courseReader:
                prerequisites = []
                if row[5] != '':
                    prerequisites = row[5].split(',')
                    for each in prerequisites:
                        each = each.strip()
                courses[row[0].strip()] = Course(row[0].strip(), row[1], Period(row[2],row[3]), row[4], prerequisites)
                
            return courses
        