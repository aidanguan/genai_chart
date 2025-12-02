import requests
import json

url = "http://localhost:8000/api/v1/generate/extract"

payload = {
    "text": "方案1的优势是成本低、实施快,劣势是功能有限。方案2的优势是功能强大、扩展性好,劣势是成本高、周期长。",
    "templateId": "compare-hierarchy-left-right",
    "llmProvider": "system"
}

print("发送请求...")
response = requests.post(url, json=payload)

print(f"状态码: {response.status_code}")
data = response.json()

print("\n生成的配置:")
config = data['data']['config']
print(json.dumps(config, ensure_ascii=False, indent=2))

print("\n\n数据检查:")
items = config['data']['items']
print(f"Items数量: {len(items)}")
for i, item in enumerate(items):
    print(f"\nItem {i+1}:")
    print(f"  label: {item['label']}")
    print(f"  children数量: {len(item.get('children', []))}")
    for j, child in enumerate(item.get('children', [])):
        print(f"    Child {j+1}: label='{child['label']}', desc='{child.get('desc', '')}'")
