import pygame
import pygame.freetype
import sys
import random
import game_objects


# 为控制器提供的辅助函数

class ControllerFunction:
    def __init__(self, cfg):
        pygame.init()
        self.font = pygame.freetype.Font("./res/fonts/zkklt.ttf", 36)
        self.cfg = cfg

    @staticmethod
    def close_game(context):
        # 释放游戏资源
        context['dsy'].close()
        sys.exit()

    @staticmethod
    def random_player():
        # 随机玩家方向（保留）
        return random.randint(0, 1)

    def words2img(self, words, size, pos):
        # 字符串生成相应的Surface
        # 默认1080p， 32字号显示昵称
        img = self.font.render(str(words), fgcolor=(0, 0, 0), size=size)[0]
        # print(words, img.get_rect())
        img = pygame.transform.smoothscale(img, (
            int(img.get_width() / 1920 * self.cfg.screen_size[0]),
            int(img.get_height() / 1080 * self.cfg.screen_size[1])))

        pos = (int(pos[0] / 1920 * self.cfg.screen_size[0]),
               int(pos[1] / 1080 * self.cfg.screen_size[1]))
        return img, pos

    @staticmethod
    def get_res(res):
        # 资源包装
        return dict(source=res[0], dest=res[1])

    @staticmethod
    def get_rect(res):
        # 返回相应矩形（相对）
        return game_objects.Rect(top=res[1][1],
                                 left=res[1][0],
                                 right=res[0].get_width() + res[1][0],
                                 bottom=res[0].get_height() + res[1][1])

    @staticmethod
    def hover(pos, rect):
        # 覆盖（鼠标指针用）
        return rect.right > pos[0] > rect.left and rect.top < pos[1] < rect.bottom

    @staticmethod
    def close_dialog(ui_context):
        # 关闭对话框（临时）
        if ui_context.umd == 'index_ui':
            ui_context.dialog_flag = False
            ui_context.user_info_flag = False
            ui_context.rank_list_flag = False
            ui_context.setting_menu_flag = False
            ui_context.about_game_flag = False
            ui_context.notice_flag = False
