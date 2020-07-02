import os
import time
from typing import *

from image_processing import img_to_pos

Pos = Tuple[float, float]


class Android:
    FINE_SLEEP_SECONDS = 0.01
    COARSE_SLEEP_SECONDS = 0.5
    TIMEOUT = 30

    def __init__(self, name: str):
        self.name = name

    @property
    def default_screenshot_path(self):
        return os.path.join(os.getcwd(), f'screenshot-{self.name}.png')

    def __repr__(self):
        return f'Android(name={repr(self.name)})'

    def _log(self, *args):
        print(f"Android {self.name}:", *args)

    def click(self, pos: Pos):
        self._log('Click', pos)
        os.system(f'adb -s {self.name} shell input tap {pos[0]} {pos[1]}')

    def swipe(self, from_: Pos, to: Pos, duration: int):
        self._log('Swipe', from_, '-', to, f'{duration}ms')
        os.system(
            f'adb -s {self.name} shell input swipe {from_[0]} {from_[1]} {to[0]} {to[1]} {duration}')

    def input(self, text: str):
        self._log(f'Input "{text}"')
        os.system(f'adb -s {self.name} shell input text "{text}"')

    def screenshot(self, path: Optional[str] = None):
        if path is None:
            path = self.default_screenshot_path
        self._log(f'Taking screenshot', path)
        os.system(f'adb -s {self.name} shell screencap /data/screen.png')
        os.system(f'adb -s {self.name} pull /data/screen.png {path}')

    def find_image_like(self, img_name: str) -> Optional[Pos]:
        self._log(f'Finding image like "{img_name}"')
        self.screenshot()
        return img_to_pos(self.default_screenshot_path, os.path.join('images', img_name + '.png'))

    def wait_for_image_like(self, img_name: str, /, on_missing: Callable[[], Any] = lambda: ()) -> Pos:
        self._log(f'Waiting for image like "{img_name}"')
        for _ in range(int(Android.TIMEOUT / Android.COARSE_SLEEP_SECONDS)):
            if pos := self.find_image_like(img_name):
                return pos
            on_missing()
            time.sleep(Android.COARSE_SLEEP_SECONDS)
        else:
            self._log(f'"{img_name}" NOT FOUND')
            raise TimeoutError(f'Can not find button {img_name}')

    def click_button_like(self, img_name: str):
        # TODO: img_name / img_name
        self._log(f'Clicking button like "{img_name}"')
        self.click(self.wait_for_image_like(img_name))
