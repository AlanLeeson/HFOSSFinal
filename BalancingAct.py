#!/usr/bin/python
import pygame
import random
from gi.repository import Gtk


class BalancingAct:
    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()

        self.x = -100
        self.y = 100

        self.vx = 10
        self.vy = 0

        self.solution = 0
    	self.userSolution = 0
    	self.operator = "+"
    	self.leftHandMultiplier = 0
    	self.rightHandMultiplier = 0
    	self.leftHandNumber = 0
    	self.rightHandNumber = 0

        self.fired = 0
        self.cooldown = 300

        self.paused = False
        self.direction = 1

        #color palette
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.green = (100,255,100)
        self.bright_green = (0,255,0)
        self.red = (255,100,100)
        self.bright_red = (255,0,0)


    def set_paused(self, paused):
        self.paused = paused

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass
    
    # Create the math equation
    def create_equation(self):
    	self.reload_data()
    	self.solution = random.randint(10,30)
    	self.leftHandMultiplier = int(str(self.solution)[0]) * 2
    	secondDigit = int(str(self.solution)[1])

    	if secondDigit  % 2 == 0 and secondDigit > 2:
    	    self.rightHandMultiplier = secondDigit / 2
    	else: 
    	    self.rightHandMultiplier = secondDigit

    # zero equations and data
    def reload_data(self):
    	self.leftHandNumber = 0
    	self.rightHandNumber = 0
    	self.userSolution = 0

    # calculate the user input
    def calculate_equation(self):
    	leftProduct = self.leftHandMultiplier * self.leftHandNumber
    	rightProduct = self.rightHandMultiplier * self.rightHandNumber
    	
    	if self.operator == "+":
    	    self.userSolution = leftProduct + rightProduct
    	elif self.operator == "-":
    	    self.userSolution = leftProduct - rightProduct

    	if self.userSolution == self.solution:
    	    self.create_equation()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, self.black)
        return textSurface, textSurface.get_rect()

    def button(self,msg,over,off,x,y,w,h,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        now = pygame.time.get_ticks()

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.screen, over,(x,y,w,h))

            if click[0] == 1 and action != None and self.fired + self.cooldown < now:
                action() 
        else:
            pygame.draw.rect(self.screen, off,(x,y,w,h))

        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.screen.blit(textSurf, textRect)

    def increaseLeft(self):
        self.fired = pygame.time.get_ticks()
        if self.leftHandNumber < 10:
            self.leftHandNumber += 1
        self.calculate_equation()

    def increaseRight(self):
        self.fired = pygame.time.get_ticks()
        if self.rightHandNumber < 10:
            self.rightHandNumber += 1
        self.calculate_equation()

    def decreaseLeft(self):
        self.fired = pygame.time.get_ticks()
        if self.leftHandNumber > 0:
            self.leftHandNumber -= 1
        self.calculate_equation()

    def decreaseRight(self):
        self.fired = pygame.time.get_ticks()
        if self.rightHandNumber > 0:
            self.rightHandNumber -= 1
        self.calculate_equation()

    # The main game loop.
    def run(self):
        self.running = True

        self.screen = pygame.display.get_surface()

        while self.running:
            # Pump GTK messages.
            while Gtk.events_pending():
                Gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.direction = -1
                    elif event.key == pygame.K_RIGHT:
                        self.direction = 1


            # Clear Display
            self.screen.fill(self.white)  # 255 for white

            # Draw increase buttons
            self.button('up',self.bright_green,self.green,200,400,100,50,self.increaseLeft)
            self.button('up',self.bright_green,self.green,500,400,100,50,self.increaseRight)

            # Draw decrease buttons
            self.button('down',self.bright_red,self.red,200,500,100,50,self.decreaseLeft)
            self.button('down',self.bright_red,self.red,500,500,100,50,self.decreaseRight)

    	    #Draw text
    	    myFont = pygame.font.SysFont("monospace",60)
    	    leftSideLabel = myFont.render(str(self.leftHandNumber) + 
    		" x " + str(self.leftHandMultiplier) + " " +
    		str(self.operator) + " " +
    		str(self.rightHandNumber) + " x " + 
    		str(self.rightHandMultiplier) + " = " +
    		str(self.userSolution),1,(25,25,255))

    	    rightSideLabel = myFont.render("Goal = " + str(self.solution),1,(255,25,25))

    	    self.screen.blit(leftSideLabel,(100,100))
    	    self.screen.blit(rightSideLabel,(100,150))

            # Flip Display
            pygame.display.flip()

            # Try to stay at 30 FPS
            self.clock.tick(30)





# This function is called when the game is run directly from the command line:
# ./TestGame.py
def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = BalancingAct()
    game.create_equation()
    game.run()

if __name__ == '__main__':
    main()
