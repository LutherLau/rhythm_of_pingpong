import controller
import game_objects
import pygame
import resource
import config
import controller_functions
import network_module
import random


class Game:
    def __init__(self):

        # 初始化
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.mixer.set_num_channels(8)

        self.cfg = config.Config()

        # 初始化窗口
        self.scr = pygame.display.set_mode(self.cfg.screen_size)
        self.title = 'Rhythm of PingPong'
        self.icon = pygame.image.load('res/images/icon.ico').convert_alpha()
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(self.title)
        pygame.mouse.set_visible(False)
        self.back_ground = pygame.image.load('res/images/start_page_bg.png').convert_alpha()
        self.back_ground = pygame.transform.smoothscale(self.back_ground, self.cfg.screen_size)
        self.scr.blit(self.back_ground, (0, 0))
        pygame.display.flip()

        # 初始化游戏组件
        self.res = resource.Resource(self.cfg)
        self.cof = controller_functions.ControllerFunction(self.cfg)
        self.data_sync = network_module.GameDataSync()

        # 游戏Context
        self.context = {'cfg': self.cfg,
                        'res': self.res,
                        'cof': self.cof,
                        'scr': self.scr,
                        'umd': 'index_ui',
                        'dsy': self.data_sync
                        }

        self.players = [game_objects.Player(0, self.context), game_objects.Player(1, self.context)]
        self.context['pys'] = self.players

        self.clock = pygame.time.Clock()
        self.index_ui = index_ui(self.context)
        self.off_line_one_ui = off_line_one_ui(self.context)
        self.off_line_two_ui = off_line_two_ui(self.context)
        self.on_line_battle = on_line_battle(self.context)
        self.on_line_ranking = on_line_ranking(self.context)
        self.current_ui = self.index_ui

    def run(self):
        # 游戏入口， 设置起始界面
        self.context['umd'] = 'index_ui'

        pygame.mixer.music.play(-1)

        while True:
            # 刷新UI
            if self.context['umd'] == 'index_ui':
                self.index_ui.update()
                controller.control(self.context, self.index_ui)
            elif self.context['umd'] == 'off_line_two_ui':
                self.off_line_two_ui.update()
                controller.control(self.context, self.off_line_two_ui)
            elif self.context['umd'] == 'off_line_one_ui':
                self.off_line_one_ui.update()
                controller.control(self.context, self.off_line_one_ui)
            elif self.context['umd'] == 'on_line_battle':
                self.on_line_battle.update()
                controller.control(self.context, self.on_line_battle)
            elif self.context['umd'] == 'on_line_ranking':
                self.on_line_ranking.update()
                controller.control(self.context, self.on_line_ranking)

            # 测试用片段
            # self.context['screen'].blit(controller_functions.words2img(self.get_fps()), (0, 0))

            pygame.display.update()
            # pygame.display.set_caption(str(self.clock.get_fps()))

            self.clock.tick(55)


class on_line_battle:
    def __init__(self, context):
        self.context = context
        self.ball = game_objects.Ball(self.context)
        self.music_flag = True
        self.over_flag = False
        self.start_pre_flag = False
        self.running_flag = False
        self.dialog_flag = False
        self.lose_flag = False
        self.tie_flag = False
        self.win_flag = False
        self.last_winner = 'right'
        self.match_flag = True
        self.pr_toast_flag = 0

        self.left_toast_flag = 0
        self.right_toast_flag = 0

        self.reset_flags()

        self.left_toast_img = self.context['cof'].words2img('本局位置在左侧！', 80, (550, 162))
        self.right_toast_img = self.context['cof'].words2img('本局位置在右侧！', 80, (550, 162))

        self.pr_toast_img = self.context['cof'].words2img('网络错误，无法联网对战', 80, (603, 162))
        self.match_flag_img = self.context['cof'].words2img('正在匹配，请稍后！', 90, (533, 450))
        self.win_img = self.context['cof'].words2img('厉害厉害，你赢了！', 90, (533, 450))
        self.lose_img = self.context['cof'].words2img('不要气馁，再战！！', 90, (533, 450))
        self.tie_img = self.context['cof'].words2img('同是高手，难分伯仲！', 90, (533, 450))

    def match(self):
        if self.context['dsy'].connect() and self.context['pys'][0].state:
            self.context['dsy'].put_data('u b')
            # print('进入匹配队列')

    def reset(self):
        self.reset_flags()
        self.ball.reset()

    def reset_flags(self):

        self.match_flag = True
        self.music_flag = True

        self.over_flag = False
        self.start_pre_flag = False
        self.running_flag = False
        self.dialog_flag = False
        self.lose_flag = False
        self.win_flag = False
        self.tie_flag = False
        self.last_winner = 'right'

    def adjust_ver(self):
        self.context['dsy'].put_data('so bv' + self.ball.get_ver_1080p() + '@')

    def update(self):
        # 贴背景
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].level_1_bg)))

        # 贴元素
        self.context['scr'].blit(**(self.context['pys'][0].paddle.get_res()))
        self.context['scr'].blit(**(self.context['pys'][1].paddle.get_res()))
        self.context['scr'].blit(**(self.ball.get_res()))

        # 贴分数
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][0].score_img)))
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][1].score_img)))

        if self.match_flag:
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].mask_bg)))
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].dialog_bg)))
            self.context['scr'].blit(**(self.context['cof'].get_res(self.match_flag_img)))
            self.context['scr'].blit(self.context['res'].arrow_dark[0], pygame.mouse.get_pos())

        elif self.dialog_flag:
            # 贴对话框
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].mask_bg)))
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].dialog_bg)))
            if self.over_flag:
                # 放音乐
                # 展示获胜者
                if self.win_flag:
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.win_img)))
                    if self.music_flag:
                        self.context['res'].win_sound.play()
                        self.music_flag = False

                elif self.lose_flag:
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.lose_img)))
                    if self.music_flag:
                        self.context['res'].lose_sound.play()
                        self.music_flag = False

                elif self.tie_flag:
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.tie_img)))
                    if self.music_flag:
                        self.context['res'].tie_sound.play()
                        self.music_flag = False

                self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].re_start)))
                self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].like)))

                # 控制处理 self.reset()
                # 再来一局
            # 返回大厅
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].back)))
            self.context['scr'].blit(self.context['res'].arrow_dark[0], pygame.mouse.get_pos())

        elif self.running_flag:
            # 如果是左侧玩家，负责演算
            self.context['pys'][0].paddle.move()

            if self.context['pys'][0].side == 'left':
                self.ball.move()
                if self.context['pys'][0].paddle.get_right() >= self.ball.get_left():
                    # 上侧边界
                    if self.context['pys'][0].paddle.get_top() <= self.ball.get_bottom() < \
                            self.context['pys'][0].paddle.get_bottom():
                        if not (self.ball.get_top() >= self.context['pys'][0].paddle.get_top()):
                            self.ball.ver[1] = -self.ball.ver[1]
                            self.ball.pos[1] = self.context['pys'][0].paddle.get_top() - self.ball.img.get_height() - 1
                            # 不只是侧面碰撞
                        self.ball.ver[0] = -self.ball.ver[0]
                        self.ball.pos[0] = self.context['pys'][0].paddle.get_right() + 1
                        self.context['res'].bounce_sound.play()
                        self.context['dsy'].put_data('so sb' + '@')

                    # 下侧边界
                    elif self.context['pys'][0].paddle.get_bottom() >= self.ball.get_top() > \
                            self.context['pys'][0].paddle.get_top():
                        if not (self.ball.get_bottom() <= self.context['pys'][0].paddle.get_bottom()):
                            self.ball.ver[1] = -self.ball.ver[1]
                            self.ball.pos[1] = self.context['pys'][0].paddle.get_bottom() + 1
                            # 不只是侧面碰撞
                        self.ball.ver[0] = -self.ball.ver[0]
                        self.ball.pos[0] = self.context['pys'][0].paddle.get_right() + 1
                        self.context['res'].bounce_sound.play()
                        self.context['dsy'].put_data('so sb' + '@')
                # 一号玩家
                if self.context['pys'][1].paddle.get_left() <= self.ball.get_right():
                    # 上侧边界
                    if self.context['pys'][1].paddle.get_top() <= self.ball.get_bottom() < \
                            self.context['pys'][1].paddle.get_bottom():
                        if not (self.ball.get_top() >= self.context['pys'][1].paddle.get_top()):
                            self.ball.ver[1] = -self.ball.ver[1]
                            self.ball.pos[1] = self.context['pys'][1].paddle.get_top() - self.ball.img.get_height() - 1
                            # 不只是侧面碰撞
                        self.ball.ver[0] = -self.ball.ver[0]
                        self.ball.pos[0] = self.context['pys'][1].paddle.get_left() - self.ball.img.get_width() - 1
                        self.context['res'].bounce_sound.play()
                        self.context['dsy'].put_data('so sb' + '@')

                    # 下侧边界
                    elif self.context['pys'][1].paddle.get_bottom() >= self.ball.get_top() > \
                            self.context['pys'][1].paddle.get_top():
                        if not (self.ball.get_bottom() <= self.context['pys'][1].paddle.get_bottom()):
                            self.ball.ver[1] = -self.ball.ver[1]
                            self.ball.pos[1] = self.context['pys'][1].paddle.get_bottom() + 1
                            # 不只是侧面碰撞
                        self.ball.ver[0] = -self.ball.ver[0]
                        self.ball.pos[0] = self.context['pys'][1].paddle.get_left() - self.ball.img.get_width() - 1
                        self.context['res'].bounce_sound.play()
                        self.context['dsy'].put_data('so sb' + '@')

                # 左右边界检查
                if 0 >= self.ball.get_left():
                    # 分数统计
                    self.context['pys'][1].score += 10
                    self.context['dsy'].put_data(
                        'so s' + str(self.context['pys'][0].score) + ' ' + str(self.context['pys'][1].score) + '@')
                    self.context['pys'][1].renew_score_img()
                    self.ball.ver[0] = -self.ball.ver[0]
                    self.ball.pos[0] = 1
                    self.context['res'].in_sound.play()
                    self.context['dsy'].put_data('so si' + '@')
                    # self.ball.reset()

                if self.context['cfg'].screen_size[0] <= self.ball.get_right():
                    # 分数统计
                    self.context['pys'][0].score += 10
                    self.context['pys'][0].renew_score_img()
                    self.context['dsy'].put_data(
                        'so s' + str(self.context['pys'][0].score) + ' ' + str(self.context['pys'][1].score) + '@')
                    # 重新发球或者直接反弹
                    self.ball.ver[0] = -self.ball.ver[0]
                    self.ball.pos[0] = self.context['cfg'].screen_size[0] - self.ball.img.get_width() - 1
                    self.context['res'].in_sound.play()
                    self.context['dsy'].put_data('so si' + '@')
                    # self.ball.reset()
                    # 检查本局胜负
                    if self.context['pys'][0].score + self.context['pys'][1].score >= 400:
                        if self.context['pys'][0].score > self.context['pys'][1].score:
                            self.dialog_flag = True
                            self.over_flag = True
                            self.win_flag = True
                            self.context['dsy'].put_data('go l' + '@')

                        elif self.context['pys'][0].score < self.context['pys'][1].score:
                            self.dialog_flag = True
                            self.over_flag = True
                            self.lose_flag = True
                            self.context['dsy'].put_data('go w' + '@')

                        elif self.context['pys'][0].score + self.context['pys'][1].score == 500:
                            self.dialog_flag = True
                            self.over_flag = True
                            self.tie_flag = True
                            self.context['dsy'].put_data('go t' + '@')

                # 上下边界检查
                if 0 >= self.ball.get_top():
                    # 分数统计
                    self.ball.ver[1] = -self.ball.ver[1]
                    self.ball.pos[1] = 1

                if self.context['cfg'].screen_size[1] <= self.ball.get_bottom():
                    # 分数统计
                    self.ball.ver[1] = -self.ball.ver[1]
                    self.ball.pos[1] = self.context['cfg'].screen_size[1] - self.ball.img.get_height() - 1
                # 左侧玩家做同步消息给服务器
                # 位置
                self.context['dsy'].put_data('so b' + self.ball.get_1080p_pos() + '@')

                # 运动的时候， 同步位置
                if self.context['pys'][0].paddle.up or self.context['pys'][0].paddle.down:
                    self.context['dsy'].put_data('so p' + self.context['pys'][0].paddle.get_1080p_pos() + '@')

            else:
                if self.context['pys'][0].paddle.get_left() <= self.ball.get_right():
                    # 只模拟自己的
                    if self.context['pys'][0].paddle.get_top() <= self.ball.get_bottom() < \
                            self.context['pys'][0].paddle.get_bottom():
                        if not (self.ball.get_top() >= self.context['pys'][0].paddle.get_top()):
                            self.ball.ver[1] = -self.ball.ver[1]
                            self.ball.pos[1] = self.context['pys'][0].paddle.get_top() - self.ball.img.get_height() - 1
                            # 不只是侧面碰撞
                        self.ball.ver[0] = -self.ball.ver[0]
                        self.ball.pos[0] = self.context['pys'][0].paddle.get_left() - self.ball.img.get_width() - 1
                    # 下侧边界
                    elif self.context['pys'][0].paddle.get_bottom() >= self.ball.get_top() > \
                            self.context['pys'][0].paddle.get_top():
                        if not (self.ball.get_bottom() <= self.context['pys'][0].paddle.get_bottom()):
                            self.ball.ver[1] = -self.ball.ver[1]
                            self.ball.pos[1] = self.context['pys'][0].paddle.get_bottom() + 1
                            # 不只是侧面碰撞
                        self.ball.ver[0] = -self.ball.ver[0]
                        self.ball.pos[0] = self.context['pys'][0].paddle.get_left() - self.ball.img.get_width() - 1

                if self.context['pys'][0].paddle.up or self.context['pys'][0].paddle.down:
                    self.context['dsy'].put_data('so p' + self.context['pys'][0].paddle.get_1080p_pos() + '@')
        if self.pr_toast_flag:
            self.pr_toast_flag -= 1
            self.context['scr'].blit(**(self.context['cof'].get_res(self.pr_toast_img)))

        if self.right_toast_flag:
            self.right_toast_flag -= 1
            self.context['scr'].blit(**(self.context['cof'].get_res(self.right_toast_img)))

        if self.left_toast_flag:
            self.left_toast_flag -= 1
            self.context['scr'].blit(**(self.context['cof'].get_res(self.left_toast_img)))


class on_line_ranking:
    def __init__(self, context):
        self.context = context
        self.ball = game_objects.Ball(self.context)
        self.music_flag = True
        self.over_flag = False
        self.start_pre_flag = False
        self.running_flag = False
        self.dialog_flag = False
        self.lose_flag = False
        self.tie_flag = False
        self.win_flag = False
        self.last_winner = 'right'
        self.match_flag = True
        self.pr_toast_flag = 0
        self.left_toast_flag = 0
        self.right_toast_flag = 0

        self.reset_flags()

        self.pr_toast_img = self.context['cof'].words2img('网络错误，无法联网对战', 80, (603, 162))
        self.left_toast_img = self.context['cof'].words2img('本局位置在左侧！', 80, (550, 162))
        self.right_toast_img = self.context['cof'].words2img('本局位置在右侧！', 80, (550, 162))
        self.match_flag_img = self.context['cof'].words2img('正在匹配，请稍后！', 90, (533, 450))
        self.win_img = self.context['cof'].words2img('厉害厉害，你赢了！', 90, (533, 450))
        self.lose_img = self.context['cof'].words2img('不要气馁，再战！！', 90, (533, 450))
        self.tie_img = self.context['cof'].words2img('同是高手，难分伯仲！', 90, (533, 450))

    def match(self):
        if self.context['dsy'].connect() and self.context['pys'][0].state:
            self.context['dsy'].put_data('u r')
            # print('进入匹配队列')

    def reset(self):
        self.reset_flags()
        self.ball.reset()

    def reset_flags(self):

        self.match_flag = True
        self.music_flag = True

        self.over_flag = False
        self.start_pre_flag = False
        self.running_flag = False
        self.dialog_flag = False
        self.lose_flag = False
        self.win_flag = False
        self.tie_flag = False
        self.last_winner = 'right'

    def adjust_ver(self):
        self.context['dsy'].put_data('so bv' + self.ball.get_ver_1080p() + '@')

    def update(self):
        # 贴背景
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].level_1_bg)))

        # 贴元素
        self.context['scr'].blit(**(self.context['pys'][0].paddle.get_res()))
        self.context['scr'].blit(**(self.context['pys'][1].paddle.get_res()))
        self.context['scr'].blit(**(self.ball.get_res()))

        # 贴分数
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][0].score_img)))
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][1].score_img)))

        if self.match_flag:
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].mask_bg)))
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].dialog_bg)))
            self.context['scr'].blit(**(self.context['cof'].get_res(self.match_flag_img)))
            self.context['scr'].blit(self.context['res'].arrow_dark[0], pygame.mouse.get_pos())

        elif self.dialog_flag:
            # 贴对话框
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].mask_bg)))
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].dialog_bg)))
            if self.over_flag:
                # 放音乐
                # 展示获胜者
                if self.win_flag:
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.win_img)))
                    if self.music_flag:
                        self.context['res'].win_sound.play()
                        self.music_flag = False

                elif self.lose_flag:
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.lose_img)))
                    if self.music_flag:
                        self.context['res'].lose_sound.play()
                        self.music_flag = False

                elif self.tie_flag:
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.tie_img)))
                    if self.music_flag:
                        self.context['res'].tie_sound.play()
                        self.music_flag = False

                self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].re_start)))
                self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].like)))

                # 控制处理 self.reset()
                # 再来一局
            # 返回大厅
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].back)))
            self.context['scr'].blit(self.context['res'].arrow_dark[0], pygame.mouse.get_pos())

        elif self.running_flag:
            # 如果是左侧玩家，负责演算
            self.context['pys'][0].paddle.move()

            if self.context['pys'][0].side == 'left':
                self.ball.move()
                if self.context['pys'][0].paddle.get_right() >= self.ball.get_left():
                    # 上侧边界
                    if self.context['pys'][0].paddle.get_top() <= self.ball.get_bottom() < \
                            self.context['pys'][0].paddle.get_bottom():
                        if not (self.ball.get_top() >= self.context['pys'][0].paddle.get_top()):
                            self.ball.ver[1] = -self.ball.ver[1]
                            self.ball.pos[1] = self.context['pys'][0].paddle.get_top() - self.ball.img.get_height() - 1
                            # 不只是侧面碰撞
                        self.ball.ver[0] = -self.ball.ver[0]
                        self.ball.pos[0] = self.context['pys'][0].paddle.get_right() + 1
                        self.context['res'].bounce_sound.play()
                        self.context['dsy'].put_data('so sb' + '@')

                    # 下侧边界
                    elif self.context['pys'][0].paddle.get_bottom() >= self.ball.get_top() > \
                            self.context['pys'][0].paddle.get_top():
                        if not (self.ball.get_bottom() <= self.context['pys'][0].paddle.get_bottom()):
                            self.ball.ver[1] = -self.ball.ver[1]
                            self.ball.pos[1] = self.context['pys'][0].paddle.get_bottom() + 1
                            # 不只是侧面碰撞
                        self.ball.ver[0] = -self.ball.ver[0]
                        self.ball.pos[0] = self.context['pys'][0].paddle.get_right() + 1
                        self.context['res'].bounce_sound.play()
                        self.context['dsy'].put_data('so sb' + '@')
                # 一号玩家
                if self.context['pys'][1].paddle.get_left() <= self.ball.get_right():
                    # 上侧边界
                    if self.context['pys'][1].paddle.get_top() <= self.ball.get_bottom() < \
                            self.context['pys'][1].paddle.get_bottom():
                        if not (self.ball.get_top() >= self.context['pys'][1].paddle.get_top()):
                            self.ball.ver[1] = -self.ball.ver[1]
                            self.ball.pos[1] = self.context['pys'][1].paddle.get_top() - self.ball.img.get_height() - 1
                            # 不只是侧面碰撞
                        self.ball.ver[0] = -self.ball.ver[0]
                        self.ball.pos[0] = self.context['pys'][1].paddle.get_left() - self.ball.img.get_width() - 1
                        self.context['res'].bounce_sound.play()
                        self.context['dsy'].put_data('so sb' + '@')

                    # 下侧边界
                    elif self.context['pys'][1].paddle.get_bottom() >= self.ball.get_top() > \
                            self.context['pys'][1].paddle.get_top():
                        if not (self.ball.get_bottom() <= self.context['pys'][1].paddle.get_bottom()):
                            self.ball.ver[1] = -self.ball.ver[1]
                            self.ball.pos[1] = self.context['pys'][1].paddle.get_bottom() + 1
                            # 不只是侧面碰撞
                        self.ball.ver[0] = -self.ball.ver[0]
                        self.ball.pos[0] = self.context['pys'][1].paddle.get_left() - self.ball.img.get_width() - 1
                        self.context['res'].bounce_sound.play()
                        self.context['dsy'].put_data('so sb' + '@')

                # 左右边界检查
                if 0 >= self.ball.get_left():
                    # 分数统计
                    self.context['pys'][1].score += 10
                    self.context['dsy'].put_data(
                        'so s' + str(self.context['pys'][0].score) + ' ' + str(self.context['pys'][1].score) + '@')
                    self.context['pys'][1].renew_score_img()
                    self.ball.ver[0] = -self.ball.ver[0]
                    self.ball.pos[0] = 1
                    self.context['res'].in_sound.play()
                    self.context['dsy'].put_data('so si' + '@')
                    # self.ball.reset()

                if self.context['cfg'].screen_size[0] <= self.ball.get_right():
                    # 分数统计
                    self.context['pys'][0].score += 10
                    self.context['pys'][0].renew_score_img()
                    self.context['dsy'].put_data(
                        'so s' + str(self.context['pys'][0].score) + ' ' + str(self.context['pys'][1].score) + '@')
                    # 重新发球或者直接反弹
                    self.ball.ver[0] = -self.ball.ver[0]
                    self.ball.pos[0] = self.context['cfg'].screen_size[0] - self.ball.img.get_width() - 1
                    self.context['res'].in_sound.play()
                    self.context['dsy'].put_data('so si' + '@')
                    # self.ball.reset()
                    # 检查本局胜负
                    if self.context['pys'][0].score + self.context['pys'][1].score >= 400:
                        if self.context['pys'][0].score > self.context['pys'][1].score:
                            self.dialog_flag = True
                            self.over_flag = True
                            self.win_flag = True
                            self.context['dsy'].put_data('go l' + '@')
                            self.context['pys'][0].rank += 1
                            self.context['pys'][1].rank = max(self.context['pys'][1].rank - 1, 0)
                            self.context['dsy'].put_data(
                                'so r' + str(self.context['pys'][0].rank) + ' ' + str(
                                    self.context['pys'][1].rank) + '@')

                        elif self.context['pys'][0].score < self.context['pys'][1].score:
                            self.dialog_flag = True
                            self.over_flag = True
                            self.lose_flag = True
                            self.context['dsy'].put_data('go w' + '@')
                            self.context['pys'][1].rank += 1
                            self.context['pys'][0].rank = max(self.context['pys'][0].rank - 1, 0)
                            self.context['dsy'].put_data(
                                'so r' + str(self.context['pys'][0].rank) + ' ' + str(
                                    self.context['pys'][1].rank) + '@')

                        elif self.context['pys'][0].score + self.context['pys'][1].score == 500:
                            self.dialog_flag = True
                            self.over_flag = True
                            self.tie_flag = True
                            self.context['dsy'].put_data('go t' + '@')
                            self.context['dsy'].put_data(
                                'so r' + str(self.context['pys'][0].rank) + ' ' + str(
                                    self.context['pys'][1].rank) + '@')

                # 上下边界检查
                if 0 >= self.ball.get_top():
                    # 分数统计
                    self.ball.ver[1] = -self.ball.ver[1]
                    self.ball.pos[1] = 1

                if self.context['cfg'].screen_size[1] <= self.ball.get_bottom():
                    # 分数统计
                    self.ball.ver[1] = -self.ball.ver[1]
                    self.ball.pos[1] = self.context['cfg'].screen_size[1] - self.ball.img.get_height() - 1
                # 左侧玩家做同步消息给服务器
                # 位置
                self.context['dsy'].put_data('so b' + self.ball.get_1080p_pos() + '@')

                # 运动的时候， 同步位置
                if self.context['pys'][0].paddle.up or self.context['pys'][0].paddle.down:
                    self.context['dsy'].put_data('so p' + self.context['pys'][0].paddle.get_1080p_pos() + '@')

            else:
                if self.context['pys'][0].paddle.get_left() <= self.ball.get_right():
                    # 只模拟自己的
                    if self.context['pys'][0].paddle.get_top() <= self.ball.get_bottom() < \
                            self.context['pys'][0].paddle.get_bottom():
                        if not (self.ball.get_top() >= self.context['pys'][0].paddle.get_top()):
                            self.ball.ver[1] = -self.ball.ver[1]
                            self.ball.pos[1] = self.context['pys'][0].paddle.get_top() - self.ball.img.get_height() - 1
                            # 不只是侧面碰撞
                        self.ball.ver[0] = -self.ball.ver[0]
                        self.ball.pos[0] = self.context['pys'][0].paddle.get_left() - self.ball.img.get_width() - 1
                    # 下侧边界
                    elif self.context['pys'][0].paddle.get_bottom() >= self.ball.get_top() > \
                            self.context['pys'][0].paddle.get_top():
                        if not (self.ball.get_bottom() <= self.context['pys'][0].paddle.get_bottom()):
                            self.ball.ver[1] = -self.ball.ver[1]
                            self.ball.pos[1] = self.context['pys'][0].paddle.get_bottom() + 1
                            # 不只是侧面碰撞
                        self.ball.ver[0] = -self.ball.ver[0]
                        self.ball.pos[0] = self.context['pys'][0].paddle.get_left() - self.ball.img.get_width() - 1

                if self.context['pys'][0].paddle.up or self.context['pys'][0].paddle.down:
                    self.context['dsy'].put_data('so p' + self.context['pys'][0].paddle.get_1080p_pos() + '@')
        if self.pr_toast_flag:
            self.pr_toast_flag -= 1
            self.context['scr'].blit(**(self.context['cof'].get_res(self.pr_toast_img)))

        if self.right_toast_flag:
            self.right_toast_flag -= 1
            self.context['scr'].blit(**(self.context['cof'].get_res(self.right_toast_img)))

        if self.left_toast_flag:
            self.left_toast_flag -= 1
            self.context['scr'].blit(**(self.context['cof'].get_res(self.left_toast_img)))


class off_line_one_ui:
    def __init__(self, context):
        self.context = context
        self.ball = game_objects.Ball(self.context)
        self.music_flag = True

        self.over_flag = False
        self.start_pre_flag = True
        self.running_flag = False
        self.dialog_flag = True
        self.lose_flag = False
        self.win_flag = False
        self.tie_flag = False
        self.last_winner = 'right'
        self.reset_flags()

        self.stars = []
        self.set_stars()

        self.yn_start_img = self.context['cof'].words2img('是否开始游戏！', 90, (668, 400))
        self.right_win_img = self.context['cof'].words2img('右方玩家获胜！', 90, (668, 400))
        self.left_win_img = self.context['cof'].words2img('左方玩家获胜！', 90, (668, 400))
        self.tie_win_img = self.context['cof'].words2img('平局平局！！', 90, (668, 400))

    def set_stars(self):
        # 随机生成星星
        self.stars.clear()
        for i in range(20):
            self.stars.append(game_objects.Star(self.context, i,
                                                random.randint(380, 1260),
                                                random.randint(235, 710),
                                                0))

    def reset(self):
        self.set_stars()
        self.reset_flags()
        self.ball.reset()

    def reset_flags(self):
        self.music_flag = True

        self.over_flag = False
        self.start_pre_flag = True
        self.running_flag = False
        self.dialog_flag = True
        self.lose_flag = False
        self.win_flag = False
        self.last_winner = 'right'
        self.music_flag = True

    def update(self):
        # 贴背景
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].level_1_bg)))

        # 贴元素
        self.context['scr'].blit(**(self.context['pys'][0].paddle.get_res()))
        self.context['scr'].blit(**(self.context['pys'][1].paddle.get_res()))
        self.context['scr'].blit(**(self.ball.get_res()))
        # 贴星星

        for star in self.stars:
            self.context['scr'].blit(**(star.get_res()))

        # 贴分数
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][0].score_img)))
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][1].score_img)))

        if self.dialog_flag:
            # 贴对话框
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].mask_bg)))
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].dialog_bg)))
            if self.start_pre_flag:
                self.context['scr'].blit(**(self.context['cof'].get_res(self.yn_start_img)))
                self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].start)))

            if self.over_flag:
                # 放音乐

                if self.win_flag:
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.left_win_img)))
                    if self.music_flag:
                        self.context['res'].win_sound.play()
                        self.music_flag = False

                elif self.lose_flag:
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.right_win_img)))
                    if self.music_flag:
                        self.context['res'].lose_sound.play()
                        self.music_flag = False

                elif self.tie_flag:
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.tie_win_img)))
                    if self.music_flag:
                        self.context['res'].tie_sound.play()
                        self.music_flag = False

                # 展示获胜者

                self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].re_start)))
                # 再来一局

            # 返回大厅
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].back)))

            self.context['scr'].blit(self.context['res'].arrow_dark[0], pygame.mouse.get_pos())

        else:
            self.ball.move()
            self.context['pys'][0].paddle.move()

            # 无敌AI （rand降低命中率）###############
            self.context['pys'][1].paddle.pos[1] = (self.ball.pos[1] + random.randint(-10, 10))
            self.context['pys'][1].paddle.move()

            # ######################
            # 零号玩家
            if self.context['pys'][0].paddle.get_right() >= self.ball.get_left():
                # 上侧边界
                if self.context['pys'][0].paddle.get_top() <= self.ball.get_bottom() < \
                        self.context['pys'][0].paddle.get_bottom():
                    if not (self.ball.get_top() >= self.context['pys'][0].paddle.get_top()):
                        self.ball.ver[1] = -self.ball.ver[1]
                        self.ball.pos[1] = self.context['pys'][0].paddle.get_top() - self.ball.img.get_height() - 1
                        # 不只是侧面碰撞
                    self.ball.ver[0] = -self.ball.ver[0]
                    self.ball.pos[0] = self.context['pys'][0].paddle.get_right() + 1
                    self.context['res'].bounce_sound.play()
                # 下侧边界
                elif self.context['pys'][0].paddle.get_bottom() >= self.ball.get_top() > \
                        self.context['pys'][0].paddle.get_top():
                    if not (self.ball.get_bottom() <= self.context['pys'][0].paddle.get_bottom()):
                        self.ball.ver[1] = -self.ball.ver[1]
                        self.ball.pos[1] = self.context['pys'][0].paddle.get_bottom() + 1
                        # 不只是侧面碰撞
                    self.ball.ver[0] = -self.ball.ver[0]
                    self.ball.pos[0] = self.context['pys'][0].paddle.get_right() + 1
                    self.context['res'].bounce_sound.play()

            # 一号玩家
            if self.context['pys'][1].paddle.get_left() <= self.ball.get_right():
                # 上侧边界
                if self.context['pys'][1].paddle.get_top() <= self.ball.get_bottom() < \
                        self.context['pys'][1].paddle.get_bottom():
                    if not (self.ball.get_top() >= self.context['pys'][1].paddle.get_top()):
                        self.ball.ver[1] = -self.ball.ver[1]
                        self.ball.pos[1] = self.context['pys'][1].paddle.get_top() - self.ball.img.get_height() - 1
                        # 不只是侧面碰撞
                    self.ball.ver[0] = -self.ball.ver[0]
                    self.ball.pos[0] = self.context['pys'][1].paddle.get_left() - self.ball.img.get_width() - 1
                    self.context['res'].bounce_sound.play()

                # 下侧边界
                elif self.context['pys'][1].paddle.get_bottom() >= self.ball.get_top() > \
                        self.context['pys'][1].paddle.get_top():
                    if not (self.ball.get_bottom() <= self.context['pys'][1].paddle.get_bottom()):
                        self.ball.ver[1] = -self.ball.ver[1]
                        self.ball.pos[1] = self.context['pys'][1].paddle.get_bottom() + 1
                        # 不只是侧面碰撞
                    self.ball.ver[0] = -self.ball.ver[0]
                    self.ball.pos[0] = self.context['pys'][1].paddle.get_left() - self.ball.img.get_width() - 1
                    self.context['res'].bounce_sound.play()

            # 左右边界检查
            if 0 >= self.ball.get_left():
                # 分数统计
                self.context['pys'][1].score += 10
                self.context['pys'][1].renew_score_img()
                self.ball.ver[0] = -self.ball.ver[0]
                self.ball.pos[0] = 1
                self.context['res'].in_sound.play()

            if self.context['cfg'].screen_size[0] <= self.ball.get_right():
                # 分数统计
                self.context['pys'][0].score += 10
                self.context['pys'][0].renew_score_img()
                self.ball.ver[0] = -self.ball.ver[0]
                self.ball.pos[0] = self.context['cfg'].screen_size[0] - self.ball.img.get_width() - 1
                self.context['res'].in_sound.play()

            # 检测胜负
            if self.context['pys'][0].score + self.context['pys'][1].score >= 400:
                if self.context['pys'][0].score > self.context['pys'][1].score:
                    self.dialog_flag = True
                    self.over_flag = True
                    self.win_flag = True

                elif self.context['pys'][0].score < self.context['pys'][1].score:
                    self.dialog_flag = True
                    self.over_flag = True
                    self.lose_flag = True

                elif self.context['pys'][0].score + self.context['pys'][1].score == 500:
                    self.dialog_flag = True
                    self.over_flag = True
                    self.tie_flag = True

            # 上下边界检查
            if 0 >= self.ball.get_top():
                # 分数统计
                self.ball.ver[1] = -self.ball.ver[1]
                self.ball.pos[1] = 1

            if self.context['cfg'].screen_size[1] <= self.ball.get_bottom():
                # 分数统计
                self.ball.ver[1] = -self.ball.ver[1]
                self.ball.pos[1] = self.context['cfg'].screen_size[1] - self.ball.img.get_height() - 1

            # 接下来要清除掉的星星的id表单
            rm_id_list = []
            for star in self.stars:
                if abs((star.get_right() - (star.img.get_width() / 2)) - (
                        self.ball.get_right() - (self.ball.img.get_width() / 2))) \
                        <= abs((star.img.get_width() + self.ball.img.get_width()) / 2) \
                        and abs((star.get_bottom() - (star.img.get_height() / 2)) - (
                        self.ball.get_bottom() - (self.ball.img.get_height() / 2))) \
                        <= abs((star.img.get_height() + self.ball.img.get_height()) / 2):
                    # print(666)
                    if self.ball.ver[1] > 0:
                        self.context['pys'][0].score += 1
                        self.context['pys'][0].renew_score_img()
                    else:
                        self.context['pys'][1].score += 1
                        self.context['pys'][1].renew_score_img()
                    self.context['res'].star_sound.play()
                    rm_id_list.append(star.id)
                '''
                # 碰撞
                if self.ball.get_rect().colliderect(star.get_rect()):
                    # pass
                    # print(666)
                    rm_id_list.append(star.id)
                if star.get_rect().colliderect(star.get_rect()):
                    print(999)
                '''

            tmp_stars = []
            for star in self.stars:
                if not (star.id in rm_id_list):
                    tmp_stars.append(star)

            self.stars.clear()
            self.stars = tmp_stars[:]


class off_line_two_ui:
    def __init__(self, context):
        self.context = context
        self.ball = game_objects.Ball(self.context)
        self.music_flag = True

        self.over_flag = False
        self.start_pre_flag = True
        self.running_flag = False
        self.dialog_flag = True
        self.lose_flag = False
        self.win_flag = False
        self.tie_flag = False
        self.last_winner = 'right'
        self.reset_flags()

        self.stars = []
        self.set_stars()

        self.yn_start_img = self.context['cof'].words2img('是否开始游戏！', 90, (668, 400))
        self.right_win_img = self.context['cof'].words2img('右方玩家获胜！', 90, (668, 400))
        self.left_win_img = self.context['cof'].words2img('左方玩家获胜！', 90, (668, 400))
        self.tie_win_img = self.context['cof'].words2img('平局平局！！', 90, (668, 400))

    def set_stars(self):
        # 随机生成星星
        self.stars.clear()
        for i in range(20):
            self.stars.append(game_objects.Star(self.context, i,
                                                random.randint(380, 1260),
                                                random.randint(235, 710),
                                                0))

    def reset(self):
        self.set_stars()
        self.reset_flags()
        self.ball.reset()

    def reset_flags(self):
        self.music_flag = True

        self.over_flag = False
        self.start_pre_flag = True
        self.running_flag = False
        self.dialog_flag = True
        self.lose_flag = False
        self.win_flag = False
        self.last_winner = 'right'
        self.music_flag = True

    def update(self):
        # 贴背景
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].level_1_bg)))

        # 贴元素
        self.context['scr'].blit(**(self.context['pys'][0].paddle.get_res()))
        self.context['scr'].blit(**(self.context['pys'][1].paddle.get_res()))
        self.context['scr'].blit(**(self.ball.get_res()))
        # 贴星星

        for star in self.stars:
            self.context['scr'].blit(**(star.get_res()))

        # 贴分数
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][0].score_img)))
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][1].score_img)))

        if self.dialog_flag:
            # 贴对话框
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].mask_bg)))
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].dialog_bg)))
            if self.start_pre_flag:
                self.context['scr'].blit(**(self.context['cof'].get_res(self.yn_start_img)))
                self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].start)))

            if self.over_flag:
                # 放音乐

                if self.win_flag:
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.left_win_img)))
                    if self.music_flag:
                        self.context['res'].win_sound.play()
                        self.music_flag = False

                elif self.lose_flag:
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.right_win_img)))
                    if self.music_flag:
                        self.context['res'].lose_sound.play()
                        self.music_flag = False

                elif self.tie_flag:
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.tie_win_img)))
                    if self.music_flag:
                        self.context['res'].tie_sound.play()
                        self.music_flag = False

                # 展示获胜者

                self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].re_start)))
                # 再来一局

            # 返回大厅
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].back)))

            self.context['scr'].blit(self.context['res'].arrow_dark[0], pygame.mouse.get_pos())

        else:
            self.ball.move()
            self.context['pys'][0].paddle.move()
            self.context['pys'][1].paddle.move()

            # 零号玩家
            if self.context['pys'][0].paddle.get_right() >= self.ball.get_left():
                # 上侧边界
                if self.context['pys'][0].paddle.get_top() <= self.ball.get_bottom() < \
                        self.context['pys'][0].paddle.get_bottom():
                    if not (self.ball.get_top() >= self.context['pys'][0].paddle.get_top()):
                        self.ball.ver[1] = -self.ball.ver[1]
                        self.ball.pos[1] = self.context['pys'][0].paddle.get_top() - self.ball.img.get_height() - 1
                        # 不只是侧面碰撞
                    self.ball.ver[0] = -self.ball.ver[0]
                    self.ball.pos[0] = self.context['pys'][0].paddle.get_right() + 1
                    self.context['res'].bounce_sound.play()
                # 下侧边界
                elif self.context['pys'][0].paddle.get_bottom() >= self.ball.get_top() > \
                        self.context['pys'][0].paddle.get_top():
                    if not (self.ball.get_bottom() <= self.context['pys'][0].paddle.get_bottom()):
                        self.ball.ver[1] = -self.ball.ver[1]
                        self.ball.pos[1] = self.context['pys'][0].paddle.get_bottom() + 1
                        # 不只是侧面碰撞
                    self.ball.ver[0] = -self.ball.ver[0]
                    self.ball.pos[0] = self.context['pys'][0].paddle.get_right() + 1
                    self.context['res'].bounce_sound.play()

            # 一号玩家
            if self.context['pys'][1].paddle.get_left() <= self.ball.get_right():
                # 上侧边界
                if self.context['pys'][1].paddle.get_top() <= self.ball.get_bottom() < \
                        self.context['pys'][1].paddle.get_bottom():
                    if not (self.ball.get_top() >= self.context['pys'][1].paddle.get_top()):
                        self.ball.ver[1] = -self.ball.ver[1]
                        self.ball.pos[1] = self.context['pys'][1].paddle.get_top() - self.ball.img.get_height() - 1
                        # 不只是侧面碰撞
                    self.ball.ver[0] = -self.ball.ver[0]
                    self.ball.pos[0] = self.context['pys'][1].paddle.get_left() - self.ball.img.get_width() - 1
                    self.context['res'].bounce_sound.play()

                # 下侧边界
                elif self.context['pys'][1].paddle.get_bottom() >= self.ball.get_top() > \
                        self.context['pys'][1].paddle.get_top():
                    if not (self.ball.get_bottom() <= self.context['pys'][1].paddle.get_bottom()):
                        self.ball.ver[1] = -self.ball.ver[1]
                        self.ball.pos[1] = self.context['pys'][1].paddle.get_bottom() + 1
                        # 不只是侧面碰撞
                    self.ball.ver[0] = -self.ball.ver[0]
                    self.ball.pos[0] = self.context['pys'][1].paddle.get_left() - self.ball.img.get_width() - 1
                    self.context['res'].bounce_sound.play()

            # 胜负判断
            if 0 >= self.ball.get_left():
                # 分数统计
                self.context['pys'][1].score += 10
                self.context['pys'][1].renew_score_img()
                self.ball.ver[0] = -self.ball.ver[0]
                self.ball.pos[0] = 1
                self.context['res'].in_sound.play()

            if self.context['cfg'].screen_size[0] <= self.ball.get_right():
                # 分数统计
                self.context['pys'][0].score += 10
                self.context['pys'][0].renew_score_img()
                self.ball.ver[0] = -self.ball.ver[0]
                self.ball.pos[0] = self.context['cfg'].screen_size[0] - self.ball.img.get_width() - 1
                self.context['res'].in_sound.play()

            # 检测胜负
            if self.context['pys'][0].score + self.context['pys'][1].score >= 400:
                if self.context['pys'][0].score > self.context['pys'][1].score:
                    self.dialog_flag = True
                    self.over_flag = True
                    self.win_flag = True

                elif self.context['pys'][0].score < self.context['pys'][1].score:
                    self.dialog_flag = True
                    self.over_flag = True
                    self.lose_flag = True

                elif self.context['pys'][0].score + self.context['pys'][1].score == 500:
                    self.dialog_flag = True
                    self.over_flag = True
                    self.tie_flag = True

            # 上下边界检查
            if 0 >= self.ball.get_top():
                # 分数统计
                self.ball.ver[1] = -self.ball.ver[1]
                self.ball.pos[1] = 1

            if self.context['cfg'].screen_size[1] <= self.ball.get_bottom():
                # 分数统计
                self.ball.ver[1] = -self.ball.ver[1]
                self.ball.pos[1] = self.context['cfg'].screen_size[1] - self.ball.img.get_height() - 1

            # 接下来要清除掉的星星的id表单
            rm_id_list = []
            for star in self.stars:
                if abs((star.get_right() - (star.img.get_width() / 2)) - (
                        self.ball.get_right() - (self.ball.img.get_width() / 2))) \
                        <= abs((star.img.get_width() + self.ball.img.get_width()) / 2) \
                        and abs((star.get_bottom() - (star.img.get_height() / 2)) - (
                        self.ball.get_bottom() - (self.ball.img.get_height() / 2))) \
                        <= abs((star.img.get_height() + self.ball.img.get_height()) / 2):
                    # print(666)
                    # 计算分数
                    # 向右，分数算左侧玩家的
                    if self.ball.ver[1] > 0:
                        self.context['pys'][0].score += 1
                        self.context['pys'][0].renew_score_img()
                    else:
                        self.context['pys'][1].score += 1
                        self.context['pys'][1].renew_score_img()
                    self.context['res'].star_sound.play()
                    rm_id_list.append(star.id)
                '''
                # 碰撞
                if self.ball.get_rect().colliderect(star.get_rect()):
                    # pass
                    # print(666)
                    rm_id_list.append(star.id)
                if star.get_rect().colliderect(star.get_rect()):
                    print(999)
                '''

            tmp_stars = []
            for star in self.stars:
                if not (star.id in rm_id_list):
                    tmp_stars.append(star)

            self.stars.clear()
            self.stars = tmp_stars[:]


class index_ui:
    # 游戏首页
    def __init__(self, context):
        self.context = context
        self.umd = 'index_ui'
        # 标志变量
        self.name_box_flag = True
        self.pass_box_flag = False
        self.rem_pass_flag = True

        self.dialog_flag = False
        self.user_info_flag = False
        self.rank_list_flag = False
        self.setting_menu_flag = False
        self.about_game_flag = False
        self.notice_flag = False
        self.pw_toast_flag = 0
        self.nu_toast_flag = 0
        self.nl_toast_flag = 0
        self.pr_toast_flag = 0

        # 排行榜 用户信息， 显示三位
        self.pr_toast_img = self.context['cof'].words2img('网络错误，无法联网对战', 80, (603, 162))
        self.nl_toast_img = self.context['cof'].words2img('请先登陆', 80, (807, 162))
        self.pw_toast_img = self.context['cof'].words2img('密码错误', 80, (807, 162))
        self.nu_toast_img = self.context['cof'].words2img('没有此用户', 80, (773, 162))

        self.net_error_img = None
        self.rank_list_1_img = None
        self.rank_list_2_img = None
        self.rank_list_3_img = None

    def match(self, mod):
        if self.context['dsy'].connect() and self.context['pys'][0].state:
            self.context['dsy'].put_data('u ' + mod)
            # print('进入匹配队列')

    def reset_flags(self):
        self.dialog_flag = False
        self.user_info_flag = False
        self.rank_list_flag = False
        self.setting_menu_flag = False
        self.about_game_flag = False
        self.notice_flag = False

    def update(self):
        # 首页背景
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].index_ui_bg)))

        # 用户头像
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][0].avatar)))
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].avatar_mask)))

        # 用户数据
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][0].nickname_top_img)))
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][0].rank_top_img)))
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][0].top_score_top_img)))

        # 模式菜单, 遮挡时， 看不见，减少绘图
        if not self.dialog_flag:
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].on_line_battle)))
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].on_line_ranking)))
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].off_line_one)))
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].off_line_two)))


        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].ranking_list)))
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].menu)))

        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].tools_bar_b1)))
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].tools_bar_b2)))
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].tools_bar_b3)))
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].tools_bar_b4)))
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].notice)))
        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].like_2)))
        # sub window
        if self.dialog_flag:
            # 阴影蒙版
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].mask_bg)))
            self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].dialog_bg)))

            # 用户信息界面
            if self.user_info_flag:
                # 已登录
                if self.context['pys'][0].state:
                    # show info
                    self.context['scr'].blit(
                        **(self.context['cof'].get_res(self.context['pys'][0].nickname_dialog_img)))
                    self.context['scr'].blit(
                        **(self.context['cof'].get_res(self.context['pys'][0].top_rank_dialog_img)))

                    self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][0].rank_dialog_img)))
                    self.context['scr'].blit(
                        **(self.context['cof'].get_res(self.context['pys'][0].top_score_dialog_img)))
                    self.context['scr'].blit(
                        **(self.context['cof'].get_res(self.context['pys'][0].rating_score_dialog_img)))
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][0].like_dialog_img)))
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.context['pys'][0].liked_dialog_img)))

                    self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].log_out)))
                # 未登录状态
                else:
                    # 输入框
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].username_box)))
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].password_box)))

                    # 用户属性 dialog img
                    self.context['scr'].blit(
                        **(self.context['cof'].get_res(self.context['pys'][0].username_img)))
                    self.context['scr'].blit(
                        **(self.context['cof'].get_res(self.context['pys'][0].password_img)))
                    # 注册，登陆， 返回
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].register)))
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].rememb)))
                    self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].login_in)))

                    # 标识符号
                    if self.name_box_flag:
                        self.context['scr'].blit(
                            **(self.context['cof'].get_res(self.context['res'].input_username_arrow)))
                    if self.pass_box_flag:
                        self.context['scr'].blit(
                            **(self.context['cof'].get_res(self.context['res'].input_password_arrow)))
                    if self.rem_pass_flag:
                        self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].rem_pass)))

                    if self.pw_toast_flag:
                        self.pw_toast_flag -= 1
                        self.context['scr'].blit(**(self.context['cof'].get_res(self.pw_toast_img)))

                    if self.nu_toast_flag:
                        self.nu_toast_flag -= 1
                        self.context['scr'].blit(**(self.context['cof'].get_res(self.nu_toast_img)))

                self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].back)))

            elif self.rank_list_flag:
                # 获取前三名(功能保留)
                self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].back)))
                pass

            elif self.setting_menu_flag:
                # 设置选项（功能保留)

                self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].login_in)))
                self.context['scr'].blit(**(self.context['cof'].get_res(self.context['res'].back)))

                # setting
                pass
            elif self.about_game_flag:
                # 跳转网页
                pass
            elif self.notice_flag:
                # 公告
                pass

        # 绘制鼠标
        if self.nl_toast_flag:
            self.nl_toast_flag -= 1
            self.context['scr'].blit(**(self.context['cof'].get_res(self.nl_toast_img)))

        if self.pr_toast_flag:
            self.pr_toast_flag -= 1
            self.context['scr'].blit(**(self.context['cof'].get_res(self.pr_toast_img)))

        self.context['scr'].blit(self.context['res'].arrow_dark[0], pygame.mouse.get_pos())


def main():
    rhythm_of_pingpong = Game()
    rhythm_of_pingpong.run()


if __name__ == '__main__':
    main()
