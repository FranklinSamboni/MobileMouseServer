import pyautogui
import socket
import time
import json

UDP_IP = "10.125.64.234"
UDP_PORT = 4445
# Internet # UDP
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT))
pos = pyautogui.position()
windowResolution = pyautogui.size()
pixelToMeter = 3779527.5590551  / 0.01 # 37.7952755906Pixel / 0.01Meter
mPosX=0
mPosY=0
mVelX=0
mVelY=0
lastTime=0

def updateposition(timeStamp, ax,ay):
    finalT = timeStamp
    global lastTime
    global mPosX
    global mPosY
    global mVelX
    global mVelY

    mPosX = -mPosX/5
    mPosY = -mPosY/5

    if(lastTime != 0):
        dT = (finalT - lastTime) / 1000.0
        
        mPosX = mVelX * dT + ax * dT * dT / 2
        mPosY = mVelY * dT + ay * dT * dT / 2

        mVelX = ax * dT
        mVelY = ay * dT

    lastTime = timeStamp

def moveMouse():
    xpixel = mPosX * pixelToMeter
    ypixel = mPosY * pixelToMeter

    currentPosition = pyautogui.position()
    newX = xpixel + currentPosition.x
    newY = ypixel + currentPosition.y
    pyautogui.moveTo(newX,newY, duration=0)


print("start")
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: {}".format(data))
    js = json.loads(data)
    timestamp = time.time()
    updateposition(timestamp,js["accX"],js["accY"])
    moveMouse()

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