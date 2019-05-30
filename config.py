'Configuration of global variables and settings for every file'

'PLC.py'
isBusy = False
x = 0
y = 0

'arm.py'
isCutting, isReleasing,isGrabbing,isClosingIn = False,False,False,False
isReady = True

'vision.py'
process = None
PORT = 'COM3'