import re
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
import time
from PIL import ImageTk, Image
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from subprocess import run
import subprocess
import webbrowser

path = os.getcwd()

print(path)

root = tk.Tk()
frame = tk.Frame(root, width="600", height="300")

frame.pack(fill=BOTH,expand=True)
#frame.configure(background='#ECECEC')

root.iconphoto(False, tk.PhotoImage(file='palera1nicon.png'))


LAST_CONNECTED_UDID = ""
LAST_CONNECTED_IOS_VER = ""

def detectDevice():
    global LAST_CONNECTED_UDID, LAST_CONNECTED_IOS_VER
    #step 1 technically
    print("Searching for connected device...")
    os.system("idevicepair unpair")
    os.system("idevicepair pair")
    os.system("./palera1n/euphoria_scripts/ideviceinfo > ./palera1n/euphoria_scripts/lastdevice.txt")
    
    time.sleep(2)

    f = open("./palera1n/euphoria_scripts/lastdevice.txt", "r")
    fileData = f.read()
    f.close()

    if("ERROR:" in fileData):
        #no device was detected, so retry user!
        print("ERROR: No device found!")

        messagebox.showinfo("No device detected! 0x404","Try disconnecting and reconnecting your device.")
    else:
        #we definitely have something connected...

        #find the UDID
        start = 'UniqueDeviceID: '
        end = 'UseRaptorCerts:'
        s = str(fileData)

        foundData = s[s.find(start)+len(start):s.rfind(end)]
        UDID = str(foundData)
        LAST_CONNECTED_UDID = str(UDID)

        #find the iOS
        #we definitely have something connected...
        start2 = 'ProductVersion: '
        end2 = 'ProductionSOC:'
        s2 = str(fileData)

        foundData2 = s2[s.find(start2)+len(start2):s2.rfind(end2)]
        deviceIOS = str(foundData2)
        LAST_CONNECTED_IOS_VER = str(deviceIOS)

        if(len(UDID) > 38):
            #stop automatic detection
            timerStatus = 0

            print("Found UDID: "+LAST_CONNECTED_UDID)
            messagebox.showinfo("iDevice is detected!","Found iDevice on iOS "+LAST_CONNECTED_IOS_VER)
#            cbeginExploit10["state"] = "normal"
#            cbeginExploit2["state"] = "normal"
            
            #messagebox.showinfo("Ready to begin!","We are ready to start bypass!")
            
            cbeginExploit10["state"] = "normal"

        else:
            print("Couldn't find your device")
            messagebox.showinfo("Somethings missing! 0x405","Try disconnecting and reconnecting your device.")

def startDFUCountdown():
    print("Get ready to put device into DFU mode...")


def enterRecMode():
    print("Kicking device into recovery mode...")
    os.system("./palera1n/euphoria_scripts/enterrecovery.sh")

def exitRecMode():
    print("Kicking device out of recovery mode...")
    os.system("./palera1n/euphoria_scripts/exitrecovery.sh")
    messagebox.showinfo("Sent command!","Kicked device out of recovery mode!\n\nNow if your device is not exiting recovery mode still and keeps looping to it, either re-jailbreak with the same jailbreak you did or remove the jailbreak you installed.")

def showDFUMessage():
    messagebox.showinfo("Step 1","Put your iDevice into DFU mode.\n\nClick Ok once its ready in DFU mode to proceed.")

def jailbreakIOS15Tethered():
    global LAST_CONNECTED_UDID, LAST_CONNECTED_IOS_VER
    
    #iOSVER = str(LAST_CONNECTED_IOS_VER)
    iOSVer = askstring('Device iOS?', 'What iOS are you trying to jailbreak?')
    
    #check if theres a valid string to continue to reversing jb
    if(len(iOSVer) < 2):
        showinfo('Jailbreak Failed', 'Give me a valid iOS version.')
    else:
        showinfo('Ready to Jailbreak...', 'Hi, iOS '+str(iOSVer)+'. \n\nWe will now attempt to jailbreak iOS '+str(iOSVer)+' Tethered.')
        print("Starting palera1n-mod jailbreak...")
        os.system("idevicepair unpair")
        os.system("idevicepair pair")
        os.system(f"cd ./palera1n/ && ./palera1n.sh --tweaks {iOSVer} ")
        #palera1n code is modified to always pass verbose command with this tool so no need to add verbose at the end
        print("Device is jailbroken!\n")
        showinfo('Jailbreak Success!', 'Device is now jailbroken!')
        
def jailbreakIOS15SemiTethered():
    global LAST_CONNECTED_UDID, LAST_CONNECTED_IOS_VER
    
    #iOSVER = str(LAST_CONNECTED_IOS_VER)
    iOSVer = askstring('Device iOS?', 'What iOS are you trying to jailbreak?')
    
    #check if theres a valid string to continue to reversing jb
    if(len(iOSVer) < 2):
        showinfo('Jailbreak Failed', 'Give me a valid iOS version.')
    else:
        showinfo('Ready to Jailbreak...', 'Hi, iOS '+str(iOSVer)+'. \n\nWe will now attempt to jailbreak iOS '+str(iOSVer)+' Semi-Tethered.')
        print("Starting palera1n-mod jailbreak...")
        os.system("idevicepair unpair")
        os.system("idevicepair pair")
        os.system(f"cd ./palera1n/ && ./palera1n.sh --tweaks {iOSVer} --semi-tethered")
        #palera1n code is modified to always pass verbose command with this tool so no need to add verbose at the end
        print("Device is jailbroken!\n")
        showinfo('Jailbreak Success!', 'Device is now jailbroken!')
        
def reverseSemiORTetheredJailbreakCode():
    iOSVer = askstring('Device iOS?', 'What iOS are you trying to reverse?')
    
    #check if theres a valid string to continue to reversing jb
    if(len(iOSVer) < 2):
        showinfo('Reverse Jailbreak Failed', 'Give me a valid iOS version.')
    else:
        showinfo('Reverse Jailbreak...', 'Hi, {}. \n\nWe will now reverse the jailbreak.'.format(iOSVer))
        os.system("idevicepair unpair")
        os.system("idevicepair pair")
        os.system(f"cd ./palera1n/ && ./palera1n.sh --restorerootfs {iOSVer} ")
        showinfo('Reversed Jailbreak!', 'Jailbreak has been reversed!\n\nDevice should now boot.')
    
def installDependenciesSH():
    print("Running install dep script...")
    os.system("bash ./install_deps.sh")
    print("Ran install deps!")
    messagebox.showinfo("Dependencies done!","We installed the required dependencies!\n\nNow you should be able to use the program without issues!")

def callback(url):
   webbrowser.open_new_tab(url)

def quitProgram():
    print("Exiting...")
    os.system("exit")


root.title('Palera1n GUI v1.2.4 - Made by @ios_euphoria + thanks to @palera1n team')
frame.pack()

# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("paleale.gif"))

# Create a Label Widget to display the text or Image
label = Label(frame, image = img)
label.place(x=150, y=30)

my_label2 = Label(frame,
                 text = "Designed for iOS 15.0 - 16.2")
 
# place the widgets
# in the gui window
my_label2.place(x=300, y=100)

my_label3 = Label(frame,
                 text = "ver 1.2.4")
 
# place the widgets
# in the gui window
my_label3.place(x=10, y=290)

cdetectDevice = tk.Button(frame,
                   text="Pair iDevice",
                   command=detectDevice)
cdetectDevice.place(x=50, y=150)

cbeginExploit10 = tk.Button(frame,
                   text="Tethered Jailbreak",
                   command=jailbreakIOS15Tethered,
                   state="normal")
cbeginExploit10.place(x=230, y=170)

cbeginExploit12 = tk.Button(frame,
                   text="Semi-Tethered Jailbreak",
                   command=jailbreakIOS15SemiTethered,
                   state="normal")
cbeginExploit12.place(x=212, y=200)

reversejailbreak1 = tk.Button(frame,
                   text="Remove Jailbreak",
                   fg='black',
                   command=reverseSemiORTetheredJailbreakCode)
reversejailbreak1.place(x=410, y=250)

cexitRecovery = tk.Button(frame,
                   text="Exit Recovery Mode",
                   command=exitRecMode)
cexitRecovery.place(x=50, y=250)

#installdepen = tk.Button(frame,
#                   text="Install Dependencies",
#                   command=installDependenciesSH)
#installdepen.place(x=400, y=250)

#Create a Label to display the link
link = Label(root, text="Made this GUI @ios_euphoria",font=('Helveticabold', 12), cursor="hand2")
link.place(x=100, y=290)
link.bind("<Button-1>", lambda e:
callback("https://twitter.com/ios_euphoria"))


#Create a Label to display the link
link2 = Label(root, text="Thanks to Jailbreak @palera1n team",font=('Helveticabold', 12), cursor="hand2")
link2.place(x=300, y=290)
link2.bind("<Button-1>", lambda e:
callback("https://twitter.com/palera1n"))

root.geometry("600x320")

root.resizable(False, False)

root.eval('tk::PlaceWindow . center')

root.mainloop()
