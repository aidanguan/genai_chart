#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试PPTX导出中文字体"""

from app.services.export_service import get_export_service

# 简单的SVG，包含中文文本
svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <rect width="800" height="600" fill="#f0f0f0"/>
  <circle cx="400" cy="300" r="150" fill="#4CAF50"/>
  <text x="400" y="300" font-family="Noto Sans CJK SC" font-size="48" fill="white" text-anchor="middle" dominant-baseline="middle">中文测试</text>
  <text x="400" y="360" font-family="Noto Sans CJK SC" font-size="24" fill="#333" text-anchor="middle">这是一个圆形</text>
</svg>'''

try:
    service = get_export_service()
    result = service.export_pptx(svg_content, title="中文字体测试", filename="test_chinese.pptx")
    print(f"✅ PPTX 导出成功!")
    print(f"   文件: {result['filename']}")
    print(f"   路径: {result['filepath']}")
    print(f"   大小: {result['size']} bytes")
    print(f"\n请打开文件检查中文是否正常显示")
except Exception as e:
    print(f"❌ PPTX 导出失败: {e}")
    import traceback
    traceback.print_exc()
