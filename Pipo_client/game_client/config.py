import os
import pygame
import platform
import configparser


class Config:
    # 游戏配置，
    def __init__(self):
        self.config_file = 'config.cfg'
        self.conf = configparser.ConfigParser()

        if os.path.exists(self.config_file):
            self.conf.read(self.config_file)

            self.music_on_off = int(self.conf.get("CONFIG", "music_on_off"))
            self.volume_level = int(self.conf.get("CONFIG", "volume_level"))
            self.sound_effect = int(self.conf.get("CONFIG", "sound_effect"))
            self.effect_level = int(self.conf.get("CONFIG", "effect_level"))
            self.screen_size = (int(self.conf.get("CONFIG", "screen_size_width")),
                                int(self.conf.get("CONFIG", "screen_size_height")))
            self.user_name = self.conf.get("CONFIG", "user_name")
            self.user_pass = self.conf.get("CONFIG", "user_pass")
        else:
            self.music_on_off = 1
            self.volume_level = 2
            self.sound_effect = 1
            self.effect_level = 2
            self.user_name = ''
            self.user_pass = ''
            self.screen_size = self.get_screen_size()

            self.conf.add_section("CONFIG")
            self.conf.set("CONFIG", "music_on_off", str(self.music_on_off))
            self.conf.set("CONFIG", "volume_level", str(self.volume_level))
            self.conf.set("CONFIG", "sound_effect", str(self.sound_effect))
            self.conf.set("CONFIG", "effect_level", str(self.effect_level))
            self.conf.set("CONFIG", "user_name", str(self.user_name))
            self.conf.set("CONFIG", "user_pass", str(self.user_pass))

            self.conf.set("CONFIG", "screen_size_width", str(self.screen_size[0]))
            self.conf.set("CONFIG", "screen_size_height", str(self.screen_size[1]))

            self.save_cfg()

    def set_cfg(self, key, value):
        self.conf.set("CONFIG", key, str(value))

    def save_cfg(self):
        with open(self.config_file, 'wt') as conf_out:
            self.conf.write(conf_out)

    @staticmethod
    def get_screen_size():
        # 最大分辨率
        screen_size_max = pygame.display.list_modes()[0]
        # 处理Windows操作系统下的DPI缩放问题
        os_type = platform.system().lower()
        if "windows" in os_type:
            import win32api
            screen_size_zoom = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
            if screen_size_zoom[0] != screen_size_max[0]:
                screen_size_max = screen_size_zoom

        if screen_size_max[0] * 9 > screen_size_max[1] * 16:
            screen_size_max[0] = int(screen_size_max[1] * 16 / 9)
            # 缩宽
        elif screen_size_max[0] * 9 < screen_size_max[1] * 16:
            screen_size_max[1] = int(screen_size_max[0] * 9 / 16)
            # 缩高

        screen_size = int(screen_size_max[0] / 3 * 2), int(screen_size_max[1] / 3 * 2)

        return screen_size


def main():
    if __name__ == "__main__":
        cfg = Config()
        print(cfg.screen_size)


main()
