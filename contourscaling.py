import cv2
import numpy as np

class ContourScaling:
    def __init__(self, cnt, scale):
        self.cnt = cnt
        self.scale = scale

    def scale_contour(self, cx, cy):
        cnt_norm = self.cnt - [cx, cy]
        cnt_scaled = cnt_norm * self.scale
        cnt_scaled = cnt_scaled + [cx, cy]
        cnt_scaled = cnt_scaled.astype(np.int32)
        return cnt_scaled
