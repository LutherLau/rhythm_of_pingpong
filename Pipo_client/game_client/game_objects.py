import hashlib
import random
import math


class GameObject:
    def __init__(self):
        pass


class Rect(GameObject):
    def __init__(self, **kwargs):
        super().__init__()
        self.top = kwargs['top']
        self.left = kwargs['left']
        self.right = kwargs['right']
        self.bottom = kwargs['bottom']


class Star(GameObject):
    def __init__(self, context, star_id, x, y, c):
        super().__init__()
        # 处理过的图像
        # id 以及 坐标（1080p） 类型
        self.context = context
        self.id = star_id
        self.c = c
        self.img = self.context['res'].stars[random.randint(0, 4)][0]

        self.pos = self.img.get_rect()

        self.pos[0] = int(x / 1920 * self.context['cfg'].screen_size[0])
        self.pos[1] = int(y / 1080 * self.context['cfg'].screen_size[1])

    def get_rect(self):
        return self.pos

    def get_res(self):
        return {'source': self.img, 'dest': self.pos}

    def get_right(self):
        return self.pos[0] + self.img.get_width()

    def get_left(self):
        return self.pos[0]

    def get_top(self):
        return self.pos[1]

    def get_bottom(self):
        return self.pos[1] + self.img.get_height()


class Ball(GameObject):
    def __init__(self, context):
        super().__init__()
        # 游戏上下文
        self.context = context
        # 贴图
        self.img = self.context['res'].ball[0]
        # 属性
        self.pos = self.img.get_rect()
        self.reset()

    # 速度
    def get_ver(self):
        sp2 = math.sqrt(self.direction[0] * self.direction[0] + self.direction[1] * self.direction[1])
        ratio = (self.speed / self.context['cfg'].screen_size[0] * 1920) / sp2
        return [int(ratio * self.direction[0]), int(ratio * self.direction[1])]

    # 设置方向
    def set_dir(self, x):
        self.direction = (x, random.randint(-10, 10))

    # 重置小球信息
    def reset(self):
        # 位置屏幕居中, 方向随机, 速度为10(相对)
        self.speed = 10
        vx = vy = 0
        while True:
            vx = random.randint(-10, 10) * 2
            vy = random.randint(-10, 10)
            if vx and vy:
                break

        self.direction = (vx, vy)
        self.ver = self.get_ver()

        # 设置位置
        self.pos = self.img.get_rect()
        self.pos[0] = int((self.context['cfg'].screen_size[0] - self.img.get_width()) / 2)
        self.pos[1] = int((self.context['cfg'].screen_size[1] - self.img.get_height()) / 2)

    # 绘图资源
    def get_res(self):
        return {'source': self.img, 'dest': self.pos}

    # 矩形
    def get_rect(self):
        return self.pos

    # 运动
    def move(self):
        self.pos[0] += self.ver[0]
        self.pos[1] += self.ver[1]

    def get_right(self):
        return self.pos[0] + self.img.get_width()

    def get_left(self):
        return self.pos[0]

    def get_top(self):
        return self.pos[1]

    def get_bottom(self):
        return self.pos[1] + self.img.get_height()

    # 设置实时速度（保留）
    def set_ver_online(self, ver):
        ver = ver.split(' ')
        self.ver[0] = int(int(ver[0]) * self.context['cfg'].screen_size[0] / 1920)
        self.ver[1] = int(int(ver[1]) * self.context['cfg'].screen_size[1] / 1080)

    # 取得实时速度，（保留）
    def get_ver_1080p(self):
        return str(self.ver[0]) + ' ' + str(self.ver[1])

    # 设置实时位置
    def set_pos_online(self, pos):
        pos = pos.split(' ')
        self.pos[0] = int(int(pos[0]) * self.context['cfg'].screen_size[0] / 1920)
        self.pos[1] = int(int(pos[1]) * self.context['cfg'].screen_size[1] / 1080)

    # 取得实时位置
    def get_1080p_pos(self):
        x = int(self.pos[0] / self.context['cfg'].screen_size[0] * 1920)
        y = int(self.pos[1] / self.context['cfg'].screen_size[1] * 1080)
        return str(x) + ' ' + str(y)


class Paddle(GameObject):
    def __init__(self, context, side):
        super().__init__()
        # 贴图
        self.img = context['res'].paddle[0]
        self.long_img = context['res'].long_paddle[0]
        # self的加长贴图
        # 运动状态
        # 暴走属性（后续添加）
        self.up = False
        self.down = False
        self.speed = 15
        # 位置
        self.side = side
        # 游戏上下文
        self.context = context
        # 取得paddle位置
        self.pos = self.img.get_rect()

        # 设置左右两侧
        self.set_pos(self.side)

    # 设置位置以及坐标
    def set_pos(self, side):
        # print(side, ' 设置---***')
        self.side = side
        if side == 'left':
            self.pos[0] = 0
            self.pos[1] = (self.context['cfg'].screen_size[1] - self.img.get_height()) / 2
        else:
            self.pos[0] = self.context['cfg'].screen_size[0] - self.img.get_width()
            self.pos[1] = (self.context['cfg'].screen_size[1] - self.img.get_height()) / 2

    # 矩形属性
    def get_rect(self):
        return self.pos

    # 所占矩形右侧坐标
    def get_right(self):
        return self.pos[0] + self.img.get_width()

    # 所占矩形左侧坐标
    def get_left(self):
        return self.pos[0]

    # 所占矩形上侧坐标
    def get_top(self):
        return self.pos[1]

    # 所占矩形下侧坐标
    def get_bottom(self):
        return self.pos[1] + self.img.get_height()

    # 重置状态和坐标
    def reset(self):
        # 重置paddle状态
        self.up = False
        self.down = False

        self.set_pos(self.side)
        # 关闭标志开关
        # 相对于1080p
        self.speed = 15

    # 运动函数
    def move(self):
        # 此处仅仅是move比较好，越界判断和复位放到主程序里
        if self.up:
            self.pos[1] -= self.speed
        elif self.down:
            self.pos[1] += self.speed
        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[1] + self.img.get_height() > self.context['cfg'].screen_size[1]:
            self.pos[1] = self.context['cfg'].screen_size[1] - self.img.get_height()

    # 绘图所需资源
    def get_res(self):
        return {'source': self.img, 'dest': self.pos}

    # 实时更新位置
    def set_pos_online(self, pos):
        pos = pos.split(' ')
        self.pos[0] = int(int(pos[0]) * self.context['cfg'].screen_size[0] / 1920)
        self.pos[1] = int(int(pos[1]) * self.context['cfg'].screen_size[1] / 1080)

    # 得到实时位置
    def get_1080p_pos(self):
        x = int(self.pos[0] / self.context['cfg'].screen_size[0] * 1920)
        y = int(self.pos[1] / self.context['cfg'].screen_size[1] * 1080)
        return str(x) + ' ' + str(y)

    # 暂且保留
    def update(self):
        # 更新状态，并绘图
        # 更好的实现，本身只实现状态更新，不实现绘图功能
        # 绘图功能一律由第三方函数实现，游戏图像资源由图片，相对位置，相对大小，从而实现比例不变
        # 目前想法，图片资源为数组形式存放
        self.context['scr'].blit(self.img, self.pos)


class Player:
    def __init__(self, player_id, context):
        self.context = context

        self.username = ''
        self.password = ''
        self.set_local_user_info()

        # 玩家数据，同步服务器
        self.nickname = '未登录'
        self.avatar_id = 1
        self.top_score = 0
        self.rank = 0
        self.rating_score = 100
        self.like = 0
        self.liked = 0
        self.top_rank = 0
        # 以上信息服务器同步并存储，以下为无需同步
        self.score = 0
        # ################################
        self.state = False
        self.player_id = player_id
        self.side = 'left'
        if player_id == 1:
            self.side = 'right'
        self.paddle = Paddle(context, self.side)

        self.re_new_img()
        self.renew_score_img()

    # 数字转换成段位字符串
    @staticmethod
    def get_rank_str(rank):
        rank_str = ['青铜', '白银', '黄金', '铂金']
        ret = rank_str[int(rank / 3)] + 'III'
        for i in range(int(rank % 3)):
            ret = ret[0:-1]
        return ret

    # 上次登陆的信息
    def set_local_user_info(self):
        try:
            with open('./data/data_1', 'rb') as user_name:
                tmp = user_name.read()
                tmp = tmp.decode(encoding='utf-8')
                self.username = tmp
            with open('./data/data_2', 'rb') as user_pass:
                tmp = user_pass.read()
                tmp = tmp.decode(encoding='utf-8')
                self.password = tmp
        except FileNotFoundError as e:
            pass
            # print(str(e))

    # 保存登录信息
    def save_local_user_username(self):
        try:
            with open('./data/data_1', 'wb') as user_name:
                user_name.write(self.username.encode(encoding='utf-8'))
        except Exception as e:
            pass
            # print(str(e))

        try:
            with open('./data/data_2', 'wb') as password:
                password.write(b'')
        except Exception as e:
            pass
            # print(str(e))

    # 记住密码，用户信息
    def save_local_user_all(self):
        self.save_local_user_username()
        try:
            with open('./data/data_2', 'wb') as password:
                password.write(self.password.encode(encoding='utf-8'))
        except Exception as e:
            pass
            # print(str(e))

    # 刷新分数Surface
    def renew_score_img(self):
        if self.side == 'left':
            self.score_img = self.context['cof'].words2img(self.score, 90, (160, 55))
        else:
            self.score_img = self.context['cof'].words2img(self.score, 90, (1660, 55))

    # 刷新用户信息展示Surface
    def re_new_img(self):
        self.set_avatar(self.avatar_id)

        # 用户属性顶部展示
        self.nickname_top_img = self.context['cof'].words2img(self.nickname, 35, (160, 55))
        self.rank_top_img = self.context['cof'].words2img('段位：' + str(self.get_rank_str(self.rank)), 35, (777, 55))
        self.top_score_top_img = self.context['cof'].words2img('最高分：' + str(self.top_score), 35, (1349, 55))

        # 用户属性对话框显示
        self.nickname_dialog_img = self.context['cof'].words2img(self.nickname, 50, (450, 245))
        self.rank_dialog_img = self.context['cof'].words2img('段位：' + str(self.get_rank_str(self.rank)), 35, (450, 400))
        self.top_rank_dialog_img = self.context['cof'].words2img('最高段位：'
                                                                 + str(self.get_rank_str(self.top_rank)), 35,
                                                                 (450, 500))
        self.top_score_dialog_img = self.context['cof'].words2img('最高分：' + str(self.top_score), 35, (450, 600))
        self.rating_score_dialog_img = self.context['cof'].words2img('信誉积分：' + str(self.rating_score), 35, (1170, 400))
        self.like_dialog_img = self.context['cof'].words2img('点赞数：' + str(self.like), 35, (1170, 500))
        self.liked_dialog_img = self.context['cof'].words2img('被赞数：' + str(self.liked), 35, (1170, 600))

        # 输入框内容显示
        self.username_img = self.context['cof'].words2img(self.username, 70, (636, 265))
        self.password_img = self.context['cof'].words2img(len(self.password) * '*', 70, (636, 440))

    # 设置用户左右方向，并更新其Paddle方向
    def set_side(self, side):
        self.side = side
        # print('我是用户', self.player_id, '我的位置在', self.side, '我的Paddle', '在', self.paddle.side)
        self.paddle.set_pos(self.side)
        self.renew_score_img()

    # 用户登陆
    def log_in(self):
        # 连接, 登陆
        if self.context['dsy'].connect():
            # print('放置消息')
            self.context['dsy'].put_data('u l ' + self.username + ' ' + self.get_pass_md5())
            return True
        return False

    # 用户注销
    def log_out(self):
        # 注销， 断开连接
        if self.context['dsy'].connect():
            self.context['dsy'].put_data('u lo')
            return True
        return False

    # 重置用户个人信息
    def reset(self):
        self.username = ''
        self.password = ''
        self.set_local_user_info()
        # 玩家数据，重设

        init_info = '未登录' + ' *' + ' 0' + ' 0' + ' 0' + ' 0' + ' 0' + ' 100' + ' 1'
        self.set_user_info(init_info)
        # 以上信息服务器同步并存储，以下为无需同步
        self.state = False
        self.side = 'left'
        self.score = 0
        self.paddle.reset()
        self.re_new_img()

    # 重置战局信息
    def reset_local(self):
        self.set_side('left')
        self.score = 0
        self.paddle.reset()
        self.re_new_img()
        self.renew_score_img()

    # 更新用户信息
    def set_user_info(self, info_str):
        info = info_str.split()
        # print(info)
        self.nickname = info[0]
        self.like = int(info[2])
        self.liked = int(info[3])
        self.top_score = int(info[4])
        self.top_rank = int(info[5])
        self.rank = int(info[6])
        self.rating_score = int(info[7])
        self.avatar_id = int(info[8])

        # self.paddle.reset()
        self.re_new_img()

    # 设置用户头像
    def set_avatar(self, index):
        # print('头像++', index)
        self.avatar = self.context['res'].avatars[index - 1]

    # 密码散列
    def get_pass_md5(self):
        return hashlib.md5((self.password + '盐').encode(encoding='utf-8')).hexdigest()

    # 供外部使用
    def set_username(self, username):
        self.username = username
        self.username_img = self.context['cof'].words2img(self.username, 70, (636, 265))

    def set_password(self, password):
        self.password = password
        self.password_img = self.context['cof'].words2img(len(self.password) * '*', 70, (636, 440))
