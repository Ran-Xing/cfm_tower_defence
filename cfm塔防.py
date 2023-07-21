# -*- encoding=utf8 -*-
__author__ = "xr"

import logging
from multiprocessing import Process
import random
from airtest.core.api import *

auto_setup(__file__)

# 设置 airtest 日志级别为 WARNING
logger = logging.getLogger("airtest")
logger.setLevel(logging.WARNING)
device = connect_device("Android://")

skip_bottom = Template(r"跳过.png", record_pos=(0.108, -0.168), resolution=(3040, 1440))
get_gift_bottom = Template(r"免费购买.png", record_pos=(-0.276, 0.021), resolution=(3040, 1440))
start_game_bottom = Template(r"开始游戏.png", record_pos=(0.167, 0.208), resolution=(3040, 1440))
shoot_bottom = Template(r"开火键.png", threshold=0.5, record_pos=(0.365, 0.132), resolution=(3040, 1440))
bot_bottom = Template(r"堡垒机器人.png", record_pos=(0.451, 0.071), resolution=(3040, 1440))
eye_bottom = Template(r"视角.png", record_pos=(-0.462, 0.135), resolution=(3040, 1440))
space_bottom = Template(r"空格.png", threshold=0.5, record_pos=(-0.175, 0.135), resolution=(3040, 1440))
gun_bottom = Template(r"机枪.png", threshold=0.5, record_pos=(-0.171, 0.068), resolution=(3040, 1440))
go_home = Template(r"返回大厅.png", record_pos=(0.385, 0.19), resolution=(3040, 1440))
exit_gift = Template(r"直接退出.png", record_pos=(-0.086, 0.132), resolution=(3040, 1440))
update_bottom = Template(r"升级.png", record_pos=(0.015, 0.148), resolution=(3040, 1440))
zhuangbei_bottom = Template(r"装备.png", record_pos=(0.396, 0.186), resolution=(3040, 1440))
wan_cheng_bottom = Template(r"完成.png", record_pos=(-0.453, -0.218), resolution=(3040, 1440))
process = [None, None, None]


def skip():
    while True:
        logger.warning("跳过")
        retry(skip_bottom, 5, 5)


def get_gift():
    while True:
        logger.warning("免费抽奖")
        if retry(get_gift_bottom, 1, 5):
            retry(exit_gift, 2, 5)


def manage():
    while True:
        for _ in range(5):
            logger.warning("新建机器人")
            if retry(shoot_bottom, 1, 3):
                if retry(eye_bottom, 1, 3):  # 开启视角
                    logger.warning("滑动视角")
                    # 大图开启
                    # int_view = random.choice([100, 1000])
                    # swipe((1554, 674), (1554, int_view))
                    # swipe((1554, 674), (1554, int_view))
                    # swipe((1554, 674), (1554, int_view))
                    # swipe((1554, 674), (1554, int_view))
                    # swipe((1554, 674), (1554, int_view))
                    logger.warning("查找空位")
                    retry(space_bottom, 2, 10)  # 选择空格
                    logger.warning("放置机枪")
                    retry(gun_bottom, 1, 5)  # 机枪
                    # retry(gun_bottom, 1, 2)  # 机枪
                    logger.warning("关闭视角")
                    retry(eye_bottom, 1, 5)  # 关闭视角
            else:
                retry(eye_bottom, 1, 5)  # 关闭视角
            if retry(update_bottom, 1, 2):  # 升级
                logger.warning("升级")
                touch((1153, 700))  # 升级 三级 设备


def retry(v1, t1, s1):
    logger.warning("查找[%s] 等待%ds 重试%d次", v1.filename, t1, s1)
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


def game_start():
    logger.warning("开始游戏")
    while True:
        if retry(shoot_bottom, 1, 1):
            break
    # 如果不需要就删除这行 》
    while True:
        if retry(bot_bottom, 1, 1):
            logger.warning("放置机枪")
            break
    # 《 如果不需要就删除这行
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
    retry(zhuangbei_bottom, 1, 5)  # 装备
    logger.warning("完成")
    retry(wan_cheng_bottom, 1, 5)  # 完成
    # 滑动屏幕
    swipe((1554, 674), (1511, 950))
    start_process()
    while True:
        if retry(shoot_bottom, 3, 1):
            time.sleep(5)
        else:
            break


def game_end():
    while True:
        if retry(go_home, 5, 100):
            stop_process()
            logger.warning("返回大厅")
            break
    time.sleep(3)
    retry(Template(r"火线防御-守护中心.png", record_pos=(-0.38, -0.175), resolution=(3040, 1440)), 1, 5)
    retry(Template(r"炼狱.png", record_pos=(-0.442, -0.056), resolution=(3040, 1440)), 1, 5)
    retry(Template(r"普通.png", record_pos=(-0.147, -0.132), resolution=(3040, 1440)), 1, 5)
    time.sleep(5)
    touch((1500, 630))
    touch((1500, 630))
    logger.warning("游戏结束")


def start_process():
    global process
    for i in process:
        if i is not None and i.is_alive():
            logger.warning("进程已经在运行中")
            i.terminate()

    process[0] = Process(target=skip)
    process[1] = Process(target=get_gift)
    process[2] = Process(target=manage)
    for i in process:
        i.start()
    logger.warning("进程已启动")


def stop_process():
    global process
    for i in process:
        if i is not None and i.is_alive():
            i.terminate()
    logger.warning("进程已经停止")


if __name__ == '__main__':
    while True:
        if retry(shoot_bottom, 1, 1):
            start_process()
            game_end()
        else:
            if retry(start_game_bottom, 1, 1):
                game_start()
            if retry(go_home, 1, 1):
                game_end()
