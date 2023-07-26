import numpy as np
from APITest import createEvent
import json 


days = {
    "Sunday" : 0,
    "Monday" : 1,
    "Tuesday" : 2,
    "Wednesday":3,
    "Thursday":4,
    "Friday" : 5,
    "Saturday" : 6,
}

class Slot():
    def __init__(self,slotName:str,slotTimes:np.array,course=None,rec="WEEKLY") -> None:
        self.slotName = slotName
        self.slotTimes = slotTimes
        self.course = course
        self.rec = rec
        if self.course:
            self.occupied = True
        
    def retrieveTime(self,day:int) -> np.array:
        return self.slotTimes[day-1]
    
    def retrieveCourse(self) -> str:
        return self.course
    
    def save(self) -> None:
        details = {
            self.slotName : {
                "slotTimes" : self.slotTimes,
                "course" : self.course,
                "reccurence":self.rec,
            }
        }
        with open("slots.json","a+") as f:
            json.dump(details,f,indent=6)
        
    

class Course():
    def __init__(self,courseName:str,slot:Slot,loc="",desc=None) -> None:
        self.courseName = courseName
        self.slot = slot
        self.loc = loc
        self.desc = desc
        
    def __repr__(self) -> str:
        return self.courseName
    
    def retrieveTime(self,day:int) -> np.array:
        return self.slot.retrieveTime(day)
    
    def retrieveLocation(self) -> str:
        return self.loc
    
    def save(self) -> None:
        details = {
            self.courseName : {
                "slot" : self.slot,
                "course" : self.course,
                "location" : self.loc,
                "description": self.desc
            }
        }
        with open("courses.json","a+") as f:
            json.dump(details,f,indent=6)
    
    