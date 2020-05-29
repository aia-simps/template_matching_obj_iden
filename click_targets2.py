import cv2 as cv
import numpy as np


parent_img = cv.imread('eastVarrock.png', cv.IMREAD_UNCHANGED)
child_ore_img = cv.imread('ironOre.png', cv.IMREAD_UNCHANGED)

child_width = child_ore_img.shape[1] #img size
child_height = child_ore_img.shape[0]

result_match_template = cv.matchTemplate(parent_img, child_ore_img, cv.TM_SQDIFF_NORMED)

#cv.imshow('Output', result_match_template)
#cv.waitKey()   #shows the template matching. Showing most similar part of parent image to child
#print(result_match_template)

#positive ID threshold
threshold = 0.01

#np.where returns two arrays of x's and y's matching locations
# IE: (array([573, 573, 574, 641, 642, 642, 642, 643], dtype=int64), array([1165, 1166, 1166, 1164, 1163, 1164, 1165, 1164], dtype=int64))
identified_locations = np.where(result_match_template <= threshold)
#print(identified_locations)

#zip these into (x,y) tuples for use
#[(1165, 573), (1166, 573), (1166, 574), (1164, 641), (1163, 642), (1164, 642), (1165, 642), (1164, 643)]
# *: unpacks x & y's  -  zip: joins corresponding XY pairs  -  list into list object
identified_locations = list(zip(*identified_locations[::-1]))
#print(identified_locations)


#create list of overlapping rectangle identifications so stop thick lines
#and multiple identifications of same object. in form [x, y, w, h]
rectangles = []
for loc in identified_locations:
  rect = [int(loc[0]), int(loc[1]), child_width, child_height]
  rectangles.append(rect)
  rectangles.append(rect)
print(rectangles)

#requires at least 2 results, so will remove a single detection result
#this is why there are two appends above
rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
print(rectangles)

if len(rectangles):
  print('Iron Ore Identified.')

  line_color = (0, 255, 0)
  line_type = cv.LINE_4
  marker_color = (255, 0, 255)
  marker_type = cv.MARKER_CROSS

  for (x, y, w, h) in rectangles: #loop over all positive ID's
    '''
    top_left = (x, y)  #box position
    bottom_right = (x + w, y + h)
    #draw rectangle
    cv.rectangle(parent_img, top_left, bottom_right, line_color, line_type)
    '''

    center_x = x + int(child_width/2)
    center_y = y + int(child_height/2)
    cv.drawMarker(parent_img, (center_x, center_y), marker_color, marker_type)

  cv.imshow('Output', parent_img)
  cv.waitKey()
  #cv.imwrite('highlightedOre.jpg', parent_img) #saves image as file extension you give

else:
  print('No Ore Found.')