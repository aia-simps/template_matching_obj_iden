import cv2 as cv
import numpy as np

parent_img = cv.imread('eastVarrock.png', cv.IMREAD_UNCHANGED)
child_ore_img = cv.imread('ironOre.png', cv.IMREAD_UNCHANGED)

result_match_template = cv.matchTemplate(parent_img, child_ore_img, cv.TM_SQDIFF_NORMED)

#cv.imshow('Output', result_match_template)
#cv.waitKey()   #shows the template matching. Showing most similar part of parent image to child
#print(result_match_template)

#positive ID threshold
threshold = 0.004

#np.where returns two arrays of x's and y's matching locations
# IE: (array([573, 573, 574, 641, 642, 642, 642, 643], dtype=int64), array([1165, 1166, 1166, 1164, 1163, 1164, 1165, 1164], dtype=int64))
identified_locations = np.where(result_match_template <= threshold)
print(identified_locations)

#zip these into (x,y) tuples for use
#[(1165, 573), (1166, 573), (1166, 574), (1164, 641), (1163, 642), (1164, 642), (1165, 642), (1164, 643)]
# *: unpacks x & y's  -  zip: joins corresponding XY pairs  -  list into list object
identified_locations = list(zip(*identified_locations[::-1]))
print(identified_locations)


if identified_locations:
  print('Iron Ore Identified.')

  child_width = child_ore_img.shape[1]
  child_height = child_ore_img.shape[0]
  line_color = (0, 255, 0)
  line_type = cv.LINE_4

  for loc in identified_locations: #loop over all positive ID's

    top_left = loc  #box position
    bottom_right = (top_left[0] + child_width, top_left[1] + child_height)
    #draw rectangle
    cv.rectangle(parent_img, top_left, bottom_right, line_color, line_type)

  cv.imshow('Output', parent_img)
  cv.waitKey()
  #cv.imwrite('highlightedOre.jpg', parent_img) #saves image as file extension you give

else:
  print('No Ore Found.')