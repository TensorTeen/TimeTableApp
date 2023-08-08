import numpy as np
from APITest import createEvent
import json 
from easygui import *

d = {}

days = {
    "Sunday": 0,
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
                "slotTimes" : self.slotTimes.tolist(),
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
                "description": self.desc,
            }
        }
        with open("courses.json","a+") as f:
            json.dump(details,f,indent=6)
    

def createSlot():
    text = "Enter the following details"
    title = "Slot Creation Window"  
    input_list = ["Slot Name : ",]
    #SlotDetails = multenterbox(text, title, input_list)
    SlotDetails = ["A"]
    input_list = []
    for i in days:
        input_list.extend([i + "Start ", i + " End"])
    #SlotTimes = np.array(multenterbox(text,title,input_list))
    SlotTimes = np.array(['', '', '08:00', '08:50', '13:00', '13:50', '', '', '11:00', '11:50', '10:00',
 '10:50', '', '',]).reshape(7,2)
    print(SlotDetails,SlotTimes)
    slot_1 = Slot(SlotDetails[0],SlotTimes)
    slot_1.save()


def createCourse():
    text = "Enter the following details"
    title = "Slot Creation Window"  
    input_list = ["Slot Name : ",]
    SlotDetails = multenterbox(text, title, input_list)
    #ils = ["A"]
    input_list = []
    for i in days:
        input_list.extend([i + "Start ", i + " End"])
    SlotTimes = np.array(multenterbox(text,title,input_list))
    #SlotTimes = np.array(['', '', '08:00', '08:50', '13:00', '13:50', '', '', '11:00', '11:50', '10:00',
# '10:50', '', '',]).reshape(7,2)
    course_1 = Slot(SlotDetails[0],SlotTimes)
    d[SlotDetails] = course_1
    



