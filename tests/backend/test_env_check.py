"""检查环境变量"""
import os
from dotenv import load_dotenv

# 不加载.env，检查系统环境变量
print("=== 系统环境变量 ===")
print(f"DIFY_API_BASE_URL (系统): {os.getenv('DIFY_API_BASE_URL')}")
print(f"DIFY_API_KEY (系统): {os.getenv('DIFY_API_KEY')}")

# 加载.env后检查
print("\n=== 加载.env后 ===")
load_dotenv()
print(f"DIFY_API_BASE_URL (.env): {os.getenv('DIFY_API_BASE_URL')}")
print(f"DIFY_API_KEY (.env): {os.getenv('DIFY_API_KEY')[:20] if os.getenv('DIFY_API_KEY') else 'None'}...")

# 检查.env文件内容
print("\n=== .env文件内容（DIFY相关） ===")
try:
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            if 'DIFY' in line and not line.strip().startswith('#'):
                print(line.rstrip())
except Exception as e:
    print(f"读取.env失败: {e}")
