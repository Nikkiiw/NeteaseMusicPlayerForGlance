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