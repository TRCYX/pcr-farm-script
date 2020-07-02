from __future__ import annotations

import os
import time
from typing import *

from image_processing import img_to_pos
from utils import noop

Pos = Tuple[float, float]
EmptyCallback = Callable[[], Any]


class Control:
    def __init__(self, android: Android, pos: Pos):
        self.android = android
        self.pos = pos

    def on(self, a: Android) -> Control:
        return Control(a, self.pos)

    def click(self):
        self.android.click(self.pos)

    def hold(self, duration: int):
        self.android.hold(self.pos, duration)

    def input(self, text: str):
        self.click()
        self.android.input(text)

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

    def hold(self, pos: Pos, duration: int):
        self._log('Hold on', pos, f'{duration}ms')
        self.swipe(pos, pos, duration)

    def input(self, text: str):
        self._log(f'Input "{text}"')
        os.system(f'adb -s {self.name} shell input text "{text}"')

    def screenshot(self, path: Optional[str] = None):
        if path is None:
            path = self.default_screenshot_path
        self._log(f'Taking screenshot', path)
        os.system(f'adb -s {self.name} shell screencap /data/screen.png')
        os.system(f'adb -s {self.name} pull /data/screen.png {path}')

    def find_image_like(self, img_name: str) -> Optional[Control]:
        self._log(f'Finding image like [{img_name}]')
        self.screenshot()
        pos = img_to_pos(self.default_screenshot_path, os.path.join('images', img_name + '.png'))
        return Control(self, pos) if pos else None

    def wait_for_image_like(self, img_name: str, /, on_missing: EmptyCallback = noop) -> Control:
        self._log(f'Waiting for image like [{img_name}]')
        for _ in range(int(Android.TIMEOUT / Android.COARSE_SLEEP_SECONDS)):
            if c := self.find_image_like(img_name):
                return c
            on_missing()
            time.sleep(Android.COARSE_SLEEP_SECONDS)
        else:
            self._log(f'[{img_name}] NOT FOUND')
            raise TimeoutError(f'Can not find button {img_name}')
