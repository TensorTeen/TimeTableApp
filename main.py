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