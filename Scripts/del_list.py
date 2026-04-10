import requests
import json
import time

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

# 2. 读取要删除的歌单 ID
file_path = "playlist_id.txt"
playlist_id = read_file_content(file_path)

if not playlist_id:
    print("❌ 错误：playlist_id.txt 文件为空")
    exit()

print(f"📋 准备删除歌单 ID: {playlist_id}")

# 3. 动态生成时间戳
timestamp = int(time.time() * 1000)

# 4. 定义完整的 URL (填入 ID 和时间戳)
url = f"{base_api_url}/playlist/delete?id={playlist_id}&timestamp={timestamp}&cookie=MUSIC_U%3{cookie}"

print(f"正在发送删除请求...")

try:
    # 4. 发送 GET 请求
    response = requests.get(url)
    
    # 检查 HTTP 状态码
    response.raise_for_status()
    
    # 5. 解析 JSON 数据
    data = response.json()
    
    # 6. 判断结果 (检查根目录下的 code)
    code_val = data.get('code')
    
    if code_val is not None and "200" in str(code_val):
        print("✅ 歌单删除成功！")
    else:
        print(f"⚠️ 删除操作返回异常: {data}")

except requests.exceptions.RequestException as e:
    print(f"❌ 网络请求错误: {e}")
except json.JSONDecodeError as e:
    print(f"❌ JSON 解析错误: {e}")
    print("返回的内容可能是:", response.text)