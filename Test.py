import cv2

# Load the input image
im = cv2.imread("in/scaled_shapes.jpg")

# Convert the image to grayscale
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# Threshold the grayscale image
_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

# Compute moments on the thresholded image
moments = cv2.moments(thresh)

print(moments['nu02']+moments['nu20'])