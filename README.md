# Rhythm-of-Pingpong

## 一个简单的弹球游戏

### 游戏功能
* 人机对战
* 双人对战
* 在线排位
* 在线匹配


### 游戏截图
<img src="https://raw.githubusercontent.com/lutherlau/rhythm-of-pingpong/master/images/20181120132837208_27797.png" width="512px"/>
<img src="https://raw.githubusercontent.com/lutherlau/rhythm-of-pingpong/master/images/20181120132856387_1962.png" width="512px"/>
<img src="https://raw.githubusercontent.com/lutherlau/rhythm-of-pingpong/master/images/20181120132939010_7753.png" width="512px"/>
<img src="https://raw.githubusercontent.com/lutherlau/rhythm-of-pingpong/master/images/20181120132921869_12896.png" width="512px"/>
<img src="https://raw.githubusercontent.com/lutherlau/rhythm-of-pingpong/master/images/20181120132959104_13985.png" width="512px"/>
<img src="https://raw.githubusercontent.com/lutherlau/rhythm-of-pingpong/master/images/20181120133010048_14548.png" width="512px"/>
<img src="https://raw.githubusercontent.com/lutherlau/rhythm-of-pingpong/master/images/20181120133050975_24855.png" width="512px"/>


### 服务端部署
- 游戏服务器
```python3
python3 game_server.py
```

- 用户管理服务器
```python3
python3 join_server.py
```

### 开始游戏
> 注意游戏的配置文件设置为正确的服务器地址

```
pip3 install pygame
python3 rhythm_of_pingpong.py
```
### 主要技术
* 游戏使用Pygame进行编写
* 游戏服务器使用原生Socket编程，主要涉及TCP，多线程，匹配队列
* 服务端使用Sqlite3作为后端存储
### 其他
* 游戏部分多媒体素材来源于网络，如有侵权，请告知删除！
