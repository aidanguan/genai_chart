#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试后端 SVG 转换功能
"""

import sys
sys.path.insert(0, 'backend')

from app.services.export_service import ExportService

# 测试 SVG（包含 foreignObject）
test_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
  <defs id="icon-defs"/>
  <g id="infographic-container">
    <!-- 测试 foreignObject + span -->
    <foreignObject x="100" y="50" width="600" height="40" overflow="visible">
      <span xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(38, 38, 38); font-size: 24px; font-weight: bold; text-align: center; justify-content: center; align-items: flex-start; width: 100%; height: 100%; display: flex;">
        测试标题文本
      </span>
    </foreignObject>
    
    <foreignObject x="100" y="120" width="600" height="30" overflow="visible">
      <span xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(90, 90, 90); font-size: 16px; text-align: left; justify-content: flex-start; align-items: flex-start; width: 100%; height: 100%; display: flex;">
        这是一段描述文本
      </span>
    </foreignObject>
    
    <!-- SVG 图形不受影响 -->
    <circle cx="400" cy="300" r="50" fill="#1783FF"/>
  </g>
</svg>"""

def test_conversion():
    """测试 SVG 转换"""
    service = ExportService()
    
    print("=" * 60)
    print("🧪 测试后端 SVG 转换功能")
    print("=" * 60)
    print()
    
    print("📄 原始 SVG:")
    print("-" * 60)
    print(test_svg[:500] + "..." if len(test_svg) > 500 else test_svg)
    print("-" * 60)
    print()
    
    # 转换 SVG
    print("🔄 开始转换...")
    converted_svg = service._convert_svg_for_ppt(test_svg)
    print()
    
    print("✅ 转换完成！")
    print()
    
    print("📄 转换后的 SVG:")
    print("-" * 60)
    print(converted_svg)
    print("-" * 60)
    print()
    
    # 分析结果
    print("🔍 转换分析:")
    print("-" * 60)
    
    has_foreign_before = test_svg.count('foreignObject')
    has_foreign_after = converted_svg.count('foreignObject')
    has_text_after = converted_svg.count('<text')
    
    print(f"转换前 foreignObject 数量: {has_foreign_before}")
    print(f"转换后 foreignObject 数量: {has_foreign_after}")
    print(f"转换后 <text> 数量: {has_text_after}")
    print()
    
    if has_foreign_after == 0 and has_text_after > 0:
        print("🎉 转换成功！所有 foreignObject 都已转换为 <text>")
    elif has_foreign_after < has_foreign_before:
        print(f"⚠️  部分转换成功，还剩 {has_foreign_after} 个 foreignObject")
    else:
        print("❌ 转换失败，foreignObject 数量未减少")
    
    print("-" * 60)
    print()
    
    # 保存转换结果
    output_file = "test_converted_svg.svg"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(converted_svg)
    
    print(f"💾 转换结果已保存到: {output_file}")
    print()
    print("✅ 您可以：")
    print("   1. 用浏览器打开该文件验证渲染")
    print("   2. 拖入 PowerPoint 测试文本显示")
    print("   3. 用 verify_svg_ppt_compatibility.py 验证兼容性")
    print()

if __name__ == '__main__':
    test_conversion()
