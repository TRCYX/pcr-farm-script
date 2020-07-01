import os
from enum import Enum
from typing import *

import cv2


def screenshot(name: str):
    path = os.path.join(os.path.abspath('.'), 'images.png')
    os.system(f'adb -s {name} shell screencap /data/screen.png')
    os.system(f'adb -s {name} pull /data/screen.png {path}')


class ImageMatchMethod(Enum):
    CCOEFF_NORMED = cv2.TM_CCOEFF_NORMED
    SQDIFF_NORMED = cv2.TM_SQDIFF_NORMED
    CCORR_NORMED = cv2.TM_CCORR_NORMED


def resize_img(img_path: str):
    img1 = cv2.imread(img_path, 0)
    img2 = cv2.imread('images.png', 0)
    height, width = img1.shape[:2]

    ratio = 1920 / img2.shape[1]
    size = (int(width/ratio), int(height/ratio))
    return cv2.resize(img1, size, interpolation=cv2.INTER_AREA)


def image_to_position(image_name: str, diff_method: ImageMatchMethod=ImageMatchMethod.CCOEFF_NORMED, threshold: float=0.7) -> Optional[Tuple[float, float]]:
    image_path = os.path.join('images', f'{image_name}.png')
    screen = cv2.imread('images.png', 0)
    template = resize_img(image_path)
    image_x, image_y = template.shape[:2]
    result = cv2.matchTemplate(screen, template, diff_method.value)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(f'Match result of {image_name}: {max_val}')
    if max_val > threshold:
        return (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
    else:
        return None
