import cv2
import numpy as np


class Deskew:

    def __init__(self, img, corners):
        self.img = img
        self.corners = corners

    def get_destination_points(self):
        corners = self.corners
        w1 = np.sqrt((corners[0][0] - corners[1][0]) ** 2 + (corners[0][1] - corners[1][1]) ** 2)
        w2 = np.sqrt((corners[2][0] - corners[3][0]) ** 2 + (corners[2][1] - corners[3][1]) ** 2)
        w = max(int(w1), int(w2))

        h1 = np.sqrt((corners[0][0] - corners[2][0]) ** 2 + (corners[0][1] - corners[2][1]) ** 2)
        h2 = np.sqrt((corners[1][0] - corners[3][0]) ** 2 + (corners[1][1] - corners[3][1]) ** 2)
        h = max(int(h1), int(h2))

        destination_corners = np.float32([(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)])

        # print('\nThe destination points are: \n')
        for index, c in enumerate(destination_corners):
            character = chr(65 + index) + "'"
            # print(character, ':', c)

        # print('\nThe approximated height and width of the original image is: \n', (h, w))
        return destination_corners, h, w

    def unwarp(self, src, dst):
        h, w = self.img.shape[:2]
        H, _ = cv2.findHomography(src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0)
        # print('\nThe homography matrix is: \n', H)
        un_warped = cv2.warpPerspective(self.img, H, (w, h), flags=cv2.INTER_LINEAR)
        return un_warped

    def deskew(self):
        destination, h, w = self.get_destination_points()
        corners = self.corners
        un_warped = self.unwarp(np.float32(corners), destination)
        cropped = un_warped[0:h, 0:w]
        return cropped
