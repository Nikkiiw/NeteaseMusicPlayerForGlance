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
url = f"{base_api_url}/playlist/create?name=daily&cookie=MUSIC_U%3{cookie}"

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