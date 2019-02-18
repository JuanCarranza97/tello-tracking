import numpy as np    ##Import numpy 
import cv2            ##Import computer vision library

video= cv2.VideoCapture(0)    ##Create a new video object, conected to the first webcam 

frame_width = int(video.get(3))
frame_height = int(video.get(4))
out = cv2.VideoWriter('prueba1_.avi',cv2.VideoWriter_fourcc('M','J','P','G'),10,(frame_width,frame_height))

fin = False
centro_x = 0

while(1):
	okay,image = video.read()  #Save video frame on image and status in okay

	if okay: #if frame image is completted
	 	blur = cv2.GaussianBlur(image,(5,5),0)      ##GaussianBlur for filtering signal
		hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) ##BGR to HSV for easier identification of object color

		#Select lower and upper color detection range
		lower_color = np.array([40,70,70])
		upper_color = np.array([80,200,200])

		#save in mask hsv image with filter color
		mask = cv2.inRange(hsv,lower_color,upper_color)
		mask = cv2.GaussianBlur(mask,(5,5),0)
		output = cv2.bitwise_and(image, image, mask = mask)
 		
 		moments = cv2.moments(mask)
 		m00 = moments['m00']
 		centro_x,centro_y = -1,-1
 		if m00 != 0:
 			centro_x = int(moments['m10']/m00)
 			centro_y = int(moments['m01']/m00)

 		if centro_y != -1 and centro_y != -1:
 			ctr = (centro_x,centro_y)
 			cv2.circle(image,ctr,5,(255,0,0),4)

		#cv2.circle(output,(300,250),50,(0,255,0))
		cv2.putText(image,"X="+str(centro_x)+", Y="+str(centro_y),(5,470),cv2.FONT_ITALIC,.4,(255,255,255),1,cv2.LINE_AA)
		cv2.putText(image,"Instituto Tecnologico de Ciudad Guzman",(316,450),cv2.FONT_ITALIC,.5,(255,255,255),1,cv2.LINE_AA)
		cv2.putText(image,"Ball and Plate Project - Ing. Electronica",(310,470),cv2.FONT_ITALIC,.5,(255,255,255),1,cv2.LINE_AA)	
		#cv2.imshow("Images",np.hstack([image,output]))
		cv2.imshow("Images",image)
		out.write(image)
		if cv2.waitKey(1) & 0xFF == ord('b'):
			fin = True
			break
out.release()
video.release()
cv2.destroyAllWindows()