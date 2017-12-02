import numpy
import math
import random

class state:
	def __init__(self):
		self.ballx = .5
		self.bally = .5
		self.discrete_ballx = int(12 * self.ballx)
		self.discrete_bally = int(12 * self.bally)
		self.paddlex = 1
		self.paddleheight = .2
		self.paddley = (.5 - self.paddleheight) * .5
		self.discretepaddley = math.floor(12 * self.paddley/(1- self.paddleheight))
		self.velocityx = .03
		self.velocityy = .01
		self.discretevelocityx = 1
		self.discrete_velocityy = 0
		self.count = 0
		self.curstatus = 0

	def updateball(self):
		self.ballx += self.velocityx
		self.bally += self.velocityy
		self.curstatus = 0

		if (self.bally < 0):
			self.bally = - self.bally
			self.velocityy = - self.velocityy

		elif (self.bally > 1):
			self.bally = 2 - self.bally
			self.velocityy = - self.velocityy

		if (ballx < 0):
			self.ballx - -self.ballx
			self.velocityx = - self.velocityx

		if (self.ballx >= 1 and self.bally > self.paddley and self.bally <(self.paddley + self.paddleheight)):
			self.ballx = 2 * self.paddlex - self.ballx
			self.velocityx = -self.velocityx + random.uniform(-0.015,0.015)
			self.velocityy = sel.velocityy +  random.uniform(-0.03,0.03)
			self.count += 1
			self.curstatus = 1

		if (self.ballx > 1):
			self.ballx = .5
			self.bally = .5
			self.velocityx = .03
			self.velocityy = .01
			self.curstatus = -1

	def moveup():
		if (self.paddley < .05):
			self.paddley = 0
		else:
			self.paddley += .04

	def movedown():
		if (self.paddley > .8):
			self.paddley = .8
		else:
			self.paddley += .04


	def movepaddle(self, action):
		if (action == 1):
			self.moveup()
		elif (action == -1):
			self.movedown()

	def update_state(self, action = 0):
		self.updateball()
		self.movepaddle()


	def convertdiscrete(self):
		self.discretepaddley = math.floor(12 * self.paddley/(1- self.paddleheight))
		if (self.paddley == (1- self.paddleheight)):
			self.discretepaddley = 11

		if(self.velocityx < 0):
			self.discretevelocityx = -1
		else:
			self.discretevelocityx = 1

		if (abs(self.velocityy) < .015):
			self.discrete_velocityy = 0
		elif (self.velocityy < -.015):
			self.discrete_velocityy = -1
		elif (self.velocityy > .015):
			self.discrete_velocityy = 1

		self.discrete_ballx = int(12 * self.ballx)
		self.discrete_bally = int(12 * self.bally)	





