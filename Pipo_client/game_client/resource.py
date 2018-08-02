import pygame


class Resource:
    def __init__(self, cfg):
        self.cfg = cfg

        # 游戏全局图像资源
        self.index_ui_bg = self.set_res('res/images/index_ui_bg.png', (0, 0))
        self.mask_bg = self.set_res('res/images/mask_bg.png', (0, 0))
        self.avatar_1 = self.set_res('res/images/def_avatar.png', (30, 30))
        self.avatar_mask = self.set_res('res/images/avatar_mask.png', (30, 30))
        self.ranking_list = self.set_res('res/images/ranking_list.png', (0, 277))
        self.menu = self.set_res('res/images/menu.png', (1771, 277))
        self.on_line_battle = self.set_res('res/images/on_line_battle.png', (430, 275))
        self.on_line_ranking = self.set_res('res/images/on_line_ranking.png', (777, 275))
        self.off_line_one = self.set_res('res/images/off_line_one.png', (1119, 272))
        self.off_line_two = self.set_res('res/images/off_line_two.png', (1119, 498))

        # 窗口
        self.dialog_bg = self.set_res('res/images/dialog_bg.png', (280, 135))
        self.close_dialog = self.set_res('res/images/close_dialog.png', (1520, 155))

        # 显示
        self.username_box = self.set_res('res/images/username_box.png', (450, 236))
        self.password_box = self.set_res('res/images/password_box.png', (450, 400))
        self.input_username_arrow = self.set_res('res/images/now.png', (1420, 236))
        self.input_password_arrow = self.set_res('res/images/now.png', (1420, 400))

        # 按钮
        self.register = self.set_res('res/images/register.png', (450, 600))
        self.rememb = self.set_res('res/images/rememb.png', (1070, 600))
        self.rem_pass = self.set_res('res/images/rem_pass.png', (1123, 632))

        self.login_in = self.set_res('res/images/login_in.png', (1170, 750))
        self.log_out = self.set_res('res/images/log_out.png', (1170, 750))

        self.back = self.set_res('res/images/back.png', (450, 750))
        self.like = self.set_res('res/images/like.png', (810, 750))
        self.re_start = self.set_res('res/images/re_start.png', (1170, 750))
        self.start = self.set_res('res/images/start.png', (1170, 750))

        self.notice = self.set_res('res/images/notice.png', (1790, 377))
        self.like_2 = self.set_res('res/images/like_2.png', (1790, 527))

        self.tools_bar_b1 = self.set_res('res/images/tools_bar_b1.png', (450, 804))
        self.tools_bar_b2 = self.set_res('res/images/tools_bar_b2.png', (750, 804))
        self.tools_bar_b3 = self.set_res('res/images/tools_bar_b3.png', (1050, 804))
        self.tools_bar_b4 = self.set_res('res/images/tools_bar_b4.png', (1350, 804))

        # 鼠标
        self.arrow_dark = self.set_res('res/images/arrow_dark.png', (0, 0))

        # 战局资源
        self.ball = self.set_res('res/images/ball.png', (0, 0))
        self.level_1_bg = self.set_res('res/images/level.png', (0, 0))
        self.level_2_bg = self.set_res('res/images/level_2.png', (0, 0))

        # 战局资源
        self.paddle = self.set_res('res/images/paddle.png', (0, 0))
        self.long_paddle = self.set_res('res/images/long_paddle.png', (0, 0))

        # 加载宝石图片
        self.stars = []
        for i in range(5):
            self.stars.append(self.set_res('res/images/star_' + str(i + 1) + '.png', (0, 0)))

        # 加载头像
        self.avatars = []
        for _ in range(5):
            self.avatars.append(self.set_res('res/images/avatars/' + str(_+1) + '.png', (30, 30)))
        # print(len(self.avatars))

        # 声音加载
        # BGM
        pygame.mixer.music.load('./res/music/bgm.ogg')
        pygame.mixer.music.set_volume(0.2 * self.cfg.volume_level / 3)\

        # 以下为音效
        self.click_sound = pygame.mixer.Sound('./res/music/click.ogg')
        self.click_sound.set_volume(0.8 * self.cfg.effect_level / 3)

        self.win_sound = pygame.mixer.Sound('./res/music/win.ogg')
        self.win_sound.set_volume(0.8 * self.cfg.effect_level / 3)

        self.lose_sound = pygame.mixer.Sound('./res/music/lose.ogg')
        self.lose_sound.set_volume(0.8 * self.cfg.effect_level / 3)

        self.tie_sound = pygame.mixer.Sound('./res/music/tie.ogg')
        self.tie_sound.set_volume(0.8 * self.cfg.effect_level / 3)

        self.bounce_sound = pygame.mixer.Sound('./res/music/bounce.ogg')
        self.bounce_sound.set_volume(0.8 * self.cfg.effect_level / 3)

        self.in_sound = pygame.mixer.Sound('./res/music/in.ogg')
        self.in_sound.set_volume(0.8 * self.cfg.effect_level / 3)

        self.star_sound = pygame.mixer.Sound('./res/music/star.ogg')
        self.star_sound.set_volume(0.8 * self.cfg.effect_level / 3)

    # 根据所得窗口的大小， 缩放资源
    def set_res(self, path, pos):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.smoothscale(img, (
            int(img.get_width() / 1920 * self.cfg.screen_size[0]),
            int(img.get_height() / 1080 * self.cfg.screen_size[1])))

        pos = (int(pos[0] / 1920 * self.cfg.screen_size[0]),
               int(pos[1] / 1080 * self.cfg.screen_size[1]))

        return img, pos
