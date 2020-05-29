import cv2 as cv
import numpy as np

parent_img = cv.imread('eastVarrock.png', cv.IMREAD_UNCHANGED)
child_ore_img = cv.imread('ironOre.png', cv.IMREAD_UNCHANGED)

result_match_template = cv.matchTemplate(parent_img, child_ore_img, cv.TM_CCOEFF_NORMED)

#cv.imshow('Output', result_match_template)
#cv.waitKey()   #shows the template matching. Showing most similar part of parent image to child

#retrieves pixel location of most similar image subsection
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result_match_template)

print('Best match top left position: %s' % str(max_loc))
print('Best match confidence: %s' % max_val)

#positive ID threshold
threshold_value = 0.8
if max_val >= threshold_value:

  print('Iron Ore Identified.')

  child_width = child_ore_img.shape[1]
  child_height = child_ore_img.shape[0]

  top_left = max_loc
  bottom_right = (top_left[0] + child_width, top_left[1] + child_height)

  cv.rectangle(parent_img, top_left, bottom_right,
               color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

  cv.imshow('Output', parent_img)
  cv.waitKey()
  #cv.imwrite('highlightedOre.jpg', parent_img) #saves image as file extension you give

else:
  print('No Ore Found.')