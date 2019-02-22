import pyautogui
import socket
import time
import json

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import bluetooth
import sys

UDP_IP = "10.125.64.234"
UDP_PORT = 4445
# Internet # UDP
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT))

cPixelX=0
cPixelY=0
windowResolution = pyautogui.size()
pixelToMeter = 3779527.5590551  / 0.01 # 37.7952755906Pixel / 0.01Meter
mPosX=0
mPosY=0
mVelX=0
mVelY=0
lastTime=0

def resolveCollisionWithBounds():
    global cPixelX
    global cPixelY 
    global mVelX
    global mVelY
    xmax = windowResolution.width
    ymax = windowResolution.height
    xpixel = cPixelX 
    ypixel = cPixelY 

    if (xpixel > xmax):
        cPixelX = xmax
        mVelX = 0
    elif (xpixel < 0):
        cPixelX = 0
        mVelX = 0

    if (ypixel > ymax):
        cPixelY = ymax
        mVelY = 0
    elif (ypixel < 0):
        cPixelY = 0
        mVelY = 0

def updateposition(timeStamp, sx,sy):
    finalT = timeStamp
    global lastTime
    global mPosX
    global mPosY
    global mVelX
    global mVelY
    global dT

    ax = -sx/5
    ay = sy/5

    if(lastTime != 0):
        dT = (finalT - lastTime) / 1000.0
        
        mPosX = mVelX * dT + ax * dT * dT / 2
        mPosY = mVelY * dT + ay * dT * dT / 2

        mVelX = ax * dT
        mVelY = ay * dT

    lastTime = timeStamp

# def moveMouse():
#     xpixel = mPosX * pixelToMeter
#     ypixel = mPosY * pixelToMeter

#     currentPosition = pyautogui.position()
#     newX = xpixel + currentPosition.x
#     newY = ypixel + currentPosition.y
#     pyautogui.moveTo(newX,newY, duration=0)

def moveMouse():
    global cPixelX
    global cPixelY
    cPixelX = mPosX * pixelToMeter
    cPixelY = mPosY * pixelToMeter

    #print(" first posX {}, posY {}, pixelX {}, pixelY {}".format(mPosX,mPosY,cPixelX,cPixelY))
    currentPosition = pyautogui.position()
    cPixelX = cPixelX + currentPosition.x
    cPixelY = cPixelY + currentPosition.y

    #print(" medium posX {}, posY {}, pixelX {}, pixelY {}".format(mPosX,mPosY,cPixelX,cPixelY))
    
    resolveCollisionWithBounds()

    #print(" last posX {}, posY {}, pixelX {}, pixelY {}".format(mPosX,mPosY,cPixelX,cPixelY))
    pyautogui.moveTo(cPixelX,cPixelY, duration=0)

print("start")
uuid = "6d64ed24-16de-4439-8e19-9b4b5dd96737"
service_matches = bluetooth.find_service( uuid = uuid )

if len(service_matches) == 0:
    print("couldn't find the service")
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("connecting to {} on {}".format(name, host))

sockBlue=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sockBlue.connect((host, port))


# Create figure for plotting
fig = plt.figure()

#plot for accX
ax = fig.add_subplot(211)
ts = []
accx = []

#plot for accY
ax2 = fig.add_subplot(212)
accy = []

# This function is called periodically from FuncAnimation
def animate(i, ts, accx, accy):

    data = sockBlue.recv(1024) # buffer size is 1024 bytes
    msg = data.decode('utf-8')
    arr = msg.split("/")
    if(len(arr)>0 and arr[0] != ''): 
        print(arr[0])
        js=None
        try:
            js = json.loads(arr[0])
            # Add x and y to lists
            ts.append(dt.datetime.now())
            accx.append(js["accX"])
            accy.append(js["accY"])

            # Limit x and y lists to 20 items
            ts = ts[-80:]
            accx = accx[-80:]
            accy = accy[-80:]

            # Draw x and y lists
            ax.clear()
            ax.plot(ts, accx)
            
            ax2.clear()
            ax2.plot(ts, accy)

            ax.set_ylim(-9.8,9.8)
            ax.set_ylabel('X')
            ax2.set_ylabel('Y')
            ax2.set_ylim(-9.8,9.8)
            #fig.align_ylabels()
        except:
            print("Fallo")
        

#ani = animation.FuncAnimation(fig, animate, fargs=(ts, accx, accy), interval=10)
#plt.show()
#sockBlue.close()

#FROM BLUETOOTH
while True:
    data = sockBlue.recv(1024) # buffer size is 1024 bytes
    #print("received message: {}".format(data))
    msg = data.decode('utf-8')
    arr = msg.split("/")
    if(len(arr)>0 and arr[0] != ''): 
        print(arr[0])
        js=None
        try:
            js = json.loads(arr[0])
            timestamp = time.time()
            updateposition(timestamp,js["accX"],js["accY"])
            moveMouse()
        except:
            print("fallo")
    
sockBlue.close()



#while True:
    #data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #print("received message: {}".format(data))
    #js = json.loads(data)
    #timestamp = time.time()
    #updateposition(timestamp,js["accX"],js["accY"])
    #moveMouse()

# print()
# print()
# print(pyautogui.onScreen(100,50))

# pyautogui.moveTo(400,300, duration=1)
# pyautogui.moveRel(350,400, duration=1)

# pyautogui.dragTo(200, 350, duration=1) 
# pyautogui.dragRel(350, 200, duration=1)

# pyautogui.moveTo(100,48, duration=1)
# pyautogui.click(x=100, y=48, clicks=2, interval=1, button='left')
# pyautogui.moveTo(200,148, duration=1)
# pyautogui.click(x=200, y=148, clicks=2, interval=1, button='right')
# pyautogui.moveTo(300,248, duration=1)
# pyautogui.click(x=300, y=248, clicks=2, interval=1, button='middle')

# pyautogui.moveTo(600,348, duration=1)
# pyautogui.click(x=600, y=348, clicks=2, interval=1, button='left')

# pyautogui.rightClick()
# pyautogui.middleClick()
# pyautogui.doubleClick()
# pyautogui.tripleClick()

# pyautogui.scroll(400, x=400, y=0)


# nearby_devices = bluetooth.discover_devices(lookup_names=True)
# print("found %d devices" % len(nearby_devices))

# for addr, name in nearby_devices:
#     print("  %s - %s" % (addr, name))