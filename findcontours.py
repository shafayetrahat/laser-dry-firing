import cv2
import numpy as np
from contourscaling import ContourScaling
class FindContour:
    def __init__(self, img, laser_center):
        self.img = img
        self.laser_center = laser_center

    def findcircle(self):
        gray_blurred = cv2.blur(self.img, (3, 3))

# Apply Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(gray_blurred,cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,param2 = 30, minRadius = 0, maxRadius = 25)
# Draw circles that are detected.
        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))
            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]
        # Draw the circumference of the circle.
                cv2.circle(self.img, (a, b), r, (255, 255, 255), 1)
        # Draw a small circle (of radius 1) to show the center.
                cv2.circle(self.img, (a, b), 1, (255, 255, 255), 1)
        return self.img


    def findcontour(self):
        img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(img, (5, 5), 100)
        _, threshold = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY)
        contours, _= cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # print(contours)
        det = 0
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.00001*cv2.arcLength(cnt, True), True)
            if 40 < len(approx) < 70:
                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(self.img, (cX, cY), 2, (255, 255, 255), -1)
                if cX>cY:
                    # cv2.drawContours(self.img, [approx], 0, (255,255,255), 1)
                    cntrsclh1 = ContourScaling(approx, 1.7)
                    h1 = cntrsclh1.scale_contour(cX, cY)
                    # cv2.drawContours(self.img, [h1], 0, (255,255,255), 1)
                    cntrsclh2 = ContourScaling(approx, 2.5)
                    h2 = cntrsclh2.scale_contour(cX, cY)
                    # cv2.drawContours(self.img, [h2], 0, (255,255,255), 1)
                    if cv2.pointPolygonTest(approx,self.laser_center,False)==1:
                        print("Head| Bull's eye, 10 points")
                        det = 1
                    elif cv2.pointPolygonTest(h1,self.laser_center,False)==1:
                        print("Head| 9 points")
                        det = 1
                    elif cv2.pointPolygonTest(h2,self.laser_center,False)==1:
                        print("Head| 8 points")
                        det = 1
                if cX<cY:
                    # cv2.drawContours(self.img, [approx], 0, (255,255,255), 1)
                    cntrscl1 = ContourScaling(approx, 1.7)
                    c1 = cntrscl1.scale_contour(cX, cY)
                    # cv2.drawContours(self.img, [c1], 0, (255,255,255), 1)
                    cntrscl2 = ContourScaling(approx, 2.5)
                    c2 = cntrscl2.scale_contour(cX, cY)
                    # cv2.drawContours(self.img, [c2], 0, (255,255,255), 1)
                    cntrscl3 = ContourScaling(approx, 3.5)
                    c3 = cntrscl3.scale_contour(cX, cY)
                    # cv2.drawContours(self.img, [c3], 0, (255,255,255), 1)
                    cntrscl4 = ContourScaling(approx, 4.5)
                    c4 = cntrscl4.scale_contour(cX, cY)
                    # cv2.drawContours(self.img, [c4], 0, (255,255,255), 1)
                    cntrscl5 = ContourScaling(approx, 6.0)
                    c5 = cntrscl5.scale_contour(cX, cY)
                    # cv2.drawContours(self.img, [c5], 0, (255,255,255), 1)
                    if cv2.pointPolygonTest(approx,self.laser_center,False)==1:
                        print("Chest| Bull's eye, 10 points")
                        det = 1
                    elif cv2.pointPolygonTest(c1,self.laser_center,False)==1:
                        print("Chest| 9 points")
                        det = 1
                    elif cv2.pointPolygonTest(c2,self.laser_center,False)==1:
                        print("Chest| 8 points")
                        det = 1
                    elif cv2.pointPolygonTest(c3,self.laser_center,False)==1:
                        print("Chest| 7 points")
                        det = 1
                    elif cv2.pointPolygonTest(c4,self.laser_center,False)==1:
                        print("Chest| 6 points")
                        det = 1
                    elif cv2.pointPolygonTest(c5,self.laser_center,False)==1:
                        print("Chest| 5 points")
                        det = 1



            # if 6 < len(approx) < 15:
            #     cv2.putText(self.img, "Ellipse", (x, y), font, 1, (0))
        return self.img, det
