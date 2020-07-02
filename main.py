import os
import sys
import time
from typing import *

from android import Android
from image_processing import img_to_pos


class UserInfo(NamedTuple):
    username: str
    password: str

farm1_leader = UserInfo('账号', '密码')  # 农场1会长
farm2_leader = UserInfo('', '')  # 农场2会长
real_account = UserInfo('', '')  # 大号


def connect():
    try:
        os.system('adb connect 127.0.0.1:5554')
    except:
        print('连接失败')


def main_run(androids: List[Android], images: List[str]):
    for image in images:
        for a in androids:
            a.wait_for_image_like(image).click()

def main_run_quick(androids: List[Android], images: List[str]):
    for image in images:
        button = androids[0].wait_for_image_like(image)
        for a in androids:
            if image == 'timeadd':
                button.on(a).hold(6000)
            else:
                button.on(a).click()


def to_homepage(androids: List[Android]):
    for _ in range(6):
        if androids[0].find_image_like('skip'):
            for a in androids:
                for _ in range(3):
                    if button := a.find_image_like('skip'):
                        print('skip')
                        print(button.pos)

                        button.click()
                        time.sleep(0.5)
                        break
                    else:
                        a.click((640, 360))
            break
        else:
            androids[0].click((640, 360))


def login(a: Android, user_info: UserInfo):
    a.wait_for_image_like('username', on_missing=lambda: a.click((1200, 50))).input(user_info.username)
    a.find_image_like('password').input(user_info.password)
    a.find_image_like('login').click()


def get_account(txtname: str):
    lines = []
    with open(txtname, 'r') as f:
        lines = f.readlines()
        return lines


def kick(androids: List[Android]):
    main_run(androids, ['clan'])
    time.sleep(2.5)
    main_run(androids, ['memberinfo'])
    time.sleep(3)
    main_run(androids, ['place', 'level', 'ok_blue'])
    main_run(androids, ['take', 'fuck_off', 'ok_blue'])
    time.sleep(2.5)
    main_run(androids, ['ok_white'])
    main_run(androids, ['level1', 'place2', 'ok_blue'])
    main_run(androids, ['homepage_red'])


def clan_add(androids: List[Android], clan_name: str):
    main_run(androids, ['clan', 'clan_setting', 'clan_search'])
    center = androids[0].wait_for_image_like('clan_name')
    print(center)
    center.input(clan_name)
    main_run(androids, ['ensurecn'])
    time.sleep(3)
    # click(enumList[0])
    main_run(androids, ['search', 'farmicon', 'farmjoin'])
    time.sleep(3)
    main_run(androids, ['ok_blue'])
    time.sleep(3)
    main_run(androids, ['ok_blue'])


if __name__ == '__main__':

    accountList = get_account('accountlist.txt')  # 获取账号列表1

    # connect()

    result = os.popen('adb devices')
    res = result.read()
    lines = res.splitlines()[1:-1]

    def parse(line: str):
        return Android(line.split('\t')[0])

    androids = list(map(parse, lines))
    print(androids)

    # TODO
    input()

    # 共28个号，4开为例
    for step in range(0, 7):
        # 依次登录4个号
        for i in range(0, len(androids)):
            login(androids[i], UserInfo(accountList[i+step*4].split(' ')[0],
                                     accountList[i+step*4].split(' ')[1][:-1]))
            print(accountList[i+step*4].split(' ')[0])
        time.sleep(5)
        to_homepage(androids)
        main_run_quick(androids, ['close_white'])

        for _ in range(0, 3):
            main_run_quick(androids, ['add_blue', 'ok_blue', 'ok_white'])

        main_run_quick(androids, ['adventure', 'masterbatch',
                             '3-1', 'timeadd', 'run_cn', 'ok_blue'])
        time.sleep(2)
        main_run_quick(androids, ['skip_cn', 'ok_white'])
        for a in androids:
            a.click((1200, 50))
        main_run(androids, ['cancel_white'])
        time.sleep(2)

        # 地下城战斗
        main_run_quick(
            androids, ['adventure_selected', 'underground', 'normalUD', 'ok_blue'])
        time.sleep(3)
        main_run_quick(androids, ['floor1'])
        time.sleep(4)
        main_run_quick(androids, ['challenge_blue'])
        time.sleep(3)
        # mainrunQuick(lines,['yui','pecorine','kokkoro','kyaru','getassist','assist','battlestart','ok_blue'])
        main_run_quick(androids, ['getassist', 'assist', 'battlestart', 'ok_blue'])
        time.sleep(4)
        main_run_quick(androids, ['menu_white', 'giveup_white', 'giveup_blue'])
        time.sleep(4)
        main_run_quick(androids, ['withdraw', 'ok_blue'])

        # 回登陆页，开始下一次iteration
        main_run_quick(androids, ['mainpage', 'backtotitle', 'ok_blue'])
        time.sleep(3)

    # 踢出换工会上支援
    login(androids[0], farm1_leader)
    # login(lines[1],farm2Sudo)
    login(androids[2], real_account)
    to_homepage([androids[0]])
    to_homepage([androids[2]])
    time.sleep(2)
    main_run([androids[0], androids[2]], ['close_white'])
    time.sleep(2)
    kick([androids[0]])
    time.sleep(2)
    clan_add([androids[2]], 'qxxxFarm2')
    time.sleep(4)
    main_run([androids[2]], ['setassist', 'addselect', 'myassist', 'set', 'ok_blue'])
    time.sleep(3)
    main_run([androids[2]], ['homepage_red'])
    time.sleep(2)
    main_run([androids[0], androids[2]], ['mainpage', 'backtotitle', 'ok_blue'])

    accountList = get_account('accountlist2.txt')  # 获取账号列表2

    # 共12个号，4开为例
    for step in range(0, 3):

        # 依次登陆4个号
        for i in range(0, len(androids)):
            login(androids[i], UserInfo(accountList[i+step*4].split(' ')[0],
                                     accountList[i+step*4].split(' ')[1][0:-1]))
            print(accountList[i+step*4].split(' ')[0])
        time.sleep(5)
        to_homepage(androids)
        main_run_quick(androids, ['close_white'])

        for _ in range(0, 3):
            main_run_quick(androids, ['add_blue', 'ok_blue', 'ok_white'])

        main_run_quick(androids, ['adventure', 'masterbatch',
                             '3-1', 'timeadd', 'run_cn', 'ok_blue'])
        time.sleep(2)
        main_run_quick(androids, ['skip_cn', 'ok_white'])
        for a in androids:
            a.click((1200, 50))
        main_run(androids, ['cancel_white'])
        time.sleep(2)

        # 地下城战斗
        main_run_quick(
            androids, ['adventure_selected', 'underground', 'normalUD', 'ok_blue'])
        time.sleep(3)
        main_run_quick(androids, ['floor1'])
        time.sleep(4)
        main_run_quick(androids, ['challenge_blue'])
        time.sleep(3)
        # mainrunQuick(lines,['yui','pecorine','kokkoro','kyaru','getassist','assist','battlestart','ok_blue'])
        main_run_quick(androids, ['getassist', 'assist', 'battlestart', 'ok_blue'])
        time.sleep(4)
        main_run_quick(androids, ['menu_white', 'giveup_white', 'giveup_blue'])
        time.sleep(4)
        main_run_quick(androids, ['withdraw', 'ok_blue'])

        # 回登陆页，开始下一次iteration
        main_run_quick(androids, ['mainpage', 'backtotitle', 'ok_blue'])
        time.sleep(3)

    # 踢出换工会上支援
    # login(lines[0],farm1Sudo)
    login(androids[1], farm2_leader)
    login(androids[2], real_account)
    to_homepage([androids[1], androids[2]])
    main_run([androids[1], androids[2]], ['close_white'])
    time.sleep(2)
    kick([androids[1]])
    time.sleep(2)
    clan_add([androids[2]], 'qxxxFarm1')
    time.sleep(4)
    main_run([androids[2]], ['setassist', 'addselect', 'myassist', 'set', 'ok_blue'])
    time.sleep(3)
    main_run([androids[2]], ['homepage_red'])
    time.sleep(3)
    main_run([androids[1], androids[2]], ['mainpage', 'backtotitle', 'ok_blue'])

    # 退出程序
    os.system('adb kill-server')
