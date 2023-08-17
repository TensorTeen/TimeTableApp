<<<<<<< HEAD
import json
from icalendar import Calendar, Event
import numpy as np
from easygui import *
import os


FILES = os.listdir("./slots")
SLOTS = {}

#from APITest import createEvent

coursesList = {}

days = {
    "Sunday": 0,
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
}


class Slot:

    def __init__(self) -> None:
        text = "Enter the following details"
        title = "Slot Creation Window"
        input_list = ["Slot Name : ", ]
        self.slotName = multenterbox(text, title, input_list)[0]
        input_list = []
        for i in days:
            input_list.extend([i + "Start ", i + " End"])
        text = "Enter the following details: (Leave blank if not required/ Fill in 24 hour format, for eg: 13:00)"
        self.slotTimes = np.array(multenterbox(text, title, input_list))
        # SlotTimes = np.array(['', '', '08:00', '08:50', '13:00', '13:50', '', '', '11:00', '11:50', '10:00',
        # '10:50', '', '', ]).reshape(7, 2)
        self.rec = "WEEKLY"
        self.save()


    def retrieveTime(self, day: int) -> np.array:
        return self.slotTimes[day - 1]

    def save(self) -> None:
        details = {
            self.slotName: {
                "slotTimes": self.slotTimes.tolist(),
                "reccurence": self.rec,
            }
        }
        with open(f"./slots/{self.slotName}.json", "w") as f:
            json.dump(details, f, indent=6)


class Course:

    def __init__(self, courseName: str, slot: Slot, loc="", desc=None) -> None:
        text = "Enter the following details"
        title = "Course Creation Window"
        input_list = ["Course Name : ", "Description", "Location"]
        SlotDetails = multenterbox(text, title, input_list)
        # ils = ["A"]
        input_list = []
        for i in days:
            input_list.extend([i + "Start ", i + " End"])
        SlotTimes = np.array(multenterbox(text, title, input_list))
        # SlotTimes = np.array(['', '', '08:00', '08:50', '13:00', '13:50', '', '', '11:00', '11:50', '10:00',
        # '10:50', '', '',]).reshape(7,2)
        course_1 = Slot(SlotDetails[0], SlotTimes)
        coursesList[SlotDetails] = course_1

        self.courseName = courseName
        self.slot = slot
        self.attrs = {
            "name": input_list[0],
            "loc": input_list[1],
            "desc": input_list[2],
        }
        #self.rules = rules

    def __repr__(self) -> str:
        return self.courseName

    def retrieveTime(self, day: int) -> np.array:
        return self.slot.retrieveTime(day)

    def retrieveLocation(self) -> str:
        return self.loc

    def save(self) -> None:
        details = {
            self.courseName: {
                "slot": self.slot,
                "course": self.course,
                "location": self.loc,
                "description": self.desc,
            }
        }
        with open("courses.json", "w+") as f:
            json.dump(details, f, indent=6)


def createCourse():
    text = "Enter the following details"
    title = "Course Creation Window"
    choices = list(SLOTS.keys())
    input_list = ["Course Name : ", "Description :", "Location :"]
    courseDetails = multenterbox(text, title, input_list)
    courseTime = choicebox("Select the slot", "Slot Selection", choices)
    course_1 = Course(courseDetails[0], SLOTS[courseTime], courseDetails[2], courseDetails[1])
    coursesList[courseDetails] = course_1

def createSlot():
    slot = Slot()
    SLOTS[slot.slotName] = slot


def ReadSlots():
    for i in FILES:
        with open(f"./slots/{i}", "r") as f:
            data = json.load(f)
            SLOTS[list(data.keys())[0]] = data[list(data.keys())[0]]["slotTimes"]


# Pls implement this
class Calendar:
    def __init__(self, start: datetime.date, end: datetime.date, courses=[], icalobj=Calendar()) -> None:
        self.start = start
        self.end = self.end
        self.end = end
        self.courses = courses
        self.icalObj = icalobj  # TODO

    def addCourse(self, course: Course) -> None:
        self.courses.append(Course)

    def createEvents(course):
        def saveIcal(self, name="cal"):
            with open(name + ".ical", "w") as calFile:
                calFile.write(self.icalObj.to_ical().decode("utf-8"))

    def createEvents(self, course):
        day = self.start
        while day != self.end + datetime.timedelta(days=1):
            # for each day check every slot
            for slot in course.slot.slotTimes:
                if slot.getDay() == day.isoweekday():
                    # add event
                    # TODO implement rule
                    event = Event()
                    event.add('summary', course.attrs["name"])
                    event.add('location', course.attrs["loc"])
                    event.add('description', course.attrs["desc"])
                    event.add("dtstart", datetime.datetime.combine(day, slot.getStart()))
                    event.add("dtend", datetime.datetime.combine(day, slot.getEnd()))
                    self.icalObj.add_component(event)

            day += datetime.timedelta(days=1)
            print(day)
        pass
        # TODO




if __name__ == '__main__':
    ReadSlots()
    while True:
        choice = choicebox("Welcome to calendar app, Please choose one of the options", "Time Table App", ["Create Course", "Export to Ical", "Create Slot", "Upload to Google Calendar","Exit"])
        if choice == "Create Course":
            createCourse()
        elif choice == "Create Slot":
            createSlot()
        elif choice == "Export to Ical":
            pass
        elif choice == "Upload to Google Calendar":
            pass
        elif choice == "Exit":
            exit(0)
=======
import numpy as np
#from APITest import createEvent
import json

#Using ical gives generality, but recurring events feature in google calendar not supported
from icalendar import Calendar, Event
import datetime
from easygui import *
import os

#iso stansard weeks start on monday. can assign 0 or , 1 better.
#TODO change to starting from 0
days = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}

SLOTFILE = "slot.txt"

FILES = os.listdir("./slots")
SLOTS = {}

class Slot():
    def __init__(self, slotName: str, slotTimes: "np.array of TimeRange", rec="WEEKLY") -> None: #I suggest slotTimes as type WeekTime
        self.slotName = slotName
        self.slotTimes = slotTimes
        self.rec = rec
        if self.course:
            self.occupied = True
            
    def addTimes(t1, t2):
        hours = t1.hour + t2.hour
        minutes = t1.minute + t2.minute
        hours += minutes // 60
        minutes %= 60
        new_time = datetime.time(hour=hours, minute=minutes)
        return new_time

    def createSlot(periodLen = 50): #periodLen minutes
        #for creating from cli text input
        name = input("Enter name of slot: ")
        slotTimes=[]
        while "y" in input("Add slot period?: ").lower():
            day = int(input("Enter day number: "))
            time = int(input("Enter start time: "))#militarytime format
            startTime = datetime.time(int(time//100), int(time%100))
            endTime = Slot.addTimes(startTime, datetime.time(0, periodLen))
            slotTimes.append(TimeRange(day, startTime, endTime))
        return Slot(name, slotTimes)
    
    def save(self):
        name = self.slotName
        slotfile = open(f"./slots/{name}", "w") 
        slotfile.write("SLOT START\n")
        name = self.slotName
        slotfile.write(name+"\n")
        for period in slot.slotTimes:
            start = period.startTime
            end = period.endTime
            day = period.day
            slotfile.writelines(["NEW PERIOD\n", str(day)+"\n", str(start)+"\n", str(end) + "\n"])
        slotfile.write("SLOT END\n")
        slotfile.close()
        
        
    def fromGui():
        slotName, slotTimes = 0, 0 #TODO
        #slotTimes = [TimeRange(),]
        return Slot(slotName, slotTimes)
    
    def loadSlots():
        #updates SLOTS and returns it too
        
        d={}
        for i in FILES:
            with open(f"./slots/{i}", "r") as file:
                while True:
                    line  = file.readline().strip()
                    if line == "":
                        break
                    elif line == "SLOT START":
                        slotTimes = []
                        name = file.readline().strip()
                        line  = file.readline().strip()
                        while line != "SLOT END":
                            if line == "NEW PERIOD":
                                day = int(file.readline().strip())
                                start = str(file.readline().strip())
                                end = str(file.readline().strip())
                                startTime = datetime.datetime.strptime(start, '%H:%M:%S').time()
                                endTime = datetime.datetime.strptime(end, '%H:%M:%S').time()
                                slotTimes.append(TimeRange(day, startTime, endTime))
                            line = file.readline().strip()
                        else:
                            d[name] = Slot(name, slotTimes)
        global SLOTS            
        SLOTS = d
        return d
    
    # def retrieveTime(self, day: int) -> np.array:
    #     return self.slotTimes[day-1] #why -1 ?

    # def retrieveCourse(self) -> str:
    #     return self.course
    
    
class TimeRange():
    def __init__(self, day:int, start:datetime.time, end:datetime.time):
        self.day = day
        self.time = start
        self.startTime = start
        self.endTime = end
    def getStart(self):
        return self.startTime
    def __repr__(self):
        return str(self.day) + ":" + str(self.startTime) + "-" + str(self.endTime)
    
    def getEnd(self):
        return self.endTime

# class Rule():
#     def __init__(self, condition, contents: dict):
#         self.content = contents
#         self.condition =condition

class Course():
    def __init__(self, courseName: str, slot: Slot, loc="", desc="") -> None:
        self.courseName = courseName
        self.slot = slot
        self.attrs = {
            "name" : courseName, 
            "loc" : loc, 
            "desc" : desc
            }
        #self.rules = rules
        
    def fromGui():
        courseName, slot = 0, 0 #TODO
        #slot is Slot object
        return Course(courseName, slot)
    
    def __repr__(self) -> str:
        return self.courseName

    # def retrieveTime(self, day: int) -> np.array: 
    #     return self.slot.retrieveTime(day)

    def retrieveLocation(self) -> str:
        return self.loc
    
    # def addRule(self, condition, contents: dict = {"attr" : "val"}) -> None:#conditions is [start, end] where both are WeekTime objs
    #     self.rules.append({condition: contents})
    
    def save(self) -> None:
        details = {
            self.courseName: {
                "slot": self.slot.slotName,
                "location": self.loc,
                "description": self.desc
            }
        }
        with open("courses.json", "a+") as f:
            json.dump(details, f, indent=6)

#implement conditions in courses

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
    
    def createEvents_ical(self, course):
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
            
    def createIcalobj(self, filename ="cal.ical"):
        #assuming empty self.ical object is empty
        for course in self.courses:
            self.createEvents_ical(course)
        self.saveIcal(filename)
        

#TODO add exams functionality


# Example usage
slot = Slot("A", [TimeRange(1, datetime.time(10, 0), datetime.time(10, 50))])
course = Course("MA", slot)
calendar= Calendar(datetime.date(2024, 7, 31), datetime.date(2024, 8, 10), [course] )
calendar.createIcalobj()
slot.save()


#TODO get user input
start, end = datetime.date(1, 1, 1), datetime.date(1, 1, 1)

if False: #__name__ == '__main__':
    CALOBJ = Calendar(start, end)
    while True:
        choice = choicebox("Welcome to calendar app, Please choose one of the options", "Time Table App", ["Create Course", "Export to Ical", "Create Slot", "Upload to Google Calendar","Exit"])
        if choice == "Create Course":
            course = Course.fromGui() #Need to update slots when this is called. after start of loop, new slot could have been created.
            CALOBJ.addCourse(course)
        elif choice == "Create Slot":
            slot = Slot.fromGui()
            slot.save() #not done automatically in __init__ as loaded slots will be saved again.
        elif choice == "Export to Ical":
            filename = 0 #TODO gui
            CALOBJ.createIcalobj()
            CALOBJ.saveIcal(filename)
            #TODO export file to user
        elif choice == "Upload to Google Calendar":
            pass
        elif choice == "Exit":
            exit(0)
        
>>>>>>> b0d5ceb (Created functions for gui interfacing)
