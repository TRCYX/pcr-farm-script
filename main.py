import os
import sys
import time
from typing import *

from image_processing import image_to_position, screenshot

AndroidName = NewType('Android', str)


class UserInfo(NamedTuple):
    username: str
    password: str

farm1Sudo = UserInfo('账号', '密码')  # 农场1会长
farm2Sudo = UserInfo('', '')  # 农场2会长
realAccount = UserInfo('', '')  # 大号


def connect():
    try:
        os.system('adb connect 127.0.0.1:5554')
    except:
        print('连接失败')

@overload
def click(x: float, y: float, name: AndroidName): ...

@overload
def click(pos: Tuple[float, float], name: AndroidName): ...

def click(*args):
    if len(args) == 2:
        (x, y), name = args
    else:
        x, y, name = args
    x: float
    y: float
    name: AndroidName
    print(name)
    print(x, y)
    os.system(f'adb -s {name} shell input tap {x} {y}')





def main_run(nameList: List[AndroidName], images: List[str]):
    for image in images:
        while True:
            screenshot(nameList[0])
            if image_to_position(image):
                for name in nameList:
                    while True:
                        screenshot(name)
                        if center := image_to_position(image):
                            print(image)
                            print(center)
                            click(center, name)
                            # time.sleep(0.5)
                            break
                break


def main_run_quick(nameList: List[AndroidName], images: List[str]):
    for image in images:
        while True:
            screenshot(nameList[0])
            if center := image_to_position(image):
                for name in nameList:
                    if image == 'timeadd':
                        os.system(f'adb -s {name} shell input swipe {center[0]} {center[1]} {center[0]} {center[1]} 6000')
                    else:
                        click(center, name)
                    # time.sleep(0.)
                break


def to_homepage(nameList: List[AndroidName]):
    for i in range(0, 6):
        screenshot(nameList[0])
        if image_to_position('skip'):
            for name in nameList:
                for _ in range(0, 3):
                    screenshot(name)
                    if center := image_to_position('skip'):
                        print('skip')
                        print(center)

                        click(center, name)
                        time.sleep(0.5)
                        break
                    else:
                        click(640, 360, name)
            break
        else:
            click(640, 360, nameList[0])


def login(name: AndroidName, idset: UserInfo):
    for image in ['ID', 'password', 'login']:
        while True:
            screenshot(name)
            if center := image_to_position(image):
                print(image)
                print(center)
                click(center[0], center[1], name)
                if image == 'ID':
                    os.system(f'adb -s {name} shell input text "{idset.username}"')
                elif image == 'password':
                    os.system(f'adb -s {name} shell input text "{idset.password}"')
                break
            else:
                click(1200, 50, name)


def get_account(txtname: str):
    lines = []
    with open(txtname, 'r') as f:
        lines = f.readlines()
        return lines


def kick(enumList: List[AndroidName]):
    main_run(enumList, ['society'])
    time.sleep(2.5)
    main_run(enumList, ['memberinfo'])
    time.sleep(3)
    main_run(enumList, ['place', 'level', 'ok_blue'])
    main_run(enumList, ['take', 'fuck_off', 'ok_blue'])
    time.sleep(2.5)
    main_run(enumList, ['ok_white'])
    main_run(enumList, ['level1', 'place2', 'ok_blue'])
    main_run(enumList, ['homepage_red'])


def soadd(enumList: List[AndroidName], soName: str):
    main_run(enumList, ['society', 'sosetting', 'sosearch'])
    screenshot(enumList[0])
    while True:
        if center := image_to_position('soname'):
            print(center)
            click(center[0], center[1], enumList[0])
            os.system(f'adb -s {enumList[0]} shell input text "{soName}"')
            main_run(enumList, ['ensurecn'])
            break
    time.sleep(3)
    # click(enumList[0])
    main_run(enumList, ['search', 'farmicon', 'farmjoin'])
    time.sleep(3)
    main_run(enumList, ['ok_blue'])
    time.sleep(3)
    main_run(enumList, ['ok_blue'])


if __name__ == '__main__':

    accountList = get_account('accountlist.txt')  # 获取账号列表1

    # connect()

    result = os.popen('adb devices')
    res = result.read()
    lines = res.splitlines()[1:]

    for i in range(0, len(lines)):
        lines[i] = lines[i].split('\t')[0]
    lines = list(map(AndroidName, lines[0:-1]))
    print(lines)

    # 共28个号，4开为例
    for step in range(0, 7):

        # 依次登录4个号

        for i in range(0, len(lines)):
            login(lines[i], UserInfo(accountList[i+step*4].split(' ')[0],
                                     accountList[i+step*4].split(' ')[1][0:-1]))
            print(accountList[i+step*4].split(' ')[0])
        time.sleep(5)
        to_homepage(lines)
        main_run_quick(lines, ['close_white'])

        for _ in range(0, 3):
            main_run_quick(lines, ['add_blue', 'ok_blue', 'ok_white'])

        main_run_quick(lines, ['explor', 'masterbatch',
                             '3-1', 'timeadd', 'run_cn', 'ok_blue'])
        time.sleep(2)
        main_run_quick(lines, ['skip_cn', 'ok_white'])
        for name in lines:
            click(1200, 50, name)
        main_run(lines, ['cancel_white'])
        time.sleep(2)

        # 地下城战斗
        main_run_quick(
            lines, ['explor_blue', 'underground', 'normalUD', 'ok_blue'])
        time.sleep(3)
        main_run_quick(lines, ['floor1'])
        time.sleep(4)
        main_run_quick(lines, ['challenge_blue'])
        time.sleep(3)
        # mainrunQuick(lines,['u1','pico','kkl','cat','getassist','assist','battlestart','ok_blue'])
        main_run_quick(lines, ['getassist', 'assist', 'battlestart', 'ok_blue'])
        time.sleep(4)
        main_run_quick(lines, ['menu_white', 'giveup_white', 'giveup_blue'])
        time.sleep(4)
        main_run_quick(lines, ['withdraw', 'ok_blue'])

        # 回登陆页，开始下一次iteration
        main_run_quick(lines, ['mainpage', 'backtotitle', 'ok_blue'])
        time.sleep(3)

    # 踢出换工会上支援
    login(lines[0], farm1Sudo)
    # login(lines[1],farm2Sudo)
    login(lines[2], realAccount)
    to_homepage([lines[0]])
    to_homepage([lines[2]])
    time.sleep(2)
    main_run([lines[0], lines[2]], ['close_white'])
    time.sleep(2)
    kick([lines[0]])
    time.sleep(2)
    soadd([lines[2]], 'qxxxFarm2')
    time.sleep(4)
    main_run([lines[2]], ['setassist', 'addselect', 'myassist', 'set', 'ok_blue'])
    time.sleep(3)
    main_run([lines[2]], ['homepage_red'])
    time.sleep(2)
    main_run([lines[0], lines[2]], ['mainpage', 'backtotitle', 'ok_blue'])

    accountList = get_account('accountlist2.txt')  # 获取账号列表2

    # 共12个号，4开为例
    for step in range(0, 3):

        # 依次登陆4个号
        for i in range(0, len(lines)):
            login(lines[i], UserInfo(accountList[i+step*4].split(' ')[0],
                                     accountList[i+step*4].split(' ')[1][0:-1]))
            print(accountList[i+step*4].split(' ')[0])
        time.sleep(5)
        to_homepage(lines)
        main_run_quick(lines, ['close_white'])

        for _ in range(0, 3):
            main_run_quick(lines, ['add_blue', 'ok_blue', 'ok_white'])

        main_run_quick(lines, ['explor', 'masterbatch',
                             '3-1', 'timeadd', 'run_cn', 'ok_blue'])
        time.sleep(2)
        main_run_quick(lines, ['skip_cn', 'ok_white'])
        for name in lines:
            click(1200, 50, name)
        main_run(lines, ['cancel_white'])
        time.sleep(2)

        # 地下城战斗
        main_run_quick(
            lines, ['explor_blue', 'underground', 'normalUD', 'ok_blue'])
        time.sleep(3)
        main_run_quick(lines, ['floor1'])
        time.sleep(4)
        main_run_quick(lines, ['challenge_blue'])
        time.sleep(3)
        # mainrunQuick(lines,['u1','pico','kkl','cat','getassist','assist','battlestart','ok_blue'])
        main_run_quick(lines, ['getassist', 'assist', 'battlestart', 'ok_blue'])
        time.sleep(4)
        main_run_quick(lines, ['menu_white', 'giveup_white', 'giveup_blue'])
        time.sleep(4)
        main_run_quick(lines, ['withdraw', 'ok_blue'])

        # 回登陆页，开始下一次iteration
        main_run_quick(lines, ['mainpage', 'backtotitle', 'ok_blue'])
        time.sleep(3)

    # 踢出换工会上支援
    # login(lines[0],farm1Sudo)
    login(lines[1], farm2Sudo)
    login(lines[2], realAccount)
    to_homepage([lines[1], lines[2]])
    main_run([lines[1], lines[2]], ['close_white'])
    time.sleep(2)
    kick([lines[1]])
    time.sleep(2)
    soadd([lines[2]], 'qxxxFarm1')
    time.sleep(4)
    main_run([lines[2]], ['setassist', 'addselect', 'myassist', 'set', 'ok_blue'])
    time.sleep(3)
    main_run([lines[2]], ['homepage_red'])
    time.sleep(3)
    main_run([lines[1], lines[2]], ['mainpage', 'backtotitle', 'ok_blue'])

    # 退出程序
    os.system('adb kill-server')
