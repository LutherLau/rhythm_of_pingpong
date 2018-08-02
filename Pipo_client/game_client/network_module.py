# 本模块用于游戏联网所需的帧同步框架

import socket
import queue
import threading


class GameDataSync:
    def __init__(self):
        # 服务器地址
        self.HOST = ('lutherlau.com', 7890)
        self.BUF_SIZE = 1024
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 队列存放字符串，用于网网络通信
        self.get_queue = queue.Queue()
        self.put_queue = queue.Queue()
        # 收发线程
        self.get_message = None
        self.put_message = None

        # 启动网络，并开启消息线程
        if self.connect():
            self.start_sync()

    # 消息循环
    def start_sync(self):
        if self.get_message is None:
            self.get_message = threading.Thread(target=self.recv_data, args=())
            self.get_message.setDaemon(True)
            self.get_message.start()
        if self.put_message is None:
            self.put_message = threading.Thread(target=self.send_data, args=())
            self.put_message.setDaemon(True)
            self.put_message.start()

    # 连接服务器
    def connect(self):
        try:
            self.client.connect(self.HOST)
            return True
        except Exception as e:
            if '10056' in str(e):
                return True
            # print('错误：' + str(e))
            return False

    # 发送数据
    def send_data(self):
        while True:
            if not self.put_queue.empty():
                data = self.put_queue.get()
                try:
                    self.client.send(data.encode(encoding='utf-8'))
                    # print('发送' + data)
                except Exception as e:
                    # print('错误：' + str(e))
                    continue

                # 退出程序，释放连接，暂且保留
                if data[0] == 'q':
                    self.put_message = None
                    break

    # 接受数据
    def recv_data(self):
        while True:
            try:
                data = self.client.recv(self.BUF_SIZE)
                # 转换并放置
                data = data.decode(encoding='utf-8')
                if data:
                    # 把数据切换成指令消息
                    data = data.split('@')
                    for str_ in data:
                        self.get_queue.put(str_)
                        # ('收取' + str_)

                    # 退出程序，释放连接 保留
                    if data[0] == 'q':
                        self.get_message = None
                        break
            except Exception as e:
                # print('错误：' + str(e))
                # 请重启游戏please restart game
                self.get_queue.put('p r')
                continue

    # 关闭连接， 保留
    def close(self):
        try:
            # 关闭网络线程
            self.client.close()
        except Exception as e:
            # print('错误：' + str(e))
            return False
        return True

    # 发送消息
    def send(self, data):
        self.client.send(data.encode(encoding='utf-8'))

    # 接受消息
    def recv(self):
        return self.client.recv(self.BUF_SIZE).decode(encoding='utf-8')

    # 取得数据
    def get_data(self):
        return self.put_queue.get()

    # 放置数据
    def put_data(self, data):
        self.put_queue.put(data)
