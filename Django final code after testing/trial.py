import cv2

#img = open("screenshot.jpg", "r+")
img = cv2.imread("screenshot.jpg")
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
