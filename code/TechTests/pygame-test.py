import cv2
import numpy
import pygame
import time

red = (255,0,0)

background_color = (0,0,0)

pygame.init()

surface = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

# Full path to the video file
path = 'brainzoom.mov'
# Open the video and determine the video dimensions
video = cv2.VideoCapture(path)

#initiate the video with a keypress and start the clock
key = None
while key == None:
   for event in pygame.event.get():
       if event.type == pygame.KEYDOWN:
           start_time = time.time()
           key = event.key
           go = True

while go:

    # Get a frame and break the loop if we failed, usually because the video
    # ended.
    success, frame = video.read()
    if not success:
        break

    #for some reasons the frames appeared inverted
    frame = numpy.fliplr(frame)
    frame = numpy.rot90(frame)

        # The video uses BGR colors and PyGame needs RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a PyGame surface
    surf = pygame.surfarray.make_surface(frame)

    #set the frame rate to 20 fps ?? To be verified.
    #self.sleep(50)

    # Fill the background color of the PyGame surface whenever a key is released
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            background_color = red
            surface.fill(background_color)
            pygame.display.update
            end_time = time.time()  

    # Show the PyGame surface!
    surface.blit(surf, (0,0))
    pygame.display.flip()



#define the experimental variable
rt = end_time- start_time
exp.set('keyreleaseRT', rt)
print('%s was released after %d ms' % (key, rt))