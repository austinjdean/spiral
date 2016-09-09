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

def spiral(polygon, startingCorner, direction, deviance):
	pass
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
	lowerSkewBound = -30 # make these changeable later
	upperSkewBound = 30
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
	pass

def main():
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

	allPoints = combinePoints(sortedSkewedInteriorPoints, sortedExteriorPoints)

	# hideturtle()
	speed(6)
	setheading(90)

	for row in allPoints:
		for point in row:
			print point
			goto(point)
			dot()

	exitonclick()

if __name__ == '__main__':
	main()

# setheading(towards(0, 0))
# goto(0, 0)
