# NetEase Music Daily Recommend Player for Glance

这是一个基于 [NeteaseMiniPlayer](https://github.com/numakkiyu/NeteaseMiniPlayer) 开发的工具，专门用于在 Glance 仪表板中通过 iFrame 嵌入。它能够自动获取网易云音乐的每日推荐歌曲，并将其更新到一个指定的歌单中，实现仪表板上的每日音乐自动更新。

## 🌟 主要功能

- **自动化歌单管理**：每日自动删除旧歌单、创建新歌单。
- **每日推荐同步**：自动从网易云音乐 API 获取每日推荐歌曲并同步。
- **Glance 仪表板优化**：深色模式适配，隐藏滚动条，专为 Glance 仪表板设计。
- **VIP 歌曲支持**：通过注入 Cookie 支持播放完整版的 VIP 歌曲。

## 🛠️ 环境准备

### 1. 自建网易云 API
你需要部署一个网易云音乐 API 服务。推荐使用 Docker 部署：

```yaml
services:
  NeteaseCloudMusicApi:
    image: moefurina/ncm-api:latest
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

### 2. Python 环境
确保系统中安装了 Python 3 和 `requests` 库：

```bash
# 检查 Python 版本
python3 --version

# 安装 requests 库 (Debian/Ubuntu)
sudo apt install -y python3-requests
```

## ⚙️ 配置说明

在使用脚本之前，请确保以下配置文件在项目根目录下：

- **api.txt**: 存放你的 API 基础 URL（例如：`http://localhost:7788`）。
- **cookie.txt**: 存放你的网易云音乐 `MUSIC_U` Cookie。
- **playlist_id.txt**: 存放当前生成的歌单 ID（由脚本自动维护）。

### 获取 Cookie 方法：
1. 访问 API 的登录接口（如 `/login/cellphone`）。
2. 登录成功后，在浏览器开发者工具中查看 `MUSIC_U` 的 Cookie 值并保存到 `cookie.txt`。

## 🚀 使用说明

### 脚本执行流程
建议按以下顺序运行脚本：

1. `del_list.py`: 删除旧的每日歌单。（这是在你网易云中创建的临时歌单）
2. `creat_list.py`: 创建新的 "daily" 歌单，并更新 `playlist_id.txt`。
3. `song_ids.py`: 获取今日推荐歌曲 ID。
4. `add_songs.py`: 将获取到的歌曲添加到新歌单中。

### Web 端集成 (Glance)
将 `netmusic.html` 作为 iFrame 嵌入到 Glance 仪表板中。

```html
<!-- Glance 配置文件示例 -->
- type: iframe
  url: http://your-server-ip/netmusic.html
  height: 400px
```

## ⏰ 自动化部署

你可以使用 Shell 脚本配合 Cron 任务实现每日自动更新：

```bash
#!/bin/bash
# update_daily_music.sh
cd /path/to/MusicPlayer
python3 del_list.py
python3 creat_list.py
python3 song_ids.py
python3 add_songs.py
```

在 Crontab 中添加任务（例如每天凌晨 6 点更新）也可以在1Panel灯面板中配置计划任务：
```bash
0 6 * * * /bin/bash /path/to/MusicPlayer/update_daily_music.sh
```

## 🔧 进阶修改

### 播放器优化
- **滚动条隐藏**: 已在 `netmusic.html` 中通过 CSS 强制隐藏。
- **播放列表自动滚动修复**: 建议在 `netease-mini-player-v2.js` 中注释掉 `activeItem.scrollIntoView(...)` 相关代码（约 1003 行），以防止 Glance 加载时页面跳动。

## 📄 开源参考
- [NeteaseMiniPlayer](https://github.com/numakkiyu/NeteaseMiniPlayer)
- [NetEaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)



