#网易云音乐API配合NeteaseMiniPlayer播放每日推荐#

## 基于[NeteaseMiniPlayer](https://github.com/numakkiyu/NeteaseMiniPlayer)，开发的一个用于Glance仪表板中iFrame嵌入，并自动更新每日歌单

## 思路：

1. 利用python中的requests库，访问自建好的api

2. 新建一个每日歌单

3. api获取每日推荐的歌曲id

4. 添加到每日歌单

5. 把每日歌单的id写到playlist-id.txt(NeteaseMiniPlayer)已经写好，读取这个文件里的id

6. 定时新建/删除（利用计划任务中的shell脚本）

### 相关api路径：

    ```HTTP
    新建歌单：
    接口地址 : /playlist/create
    调用例子 : /playlist/create?name=测试歌单
      
    获取每日推荐歌曲：
    接口地址 : /recommend/songs
    调用例子 : /recommend/songs
      
    对歌单添加或删除歌曲：
    必选参数 :
    op: 从歌单增加单曲为 add, 删除为 del
    pid: 歌单 id tracks: 歌曲 id,可多个,用逗号隔开
    接口地址 : /playlist/tracks
    调用例子 : /playlist/tracks?op=add&pid=24381616&tracks=347231 
      （对应把歌曲添加到 ' 我 ' 的歌单 , 测试的时候请把这里的 pid 换成你自己的, id 和 tracks 不对可能会报 502 错误）
     
    删除歌单：
    必选参数 : id : 歌单 id,可多个,用逗号隔开
    接口地址 : /playlist/delete
    调用例子 : /playlist/delete?id=2947311456 , /playlist/delete?id=5013464397,5013427772
    
    ```
    
## 首先解决：

#### 自建网易云api

    [网易云音乐 API - Docker容器运行](https://github.com/neteasecloudmusicapienhanced/api-enhanced?tab=readme-ov-file#docker-%E9%83%A8%E7%BD%B2%E8%AF%B4%E6%98%8E)

    ```YAML
    services:
        NeteaseCloudMusicApi:
            image: moefurina/ncm-api:latest #使用二次开发api：https://github.com/neteasecloudmusicapienhanced/api-enhanced
            restart: always
            ports:
                - '7788:3000'
            environment:
                http_proxy: 
                https_proxy: 
                HTTP_PROXY: 
                HTTPS_PROXY: 
                no_proxy:
                NO_PROXY:
    ```

    



#### 登录vip账号并获取Cookies

    ```HTTP
    发送验证码
    说明 : 调用此接口 ,传入手机号码, 可发送验证码
    接口地址 : /captcha/sent
    调用例子 : /captcha/sent?phone=13xxx
     
    手机短信获取验证码后
     
    手机登录：
    接口地址 : /login/cellphone
    调用例子 : /login/cellphone?phone=xxx&captcha=1234
    ```

    登录后浏览器访问任意接口，F12-应用-存储-cookies-MUSIC_U，获取Cookies



#### 修改NeteaseMiniPlayer，实现导入Cookies后可播放完整VIP歌曲，并读取相同目录下playlist_id.txt里的值作为歌单id（样式稍微修改背景色，配合Glance）

    ```HTML
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>网易云音乐</title>
    
        <!-- 引入播放器样式文件 -->
        <link rel="stylesheet" href="netease-mini-player-v2.css">
    
        <style>
            /* 针对整个网页进行设置 */
            html, body {
                /* 1. 强制隐藏水平和垂直滚动条 */
                overflow: hidden;
    
                /* 2. 确保背景色生效且铺满全屏 */
                background-color: #151518 !important;
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
            }
        </style>
    </head>
    <body>
    
    <script>
        // 使用 Fetch API 读取文件
        fetch('playlist_id.txt')
            .then(response => response.text())  // 读取文件内容
            .then(data => {
                const playlistId = data.trim();  // 去掉文件内容前后的空白字符
    
                // 创建播放器 div 元素
                const playerDiv = document.createElement('div');
                playerDiv.className = 'netease-mini-player';
                playerDiv.setAttribute('data-playlist-id', playlistId);
                playerDiv.setAttribute('data-embed', 'false');
                playerDiv.setAttribute('data-position', 'static');
                playerDiv.setAttribute('data-lyric', 'true');
                playerDiv.setAttribute('data-theme', 'dark');
                playerDiv.setAttribute('data-auto-pause', 'true');
                playerDiv.setAttribute('data-cookie', '手动读取的Cookie值');      
    
                // 将播放器 div 插入到 body 中
                document.body.appendChild(playerDiv);
    
                console.log('新的 Playlist ID:', playlistId);
    
                // 动态加载播放器脚本
                const script = document.createElement('script');
                script.src = 'netease-mini-player-v2.js';
                document.body.appendChild(script);
            })
            .catch(error => {
                console.error('读取文件失败:', error);
            });
    </script>
    
    </body>
    </html>
    ```

    也需要修改一下js文件，让其包含cookies元素

    [github.com:netease-mini-player-v2.js](https://github.com/Nikkiiw/NeteaseMiniPlayer/blob/main/netease-mini-player-v2.js)

    ![Image_2026-04-07_13-03-32_3xya1jnf.s0u.png](https://flowus.cn/preview/819a0306-4f7f-433e-bfee-3056cd754a72)

    现在就可以在同目录下的playlist_id.txt里指定歌单id了

    顺手修复一个小bug，播放列表里面的内部滚动行为会让Glace加载完以后向下滚动，将1003行的activeItem.scrollIntoView(...)注释掉就好了



#### 检查Debian13的python有无requests库

    ### 🔍 怎么确认？

    在终端输入：

    ```Shell
    python3 --version
    ```

    如果看到类似：

    ```Shell
    Python 3.x.x
    ```

    说明已经安装了 Python

    ---

    再检查 requests：

    ```Shell
    python3 -c "import requests; print(requests.__version__)"
    ```

    

    如果没安装：

    ```Shell
    sudo apt install -y python3-requests
    ```



#### Debian使用云音乐api:

    似乎Debian直接登录会触发风控，只需要在调用api接口时最后接上登录后获取的Cookie：

    参照[网易云音乐 NodeJS API Enhanced](https://neteasecloudmusicapienhanced.js.org/#/?id=_2-%e9%82%ae%e7%ae%b1%e7%99%bb%e5%bd%95)的Cookie部分

    ```Shell
    http://192.168.50.5:7788/user/account?cookie=MUSIC_U%3后面加获取的Cookie值
    ```

    还需要添加时间戳



## 编写Python脚本：

脚本目录新建cookie.txt文件，放入cookie;

新建api.txt，放入api地址



#### 获取日推歌曲id并保存到song_ids.txt

    ```Python
    import requests
    
    # 1. 定义读取文件的函数
    def read_file_content(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"❌ 错误：找不到文件 {filename}")
            exit()
    
    # 读取 Cookie
    cookie = read_file_content('cookie.txt')
    
    # 读取 API 基础 URL
    base_api_url = read_file_content('api.txt')
    
    # API 地址（替换成你的真实接口）
    url = f"{base_api_url}/recommend/songs?cookie=MUSIC_U%3{cookie}"
    
    # 发送请求
    response = requests.get(url)
    
    # 转为 JSON
    data = response.json()
    
    # 提取 dailySongs 列表
    songs = data.get("data", {}).get("dailySongs", [])
    
    # 存储 id
    ids = []
    
    for song in songs:
        song_id = song.get("id")
        if song_id:
            ids.append(str(song_id))
    
    # 写入 txt 文件
    with open("song_ids.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(ids))
    
    print("提取完成，已保存到 song_ids.txt")
    ```



#### 新建歌单并将id保存到playlist_id.txt

    ```Python
    import requests
    import json
    
    # 1. 定义读取文件的函数
    def read_file_content(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"❌ 错误：找不到文件 {filename}")
            exit()
    
    # 读取 Cookie
    cookie = read_file_content('cookie.txt')
    
    # 读取 API 基础 URL
    base_api_url = read_file_content('api.txt')
    
    # 2. 定义完整的 URL
    url = f"{base_api_url}/playlist/create?name=daily1&cookie=MUSIC_U%3{cookie}"
    
    print(f"正在请求创建歌单: {url}")
    
    try:
        # 2. 发送 GET 请求
        response = requests.get(url)
        
        # 检查 HTTP 状态码
        response.raise_for_status()
        
        # 3. 解析 JSON 数据
        data = response.json()
        
        # --- 修改点：直接判断根目录下的 code ---
        # 只要 code 字段存在且包含 "200"，就视为成功
        code_val = data.get('code')
        
        if code_val is not None and "200" in str(code_val):
            print("✅ 接口请求成功")
            
            # --- 修改点：直接从根目录提取 id ---
            playlist_id = data.get("id")
            
            if playlist_id:
                # 5. 保存到文件
                file_path = "playlist_id.txt"
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(playlist_id))
                    
                print(f"✅ 提取到的 ID 为: {playlist_id}")
                print(f"✅ ID 已保存至文件: {file_path}")
            else:
                print("❌ 错误：JSON 中未找到 'id' 字段")
                print("返回的完整数据:", data)
        else:
            print(f"⚠️ 接口返回异常，Code: {code_val}")
            print("返回的完整数据:", data)
    
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求错误: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析错误: {e}")
        print("返回的内容可能是:", response.text)
    ```



#### 向歌单添加歌曲

    ```Python
    import requests
    import time
    
    # 1. 读取配置文件内容
    def read_file_content(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"❌ 错误：找不到文件 {filename}")
            exit()
    
    # 读取歌单ID
    playlist_id = read_file_content('playlist_id.txt')
    
    # 读取 Cookie
    cookie = read_file_content('cookie.txt')
    
    # 读取 API 基础 URL
    base_api_url = read_file_content('api.txt')
    
    # 读取歌曲ID列表
    with open('song_ids.txt', 'r', encoding='utf-8') as f:
        song_ids = [line.strip() for line in f if line.strip()]
    
    if not song_ids:
        print("❌ 错误：song_ids.txt 是空的")
        exit()
    
    # --- 修改点：列表倒序 ---
    # 使用切片 [::-1] 将列表反转
    song_ids.reverse() 
    # ----------------------
    
    print(f"📋 目标歌单: {playlist_id}")
    print(f"🎵 待添加歌曲数量: {len(song_ids)} (倒序模式)")
    print("-" * 30)
    
    # URL 模板 (去掉了固定的 timestamp)
    base_url_template = "{api_url}/playlist/tracks?op=add&pid={pid}&tracks={track}&timestamp={ts}&cookie=MUSIC_U%3{cookie}"
    
    success_count = 0
    fail_count = 0
    
    # 2. 循环发起请求
    for i, track_id in enumerate(song_ids, 1):
        # 动态生成当前时间戳
        current_timestamp = int(time.time() * 1000)
        
        # 格式化 URL
        url = base_url_template.format(api_url=base_api_url, pid=playlist_id, track=track_id, ts=current_timestamp, cookie=cookie)
        
        print(f"[{i}/{len(song_ids)}] 正在添加歌曲: {track_id} ...", end=" ")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # --- 修改点：获取嵌套在 body 中的 code ---
            # 逻辑：先获取 body 字典，如果 body 存在，再获取其中的 code
            body_data = data.get('body')
            code_val = body_data.get('code') if body_data else None
            
            # 判断是否包含 200
            if code_val is not None and "200" in str(code_val):
                print("✅ 成功")
                success_count += 1
            else:
                print(f"⚠️ 响应异常: {data}")
                fail_count += 1
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            fail_count += 1
        
        # 暂停 0.5秒
        time.sleep(0.5)
    
    print("-" * 30)
    print(f"🏁 任务结束。成功: {success_count}, 失败: {fail_count}")
    ```



这时播放器已经可以读取每日推荐了



## 每日更新：

用1Panel的计划任务很容易就可以实现，其实就是Cronjob：

### 1.在 1Panel 中创建计划任务

1. 登录 1Panel 面板。

2. 在左侧菜单栏点击 **“计划任务”**。

3. 点击页面右上角的 **“创建计划任务”** 按钮。

### 2. 配置任务详情

在弹出的窗口中，按照以下说明填写：

|配置项|说明|示例/填写建议|
|-|-|-|
|**任务类型**|选择 **Shell 脚本**|默认通常就是 Shell 脚本|
|**任务名称**|自定义名称|例如：`删除歌单`|
|**执行周期**|设置运行时间|例如：`每天` -> `05:30`（根据需求设定）|
|**脚本内容**|**核心部分**（见下方代码）|必须使用绝对路径|

```Shell
cd /opt/1panel/www/sites/http/index/MusicPlayer/  ##脚本和播放器的目录
python3 /opt/1panel/www/sites/http/index/MusicPlayer/song_ids.py
python3 /opt/1panel/www/sites/http/index/MusicPlayer/creat_list.py
python3 /opt/1panel/www/sites/http/index/MusicPlayer/add_songs.py
```

```Shell
cd /opt/1panel/www/sites/http/index/MusicPlayer/ ##脚本和播放器的目录
python3 /root/scripts/delete_playlist.py
```

Cronjob是依次运行的。不必担心第一个没完成就执行第二个。

