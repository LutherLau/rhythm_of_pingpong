import pygame
import webbrowser


def control(context, ui_context):
    # 游戏首页
    if context['umd'] == 'index_ui':
        # 获取消息队列
        while not context['dsy'].get_queue.empty():
            data = context['dsy'].get_queue.get()
            # 重启游戏
            if data == 'p r':
                ui_context.pr_toast_flag = 22
            # User Login Success
            if data == 'u l s':
                context['pys'][0].state = True
                if ui_context.rem_pass_flag:
                    context['pys'][0].save_local_user_all()
                else:
                    context['pys'][0].save_local_user_username()
            # User Logout Success
            elif data == 'u lo s':
                # 放在消息中处理
                context['pys'][0].state = False
                context['pys'][0].reset()
            # User Login No`this User
            elif data == 'u l nu':
                ui_context.nu_toast_flag = 22
            # User Password Wrong
            elif data == 'u l wp':
                ui_context.pw_toast_flag = 22
            # Set User_info
            elif data[0:3] == 's u':
                # print(data[3:-1])
                context['pys'][0].set_user_info(data[3:-1])

        # 获取事件队列
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                context['cof'].close_game(context)
            # 鼠标点击
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 播放音效
                context['res'].click_sound.play()
                # 鼠标左键单击
                if event.button == 1:
                    if ui_context.dialog_flag:
                        if ui_context.user_info_flag:
                            # 用户已经登陆
                            if context['pys'][0].state:
                                # 注销， 返回大厅
                                if context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].log_out)):
                                    if context['pys'][0].log_out():
                                        pass
                                        # print('用户注销成功')
                            # 用户没有登陆(未登录界面)
                            else:
                                # 用户名输入框光标Flag
                                if context['cof'].hover(event.pos,
                                                        context['cof'].get_rect(context['res'].username_box)):
                                    ui_context.pass_box_flag = False
                                    ui_context.name_box_flag = True
                                # 密码输入框
                                elif context['cof'].hover(event.pos,
                                                          context['cof'].get_rect(context['res'].password_box)):
                                    ui_context.name_box_flag = False
                                    ui_context.pass_box_flag = True
                                # 记住密码
                                elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].rememb)):
                                    ui_context.rem_pass_flag = not ui_context.rem_pass_flag
                                # 登陆
                                elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].login_in)):
                                    ui_context.pass_box_flag = False
                                    if context['pys'][0].log_in():
                                        pass
                                        # print("点击登录按钮")
                                    continue
                                # 注册
                                elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].register)):
                                    webbrowser.open('http://kuafulab.com/rhythm_of_pingpong/join/')
                            if context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].back)):
                                # print("返回游戏大厅")
                                context['cof'].close_dialog(ui_context)

                        elif ui_context.rank_list_flag:
                            # 排行榜显示界面控制
                            pass
                        elif ui_context.setting_menu_flag:
                            # 显示设置菜单控制
                            pass
                    else:
                        if context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].like_2)):
                            webbrowser.open('https://github.com/LutherLau/rhythm_of_pingpong')
                        elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].notice)):
                            webbrowser.open('http://kuafulab.com/rhythm_of_pingpong/notice/')
                        elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].tools_bar_b1)):
                            webbrowser.open('http://kuafulab.com/rhythm_of_pingpong/about/')
                        elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].tools_bar_b2)):
                            webbrowser.open('http://kuafulab.com/rhythm_of_pingpong/update/')
                        elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].tools_bar_b3)):
                            context['cof'].close_game(context)
                        elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].tools_bar_b4)):
                            webbrowser.open('http://kuafulab.com/rhythm_of_pingpong/feedback/')

                        if context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].on_line_battle)):
                            # print("点击在线对战")
                            # 用户在线， 进入匹配
                            if context['pys'][0].state:
                                ui_context.match('b')
                                context['umd'] = 'on_line_battle'
                                return
                            else:
                                # No Login
                                # 提示登陆
                                ui_context.nl_toast_flag = 22
                                continue

                        elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].on_line_ranking)):
                            # print("点击在线排位")
                            # 用户在线， 进入匹配
                            if context['pys'][0].state:
                                ui_context.match('r')
                                context['umd'] = 'on_line_ranking'
                                return
                            else:
                                # No Login
                                # 提示登陆
                                ui_context.nl_toast_flag = 22
                                continue

                        elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].off_line_one)):
                            context['umd'] = 'off_line_one_ui'
                            # print("点击单机")
                            return
                        elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].off_line_two)):
                            # print("点击双人对战")
                            context['umd'] = 'off_line_two_ui'
                            return
                        elif context['cof'].hover(event.pos, context['cof'].get_rect(context['pys'][0].avatar)):
                            # print("点击头像")
                            ui_context.user_info_flag = True
                            ui_context.dialog_flag = True
                        elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].ranking_list)):
                            pass
                            # 　print("点击排行榜")
            # 键盘响应
            elif event.type == pygame.KEYDOWN:
                this_key = event
                # 根据不同的场景，监视不同的按键
                # 对话框
                if ui_context.dialog_flag:
                    if this_key.key == pygame.K_ESCAPE:
                        context['cof'].close_dialog(ui_context)
                    if ui_context.user_info_flag:
                        if not context['pys'][0].state:
                            if this_key.key == pygame.K_RETURN:
                                # 回车切换输入框
                                if ui_context.name_box_flag:
                                    ui_context.name_box_flag = False
                                    ui_context.pass_box_flag = True
                                    continue
                                # 回车登陆
                                elif ui_context.pass_box_flag:
                                    ui_context.pass_box_flag = False
                                    if context['pys'][0].log_in():
                                        pass
                                        # print("回车登陆")
                                    continue
                            elif this_key.key == pygame.K_BACKSPACE:
                                # print('退格')
                                if ui_context.name_box_flag:
                                    context['pys'][0].set_username(context['pys'][0].username[0:-1])
                                elif ui_context.pass_box_flag:
                                    context['pys'][0].set_password(context['pys'][0].password[0:-1])
                            else:
                                key_char = str(this_key.unicode)
                                if key_char.isalnum():
                                    if ui_context.name_box_flag:
                                        if len(context['pys'][0].username) < 16:
                                            context['pys'][0].set_username(context['pys'][0].username + key_char)
                                            # print('username', context['pys'][0].username)
                                    elif ui_context.pass_box_flag:
                                        if len(context['pys'][0].password) < 16:
                                            context['pys'][0].set_password(context['pys'][0].password + key_char)
                                            # print('password', context['pys'][0].password)

                    elif ui_context.rank_list_flag:
                        pass
                    elif ui_context.setting_menu_flag:
                        pass
                    elif ui_context.about_game_flag:
                        pass
                    elif ui_context.notice_flag:
                        pass
                else:
                    # 弹出退出确认界面（保留）
                    context['cof'].close_game(context)

    # 双人离线
    elif context['umd'] == 'off_line_two_ui':
        # 获取事件队列
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                context['cof'].close_game(context)
            # 鼠标点击
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标左键单击
                if event.button == 1:
                    if ui_context.dialog_flag:
                        context['res'].click_sound.play()
                        # 游戏结算界面
                        if ui_context.start_pre_flag or ui_context.over_flag:
                            # 回主菜单，第一次开始与重新开始并无差
                            if context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].start)):
                                # print("开始游戏")
                                ui_context.reset()
                                ui_context.start_pre_flag = False
                                ui_context.running_flag = True
                                ui_context.dialog_flag = False
                                context['pys'][0].reset_local()
                                context['pys'][1].reset_local()
                                context['pys'][0].set_side('left')
                                context['pys'][1].set_side('right')
                        if context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].back)):
                            # 回主菜单
                            # print("回主菜单")
                            ui_context.reset()
                            context['umd'] = 'index_ui'

            # 键盘响应
            elif event.type == pygame.KEYDOWN:
                this_key = event
                # 根据不同的场景，监视不同的按键
                # 对话框
                if ui_context.dialog_flag:
                    if this_key.key == pygame.K_ESCAPE:
                        ui_context.reset()
                        context['umd'] = 'index_ui'
                    elif this_key.key == pygame.K_RETURN:
                        # print("开始游戏")
                        ui_context.reset()
                        ui_context.start_pre_flag = False
                        ui_context.running_flag = True
                        ui_context.dialog_flag = False
                        context['pys'][0].reset_local()
                        context['pys'][1].reset_local()
                        context['pys'][0].set_side('left')
                        context['pys'][1].set_side('right')
                else:
                    # 游戏界面
                    if this_key.key == pygame.K_w:
                        # print('按下W')
                        context['pys'][0].paddle.up = True
                    elif this_key.key == pygame.K_s:
                        context['pys'][0].paddle.down = True
                        # print('按下S')
                    elif this_key.key == pygame.K_UP:
                        context['pys'][1].paddle.up = True
                        # print('按下↑')
                    elif this_key.key == pygame.K_DOWN:
                        context['pys'][1].paddle.down = True
                        # print('按下↓')

            elif event.type == pygame.KEYUP:
                this_key = event
                if ui_context.running_flag:
                    if this_key.key == pygame.K_w:
                        # print('松开W')
                        context['pys'][0].paddle.up = False
                    elif this_key.key == pygame.K_s:
                        context['pys'][0].paddle.down = False
                        # print('松开S')
                    elif this_key.key == pygame.K_UP:
                        context['pys'][1].paddle.up = False
                        # print('松开↑')
                    elif this_key.key == pygame.K_DOWN:
                        context['pys'][1].paddle.down = False
                        # print('松开↓')

    elif context['umd'] == 'off_line_one_ui':
        while not context['dsy'].get_queue.empty():
            data = context['dsy'].get_queue.get()
            if data == 'u l s':
                context['pys'][0].state = True
            elif True:
                pass

        # 获取事件队列
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                context['cof'].close_game(context)
            # 鼠标点击
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标左键单击
                if event.button == 1:
                    if ui_context.dialog_flag:
                        context['res'].click_sound.play()
                        # 游戏结算界面
                        if ui_context.start_pre_flag or ui_context.over_flag:
                            # 回主菜单，第一次开始与重新开始并无差别
                            if context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].start)):
                                # print("开始游戏")
                                ui_context.reset()
                                ui_context.start_pre_flag = False
                                ui_context.running_flag = True
                                ui_context.dialog_flag = False
                                context['pys'][0].reset_local()
                                context['pys'][1].reset_local()
                                context['pys'][0].set_side('left')
                                context['pys'][1].set_side('right')
                        if context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].back)):
                            # 回主菜单
                            # print("回主菜单")
                            ui_context.reset()
                            context['umd'] = 'index_ui'

            # 键盘响应
            elif event.type == pygame.KEYDOWN:
                this_key = event
                # 根据不同的场景，监视不同的按键
                # 对话框时
                if ui_context.dialog_flag:
                    if this_key.key == pygame.K_ESCAPE:
                        ui_context.reset()
                        context['umd'] = 'index_ui'
                    elif this_key.key == pygame.K_RETURN:
                        # print("开始游戏")
                        ui_context.reset()
                        ui_context.start_pre_flag = False
                        ui_context.running_flag = True
                        ui_context.dialog_flag = False
                        context['pys'][0].reset_local()
                        context['pys'][1].reset_local()
                        context['pys'][0].set_side('left')
                        context['pys'][1].set_side('right')
                else:
                    # 游戏界面
                    if this_key.key == pygame.K_w:
                        # print('按下W')
                        context['pys'][0].paddle.up = True
                    elif this_key.key == pygame.K_s:
                        context['pys'][0].paddle.down = True
                        # print('按下S')
                    elif this_key.key == pygame.K_UP:
                        context['pys'][1].paddle.up = True
                        # print('按下↑')
                    elif this_key.key == pygame.K_DOWN:
                        context['pys'][1].paddle.down = True
                        # print('按下↓')

            elif event.type == pygame.KEYUP:
                this_key = event
                if ui_context.running_flag:
                    if this_key.key == pygame.K_w:
                        # print('松开W')
                        context['pys'][0].paddle.up = False
                    elif this_key.key == pygame.K_s:
                        context['pys'][0].paddle.down = False
                        # print('松开S')
                    elif this_key.key == pygame.K_UP:
                        context['pys'][1].paddle.up = False
                        # print('松开↑')
                    elif this_key.key == pygame.K_DOWN:
                        context['pys'][1].paddle.down = False
                        # print('松开↓')

    elif context['umd'] == 'on_line_battle':
        while not context['dsy'].get_queue.empty():
            try:
                data = context['dsy'].get_queue.get()
                # print('对战模式收到', data)
                # Set Object（右侧玩家会收到此类信息, 左侧玩家会收到设置paddle的信息）
                if data[0:2] == 'so':
                    # 截取
                    data = data[3:]
                    # Ball Ver 速度
                    if data[0:2] == 'bv':
                        ui_context.ball.set_ver_online(data[2:])

                    # Ball bounce反弹音效
                    elif data[0:2] == 'sb':
                        context['res'].bounce_sound.play()
                    # Ball In
                    elif data[0:2] == 'si':
                        context['res'].in_sound.play()
                    # 设置球的位置
                    elif data[0] == 'b':
                        ui_context.ball.set_pos_online(data[1:])
                    # paddle 的位置
                    elif data[0] == 'p':
                        # 设置paddle的位置
                        context['pys'][1].paddle.set_pos_online(data[1:])
                    elif data[0] == 's':
                        # 分数更新
                        data = data[1:].split(' ')
                        context['pys'][1].score = int(data[0])
                        context['pys'][0].score = int(data[1])
                        context['pys'][0].renew_score_img()
                        context['pys'][1].renew_score_img()
                # match success
                elif data[0:3] == 'm s':
                    # 匹配成功
                    # 重置用户信息
                    context['pys'][1].set_user_info(data[5:-1])
                    context['pys'][0].reset_local()
                    context['pys'][1].reset_local()
                    if data[4] == 'l':
                        context['pys'][0].set_side('left')
                        context['pys'][1].set_side('right')
                        ui_context.left_toast_flag = 30
                    elif data[4] == 'r':
                        context['pys'][1].set_side('left')
                        context['pys'][0].set_side('right')
                        ui_context.right_toast_flag = 30
                    # 重置游戏信息
                    ui_context.reset_flags()

                    ui_context.running_flag = True
                    ui_context.match_flag = False
                elif data[0:2] == 'go':
                    ui_context.dialog_flag = True
                    ui_context.over_flag = True
                    if data[3] == 'l':
                        ui_context.lose_flag = True
                    elif data[3] == 'w':
                        ui_context.win_flag = True
                    elif data[3] == 't':
                        ui_context.tie_flag = True
                if data == 'p r':
                    ui_context.pr_toast_flag = 22
            except Exception:
                # 收到的信息可能有空的
                pass

        # 获取事件队列
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                context['cof'].close_game(context)
            # 鼠标点击
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标左键单击
                if event.button == 1:
                    if ui_context.dialog_flag:
                        context['res'].click_sound.play()
                        # 游戏结算界面
                        if ui_context.over_flag:
                            # 回主菜单，第一次开始与重新开始并无差别
                            if context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].re_start)):
                                ui_context.reset()
                                # ("再来一局")
                                # 更新分数还是放在本地比较大小更好些，待优化
                                context['dsy'].put_data('update score ' + str(context['pys'][0].score))
                                ui_context.match()
                            elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].back)):
                                # 回主菜单
                                # print("回主菜单")
                                ui_context.reset()
                                # 更新分数
                                context['dsy'].put_data('update score ' + str(context['pys'][0].score))
                                context['umd'] = 'index_ui'
                            elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].like)):
                                # 回主菜单
                                # print("为对手点赞")
                                context['dsy'].put_data('update like ' + context['pys'][1].nickname)

            # 键盘响应
            elif event.type == pygame.KEYDOWN:
                this_key = event
                # 根据不同的场景，监视不同的按键
                # 对话框时
                if ui_context.dialog_flag:
                    if this_key.key == pygame.K_ESCAPE:
                        ui_context.reset()
                        context['umd'] = 'index_ui'
                        context['dsy'].put_data('update score ' + str(context['pys'][0].score))

                    elif this_key.key == pygame.K_RETURN:
                        ui_context.reset()
                        # print("再来一局")
                        # 更新分数
                        context['dsy'].put_data('update score ' + str(context['pys'][0].score))
                        ui_context.match()
                else:
                    # 游戏界面
                    if context['pys'][0].side == 'left':
                        if this_key.key == pygame.K_w:
                            # print('按下W')
                            context['pys'][0].paddle.up = True
                        elif this_key.key == pygame.K_s:
                            context['pys'][0].paddle.down = True
                            # print('按下S')
                    else:
                        if this_key.key == pygame.K_UP:
                            context['pys'][0].paddle.up = True
                            # print('按下↑')
                        elif this_key.key == pygame.K_DOWN:
                            context['pys'][0].paddle.down = True
                            # print('按下↓')

            elif event.type == pygame.KEYUP:
                this_key = event
                if ui_context.running_flag:
                    if context['pys'][0].side == 'left':
                        if this_key.key == pygame.K_w:
                            # print('松开W')
                            context['pys'][0].paddle.up = False
                        elif this_key.key == pygame.K_s:
                            context['pys'][0].paddle.down = False
                            # print('松开S')
                    else:
                        if this_key.key == pygame.K_UP:
                            context['pys'][0].paddle.up = False
                            # print('松开↑')
                        elif this_key.key == pygame.K_DOWN:
                            context['pys'][0].paddle.down = False
                            # print('松开↓')

    elif context['umd'] == 'on_line_ranking':
        while not context['dsy'].get_queue.empty():
            try:
                data = context['dsy'].get_queue.get()
                # print('对战模式收到', data)
                # Set Object（右侧玩家会收到此类信息, 左侧玩家会收到设置paddle的信息）
                if data[0:2] == 'so':
                    # 截取
                    data = data[3:]
                    # Ball Ver 速度
                    if data[0:2] == 'bv':
                        ui_context.ball.set_ver_online(data[2:])

                    # Ball bounce反弹音效
                    elif data[0:2] == 'sb':
                        context['res'].bounce_sound.play()
                    # Ball In
                    elif data[0:2] == 'si':
                        context['res'].in_sound.play()
                    # 设置球的位置
                    elif data[0] == 'b':
                        ui_context.ball.set_pos_online(data[1:])
                    # paddle 的位置
                    elif data[0] == 'p':
                        # 设置paddle的位置
                        context['pys'][1].paddle.set_pos_online(data[1:])
                    elif data[0] == 's':
                        # 分数更新
                        data = data[1:].split(' ')
                        context['pys'][1].score = int(data[0])
                        context['pys'][0].score = int(data[1])
                        context['pys'][0].renew_score_img()
                        context['pys'][1].renew_score_img()
                    elif data[0] == 'r':
                        # 段位更新
                        data = data[1:].split(' ')
                        context['pys'][1].rank = int(data[0])
                        context['pys'][0].rank = int(data[1])

                # match success
                elif data[0:3] == 'm s':
                    # 匹配成功
                    # 重置用户信息
                    context['pys'][1].set_user_info(data[5:-1])
                    context['pys'][0].reset_local()
                    context['pys'][1].reset_local()
                    if data[4] == 'l':
                        context['pys'][0].set_side('left')
                        context['pys'][1].set_side('right')
                        ui_context.left_toast_flag = 30
                    elif data[4] == 'r':
                        context['pys'][1].set_side('left')
                        context['pys'][0].set_side('right')
                        ui_context.right_toast_flag = 30

                    # 重置游戏信息
                    ui_context.reset_flags()

                    ui_context.running_flag = True
                    ui_context.match_flag = False
                elif data[0:2] == 'go':
                    ui_context.dialog_flag = True
                    ui_context.over_flag = True
                    if data[3] == 'l':
                        ui_context.lose_flag = True
                    elif data[3] == 'w':
                        ui_context.win_flag = True
                    elif data[3] == 't':
                        ui_context.tie_flag = True
                if data == 'p r':
                    ui_context.pr_toast_flag = 22
            except Exception:
                # 收到的信息可能有空的
                pass

        # 获取事件队列
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                context['cof'].close_game(context)
            # 鼠标点击
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标左键单击
                if event.button == 1:
                    if ui_context.dialog_flag:
                        context['res'].click_sound.play()
                        # 游戏结算界面
                        if ui_context.over_flag:
                            # 回主菜单，第一次开始与重新开始并无差别
                            if context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].re_start)):
                                ui_context.reset()
                                # print("再来一局")
                                # 更新分数还是放在本地比较大小更好些，待优化
                                context['dsy'].put_data('update score ' + str(context['pys'][0].score))
                                context['dsy'].put_data('update rank ' + str(context['pys'][0].score))
                                ui_context.match()
                            elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].back)):
                                # 回主菜单
                                # print("回主菜单")
                                ui_context.reset()
                                # 更新分数
                                context['dsy'].put_data('update score ' + str(context['pys'][0].score))
                                context['dsy'].put_data('update rank ' + str(context['pys'][0].score))
                                context['umd'] = 'index_ui'
                            elif context['cof'].hover(event.pos, context['cof'].get_rect(context['res'].like)):
                                # 回主菜单
                                # print("为对手点赞")
                                context['dsy'].put_data('update like ' + context['pys'][1].nickname)

            # 键盘响应
            elif event.type == pygame.KEYDOWN:
                this_key = event
                # 根据不同的场景，监视不同的按键
                # 对话框时
                if ui_context.dialog_flag:
                    if this_key.key == pygame.K_ESCAPE:
                        ui_context.reset()
                        context['umd'] = 'index_ui'
                        context['dsy'].put_data('update score ' + str(context['pys'][0].score))
                        context['dsy'].put_data('update rank ' + str(context['pys'][0].score))
                    elif this_key.key == pygame.K_RETURN:
                        ui_context.reset()
                        # print("再来一局")
                        # 更新分数
                        context['dsy'].put_data('update score ' + str(context['pys'][0].score))
                        context['dsy'].put_data('update rank ' + str(context['pys'][0].score))
                        ui_context.match()
                else:
                    # 游戏界面
                    if context['pys'][0].side == 'left':
                        if this_key.key == pygame.K_w:
                            # print('按下W')
                            context['pys'][0].paddle.up = True
                        elif this_key.key == pygame.K_s:
                            context['pys'][0].paddle.down = True
                            # print('按下S')
                    else:
                        if this_key.key == pygame.K_UP:
                            context['pys'][0].paddle.up = True
                            # print('按下↑')
                        elif this_key.key == pygame.K_DOWN:
                            context['pys'][0].paddle.down = True
                            # print('按下↓')

            elif event.type == pygame.KEYUP:
                this_key = event
                if ui_context.running_flag:
                    if context['pys'][0].side == 'left':
                        if this_key.key == pygame.K_w:
                            # print('松开W')
                            context['pys'][0].paddle.up = False
                        elif this_key.key == pygame.K_s:
                            context['pys'][0].paddle.down = False
                            # print('松开S')
                    else:
                        if this_key.key == pygame.K_UP:
                            context['pys'][0].paddle.up = False
                            # print('松开↑')
                        elif this_key.key == pygame.K_DOWN:
                            context['pys'][0].paddle.down = False
                            # print('松开↓')
