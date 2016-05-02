#!/usr/bin/python
import pygame
import random
import math
from gi.repository import Gtk

def enum(**enums):
    return type('Enum', (), enums)

class BalancingAct:

    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()

        self.screenWidth = pygame.display.Info().current_w
	self.screenHeight = pygame.display.Info().current_h
	
        self.solution = 0
    	self.userSolution = 0
    	self.operator = "+"
    	self.leftHandMultiplier = 0
    	self.rightHandMultiplier = 0
    	self.leftHandNumber = 0
    	self.rightHandNumber = 0

        #numbers to calculate left side of scale
        self.weight = 1.0
        self.scaleWidth = 300
        self.scaleHeight = 30
        self.scaleBasePositionX = self.screenWidth/4
        self.scaleBasePositionY = self.screenHeight * 0.65
        self.scaleCurrentPosition = 0.0
        self.scaleCorrectPosition = 0.0
        self.scaleSpeed = 1.0

        self.correct = False
        self.buttonsEnabled = True

        self.fired = 0
        self.cooldown = 300

        self.playStates = enum(Menu=0,Play=1,Paused=2)
        self.currentPlayState = self.playStates.Play
        self.paused = False
        self.direction = 1

        #color palette
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.green = (100,255,100)
        self.bright_green = (0,255,0)
        self.red = (255,100,100)
        self.bright_red = (255,0,0)
        self.blue = (100,100,255)
        self.bright_blue = (0,0,255)

    # Called to pause the game
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
    	self.solution = random.randint(10,30)
    	self.leftHandMultiplier = int(str(self.solution)[0]) * 2
    	secondDigit = int(str(self.solution)[1])

    	if secondDigit  % 2 == 0 and secondDigit > 2:
    	    self.rightHandMultiplier = secondDigit / 2
    	else: 
    	    self.rightHandMultiplier = secondDigit

        self.calculate_equation()

    # zero equations and data
    def reset_problem(self):
    	self.leftHandNumber = 0
    	self.rightHandNumber = 0
    	self.userSolution = 0
        self.solutionText = 0
        self.solution = 0
        self.buttonsEnabled = True
        self.correct = False
        self.create_equation()


    # calculate the user input
    def calculate_equation(self):
    	leftProduct = self.leftHandMultiplier * self.leftHandNumber
    	rightProduct = self.rightHandMultiplier * self.rightHandNumber
    	
    	if self.operator == "+":
    	    self.userSolution = leftProduct + rightProduct
    	elif self.operator == "-":
    	    self.userSolution = leftProduct - rightProduct

    	self.weight = self.userSolution / (self.solution * 2.0)
        if self.weight > 1.0:
            self.weight = 1.0

        self.setScales()

    #calculate the correct position of the scale
    def setScales(self):
        self.scaleCorrectPosition = 100.0 * self.weight

    #calculate positions for the scales each frame as they balance
    def tipScales(self):
        if self.scaleCurrentPosition < self.scaleCorrectPosition:
            self.scaleCurrentPosition += self.scaleSpeed

        if self.scaleCurrentPosition > self.scaleCorrectPosition:
            self.scaleCurrentPosition -= self.scaleSpeed

        if self.scaleCurrentPosition == self.scaleCorrectPosition:
            self.checkCorrect(True)

    #draw the scale graphic #TODO this could be greatly simplified or refactored into reusable functions
    def drawScales(self):        
        #left scale
        leftCalculatedX = self.scaleBasePositionX
        leftCalculatedY = self.scaleBasePositionY - self.scaleCurrentPosition #basePosition plus or minus 50 pixels

        leftPointOne = (leftCalculatedX, leftCalculatedY) #left point of left triangle
        leftPointTwo = (leftCalculatedX + (self.scaleWidth / 2.0), leftCalculatedY - 120) #top point of left triangle
        leftPointThree = (leftCalculatedX + self.scaleWidth, leftCalculatedY) #right point of right triangle

        pygame.draw.line(self.screen, self.black, leftPointOne, leftPointTwo, 5)
        pygame.draw.line(self.screen, self.black, leftPointTwo, leftPointThree, 5)
        pygame.draw.rect(self.screen, self.blue, (leftCalculatedX, leftCalculatedY, self.scaleWidth, self.scaleHeight)) #scale
        self.textBox(self.problemText, leftCalculatedX, leftCalculatedY, self.scaleWidth, -15) #right side label
        
        #right scale
        rightCalculatedX = self.scaleBasePositionX + 400
        rightCalculatedY = self.scaleBasePositionY - 100.0 + self.scaleCurrentPosition #basePosition plus this opposite adjustment of the left side
        
        rightPointOne = (rightCalculatedX, rightCalculatedY) #left point of right triangle
        rightPointTwo = (rightCalculatedX + (self.scaleWidth / 2.0), rightCalculatedY - 120) #top point of right triangle
        rightPointThree = (rightCalculatedX + self.scaleWidth, rightCalculatedY) #right point of right triangle

        pygame.draw.line(self.screen, self.black, rightPointOne, rightPointTwo, 5) #
        pygame.draw.line(self.screen, self.black, rightPointTwo, rightPointThree, 5)
        pygame.draw.rect(self.screen, self.blue, (rightCalculatedX, rightCalculatedY, self.scaleWidth, self.scaleHeight))
        self.textBox(self.solutionText, rightCalculatedX, rightCalculatedY, self.scaleWidth, -15) #right side label

        #center stand
        centerPointOne = ((leftPointTwo[0] + rightPointTwo[0]) / 2),((leftPointTwo[1] + rightPointTwo[1]) / 2) #top point of base
        centerPointTwo = (centerPointOne[0], centerPointOne[1] + 400) #center point of base
        centerPointThree = (centerPointTwo[0] - 100, centerPointTwo[1]) #left point of base
        centerPointFour = (centerPointTwo[0] + 100, centerPointTwo[1]) #right point of base

        pygame.draw.line(self.screen, self.black, leftPointTwo, rightPointTwo, 5) #scale beam
        pygame.draw.line(self.screen, self.black, centerPointOne, centerPointTwo, 5) #scale trunk
        pygame.draw.line(self.screen, self.black, centerPointThree, centerPointFour, 5) #scale feet

    #determine if the scale is set to the correct position or just passing over it
    def checkCorrect(self, correctPos):
        if self.userSolution == self.solution and correctPos:
            self.correct = True

    #get bound of text before rendering to page
    def text_objects(self, text, font):
        textSurface = font.render(text, True, self.black)
        return textSurface, textSurface.get_rect()

    #place button on screen (self,message,mouseover color,mouseoff color,x,y,width,height,function to fire)
    def button(self,msg,over,off,x,y,w,h,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        now = pygame.time.get_ticks()

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.screen, over,(x,y,w,h))

            if click[0] == 1 and action != None and self.fired + self.cooldown < now: #debounce clicks
                action() 
        else:
            pygame.draw.rect(self.screen, off,(x,y,w,h))

        self.textBox(msg,x,y,w,h)

    def textBox(self,msg,x,y,w,h):
        smallText = pygame.font.Font("freesansbold.ttf",40)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.screen.blit(textSurf, textRect)

    #increase left number up to maximum of 10
    def increaseLeft(self):
        self.fired = pygame.time.get_ticks()
        if self.leftHandNumber < 10 and self.buttonsEnabled:
            self.leftHandNumber += 1
        self.calculate_equation()

    #increase right number up to maximum of 10
    def increaseRight(self):
        self.fired = pygame.time.get_ticks()
        if self.rightHandNumber < 10 and self.buttonsEnabled:
            self.rightHandNumber += 1
        self.calculate_equation()

    #decrease left number down to minimum of 0
    def decreaseLeft(self):
        self.fired = pygame.time.get_ticks()
        if self.leftHandNumber > 0 and self.buttonsEnabled:
            self.leftHandNumber -= 1
        self.calculate_equation()

    #decrese right number down to minimum of 0
    def decreaseRight(self):
        self.fired = pygame.time.get_ticks()
        if self.rightHandNumber > 0 and self.buttonsEnabled:
            self.rightHandNumber -= 1
        self.calculate_equation()

    #end the current problem and enable next problem button
    def showCorrect(self):
        self.buttonsEnabled = False;
        self.button('Next Problem',self.bright_green,self.green,800,200,400,195,self.reset_problem)

    # Start the game 
    def setupPlay(self):
        self.currentPlayState = self.playStates.Play
        self.create_equation()

    # Return to the menu
    def returnToMenu(self):
        self.currentPlayState = self.playStates.Menu

    # The screen for the menu
    def drawMenuState(self):
        self.textBox("Balancing Act", self.screenWidth/2 - 30, 200, 60, -15)
        self.button('Start',self.bright_blue,self.blue,self.screenWidth/2-60,400,120,60,self.setupPlay)

    # The screen during play
    def drawPlayState(self):
        # Draw increase buttons
        self.button('+',self.bright_green,self.green,50,400,100,50,self.increaseLeft)
        self.button('+',self.bright_green,self.green,200,400,100,50,self.increaseRight)

        # Draw decrease buttons
        self.button('-',self.bright_red,self.red,50,500,100,50,self.decreaseLeft)
        self.button('-',self.bright_red,self.red,200,500,100,50,self.decreaseRight)

        self.button('menu',self.bright_blue,self.blue,5,5,120,50,self.returnToMenu)

        #update text
        self.problemText = str(self.leftHandNumber) + " x " + str(self.leftHandMultiplier) + " " + str(self.operator) + " " + str(self.rightHandNumber) + " x " +  str(self.rightHandMultiplier)
        self.solutionText = str(self.solution)
        self.userSolutionText = str(self.userSolution)

        #move the scale
        self.tipScales()

        #draw the scale
        self.drawScales()

        #show correct animation
        if self.correct:
            self.showCorrect()


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
                        self.currentPlayState = self.playStates.Paused


            # Clear Display
            self.screen.fill(self.white)

            options = { 0 : self.drawMenuState,
                        1 : self.drawPlayState,
                        2 : self.drawPlayState
            }
            options[self.currentPlayState]()

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
