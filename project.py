import pygame
import pygame.camera
import sys
from pygame.locals import *

#Initialize pygame[sdl2 wrapper for python]
pygame.init()
#create display or the screen
screen = pygame.display.set_mode((600,600))

#Initialize the camera
pygame.camera.init()

#choose camera, in my case it is "HP TrueVision HD Camera"
cam = pygame.camera.Camera("HP TrueVision HD Camera")
#start camera
cam.start()

#No of circles draw on screen
circles = []

#RGB colour of eye
cr,cg,cb = 48,62,85

#Mode, start will start looking for the eye
mode = "start"

#Debug text on screen
def write(t,size,colour,pos):
	fnt = pygame.font.Font(None,size)
	text = fnt.render(t,True,colour)
	screen.blit(text,pos)



#Loop
while 1:
	#fill screen with black to prevent overlapping of text
	screen.fill((0,0,0))

	#get cameras image
	frame = cam.get_image()
	#scale and flip camera image
	frame = pygame.transform.scale(pygame.transform.flip(frame,1,0),(600,400))
	#render camera image on screen
	screen.blit(frame,(0,0))

	#check if the mode is start
	if mode == "start":
		#loop through every pixel on the x axis
		for x in range(0,600):
			#loop through every pixel on the y axis
			for y in range(0,300):
				#Get pixel colour
				r,g,b,_ = frame.get_at((x,y))
				#check if the pixel colour is not to light to be an eye ball
				if r not in range(35,50) and g not in range(35,50) and b not in range(35,50):
					#check if the pixel colour matches with the eye ball colour
					if r <= cr and g <= cg and b <= cb:
						#append coordinates to the eye ball rendering list[circles]
						circles.append((x,y))
				
				#check if their are more than 1 circles rendered and delete the old ones
				#In this case we are tracing only one eye, if you change the value to 2, both the eyes will be circled
				if len(circles) > 1:
					#Remove from list
					circles.remove(circles[0])

		#Get corrds to render circle
		x,y = circles[0]
		#Debug on screen
		write(f"POS : X : {x} Y : {y}",30,(255,255,255),(100,500))

		#draw the inner and outer circles and target lines
		pygame.draw.circle(screen,(150,155,0),(x,y),(5))
		pygame.draw.circle(screen,(255,0,0),(x,y),(30),(1))
		pygame.draw.line(screen,(0,0,0),(x,y-15),(x,y+15),(1))
		pygame.draw.line(screen,(0,0,0),(x-15,y),(x+15,y),(1))

	
	
	#check through events to see if the user wants to exit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			#stop camera
			cam.stop()
			#stop eye tracking
			mode = "stop"
			#close window
			pygame.quit()
			#stop the program
			sys.exit()

		#check if the user clicks the mouse button and if so,
		#print the rgb value of the pixel on which the cursor is hovering
		#this can be used if the eye is not detected, you can click on the eye and use the printed rgb values
		if event.type == pygame.MOUSEBUTTONDOWN:
			print(frame.get_at(pygame.mouse.get_pos()))

		#check if the user pressed the "s" key on the keyboard
		#if so then save an image of the camera frame/image with name "camera_frame.png"
		if event.type == pygame.KEYDOWN:
			if event.key == ord("s"):
				pygame.image.save(screen,"camera_frame.png")

	#update display
	pygame.display.update()