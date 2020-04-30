# _*_ coding: utf-8 _*_
"""
author: QIN ZIXUAN
email: qin.z.aa@m.titech.ac.jp
Tel: 080-7888-0839
Tokyo Institute of Technology
"""

import time
import pygame
from pygame.locals import *
import random

class  Snake_Head(pygame.sprite.Sprite):
	def __init__(self, screen, pos):
		super(Snake_Head,self).__init__()
		self.screen = screen
		self.length = 10
		self.pos = pos
		self.speed = 20
		self.width = 20
		# direction: 1 means right, 2 means down, 3 means left, 4 means up
		self.direction = random.randint(1, 4)
		self.score = 0

	def draw(self):
		# head
		pygame.draw.rect(self.screen,[255,255,255],[self.pos[0],self.pos[1],self.width,self.width],3)

	def move(self):
		if self.direction == 1:
			self.pos[0] += self.speed
			if self.pos[0] > 960:
				self.pos[0] -= 960
		elif self.direction == 2:
			self.pos[1] += self.speed
			if self.pos[1] > 540:
				self.pos[1] -= 540
		elif self.direction == 3:
			self.pos[0] -= self.speed
			if self.pos[0] < 0:
				self.pos[0] += 960
		elif self.direction == 4:
			self.pos[1] -= self.speed
			if self.pos[1] < 0:
				self.pos[1] += 540

	def update(self,pressed_keys):
		# judge pattern
		can_do = []
		can_do.append(self.direction-1)
		can_do.append(self.direction+1)
		for i in range(2):
			if can_do[i] == 0:
				can_do[i] = 4
			elif can_do[i] == 5:
				can_do[i] = 1

		# keyboard control
		if (pressed_keys[K_UP] or pressed_keys[K_w]) and 4 in can_do:
			self.direction = 4
			turn_point.append((self.pos[0],self.pos[1]))
			turn_direction.append(self.direction)
		if (pressed_keys[K_DOWN] or pressed_keys[K_s]) and 2 in can_do:
			self.direction = 2
			turn_point.append((self.pos[0],self.pos[1]))
			turn_direction.append(self.direction)
		if (pressed_keys[K_LEFT] or pressed_keys[K_a]) and 3 in can_do:
			self.direction = 3
			turn_point.append((self.pos[0],self.pos[1]))
			turn_direction.append(self.direction)
		if (pressed_keys[K_RIGHT] or pressed_keys[K_d]) and 1 in can_do:
			self.direction = 1
			turn_point.append((self.pos[0],self.pos[1]))
			turn_direction.append(self.direction)

class  Snake_Body(pygame.sprite.Sprite):
	def __init__(self, screen, pos, direction):
		super(Snake_Body,self).__init__()
		self.screen = screen
		self.pos = pos
		self.speed = 20
		self.width = 20
		# direction: 1 means right, 2 means down, 3 means left, 4 means up
		self.direction = direction

	def draw(self):
		# head
		pygame.draw.rect(self.screen,[255,255,255],[self.pos[0],self.pos[1],self.width,self.width],3)

	def move(self, id):
		if self.direction == 1:
			self.pos[0] += self.speed
			if self.pos[0] > 960:
				self.pos[0] -= 960
		elif self.direction == 2:
			self.pos[1] += self.speed
			if self.pos[1] > 540:
				self.pos[1] -= 540
		elif self.direction == 3:
			self.pos[0] -= self.speed
			if self.pos[0] < 0:
				self.pos[0] += 960
		elif self.direction == 4:
			self.pos[1] -= self.speed
			if self.pos[1] < 0:
				self.pos[1] += 540

		if (self.pos[0], self.pos[1]) in turn_point:
			self.direction = turn_direction[turn_point.index((self.pos[0], self.pos[1]))]
			if id == player.length-1:
				del turn_point[0]
				del turn_direction[0]


# parameters
BLACK = [0,0,0]
GOLD = [255,215,0]
RED = [255,0,0]
WHITE = [255,255,255]
ST = [135,38,87]
GREEN = (0,255,0)
BLUE = (0,0,128)
turn_point = []
turn_direction = []

# initialization
pygame.init()
screen = pygame.display.set_mode((960,540))
pygame.display.set_caption('Greedy Snake')
fontObj = pygame.font.Font('freesansbold.ttf',60)
fontObj_score = pygame.font.Font('freesansbold.ttf',30)
textSurfaceObj = fontObj.render('Game Over!',True,GREEN,BLUE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center=(480,270)

# start window
fontObj_start = pygame.font.Font('freesansbold.ttf',60)
fontObj_name = pygame.font.Font('freesansbold.ttf',20)
fontObj_other = pygame.font.Font('freesansbold.ttf',30)
start = pygame.Surface(screen.get_size()).convert()
start.fill(BLACK)
title = fontObj_start.render('Greedy Snake!', True, [0,0,255])
name = fontObj_name.render('————made by ZIXUAN QIN', True, [0,0,255])
other1 = fontObj_other.render('Press ENTER to start!', True, WHITE)
other2 = fontObj_other.render('Press Q to quit!', True, WHITE)
start_window = True

while start_window:
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
		elif event.type == QUIT:
			running = False

	screen.fill(BLACK)
	screen.blit(title, [280, 120])
	screen.blit(name, [600, 200])
	screen.blit(other1, [350, 360])
	screen.blit(other2, [400, 400])

	pressed_keys = pygame.key.get_pressed()
	if pressed_keys[K_RETURN]:
		start_window = False
	elif pressed_keys[K_q]:
		pygame.quit()
		exit()
	
	pygame.display.update()


# initial player
player = Snake_Head(screen, [100, 100])

# bonus and score settings
sc = fontObj_score.render('Score: {:d}'.format(player.score), True, RED)

# initial body
for i in range(1, player.length):
	if i == 1:
		pre = player
	else:
		pre = locals()['body'+str(i-1)]

	if pre.direction == 1:
		X = pre.pos[0] - pre.width
		Y = pre.pos[1]
	elif pre.direction == 2:
		X = pre.pos[0]
		Y = pre.pos[1] - pre.width
	elif pre.direction == 3:
		X = pre.pos[0] + pre.width
		Y = pre.pos[1]
	elif pre.direction == 4:
		X = pre.pos[0]
		Y = pre.pos[1] + pre.width
	locals()['body'+str(i)] = Snake_Body(screen, [X,Y], pre.direction)


running = True
food = False
food_size = 6
while running:
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
		elif event.type == QUIT:
			running = False

	print(player.pos)
	# print bg and score
	screen.fill(BLACK)
	sc = fontObj_score.render('Score: {:d}'.format(player.score), True, RED)
	screen.blit(sc, [750, 20])

	# each body position
	position = []
	for i in range(1, player.length):
		body = locals()['body'+str(i)]
		position.append((body.pos[0],body.pos[1]))

	# lose the game
	if (player.pos[0], player.pos[1]) in position:
		break

	# judge food
	if food == False:
		pd = True
		while pd:
			food_x = random.randint(10, 950)
			food_y = random.randint(10, 530)
			if food_x % player.speed == 0 and food_y % player.speed == 0 and (food_x,food_y) not in position:
				pd = False
		bonus = random.randint(0,100)
		if bonus in range(0,10):
			food_color = GOLD
		elif bonus in range(10,30):
			food_color = ST
		else:
			food_color = WHITE
		pygame.draw.rect(screen,food_color,[food_x,food_y,20,20],food_size)
		food = True
	else:
		pygame.draw.rect(screen,food_color,[food_x,food_y,20,20],food_size)
		if player.pos[0] == food_x and player.pos[1] == food_y:
			if food_color == GOLD:
				player.score += 50
			elif food_color == ST:
				player.score += 30
			else:
				player.score += 5

			player.length += 1

			pre = locals()['body'+str(player.length-1-1)]
			if pre.direction == 1:
				X = pre.pos[0] - pre.width
				Y = pre.pos[1]
			elif pre.direction == 2:
				X = pre.pos[0]
				Y = pre.pos[1] - pre.width
			elif pre.direction == 3:
				X = pre.pos[0] + pre.width
				Y = pre.pos[1]
			elif pre.direction == 4:
				X = pre.pos[0]
				Y = pre.pos[1] + pre.width
			locals()['body'+str(player.length-1)] = Snake_Body(screen, [X,Y], pre.direction)
			food = False

	# update key_press
	pressed_keys = pygame.key.get_pressed()
	player.update(pressed_keys)

	# draw head
	player.move()
	player.draw()
	# draw body
	for i in range(1, player.length):
		if i == 1:
			pre = player
		else:
			pre = locals()['body'+str(i-1)]

		locals()['body'+str(i)].move(i)
		locals()['body'+str(i)].draw()
	

	time.sleep(0.01)
	pygame.display.update()

running = True
while running:
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
		elif event.type == QUIT:
			running = False

	screen.fill(BLACK)
	sc = fontObj_score.render('Score: {:d}'.format(player.score), True, RED)
	screen.blit(sc, [750, 20])
	screen.blit(textSurfaceObj,textRectObj)

	time.sleep(0.01)
	pygame.display.update()

	