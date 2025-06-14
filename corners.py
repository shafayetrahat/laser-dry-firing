import cv2
import numpy as np
"""
This class give the corner of the answer sheet
"""


class Corners:
    def __init__(self, img):
        self.img = img

    def getCorners(self):
        templates = [cv2.imread("tl.png", cv2.IMREAD_GRAYSCALE),
                     cv2.imread("tr.png", cv2.IMREAD_GRAYSCALE),
                     cv2.imread("bl.png", cv2.IMREAD_GRAYSCALE),
                     cv2.imread("br.png", cv2.IMREAD_GRAYSCALE)]

        blurGray = cv2.medianBlur(self.img, 3)
        thresh = cv2.adaptiveThreshold(
            blurGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 151, 11)
        corners = []
        fin_corner = []
        wnet = 0
        hnet = 0
        for template in templates:
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(thresh, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            # print("Probability")
            # print(res)
            threshold = 0.8
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                if bottom_right not in corners and top_left not in corners:
                    # cv2.rectangle(res_img, top_left, bottom_right, (0, 255, 0), 3)
                    corners.append(bottom_right)
            wnet = wnet + w
            hnet = hnet + h
        w_av = wnet/4
        h_av = hnet/4
        # print(corners)
        for corner in corners:
            if corners.index(corner) == 0:
                fin_corner.append([corner[0], corner[1]])
            if corners.index(corner) == 1:
                fin_corner.append([corner[0]-w_av, corner[1]])
            if corners.index(corner) == 2:
                fin_corner.append([corner[0], corner[1]-h_av])
            if corners.index(corner) == 3:
                fin_corner.append([corner[0]-w_av, corner[1]-h_av])
        return fin_corner
