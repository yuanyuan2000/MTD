import MTDNetwork.data.constants as constants
import random
import threading

# # 定义节点的 MTD 状态，0表示正在配置MTD策略，1表示随时可以被配置，2表示需等待其他节点完成配置
# MTD_STATE_CONFIGURING = constants.MTD_STATE_CONFIGURING
# MTD_STATE_READY = constants.MTD_STATE_READY
# MTD_STATE_WAITING = constants.MTD_STATE_WAITING
#
# # 定义节点的攻击状态, 0表示没有被攻击，1表示正在被攻击，2表示已经被攻破
# ATTACK_STATE_NOT_ATTACKED = constants.ATTACK_STATE_NOT_ATTACKED
# ATTACK_STATE_ATTACKING = constants.ATTACK_STATE_ATTACKING
# ATTACK_STATE_ATTACKED = constants.ATTACK_STATE_ATTACKED


# 定义节点类，用于储存每个节点的当前状态（如位置，颜色，MTD策略，是否被破解等）
class Node:

    def __init__(self, num, x, y, color):
        self.id = num
        self.x = x
        self.y = y
        self.color = color

        self.is_chosen = False  # 表示节点是否被鼠标选中
        # self.mtd_state = MTD_STATE_READY
        # self.mtd_time = 0  # 当前节点距离MTD策略执行完成的时间
        # self.mtd_strategy = constants.MTD_STRATEGY[0]
        #
        # self.attack_state = ATTACK_STATE_NOT_ATTACKED
        # self.attack_time = 0  # 当前节点距离被攻破的时间

    # 当节点状态发生变化时，更新节点的位置，大小，颜色等参数
    # def update(self):
    #     if self.mtd_state == MTD_STATE_CONFIGURING:
    #         self.color = (0, 255, 0)  # MTD策略配置中，节点为绿色
    #     elif self.mtd_state == MTD_STATE_READY:
    #         self.color = constants.NODE_COLOR  # 空闲时，节点为白色
    #     elif self.mtd_state == MTD_STATE_READY:
    #         self.color = (128, 128, 128)  # 等待其他节点完成配置时，节点为灰色
    #
    #     if self.attack_state == ATTACK_STATE_ATTACKED:
    #         self.color = (20, 20, 20)  # 被破解，节点为黑色，无法再配置新的MTD策略
    #     elif self.attack_state == ATTACK_STATE_ATTACKING:
    #         if self.mtd_state == MTD_STATE_CONFIGURING:
    #             self.color = (255, 255, 0)  # MTD策略配置中且正在被攻击，节点为橙色
    #         else:
    #             self.color = (255, 0, 0)  # 空闲或等待时被攻击，节点为红色
    #
    #     if self.is_chosen:
    #         self.radius = constants.NODE_RADIUS * 1.3
    #     else:
    #         self.radius = constants.NODE_RADIUS

    # 用于改变节点的MTD状态和类型
    # def set_mtd(self, mtd_state, mtd_type):
    #     if mtd_state == MTD_STATE_CONFIGURING:
    #         self.mtd_strategy = constants.MTD_STRATEGY[mtd_type]
    #         self.mtd_state = MTD_STATE_CONFIGURING
    #     elif mtd_state == MTD_STATE_READY:
    #         self.mtd_state = MTD_STATE_READY
    #         self.mtd_strategy = constants.MTD_STRATEGY[0]
    #     elif mtd_state == MTD_STATE_WAITING:
    #         self.mtd_state = MTD_STATE_WAITING
    #         self.mtd_strategy = constants.MTD_STRATEGY[0]
    #     self.update()

    # # 当鼠标在节点上时
    # def on_it(self):
    #     self.is_chosen = True
    #     self.update()
    #
    # # 当鼠标没有在节点上时
    # def not_on_it(self):
    #     self.is_chosen = False
    #     self.update()
    #
    # # 当节点开始被攻击时触发此函数
    # def being_attack(self):
    #     if self.attack_state == ATTACK_STATE_NOT_ATTACKED:
    #         self.attack_state = ATTACK_STATE_ATTACKING
    #         self.attack_time = constants.TIME_COMPROMISE
    #         self.update()
    #
    # # 当节点被攻破时触发此函数
    # def compromise(self):
    #     if self.attack_state == ATTACK_STATE_ATTACKING:
    #         self.attack_state = ATTACK_STATE_ATTACKED
    #         self.attack_time = 0
    #         self.update()
    #
    # # 当节点正在攻击时被MTD策略中断时触发此函数
    # def interrupt(self):
    #     if self.attack_state == ATTACK_STATE_ATTACKING:
    #         self.attack_time = constants.TIME_COMPROMISE
    #         self.update()
