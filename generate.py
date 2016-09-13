#!/usr/bin/env python

from turtle import *
import random

frameHeight_g	= 750
frameWidth_g	=  ((1 + sqrt(5)) / 2) * frameHeight_g # golden ratio
vDivs_g			= 5
hDivs_g			= 8
divHeight_g		= frameHeight_g / vDivs_g
divWidth_g		= frameWidth_g / hDivs_g
canvas_g		= ""
leftEdge_g		= 0
topEdge_g		= 0
rightEdge_g		= 0
bottomEdge_g	= 0
allPoints_g		= []
polygons_g		= [] # order of points is bottom left first, going counterclockwise
skewMargin_g	= 70

def drawCanvas():
	global canvas_g, leftEdge_g, topEdge_g, rightEdge_g, bottomEdge_g

	penup()
	goto(-frameWidth_g / 2, -frameHeight_g / 2)
	pendown()

	begin_poly()
	setheading(0)
	forward(frameWidth_g)
	left(90)
	forward(frameHeight_g)
	left(90)
	forward(frameWidth_g)
	left(90)
	end_poly()
	forward(frameHeight_g)
	left(90)
	canvas_g		= get_poly()
	leftEdge_g		=  canvas_g[0][0] # all edge info can be derived from first (bottom left) point because canvas is centered
	topEdge_g		= -canvas_g[0][1]
	rightEdge_g		= -canvas_g[0][0]
	bottomEdge_g	=  canvas_g[0][1]

def populateInteriorPoints():
	heightMarkers = []
	widthMarkers = []

	penup()
	goto(canvas_g[0]) # first element is bottom left corner because of how it's drawn
	setheading(90)

	# vertical first
	for i in range(0, vDivs_g - 1): # minus one to discard first and last
		forward(divHeight_g)
		heightMarkers.append(ycor())

	# horizontal next
	goto(canvas_g[0]) # first element is bottom left corner because of how it's drawn
	setheading(0)

	for i in range(0, hDivs_g - 1): # minus one to discard first and last
		forward(divWidth_g)
		widthMarkers.append(xcor())

	# thanks: http://stackoverflow.com/a/19334433/2929868
	coordinates = [(x,y) for x in widthMarkers for y in heightMarkers]
	return coordinates

def populateExteriorPoints():
	coordinates = []
	goto(canvas_g[0]) # first element is bottom left corner because of how it's drawn
	setheading(0)
	# bottom edge
	for i in range(0, hDivs_g):
		coordinates.append(position())
		forward(divWidth_g)
	left(90)
	# right edge
	for i in range(0, vDivs_g):
		coordinates.append(position())
		forward(divHeight_g)
	left(90)
	# top edge
	for i in range(0, hDivs_g):
		coordinates.append(position())
		forward(divWidth_g)
	left(90)
	# left edge
	for i in range(0, vDivs_g):
		coordinates.append(position())
		forward(divHeight_g)

	return coordinates

def skewPoints(points):
	skewedPoints = []

	# lowerSkewBound = -divHeight_g / 2.5
	# upperSkewBound = divHeight_g / 2.5

	lowerSkewBound = -skewMargin_g
	upperSkewBound = skewMargin_g

	for point in points:
		skewedPoint = ()
		for component in point:
			skewFactor = random.uniform(lowerSkewBound, upperSkewBound)
			component = component + skewFactor
			skewedPoint += (component,)
		skewedPoints.append(skewedPoint)
	return skewedPoints

def getKey(item):
	return item[1]

def sortInteriorPoints(points):
	rows = []

	sortedPoints = sorted(points, key = getKey, reverse = True)

	i = 0
	currentRow = []

	for point in sortedPoints:
		currentRow.append(point)

		if i % (hDivs_g - 1) == (hDivs_g - 2): # bane of my existence
			rows.append(currentRow)
			currentRow = []

		i += 1

	for row in rows:
		row.sort()

	return rows

def sortExteriorPoints(points):
	rows = []

	sortedPoints = sorted(points, key = getKey, reverse = True)

	i = 0
	currentRow = []

	for point in sortedPoints:
		currentRow.append(point)

		# if we're at the right most edge, append the current row and clear it
		if (point[0] >= rightEdge_g - 1) and (point[0] <= rightEdge_g + 1): # account for decimal rounding errors ffs
			rows.append(currentRow)
			currentRow = []

	return rows

def combinePoints(interiorPoints, exteriorPoints):
	rows = []
	i = 0

	for row in exteriorPoints:
		if len(row) == 2:
			row[1:1] = interiorPoints[i] # thanks: http://stackoverflow.com/a/23181066/2929868
			i += 1
		rows.append(row)

	return rows

def drawFunkyGrid():
	# horizontals
	for row in allPoints_g[1:-1]:
		penup()
		for point in row:
			goto(point)
			pendown()

	penup()

	# verticals
	columnIndex = 1 # start at second point
	for topOfColumn in allPoints_g[0][1:-1]: # top row of points
		penup()
		goto(topOfColumn)
		for rowIndex in range(0, vDivs_g + 1):
			goto(allPoints_g[rowIndex][columnIndex])
			pendown()
		columnIndex += 1

	penup()

def registerPolygons():
	global polygons_g
	ul = [] # upper left coordinates
	ur = [] # upper right coordinates
	bl = [] # bottom left coordinates
	br = [] # bottom right coordinates

	for row in allPoints_g[:-1]:
		for point in row[:-1]:
			ul.append(point)

	for row in allPoints_g[:-1]:
		for point in row[1:]:
			ur.append(point)

	for row in allPoints_g[1:]:
		for point in row[:-1]:
			bl.append(point)

	for row in allPoints_g[1:]:
		for point in row[1:]:
			br.append(point)

	for i in range(0, len(ul)): # all four should be same size
		poly = (bl[i], br[i], ur[i], ul[i])
		polygons_g.append(poly)

	# clear()

	# for poly in polygons_g:
	# 	penup()
	# 	for point in poly:
	# 		goto(point)
	# 		# dot()
	# 		pendown()
	# 	goto(poly[0])

def spiral(polygon, direction, deviance):
	penup()
	startingIndex = random.randint(0,3)
	startingCorner = polygon[startingIndex]
	goto(startingCorner)

	# bottom left
	if startingIndex == 0:

		if direction == 'clock':

			# turn to face 3
			setheading(towards(polygon[3]))

			# offset from deviance
			forward(deviance) # this will replace the starting corner

			# draw line
			pendown()
			goto(polygon[1])
			penup()

		else:

			# turn to face 1
			setheading(towards(polygon[1]))

			# offset from deviance
			forward(deviance) # this will replace the starting corner

			# draw line
			pendown()
			goto(polygon[3])
			penup()

	# bottom right
	elif startingIndex == 1:

		if direction == 'clock':

			# turn to face 0
			setheading(towards(polygon[0]))

			# offset from deviance
			forward(deviance) # this will replace the starting corner

			# draw line
			pendown()
			goto(polygon[2])
			penup()

		else:

			# turn to face 2
			setheading(towards(polygon[2]))

			# offset from deviance
			forward(deviance) # this will replace the starting corner

			# draw line
			pendown()
			goto(polygon[0])
			penup()

	# top right
	elif startingIndex == 2:

		if direction == 'clock':

			# turn to face 1
			setheading(towards(polygon[1]))

			# offset from deviance
			forward(deviance) # this will replace the starting corner

			# draw line
			pendown()
			goto(polygon[3])
			penup()

		else:

			# turn to face 3
			setheading(towards(polygon[3]))

			# offset from deviance
			forward(deviance) # this will replace the starting corner

			# draw line
			pendown()
			goto(polygon[1])
			penup()

	# top left
	elif startingIndex == 3:

		if direction == 'clock':

			# turn to face 2
			setheading(towards(polygon[2]))

			# offset from deviance
			forward(deviance) # this will replace the starting corner

			# draw line
			pendown()
			goto(polygon[0])
			penup()

		else:

			# turn to face 0
			setheading(towards(polygon[0]))

			# offset from deviance
			forward(deviance) # this will replace the starting corner

			# draw line
			pendown()
			goto(polygon[2])
			penup()

	# polygon is which shape to spiral
	# startingCorner is which corner to start in
	# direction is clockwise or counterclockwise
	# deviance is how many pixels away from the current edge the end of the line will be
	# 	deviance could also be done as:
	# 	- a percentage of the opposing side
	# 	- a percentage of the angle
	# 	- a raw angle (e.g. 5 degrees)
	# 	should we have options for all of these?

	# function outline:
	# pen up
	# jump to starting corner
	#
	# definitely gonna be using towards(x, y)
	# so how to get x, y?

def main():
	global allPoints_g
	speed(0)
	drawCanvas()

	# For all positive integers NUM and DEN <= 10, where NUM > DEN, the combination 
	# 8/5 (1.6) yielded the closest decimal approximation to the golden ratio (1.61803398875).
	# Therefore, a canvas of golden ratio proportions can be divided using 8 segments
	# on the long side, and 5 segments on the short side. The cells made as a result
	# of the segmented sides are the closest to squares that such cells could get
	# without altering the canvas proportions.

	interiorPoints = populateInteriorPoints()
	skewedInteriorPoints = skewPoints(interiorPoints)

	exteriorPoints = populateExteriorPoints()

	sortedSkewedInteriorPoints = sortInteriorPoints(skewedInteriorPoints)

	sortedExteriorPoints = sortExteriorPoints(exteriorPoints) # what the fuck this was just fucking working

	allPoints_g = combinePoints(sortedSkewedInteriorPoints, sortedExteriorPoints)

	# hideturtle()
	speed(10)
	setheading(90)

	drawFunkyGrid()

	registerPolygons()

	for poly in polygons_g:
		spiral(poly, 'clock', 15)

	exitonclick()

if __name__ == '__main__':
	main()

# setheading(towards(0, 0))
# goto(0, 0)
