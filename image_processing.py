import os
from enum import Enum
from typing import *

import cv2


class ImageMatchMethod(Enum):
    CCOEFF_NORMED = cv2.TM_CCOEFF_NORMED
    SQDIFF_NORMED = cv2.TM_SQDIFF_NORMED
    CCORR_NORMED = cv2.TM_CCORR_NORMED


def img_to_pos(screen_path: str, template_path: str, diff_method: ImageMatchMethod = ImageMatchMethod.CCOEFF_NORMED, threshold: float = 0.7) -> Optional[Tuple[float, float]]:
    screen = cv2.imread(screen_path, 0)

    def resize_img():
        img = cv2.imread(template_path, 0)
        height, width = img.shape[:2]

        ratio = 1920 / screen.shape[1]
        size = (int(width/ratio), int(height/ratio))
        return cv2.resize(img, size, interpolation=cv2.INTER_AREA)

    template = resize_img()
    image_x, image_y = template.shape[:2]
    result = cv2.matchTemplate(screen, template, diff_method.value)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(f'Match result of {template_path}: {max_val}')
    if max_val > threshold:
        return (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
    else:
        return None
