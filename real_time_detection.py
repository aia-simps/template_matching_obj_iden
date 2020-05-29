import cv2 as cv
import numpy as np
from time import time

import win32gui, win32ui, win32con

class WindowCapture:

  #properties / Attributes
  screen_width = 0
  screen_height = 0
  hwnd = None
  cropped_x = 0
  cropped_y = 0
  offset_x = 0
  offset_y = 0

  #constructor
  def __init__(self, window_name):
    
    self.hwnd = win32gui.FindWindow(None, window_name)
    if not self.hwnd:
      raise Exception('Window not found: {}'.format(window_name))

    #gets the size of the window automatically
    window_dimension = win32gui.GetWindowRect(self.hwnd)
    self.screen_width = window_dimension[2] - window_dimension[0]
    self.screen_height = window_dimension[3] - window_dimension [1]

    #accounts for border and title bar and crops
    border_pixels = 8
    title_pixels = 30
    self.screen_width = self.screen_width - (border_pixels * 2) #left and right border
    self.screen_height = self.screen_height - title_pixels - border_pixels
    self.cropped_x = border_pixels
    self.cropped_y = title_pixels

    #set the cropped coords offset so can translate screencap into actual screen locations
    self.offset_x = window_dimension[0] + self.cropped_x
    self.offset_y = window_dimension[1] + self.cropped_y


  #screenshot code makes use of windows ONLY library
  def getScreenshot(self):

    #get window image data
    wDC = win32gui.GetWindowDC(self.hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, self.screen_width, self.screen_height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0), (self.screen_width, self.screen_height), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (self.screen_height, self.screen_width, 4)

    #free resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(self.hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    #drop alpha channel otherwise cv.matchTemplate will throw error
    img = img[...,:3]
    #make array contiguous values or cv cannot draw rectangles
    img = np.ascontiguousarray(img)

    return img

  
  #provides relative screen locations of client. Relative position is only calculated once
  #at the start of the program in the object constructor, so do not move the client window
  #after the script has started.
  def getScreenLocation(self, pos):
    return (pos[0] + self.offset_x, pos[1] + self.offset_y)


wincap = WindowCapture('Ikov') #create object for screencapping
loop_time = time()
while(True):

  screenshot = wincap.getScreenshot()

  cv.imshow('Computer Vision', screenshot)
  print('FPS {}'.format(1 / (time() - loop_time)))
  loop_time = time()

  #press 'q' with ouput window focused to exit
  #waits 1ms every loop to process key
  if cv.waitKey(1) == ord('q'):
    cv.destroyAllWindows()
    break

print('Done.')