import numpy as np
from APITest import createEvent
import json
import datetime

#iso stansard weeks start on monday. can assign 0 or , 1 better.
days = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7,
}


class Slot():
    def __init__(self, slotName: str, slotTimes: np.array, course=None, rec="WEEKLY") -> None: #I suggest slotTimes as type WeekTime
        self.slotName = slotName
        self.slotTimes = slotTimes
        self.course = course 
        self.rec = rec
        if self.course:
            self.occupied = True

    def retrieveTime(self, day: int) -> np.array:
        return self.slotTimes[day-1] #why -1 ?

    def retrieveCourse(self) -> str:
        return self.course

    def save(self) -> None:
        details = {
            self.slotName: {
                "slotTimes": self.slotTimes,
                "course": self.course,
                "reccurence": self.rec,
            }
        }
        with open("slots.json", "a+") as f:
            json.dump(details, f, indent=6)

class WeekTime():
    def __init__(self, day:int, time: datetime.time):
        self.day = day
        self.time = time

class Course():
    def __init__(self, courseName: str, slot: Slot, loc="", desc=None, rules=[]) -> None:
        self.courseName = courseName
        self.slot = slot
        self.loc = loc
        self.desc = desc
        self.attrs = ['loc', 'desc']
        self.rules = rules

    def __repr__(self) -> str:
        return self.courseName

    def retrieveTime(self, day: int) -> np.array:
        return self.slot.retrieveTime(day)

    def retrieveLocation(self) -> str:
        return self.loc
    
    def addRule(self, condition, contents: dict = {"attr" : "val"}) -> None:#conditions is [start, end] where both are WeekTime objs
        self.rules.append({condition: contents})
    
    def save(self) -> None:
        details = {
            self.courseName: {
                "slot": self.slot, #Why the whole slot, is slot.slotName not enough
                "course": self.course,
                "location": self.loc,
                "description": self.desc
            }
        }
        with open("courses.json", "a+") as f:
            json.dump(details, f, indent=6)

#implement conditions in courses
#need to convert calendar object to ical, converting recurrent events to actual dates and times

class Caleder():
    def __init__(self, start: datetime.day, end: datetime.day, courses = []) -> None:
        self.start = start
        self.end = self.end
        self.courses = courses
    
    def addCourse(self, course: Course) -> None:
        self.courses.append(Course)
    
    def createEvents(course):
        
        
        
        
