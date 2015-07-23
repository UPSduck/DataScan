import numpy as np
from matplotlib import pyplot as plt
import cv2

# Capture an Image
camera_port = 0
ramp_frames = 30
camera = cv2.VideoCapture(camera_port)
def get_image():
 retval, im = camera.read()
 return im

for i in xrange(ramp_frames):
 temp = get_image()
print("Taking image...")
camera_capture = get_image()
file = "captured_image.png"
cv2.imwrite(file, camera_capture)
del(camera)

def ImgScale(image,newSize):
    r = float(newSize) / image.shape[1]
    dim = (int(newSize), int(image.shape[0] * r))
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return image


def ImgThresh(image,thresh=0):
        if thresh != 0:
            ret,newImage = cv2.threshold(image,thresh,255,cv2.THRESH_BINARY)
        else:
            ret,newImage = cv2.threshold(image,0,255,cv2.THRESH_OTSU)
        return newImage


def FindCenter(contour):
    (x,y),radius = cv2.minEnclosingCircle(contour)
    center = (int(x),int(y))
    return center


def FindMark(contours,mark=0):
    	l = len(contours)
    	c = mark
	while l > c:
			(x1,y1) = FindCenter(contours[c-1])
			(x,y) = FindCenter(contours[c])
			difference = (x1-x)+(y1-y)
			print 'Center Difference:',(x1-x)+(y1-y),''
			if bufValue*-1 < difference < bufValue:
				mark = int(c)
				c = l+1
				print 'Mark Found at array',mark
				print 'Verrifying...'
				ConfirmMark(contours,mark)
			else:
				c = c + 1
			if l == c:
				print 'No Marker Found'
	return mark


def ConfirmMark(contours,mark):
	A1 = cv2.contourArea(contours[mark])+1
	A2 = cv2.contourArea(contours[mark-1])+1
	KEY = 0
	if A1 < A2:
		KEY = A2/A1
	else:
		KEY = A1/A2
	if 6.5 < KEY < 8.5:
		print 'KEY:',KEY
		print 'Mark VERIFIED!'
	else:
		print 'FAILED'
		print KEY , 'Search for new mark...'
		FindMark(contours,mark+1)
		
def DrawMark(image,contours,mark,I=255,border=2):
	rect = cv2.minAreaRect(contours[mark])
	box = cv2.cv.BoxPoints(rect)
	box = np.int0(box)
	#Get Corners for box 2
	rect1 = cv2.minAreaRect(contours[mark-1])
	box1 = cv2.cv.BoxPoints(rect1)
	box1 = np.int0(box1)
	#Draw
	cv2.drawContours(image,[box],0,(I,I,I),border)
	cv2.drawContours(image,[box1],0,(I,I,I),border)
	
		
scale = 5
bufValue = 1.5*scale
wipSize = 100 * scale
finSize = 500
blur = 1
minEdge = 100
maxEdge = 200

# Process Image
imgOrig = cv2.imread(file,0) #imgPath for sample file for camera
imgScaled = ImgScale(imgOrig,wipSize)
imgBlured = cv2.GaussianBlur(imgScaled, (blur, blur), 0)
imgThreshed = ImgThresh(imgBlured)
imgEdged = cv2.Canny(imgThreshed,minEdge,maxEdge)

#Create and sort Contours
contours, hierarchy = cv2.findContours(imgThreshed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cntsArea = sorted(contours, key = cv2.contourArea, reverse = True)[:50]
cntsCent = sorted(cntsArea, key = FindCenter)


#Find Mark
mark = FindMark(cntsCent)
DrawMark(imgScaled,cntsCent,mark,255,2)

#display Marker
plt.imshow(imgScaled,'gray')
plt.title('marker')
plt.xticks([]),plt.yticks([])
plt.show()

