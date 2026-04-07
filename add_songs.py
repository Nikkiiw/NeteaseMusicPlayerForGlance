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