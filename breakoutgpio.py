#####
# Filename:    breakoutgpio.py
# Description: Breakout type game in Python for Pimoroni Unicorn Hat
#              Uses 3 buttons connected to GPIO 20 (left), 26 (right) 
#              and 6 (flap) plus 19 (start).
# Author:      Simon Prickett
#####

from collections import deque
from random import randint
import time
import thread
import unicornhat as UH
import RPi.GPIO as GPIO

#####
# Global variables
#####

ballX = 3
ballY = 6
batX = 2
batSize = 3
ballOnBat = True
score = 0
startPressed = False
buttonAPressed = False
leftPressed = False
rightPressed = False

#####
# Button press callback
#####
def buttonPressed(gpioPinNumber):
	global startPressed
	global buttonAPressed
	global leftPressed
	global rightPressed

	if (gpioPinNumber == 6):
		buttonAPressed = True
	if (gpioPinNumber == 19):
		startPressed = True
	if (gpioPinNumber == 26):
		rightPressed = True
	if (gpioPinNumber == 20):
		leftPressed = True

#####
# Set the playfield to blank
#####
def clearPlayField():
	UH.clear()

#####
# Render the initial wall
#####
def renderWall():
	for n in range(8):
		# TODO make wall depth configurable?
		for m in range(3):
			# TODO make coloured bricks
			UH.set_pixel(n, m, 255, 0, 0)
	UH.show()

#####
# Render the bat
#####
def renderBat():
	global batX
	global batSize

	for n in range(8):
		UH.set_pixel(n, 7, 0, 0, 0)

	for n in range(batSize):
		UH.set_pixel(batX + n, 7, 0, 0, 255)

	UH.show()

def clearBall():
	global ballX
	global ballY

	UH.set_pixel(ballX, ballY, 0, 0, 0)
	UH.show()

#####
# Render the ball
#####
def renderBall():
	global ballX
	global ballY
	global ballOnBat

	if (ballOnBat == True):
		ballY = 6
		ballX = batX + 1

	UH.set_pixel(ballX, ballY, 255, 255, 255)
	UH.show()
	
#####
# Wait for a player to come and start a game, alternate 
# between two images simulating pressing of a button
#####
def waitForPlayer():
	global startPressed

	startPressed = False
	GPIO.add_event_detect(19, GPIO.FALLING, buttonPressed, bouncetime=1000)
	showFrameOne = True
	screen = []

	frameOne = [[ 0, 0, 0, 1, 1, 0, 0, 0 ],
	            [ 0, 0, 0, 1, 1, 0, 0, 0 ],
	            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
	            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
	            [ 0, 0, 1, 1, 1, 1, 0, 0 ],
	            [ 0, 0, 1, 1, 1, 1, 0, 0 ],
	            [ 0, 1, 1, 1, 1, 1, 1, 0 ],
	            [ 0, 0, 0, 0, 0, 0, 0, 0 ]
	           ]

	frameTwo = [[ 0, 0, 0, 1, 1, 0, 0, 0 ],
	            [ 0, 0, 0, 1, 1, 0, 0, 0 ],
	            [ 0, 0, 0, 1, 1, 0, 0, 0 ],
	            [ 0, 0, 0, 1, 1, 0, 0, 0 ],
	            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
	            [ 0, 0, 1, 1, 1, 1, 0, 0 ],
	            [ 0, 1, 1, 1, 1, 1, 1, 0 ],
	            [ 0, 0, 0, 0, 0, 0, 0, 0 ]
	           ]

	while (not startPressed):	
		if (showFrameOne):
			screen = frameOne
		else:
			screen = frameTwo

		showFrameOne = not showFrameOne

		for y in range(8):
			for x in range(8):
				r = screen[y][x] * 255
				UH.set_pixel(x, y, r, 0, 0)

		UH.show()

		time.sleep(1)

	GPIO.remove_event_detect(19)

#####
# Game ended, display score and end screen
#####
def gameEnded():
	global score
	print "TODO"

#####
# Play an instance of the game
#####
def playGame():
	global score
	global gameOver
	global buttonAPressed
	global leftPressed
	global rightPressed
	global batX
	global batSize
	global ballOnBat

	score = 0
	gameOver = False

	GPIO.add_event_detect(6, GPIO.FALLING, buttonPressed, bouncetime=200)
	GPIO.add_event_detect(26, GPIO.FALLING, buttonPressed, bouncetime=50)
	GPIO.add_event_detect(20, GPIO.FALLING, buttonPressed, bouncetime=50)

	clearPlayField()
	renderWall()

	while (not gameOver):
		# TODO game logic

		clearBall()

		if (buttonAPressed):
			buttonAPressed = False
			if (ballOnBat == True):
				# Release the ball
				ballOnBat = False
		if (not GPIO.input(20)):
			leftPressed = False
			if (batX > 0):
				batX -=1
		if (not GPIO.input(26)):
			rightPressed = False
			if (8 > (batX + batSize)):
				batX += 1 

		renderBat()
		renderBall()
		time.sleep(0.1)

	GPIO.remove_event_detect(6)
	GPIO.remove_event_detect(26)
	GPIO.remove_event_detect(20)

#####
# Hardware setup
#####

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#####
# Entry point, main loop
#####
while (True):
	waitForPlayer()
	playGame()
	gameEnded()
