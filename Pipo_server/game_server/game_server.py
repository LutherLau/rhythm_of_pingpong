from socket import *
import threading
import sqlite3

pingpong_server = socket(AF_INET, SOCK_STREAM)
pingpong_server.bind(('', 7890))
pingpong_server.listen(30)

match_queue_battle = []
match_queue_rank = []

rooms = {}  # socket socket，正在房间中对战的游客
all_user = {}  # sock 用户信息


# 定义一个房间类，然后该房间维护对局，信息接受负责
def get_update_str(key, value, user):
    ret = 'update users_info set ' + key + ' = ' + value + ' where username = ' + "'" + user + "'"
    return ret


def get_user_info_str(list_):
    ret = ''
    for i in list_:
        ret += (str(i) + ' ')
    return ret


def queue_to_rom_rank():
    global match_queue_rank
    while True:
        # 匹配队列
        if len(match_queue_rank) >= 2:
            rooms[match_queue_rank[0]] = match_queue_rank[1]
            rooms[match_queue_rank[1]] = match_queue_rank[0]
            # print('加入房间')
            # 先匹配成功，然后设置双方位置
            match_queue_rank[0].send(
                ('m s l' + get_user_info_str(all_user[match_queue_rank[1]][0])).encode(encoding='utf-8'))
            match_queue_rank[1].send(
                ('m s r' + get_user_info_str(all_user[match_queue_rank[0]][0])).encode(encoding='utf-8'))
            match_queue_rank[0].send('left@'.encode(encoding='utf-8'))
            match_queue_rank[1].send('right@'.encode(encoding='utf-8'))

            # print('发送匹配成功')
            # 用户状态
            all_user[match_queue_rank[0]][1] = 1
            all_user[match_queue_rank[1]][1] = 1
            # 更新匹配队列
            match_queue_rank = match_queue_rank[2:]


def queue_to_rom_battle():
    global match_queue_battle
    while True:
        if len(match_queue_battle) >= 2:
            rooms[match_queue_battle[0]] = match_queue_battle[1]
            rooms[match_queue_battle[1]] = match_queue_battle[0]
            # print('加入房间')
            # 先匹配成功，然后设置双方位置
            match_queue_battle[0].send(
                ('m s l' + get_user_info_str(all_user[match_queue_battle[1]][0])).encode(encoding='utf-8'))
            match_queue_battle[1].send(
                ('m s r' + get_user_info_str(all_user[match_queue_battle[0]][0])).encode(encoding='utf-8'))
            match_queue_battle[0].send('left@'.encode(encoding='utf-8'))
            match_queue_battle[1].send('right@'.encode(encoding='utf-8'))

            # print('发送匹配成功')
            # 用户状态
            all_user[match_queue_battle[0]][1] = 1
            all_user[match_queue_battle[1]][1] = 1
            # 更新匹配队列
            match_queue_battle = match_queue_battle[2:]


def pingpong_data_sync(sock):
    # 数字0表示 未在游戏，1 表示游戏中
    # 数据库链接
    global match_queue_battle
    global match_queue_rank
    while True:
        trans_data = b'*'
        # print(all_user)
        try:
            trans_data = sock.recv(1024)
            # print(trans_data.decode(encoding='utf-8'))
        except Exception as e:
            # 删除, 对方断开
            if sock in all_user.keys():
                del all_user[sock]
            # print(str(e))
            # print(all_user)
            sock.close()
            return

        trans_data = trans_data.decode(encoding='utf-8')
        if trans_data != '*':
            # print('收到信息', trans_data)
            if trans_data[0:4] == 'u l ':  # 用户登陆
                # print('用户登陆', trans_data)
                trans_data = trans_data.split()
                user_info = trans_data[2:]
                ret = 'u l nu'
                # 数据库对比
                conn = sqlite3.connect('../data/users_info.db')
                cursor = conn.cursor()
                user_info_s = cursor.execute(
                    "select * from users_info where username = '" + user_info[0] + "';").fetchall()
                conn.close()

                # print(user_info_s)
                if len(user_info_s) > 0:
                    if user_info[1] == user_info_s[0][1]:
                        ret = 'u l s'
                        all_user[sock] = [user_info_s[0], 0]
                    else:
                        ret = 'u l wp'
                sock.send(ret.encode(encoding='utf-8'))
                if ret == 'u l s':
                    sock.send(('s u' + get_user_info_str(user_info_s[0])).encode(encoding='utf-8'))

            elif trans_data[0:4] == 'u lo':  # 用户注销
                ret = 'u lo s'
                # print('用户注销')
                sock.send(ret.encode(encoding='utf-8'))
                del all_user[sock]
                # print(all_user)
            elif trans_data[0:3] == 'u b':  # 对战
                # 只存取socket
                # print('正在匹配')
                match_queue_battle.append(sock)
                # match wait
                sock.send('m w'.encode(encoding='utf-8'))

            elif trans_data[0:3] == 'u r':  # 排位
                # 只存取socket
                # print('正在匹配')
                match_queue_rank.append(sock)
                # match wait
                sock.send('m w'.encode(encoding='utf-8'))

                # print(all_user)
            elif trans_data[0:2] == 'so':
                rooms[sock].send(trans_data.encode(encoding='utf-8'))

            elif trans_data[0:2] == 'go':
                rooms[sock].send(trans_data.encode(encoding='utf-8'))
                del rooms[rooms[sock]]
                del rooms[sock]
            elif trans_data[0:6] == 'update':
                conn = sqlite3.connect('../data/users_info.db')
                cursor = conn.cursor()
                user_info_s = cursor.execute(
                    "select * from users_info where username = '" + all_user[sock][0][0] + "';").fetchall()[0]
                # print('debug', user_info_s)
                item = trans_data.split(' ')[1:]
                if item[0] == 'score':
                    if int(item[1]) > int(user_info_s[4]):
                        update_sc = get_update_str('top_score', item[1], all_user[sock][0][0])
                        cursor.execute(update_sc)

                elif item[0] == 'rank':
                    if int(item[1]) > int(user_info_s[5]):
                        update_sc = get_update_str('top_rank', item[1], all_user[sock][0][0])
                        cursor.execute(update_sc)
                    update_sc = get_update_str('current_rank', item[1], all_user[sock][0][0])
                    cursor.execute(update_sc)
                elif item[0] == 'like':
                    update_sc = get_update_str('like', str(int(user_info_s[2]) + 1), all_user[sock][0][0])
                    cursor.execute(update_sc)
                    target_user_info = \
                        cursor.execute("select * from users_info where username = '" + item[1] + "';").fetchall()[0]
                    update_sc = get_update_str('liked', str(target_user_info[3] + 1), item[1])
                    cursor.execute(update_sc)
                conn.commit()
                conn.close()


# 连接之后，启动一个新线程
if __name__ == '__main__':
    battle_match = threading.Thread(target=queue_to_rom_battle, args=())
    battle_match.start()
    rank_match = threading.Thread(target=queue_to_rom_rank, args=())
    rank_match.start()

    # print('匹配程序启动')
    while True:
        # print('等待下一个用户连接...')
        pingpong_client, client_addr = pingpong_server.accept()
        # print(client_addr, '已连接.')
        pingpong_user = threading.Thread(target=pingpong_data_sync, args=(pingpong_client,))
        pingpong_user.start()
