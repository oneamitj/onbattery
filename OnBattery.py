# -*- coding: utf-8 -*-
# © iVoIP
# Get power status of the system using ctypes to call GetSystemPowerStatus
# status.ACLineStatus::   0 = not charging, 1 = charging


# takes input from user and shutdown laptop after that time of use in battery and cancels shutdown if power is restored


import ctypes
from ctypes import wintypes
import time
import os
from Tkinter import *
import tkMessageBox
import Tkinter
import threading

#class to identify battery info and status
class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [('ACLineStatus', wintypes.BYTE)]

def main():
    global top
    global entry1
    global b_reset
    global count
    global b_start
    global choice
    global label1
    global var
    count = 2
    top = Tkinter.Tk()#main interface
    #top.iconbitmap('icon.ico')
    top.title("Shutdown")
    x=(0,0,0,0)
    C = Tkinter.Canvas(top, bg="grey",bd=5,scrollregion=x, height=160, width=150,confine="false")
    C.pack()

    label = Label( top,bg="grey", text="Time to wait for power...")
    label.place(bordermode=OUTSIDE,x=10,y=10)

    label1 = Label( top,bg="grey", text="      (Time in Seconds)")
    label1.place(bordermode=OUTSIDE,x=10,y=28)

    label2 = Label( top,bg="grey", text="Not Started!!!")
    label2.place(bordermode=OUTSIDE,x=5,y=150)

    label3 = Label( top,bg="grey", text="© iVoIP")
    label3.place(bordermode=OUTSIDE,x=115,y=150)

    #entry box
    entry1 = Entry(top,fg="black", width=10)
    entry1.place(x=10,y=52)

    entry1.insert(0, '')
    entry1.focus_set()

    #radion button to choose time unit
    var = IntVar()
    choice1 = Radiobutton(top, text="Sec",bg="grey", variable=var, value=1, command=unit)
    choice1.place(x=55,y=52)

    choice2 = Radiobutton(top, text="Mins",bg="grey", variable=var, value=2, command=unit)
    choice2.place(x=100,y=52)

    #button to start job
    b_start = Button(top, text="Start",bg="grey", width=10)
    b_start.place(bordermode=OUTSIDE,x=45,y=80)

    #button to stop job
    b_reset = Button(top, text="Reset",bg="grey", width=8)
    b_reset.place(bordermode=OUTSIDE,x=10,y=120)

    #button to exit (doesn't work)
    b_exit = Button(top, text="Exit",bg="grey", width=8)
    b_exit.place(bordermode=OUTSIDE,x=88,y=120)

    b_start.bind("<Button-1>",callThread)
    b_start.bind("<Return>",callThread)
    entry1.bind("<Return>",callThread)

    b_reset.bind("<Button-1>",reset)
    b_reset.bind("<Return>",reset)

    b_exit.bind("<Button-1>",destroy)
    b_exit.bind("<Return>",destroy)

    top.mainloop()



def unit():#change unit of time (resopnse to radiobutton)
    if var.get()==1:
        txt = "      (Time in Seconds)"
    elif var.get()==2:
        txt = "      (Time in Minutes)"
    label1.config(text=txt)

def callThread(event):#create thread to continuos power check in different thread process
    t=threading.Thread(target=callback,args=())
    t.start()

def callback():#takes input from text box and calls status check function
    reset(event=None)
    global count
    count = 0
    val=entry1.get()
    val=int(val)
    if var.get()==2:
        val*=60
    status(val)

def check_status():#Shows feedback whether thread is running or not
    if count == 1:
        label3 = Label( top,bg="grey", text="Stopped!!!       ")
        label3.place(bordermode=OUTSIDE,x=5,y=150)
    elif count == 0:
        label4 = Label( top,bg="grey", text="Running!!!       ")
        label4.place(bordermode=OUTSIDE,x=5,y=150)

def reset(event):#Stop the running thread
    #b_start.config(state=ACTIVE)
    global count
    count = 1
    check_status()
    if check_battery()==0:
        os.system('shutdown -a')
        print "Stopped!!!"

def destroy(event):#for exit the app (not complete)
    reset(event)
    #top.Destroy()

def status(val):#takes status of power
    print val
    check_status()
    global count
    while(1):#loop till power on battery
        if count == 1:
            return
        if check_battery()==1:
            continue
        elif check_battery()==0:
            break

    localtime = time.asctime(time.localtime(time.time()))#gives current time
    
    #generate system commanand to shutdown computer with custom message
    if val>59:
        cmd='"shutdown /s /f /t '+ str(val) +' /c "Planned Shutdown by user as Battery is Discharging (Shutdown in '+ str(round(val/60.0,2)) + ' Minutes). '
    else:
        cmd='"shutdown /s /f /t '+ str(val) +' /c "Planned Shutdown by user as Battery is Discharging (Shutdown in '+ str(val) + ' Seconds). '
    cmd1=cmd +  'Message Generated at '+ str(localtime)+ '""'
    
    os.system(cmd1)#shutdown at desired time (system call)
    
    while(1):
        if count == 1:
            return
        if check_battery()==1:
            os.system('shutdown -a')
            status(val)

def check_battery():#check power status, return 1 if on power and 0 if on battery
    SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)

    GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
    GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
    GetSystemPowerStatus.restype = wintypes.BOOL

    status = SYSTEM_POWER_STATUS()
    if not GetSystemPowerStatus(ctypes.pointer(status)):
        raise ctypes.WinError()
    print 'ACLineStatus', status.ACLineStatus
    return status.ACLineStatus

if __name__ == "__main__": main()
