import cv2 
import numpy as np 



def draw():

	cap = cv2.VideoCapture(0)
	drawing = True		# This boolean is to activate drawing
	pts = []

	################### Before entering the loop, we gonna set up our blob detector #############

	params = cv2.SimpleBlobDetector_Params()

	params.filterByConvexity = True
	params.minConvexity = 0.9

	params.filterByArea = True
	params.minArea = 50

	spot = cv2.SimpleBlobDetector_create(params)

	tabishere = False

	################# We're ready to go now #########################
	print("Let's Draw\n")
	while(1):

   		# Take each frame
		_, frame = cap.read()
		if not tabishere:		### Creating the table containing the points we gonna draw, we need the frames size, that's why it's done here

			tab = np.zeros((len(frame), len(frame[0])))
			tabishere = True


   		# Convert BGR to HSV
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    	# define range of blue color in HSV, cuz I use a pkmn blue GB cartridge for this
    	
		lower_blue = np.array([110,150,50])
		upper_blue = np.array([130,255,255])

    	# Threshold the HSV image to get only blue colors and track our blue item
		mask = cv2.inRange(hsv, lower_blue, upper_blue)

    	################ Now we gonna perform blob detection to get the coordinates of our "pen" ###################

		#mask = cv2.fastNlMeansDenoising(mask,None,30,7,21)		# first we denoise our picture to make it cleaner//// Nope makes everything too slow
		blob = spot.detect(mask)

		if len(blob) == 1 and drawing:				#### Just to not mess up the whole deal
			
			pts.append(blob[0].pt)		# We add the new point to draw
			y = len(frame) - int(blob[0].pt[0])
			x = int(blob[0].pt[1])

    	###### Now let's change the color of a group of pixels around the center of the blob
    	###### cuz a single pixel is hard to see
			
			try:								# to avoid a crash
				tab[x-2:x+2, y-2:y+2] = 255	
		
			except:

				print("Outta Boundaries, you went too far\n")



		cv2.imshow('frame',mask)
		cv2.imshow("tadaa", tab)
		k = cv2.waitKey(5) 
		if k == 27:
			break

		elif k == 99:		# if you press c, the table gets cleared

			tab = np.zeros((len(frame), len(frame[0])))
			pts.clear()
			print("table cleared\n")

		elif k == 100:		# if you press d, we just stop or restart drawing, without erasing what was done before

			drawing = not(drawing)

			if drawing:
				print("drawing enabled\n")
			else:
				print("drawing disabled\n")



	cv2.destroyAllWindows()