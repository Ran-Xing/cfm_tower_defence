# -*- encoding=utf8 -*-
__author__ = "xr"

import logging
import time

from airtest.core.api import *

auto_setup(__file__)

# 设置 airtest 日志级别为 WARNING
logger = logging.getLogger("airtest")
logger.setLevel(logging.WARNING)
device = connect_device("Android://")

skip_bottom = Template(r"跳过.png", record_pos=(0.108, -0.168), resolution=(3040, 1440))
start_game_bottom = Template(r"开始游戏.png", record_pos=(0.167, 0.208), resolution=(3040, 1440))
shoot_bottom = Template(r"开火键.png", threshold=0.5, record_pos=(0.365, 0.132), resolution=(3040, 1440))
bot_bottom = Template(r"堡垒机器人.png", record_pos=(0.451, 0.071), resolution=(3040, 1440))
go_home = Template(r"返回大厅.png", record_pos=(0.385, 0.19), resolution=(3040, 1440))
gun_bottom = Template(r"机枪.png", threshold=0.6, record_pos=(-0.171, 0.068), resolution=(3040, 1440))
gun_plus_bottom = Template(r"机枪Plus.png", threshold=0.6, record_pos=(-0.171, 0.068), resolution=(3040, 1440))
zhuang_bei_bottom = Template(r"装备.png", record_pos=(0.396, 0.186), resolution=(3040, 1440))
wan_cheng_bottom = Template(r"完成.png", record_pos=(-0.453, -0.218), resolution=(3040, 1440))
eye_bottom = Template(r"视角.png", record_pos=(-0.462, 0.135), resolution=(3040, 1440))
space_bottom = Template(r"空格.png", threshold=0.5, record_pos=(-0.175, 0.135), resolution=(3040, 1440))
update_bottom = Template(r"升级.png", record_pos=(0.015, 0.148), resolution=(3040, 1440))
exit_gift = Template(r"直接退出.png", record_pos=(-0.086, 0.132), resolution=(3040, 1440))
get_gift_bottom = Template(r"免费购买.png", record_pos=(-0.276, 0.021), resolution=(3040, 1440))


def retry(v1, t1, s1):
    logger.warning("查找[%s] 等待%ds 重试%d次", v1.filename.replace(".png", ""), t1, s1)
    try:
        for i in range(s1):
            if exists(v1):
                touch(v1)
                return True
            else:
                time.sleep(t1)
            if i == s1:
                return False
    except:
        return False
    return False


def app():
    while True:
        if retry(shoot_bottom, 1, 1):
            in_game()
            return
        if retry(start_game_bottom, 1, 1):
            break
        if retry(go_home, 1, 1):
            return
    retry(start_game_bottom, 1, 1)
    print("\033[H\033[2J")  # 清理屏幕
    logger.warning("开始游戏")
    time.sleep(7)
    # 如果不需要就删除这行 ==>
    while True:
        if retry(bot_bottom, 1, 3):
            logger.warning("放置机枪")
            break
    # <== 如果不需要就删除这行
    logger.warning("进入管理")
    touch((958, 1358))
    time.sleep(2)
    logger.warning("删除装备")
    touch((908, 248))  # 删除装备
    touch((908, 248))  # 删除装备
    touch((908, 248))  # 删除装备
    touch((908, 248))  # 删除装备
    touch((908, 248))  # 删除装备
    logger.warning("选择装备")
    retry(gun_bottom, 1, 5)  # 机枪
    logger.warning("添加装备")
    retry(zhuang_bei_bottom, 1, 5)  # 装备
    logger.warning("完成")
    retry(wan_cheng_bottom, 1, 5)  # 完成
    swipe((1554, 674), (1511, 950))  # 滑动
    in_game()
    while True:
        if retry(go_home, 5, 5):
            logger.warning("返回大厅")
            break


def in_game():
    while True:
        if retry(shoot_bottom, 1, 1):
            if retry(skip_bottom, 1, 1):
                logger.warning("跳过")
            if retry(get_gift_bottom, 1, 1):
                logger.warning("领取礼包")
                retry(exit_gift, 1, 1)
            if retry(eye_bottom, 1, 3):  # 开启视角
                logger.warning("新建机器人")
                logger.warning("查找空位")
                retry(space_bottom, 2, 10)  # 选择空格
                logger.warning("放置机枪")
                if not retry(gun_bottom, 1, 1):  # 机枪
                    retry(gun_plus_bottom, 1, 1)  # 机枪Plus
                logger.warning("关闭视角")
                retry(eye_bottom, 1, 5)  # 关闭视角
                if retry(update_bottom, 1, 1):  # 升级
                    retry(gun_plus_bottom, 1, 1)  # touch((1452, 656))  # 升级
        else:
            if not retry(eye_bottom, 1, 3):
                break


if __name__ == '__main__':
    for i in range(100):
        app()
