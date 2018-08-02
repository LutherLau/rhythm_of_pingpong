import os
import socket
import hashlib
import sqlite3
import datetime

# 地址信息
HOST = ('', 3721)

# 返回的头部信息
POST_RET = '''HTTP/1.x 200 OK  
Content-Type: text/html
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: POST

'''

# Socket配置（HTTP）
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(HOST)
server.listen(100)

# 用户数据存储路径
os.chdir('../data/')

# 报文首部与正文分隔符
line_separator = '\r\n'

def get_insert_sql_str(username, password, avatar):
    sql_str = "insert into users_info values ('"
    sql_str += username
    sql_str += "', '"
    sql_str += password
    sql_str += "', "
    sql_str += "0"
    sql_str += ", "
    sql_str += "0"
    sql_str += ", "
    sql_str += "0"
    sql_str += ", "
    sql_str += "0"
    sql_str += ", "
    sql_str += "0"
    sql_str += ", "
    sql_str += "100"
    sql_str += ", "
    sql_str += avatar
    sql_str += ")"
    return sql_str







# 创建数据库，用户信息表
if not os.path.exists('users_info.db'):
    conn = sqlite3.connect('../data/users_info.db')
    cursor = conn.cursor()
    cursor.execute('''create table users_info
                    (username varchar(20) primary key,
                     password varchar(40),
                     like int,
                     liked int,
                     top_score int,
                     top_rank int,
                     current_rank int,
                     rating_score int,
                     avatar int);''')
    conn.commit()
    conn.close()

conn = sqlite3.connect('../data/users_info.db')
cursor = conn.cursor()

while True:
    client, address = server.accept()
    try:
        request = client.recv(2048).decode(encoding='utf-8')
    except Exception:
        client.sendall((POST_RET + '发生了一些错误，请稍后重试').encode(encoding='utf-8'))
        client.close()
        continue
  
    method = request.split(' ')[0]

    if method == 'POST':
        # 获取表单
        user_info = request.split(line_separator)[-1]

        # print(user_info)

        user_info = user_info.split('&')

        user_info_list_len = len(user_info)

        # 处理提交数据，判断是否注册可以注册
        return_message = '非法信息'
        if user_info_list_len == 1:
            if 'feed' in user_info[0]:
                data_f = user_info[0].split('=')[-1]
                return_message = '感谢吐槽...'
                file_name = str(datetime.datetime.now())
                if len(os.listdir('./feedback/')) < 50:
                    try:
                        with open('./feedback/' + file_name.replace(':', '_').replace('-', '_').replace(' ', '_') + '.txt', 'wt') as fout:
                            fout.write(data_f)
                    except:
                        return_message = '很不幸，服务器出错了...'
                else:
                    return_message = '很不幸，信箱太满了, 塞不进去了...'

        elif user_info_list_len == 4:

            # 取得值
            for i in range(4):
                user_info[i] = user_info[i].split('=')[-1]
                # print(user_info)

            # 用户名长度
            if len(user_info[0]) < 16:
                # 用户名以及密码组成'
                if user_info[0].isalnum() and user_info[1].isalnum() and user_info[2].isalnum():
                    users = cursor.execute("select username from users_info where username = '" + user_info[0] + "';").fetchall()
                    if len(users) > 0:
                        return_message = '啊哦， 注册名已被占用，换个试试吧'
                    else:
                        if user_info[1] == user_info[2]:
                            # 检查头像
                            if user_info[3].isdigit() and int(user_info[3]) in range(1,6):
                                user_info[1] += '盐'
                                password_md5 = hashlib.md5(user_info[1].encode(encoding='utf-8')).hexdigest()
                                sql_str = get_insert_sql_str(user_info[0], password_md5, user_info[3])
                                # print(sql_str)
                                # 写入数据库
                                try:
                                    cursor.execute(sql_str)
                                    conn.commit()
                                    return_message = '恭喜，注册成功'
                                    # print('注册用户 + 1')
                                except:
                                    pass
                            else:
                                return_message = '啊哦，请重新选择头像'
                        else:
                            return_message = '啊哦，两次密码输入不一致'
                else:
                    return_message = '啊哦，用户名或密码含有非法字符，请保证只含有大小写拉丁字母和数字'
            else:
                return_message = '啊哦，用户名过长'
        # 返回处理结果
        client.sendall((POST_RET + return_message).encode(encoding='utf-8'))
    else:
        client.sendall((POST_RET + '不支持的请求').encode(encoding='utf-8'))
    client.close()