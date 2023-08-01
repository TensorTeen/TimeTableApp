import numpy as np
#from APITest import createEvent
import json

#Using ical gives generality, but recurring events feature in google calendar not supported
from icalendar import Calendar, Event
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
    def __init__(self, slotName: str, slotTimes: "np.array of TimeRange", course=None, rec="WEEKLY") -> None: #I suggest slotTimes as type WeekTime
        self.slotName = slotName
        self.slotTimes = slotTimes
        self.course     = course 
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
    def __init__(self, day:int, time: datetime.time ):
        self.day = day
        self.time = time
    def getDay(self):
        return self.day
    def getTime(self):
        return self.time
    
class TimeRange(WeekTime):
    def __init__(self, day:int, start:datetime.time, end:datetime.time):
        self.day = day
        self.time = start
        self.startTime = start
        self.endTime = end
    def getStart(self):
        return self.startTime
    
    def getEnd(self):
        return self.endTime

class Rule():
    def __init__(self, condition, contents: dict):
        self.content = contents
        self.condition =condition
    
    

class Course():
    def __init__(self, courseName: str, slot: Slot, loc="", desc="", rules=[]) -> None:
        self.courseName = courseName
        self.slot = slot
        self.attrs = {
            "name" : courseName, 
            "loc" : loc, 
            "desc" : desc
            }
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

class Calendar():
    def __init__(self, start: datetime.date, end: datetime.date, courses = [], icalobj = Calendar()) -> None:
        self.start = start
        self.end = end
        self.courses = courses
        self.icalObj = icalobj #TODO
    
    def addCourse(self, course: Course) -> None:
        self.courses.append(Course)
    
    def saveIcal(self, name = "cal"):
        with open(name+".ical", "w") as calFile:
            calFile.write(self.icalObj.to_ical().decode("utf-8"))
    
    def createEvents(self, course):
        day = self.start
        while day != self.end + datetime.timedelta(days=1):
            #for each day check every slot
            for slot in course.slot.slotTimes:
                if slot.getDay() == day.isoweekday():
                    #add event
                    #TODO implement rule
                    event = Event()
                    event.add('summary', course.attrs["name"])
                    event.add('location', course.attrs["loc"])
                    event.add('description', course.attrs["desc"])
                    event.add("dtstart", datetime.datetime.combine(day, slot.getStart()))
                    event.add("dtend", datetime.datetime.combine(day, slot.getEnd()))
                    self.icalObj.add_component(event)
            
            day += datetime.timedelta(days = 1)

#TODO add exams functionality


# Example usage
# slot = Slot("A", [TimeRange(1, datetime.time(10, 0), datetime.time(10, 50))])
# course = Course("MA", slot)
# calendar= Calendar(datetime.date(2024, 7, 31), datetime.date(2024, 8, 10), [course] )
# calendar.createEvents(calendar.courses[0])
        
        
        
        
