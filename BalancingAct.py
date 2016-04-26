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

        self.paused = False
        self.direction = 1

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
	elif self.userSolution > self.solution:
	    self.reload_data()

    # The main game loop.
    def run(self):
        self.running = True

        screen = pygame.display.get_surface()

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
		    #Controls to add numbers to multipliers
		    elif event.key == pygame.K_UP:
			self.leftHandNumber += 1;
			self.calculate_equation()
		    elif event.key == pygame.K_DOWN:
			self.rightHandNumber += 1;
			self.calculate_equation()

            # Move the ball
            if not self.paused:
                self.x += self.vx * self.direction
                if self.direction == 1 and self.x > screen.get_width() + 100:
                    self.x = -100
                elif self.direction == -1 and self.x < -100:
                    self.x = screen.get_width() + 100

                self.y += self.vy
                if self.y > screen.get_height() - 100:
                    self.y = screen.get_height() - 100
                    self.vy = -self.vy

                self.vy += 5

            # Clear Display
            screen.fill((255, 255, 255))  # 255 for white

            # Draw the ball
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 100)

	    #Draw text
	    myFont = pygame.font.SysFont("monospace",60)
	    leftSideLabel = myFont.render(str(self.leftHandNumber) + 
		" x " + str(self.leftHandMultiplier) + " " +
		str(self.operator) + " " +
		str(self.rightHandNumber) + " x " + 
		str(self.rightHandMultiplier) + " = " +
		str(self.userSolution),1,(25,25,255))

	    rightSideLabel = myFont.render("Goal = " + str(self.solution),1,(255,25,25))

	    screen.blit(leftSideLabel,(100,100))
	    screen.blit(rightSideLabel,(100,150))

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
