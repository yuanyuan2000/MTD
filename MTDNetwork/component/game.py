import pygame
import simpy
import MTDNetwork.data.constants as constants
import MTDNetwork.component.node as no
from MTDNetwork.component.time_network import TimeNetwork
from MTDNetwork.operation.mtd_operation import MTDOperation
from MTDNetwork.data.constants import ATTACKER_THRESHOLD
from MTDNetwork.component.adversary import Adversary
from MTDNetwork.operation.attack_operation import AttackOperation
from MTDNetwork.snapshot.snapshot_checkpoint import SnapshotCheckpoint
# from MTDNetwork.statistic.metrics import Metrics
import sys
import logging
# from threading import Timer


class Game:
    def __init__(self):
        # initialize the environment
        pygame.init()
        self.env = simpy.Environment()

        # initialize game window
        self.window = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.display.set_caption("Moving Target Defense Game")
        self.width = constants.WIDTH
        self.height = constants.HEIGHT

        # initialize logging information
        logging.basicConfig(level=logging.INFO)

        # load the background image
        try:
            self.background = pygame.image.load("MTDNetwork/resource/image/background.png")
        except pygame.error:
            logging.error("Could not load background image")
            pygame.quit()
            sys.exit()
        # logging.info(f"Background size: {self.background.get_size()}")
        bg_width, bg_height = self.background.get_size()
        if bg_width < constants.WIDTH or bg_height < constants.HEIGHT:
            self.background = pygame.transform.scale(self.background, (constants.WIDTH, constants.HEIGHT))

        # initialize the game clock
        self.clock = pygame.time.Clock()

        # the physical time we start the game, in milliseconds
        self.game_start_time = None
        # the physical time of last game loop, in milliseconds
        self.game_last_time = 0
        # the simulation time, but numerically equal to physical time we run the game in seconds
        self.sim_time = 0.0

        # initialize information about network
        self.network = None
        self.nodes = []

        # initialize the adversary
        self.adversary = None

        # initialize parameters about user interface
        self.node_radius = constants.NODE_RADIUS
        self.edge_width = constants.EDGE_WIDTH
        # self.game_time = constants.GAME_TIME
        # self.time_mtd = constants.TIME_MTD
        # self.time_compromise = constants.TIME_COMPROMISE
        # self.settings_open = False
        # self.selected_node = None
        # self.selected_strategy = None
        # self.time_since_compromise = 0

        # x, y coordinates in class Network scale and shift to get the screen coordinates
        self.scale_x = 1
        self.scale_y = 1
        self.shift_y = 0

    def init(self, start_time=0, finish_time=1000, scheme='randomly', checkpoints=None):
        """
        all operation about initialize the game
        """
        # initialise the snapshot checkpoint
        snapshot_checkpoint = SnapshotCheckpoint(env=self.env, checkpoints=checkpoints)

        # load saved snapshots and initialise the network
        if start_time != 0:
            self.network, self.adversary = snapshot_checkpoint.load_snapshots(start_time)
            self.sim_time = start_time
        # initialise the network
        else:
            self.network = TimeNetwork()
            self.sim_time = 0.0
        self.update_network()

        # initialise the adversary
        self.adversary = Adversary(network=self.network, attack_threshold=ATTACKER_THRESHOLD)

        # start attack
        attack_operation = AttackOperation(env=self.env, adversary=self.adversary, proceed_time=start_time)
        attack_operation.proceed_attack()

        # start mtd
        if scheme != 'None':
            mtd_operation = MTDOperation(env=self.env, network=self.network, scheme=scheme,
                                         attack_operation=attack_operation, proceed_time=start_time)
            mtd_operation.proceed_mtd()

        # save snapshot
        if checkpoints is not None:
            snapshot_checkpoint.proceed_save(self.network, self.adversary)

        # time_network.get_mtd_stats().save_record(sim_time=finish_time, scheme=scheme)
        # adversary.get_attack_stats().save_record(sim_time=finish_time, scheme=scheme)
        # metrics = Metrics(network=time_network, adversary=adversary)
        # return metrics

    def update_network(self):
        """
        update the information about the network and the nodes in network
        """
        self.scale_x = 140
        self.scale_y = (self.height - constants.BLANK * 2) // (self.network.max_y_pos - self.network.min_y_pos)
        self.shift_y = self.height - constants.BLANK * 2 - self.scale_y * self.network.max_y_pos

        pos_dict = self.network.pos
        color_list = self.network.colour_map
        self.nodes = []
        for key, color in zip(pos_dict, color_list):
            x = (pos_dict[key][0] * self.scale_x) + constants.BLANK
            y = (pos_dict[key][1] * self.scale_y) + self.shift_y + constants.BLANK
            self.nodes.append(no.Node(key, x, y, color))

    def draw_nodes(self):
        """
        draw all the node in the network
        """
        for node in self.nodes:
            pygame.draw.circle(self.window, node.color, (node.x, node.y), self.node_radius)
            # pygame.draw.circle(self.window, (255, 255, 255), (node.x, node.y), self.node_radius, 1)
            self.draw_text(str(node.id), (node.x, node.y), (0, 0, 0), 12)

    def draw_edges(self):
        """
        draw lines between adjacent nodes
        """
        graph = self.network.graph
        for edge in graph.edges:
            start_x = (self.network.pos[edge[0]][0] * self.scale_x) + constants.BLANK
            start_y = (self.network.pos[edge[0]][1] * self.scale_y) + self.shift_y + constants.BLANK
            end_x = (self.network.pos[edge[1]][0] * self.scale_x) + constants.BLANK
            end_y = (self.network.pos[edge[1]][1] * self.scale_y) + self.shift_y + constants.BLANK
            pygame.draw.line(self.window, (150, 150, 150), (start_x, start_y), (end_x, end_y), 1)

    def draw_text(self, text, pos, color, size):
        """
        draw the text
        :param text: the content of text
        :param pos: the position of text
        :param color: the color of text
        :param size: the size of text
        """
        font = pygame.font.SysFont('comicsansms', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = pos
        self.window.blit(text_surface, text_rect)

    # def draw_button(self, text, pos, size, action):
    #     """
    #     绘制按钮
    #     :param text: 按钮上显示的文字
    #     :param pos: 按钮的位置
    #     :param size: 按钮的大小
    #     :param action: 点击按钮触发的事件
    #     """
    #     button_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
    #     mouse_pos = pygame.mouse.get_pos()
    #     if button_rect.collidepoint(mouse_pos):
    #         pygame.draw.rect(self.window, (210, 210, 210), button_rect)
    #     else:
    #         pygame.draw.rect(self.window, (255, 255, 255), button_rect)
    #     self.draw_text(text, (pos[0] + size[0] // 2, pos[1] + size[1] // 2), (0, 0, 0), 12)
    #
    #     # 判断鼠标是否在按钮上
    #     if button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
    #         self.action(action)

    # def draw_mtd_button(self):
    #     """
    #     绘制游戏选择MTD策略的按钮
    #     """
    #     self.draw_button("IP Shuffling", (self.width - 150, self.height // 2 - 100), (100, 25),
    #                      constants.BUTTON_IP_SHUFFLING)
    #     self.draw_button("Port Shuffling", (self.width - 150, self.height // 2 - 25), (100, 25),
    #                      constants.BUTTON_PORT_SHUFFLING)
    #     self.draw_button("Topology Shuffling", (self.width - 150, self.height // 2 + 50), (100, 25),
    #                      constants.BUTTON_TOPOLOGY_SHUFFLING)

    # def action(self, action):
    #     """
    #     处理各种响应事件
    #     """
    #     if action == constants.BUTTON_IP_SHUFFLING or action == constants.BUTTON_PORT_SHUFFLING \
    #             or action == constants.BUTTON_TOPOLOGY_SHUFFLING:
    #         self.start_mtd(action)

    # def start_mtd(self, action):
    #     check = True
    #     num = -1
    #     for i, node in enumerate(self.nodes):
    #         if node.mtd_state == constants.MTD_STATE_CONFIGURING:
    #             check = False
    #         if node.is_chosen:
    #             num = i
    #     if check and num >= 0:
    #         self.nodes[num].set_mtd(constants.MTD_STATE_CONFIGURING, action)
    #         # 启动计时线程
    #         # timer_thread = TimerThread(constants.TIME_MTD, lambda: self.finish_mtd())
    #         # timer_thread.start()
    #         t = Timer(constants.TIME_MTD, self.finish_mtd)
    #         t.start()
    #
    # def finish_mtd(self):
    #     for i, node in enumerate(self.nodes):
    #         if node.mtd_state == constants.MTD_STATE_CONFIGURING:
    #             node.set_mtd(constants.MTD_STATE_READY, None)
    #         elif node.mtd_state == constants.MTD_STATE_WAITING:
    #             node.set_mtd(constants.MTD_STATE_READY, None)

    def run(self):
        """
        main game loop
        """
        running = True

        # record the time we start the game
        self.game_start_time = pygame.time.get_ticks()
        self.game_last_time = self.game_start_time

        while running:
            self.clock.tick(60)  # game loop run at most 60 frames per second

            # time
            time_step = (pygame.time.get_ticks() - self.game_last_time) / 1000.0
            if time_step > 0.0:
                # update the simulation time
                self.sim_time += time_step
                self.game_last_time = pygame.time.get_ticks()
                # run simulation
                self.env.run(until=self.sim_time)

            # update
            self.update_network()

            # handle events
            for event in pygame.event.get():
                # QUIT event
                if event.type == pygame.QUIT:
                    running = False
            #     # 点击节点事件
            #     # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #     # 鼠标移动到节点上
            #     if event.type == pygame.MOUSEMOTION:
            #         mouse_pos = pygame.mouse.get_pos()
            #         for node in self.nodes:
            #             node_pos = pygame.math.Vector2(node.x, node.y)
            #             distance = node_pos.distance_to(mouse_pos)
            #             if distance <= node.radius:
            #                 for node2 in self.nodes:
            #                     node2.not_on_it()
            #                 node.on_it()
            #                 break

            # draw the windows
            self.window.fill((50, 50, 50))
            self.window.blit(self.background, (0, 0))
            self.draw_edges()
            self.draw_nodes()
            # self.draw_text("Time remaining: {}s".format(int(self.game_time - (pygame.time.get_ticks() + game_start_time)
            #                                                 / 1000)), (self.width // 2, 20), (255, 255, 255), 20)
            # self.draw_mtd_button()

            pygame.display.flip()

        pygame.quit()
