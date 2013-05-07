'''
Created on 22.4.2013

@author: Juho Salmi
'''

import csv

from course import Course
from period import Period
from studyPlan import StudyPlan

class PlannerIO(object):

    # TODO: add error handling
    
    '''
    loadCourses is the only way to set up the dictionary of all courses for Planner
    '''
    def loadCourses(self, inputFile):
        with open(inputFile, 'rb') as csvfile:
            courseReader = csv.reader(csvfile, delimiter=';')
            courses = {}
            for row in courseReader:
                prerequisites = []
                if row[5] != '':
                    prerequisites = row[5].split(',')
                    for i in range(0, len(prerequisites)):
                        prerequisites[i] = prerequisites[i].strip()
                courses[row[0].strip()] = Course(row[0].strip(), row[1], Period(row[2],row[3]), row[4], prerequisites)
                
            return courses
    
    '''
    loadStudyPlan 
    '''
    def loadStudyPlan(self, inputFile):
        with open(inputFile, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            studyPlan = StudyPlan()
            for row in reader:
                year = int(row[1])
                if year == StudyPlan.UNSCHEDULED:
                    studyPlan.addCourse(row[0])
                elif year == StudyPlan.COMPLETED:
                    studyPlan.addCompletedCourse(row[0])
                else:
                    studyPlan.scheduleCourse(row[0], year, Period(row[2],row[3]))
                    
            return studyPlan
    
    '''
    saveStudyPlan
    '''
    def saveStudyPlan(self, outputFile, studyPlan):
        with open(outputFile, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for each in studyPlan.unscheduledCourses:
                writer.writerow([each, StudyPlan.UNSCHEDULED, '', ''])
            for each in studyPlan.completedCourses:
                writer.writerow([each, StudyPlan.COMPLETED, '', ''])
            for i in range(0, len(studyPlan.schedule)):
                for courseName, period in studyPlan.schedule[i].iteritems():
                    writer.writerow([courseName, i, period.begin, period.end])
        