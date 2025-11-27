#!/usr/bin/env python3
"""分析SVG中的文本结构"""

from xml.etree import ElementTree as ET
import json

svg_sample = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 243" width="800px" height="500px" style="">
<foreignObject x="0" y="0" width="720" height="32" overflow="visible" data-element-type="title" data-text-alignment="CENTER TOP">
<span xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(38, 38, 38); overflow: visible; font-size: 24px; line-height: 1.4; width: 100%; height: 100%; display: flex; flex-wrap: wrap; word-break: break-word; text-align: center; place-content: flex-start center; align-items: flex-start;">简单的三步流程</span>
</foreignObject>
<text data-element-type="text" y="17.6" fill="#1783ff" font-size="20" text-anchor="start" dominant-baseline="baseline" data-text-alignment="LEFT TOP" width="0" height="0" font-weight="bold" style="user-select: none; pointer-events: none;">01</text>
<foreignObject x="28" y="0" width="160" height="23" overflow="visible" data-element-type="item-label" data-x="28" data-text-alignment="LEFT TOP" data-indexes="0">
<span xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(90, 90, 90); overflow: visible; font-weight: bold; font-size: 16px; line-height: 1.4; width: 100%; height: 100%; display: flex; flex-wrap: wrap; word-break: break-word; text-align: left; place-content: flex-start; align-items: flex-start;">第一步：准备</span>
</foreignObject>
</svg>"""

def extract_all_texts(element, parent_x=0, parent_y=0):
    """递归提取所有文本元素（text和foreignObject）"""
    texts = []
    tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
    
    # 处理 text 元素
    if tag == 'text':
        text_content = element.text or ''
        for child in element:
            if child.text:
                text_content += child.text
            if child.tail:
                text_content += child.tail
        
        if text_content.strip():
            texts.append({
                'type': 'text',
                'tag': tag,
                'text': text_content.strip(),
                'x': float(element.get('x', parent_x)),
                'y': float(element.get('y', parent_y)),
                'font_size': element.get('font-size', '14'),
                'fill': element.get('fill', 'black'),
                'font_weight': element.get('font-weight', ''),
                'element_type': element.get('data-element-type', '')
            })
    
    # 处理 foreignObject 元素
    elif tag == 'foreignObject':
        x = float(element.get('x', parent_x))
        y = float(element.get('y', parent_y))
        
        # 查找 span 子元素
        for span in element:
            span_tag = span.tag.split('}')[-1] if '}' in span.tag else span.tag
            if span_tag == 'span':
                text_content = span.text or ''
                
                # 解析 style 属性
                style = span.get('style', '')
                font_size = '14'
                color = 'black'
                font_weight = ''
                
                if 'font-size:' in style:
                    import re
                    match = re.search(r'font-size:\s*(\d+)px', style)
                    if match:
                        font_size = match.group(1)
                
                if 'color:' in style:
                    import re
                    match = re.search(r'color:\s*([^;]+);', style)
                    if match:
                        color = match.group(1).strip()
                
                if 'font-weight:' in style:
                    import re
                    match = re.search(r'font-weight:\s*([^;]+);', style)
                    if match:
                        font_weight = match.group(1).strip()
                
                if text_content.strip():
                    texts.append({
                        'type': 'foreignObject',
                        'tag': 'foreignObject->span',
                        'text': text_content.strip(),
                        'x': x,
                        'y': y,
                        'width': float(element.get('width', '0')),
                        'height': float(element.get('height', '0')),
                        'font_size': font_size,
                        'fill': color,
                        'font_weight': font_weight,
                        'element_type': element.get('data-element-type', '')
                    })
    
    # 递归处理子元素
    for child in element:
        texts.extend(extract_all_texts(child, parent_x, parent_y))
    
    return texts

# 解析SVG
root = ET.fromstring(svg_sample)
all_texts = extract_all_texts(root)

print("找到的文本元素：")
for i, text_info in enumerate(all_texts):
    print(f"\n文本 #{i+1}:")
    print(json.dumps(text_info, indent=2, ensure_ascii=False))
