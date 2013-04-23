'''
Created on 22.3.2013

@author: jtsalmi
'''

class Period(object):
    '''
    Period tells in which period the course will begin and end. Course has a
    list of Periods because course can be held multiple times in a year.
    '''
    
    I, II, III, IV = range(1,5) # Period enumerators

    def __init__(self, begin, end):
        self.begin = int(begin)
        self.end = int(end) 
        
    
    def __str__(self):
        romans = ["I", "II", "III", "IV"]
        return romans[self.begin-1] + '-' + romans[self.end-1] 
    
    '''
    COMPARITIONS
    '''
    def __eq__(self, other):
        return self.begin == other.begin and self.end == other.end
    
    def __ne__(self, other):
        return self.begin != other.begin or self.end != other.end
    
    def __ge__(self, other):
        return self.begin >= other.begin
    
    def __le__(self, other):
        return self.begin <= other.begin
    
    def __gt__(self, other):
        return self.begin > other.begin
    
    def __lt__(self, other):
        return self.begin < other.begin
    
    