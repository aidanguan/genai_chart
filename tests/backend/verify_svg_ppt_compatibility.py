#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG PowerPoint 兼容性检查工具

用法：
    python verify_svg_ppt_compatibility.py <svg_file_path>
    
示例：
    python verify_svg_ppt_compatibility.py infographic_1234567890.svg
"""

import sys
import re
from pathlib import Path


def analyze_svg_file(svg_path):
    """分析 SVG 文件的 PPT 兼容性"""
    
    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
    except FileNotFoundError:
        print(f"❌ 错误: 文件不存在 '{svg_path}'")
        return False
    except Exception as e:
        print(f"❌ 错误: 无法读取文件 - {e}")
        return False
    
    print("=" * 60)
    print(f"📄 分析文件: {svg_path}")
    print("=" * 60)
    print()
    
    # 检查 foreignObject
    foreign_objects = re.findall(r'<foreignObject[^>]*>', svg_content)
    has_foreign_object = len(foreign_objects) > 0
    
    # 检查 span
    spans = re.findall(r'<span[^>]*>', svg_content)
    has_span = len(spans) > 0
    
    # 检查 text 元素
    text_elements = re.findall(r'<text[^>]*>([^<]+)</text>', svg_content)
    has_text = len(text_elements) > 0
    
    # 提取所有文本内容
    all_texts = []
    
    # 从 text 元素提取
    for text in text_elements:
        cleaned = text.strip()
        if cleaned:
            all_texts.append(('text', cleaned))
    
    # 从 foreignObject/span 提取（如果有）
    if has_foreign_object:
        foreign_texts = re.findall(r'<foreignObject[^>]*>.*?<span[^>]*>([^<]+)</span>.*?</foreignObject>', 
                                   svg_content, re.DOTALL)
        for text in foreign_texts:
            cleaned = text.strip()
            if cleaned:
                all_texts.append(('foreignObject/span', cleaned))
    
    # 显示分析结果
    print("🔍 元素统计:")
    print(f"   - <foreignObject> 元素: {len(foreign_objects)}")
    print(f"   - <span> 元素: {len(spans)}")
    print(f"   - <text> 元素: {len(text_elements)}")
    print()
    
    # 兼容性判断
    is_compatible = True
    
    if has_foreign_object:
        print("❌ 检测到 foreignObject 元素")
        print("   PowerPoint 不支持 foreignObject，文本可能无法显示")
        is_compatible = False
    else:
        print("✅ 未检测到 foreignObject 元素")
    
    print()
    
    if has_span:
        print("⚠️  检测到 HTML <span> 元素")
        print("   PowerPoint 不支持 HTML 元素")
        is_compatible = False
    else:
        print("✅ 未检测到 HTML span 元素")
    
    print()
    
    if has_text:
        print(f"✅ 检测到 {len(text_elements)} 个标准 SVG <text> 元素")
    else:
        print("❌ 未检测到 <text> 元素")
        print("   SVG 中可能没有文本内容")
        is_compatible = False
    
    print()
    print("=" * 60)
    
    if is_compatible:
        print("🎉 兼容性检查：通过")
        print("   此 SVG 文件与 PowerPoint 完全兼容")
    else:
        print("⚠️  兼容性检查：失败")
        print("   此 SVG 文件在 PowerPoint 中可能无法正确显示文本")
    
    print("=" * 60)
    
    # 显示文本内容
    if all_texts:
        print()
        print("📝 提取的文本内容:")
        print("-" * 60)
        for idx, (source, text) in enumerate(all_texts, 1):
            print(f"  {idx}. [{source}] {text}")
        print("-" * 60)
    
    print()
    
    # 建议
    if not is_compatible:
        print("💡 修复建议:")
        print("   1. 确保使用最新版本的 @antv/infographic 库")
        print("   2. 重新编译库: cd antv_infographic/infographic && npm run build")
        print("   3. 重新生成并导出 SVG")
        print("   4. 如果问题仍然存在，请检查 exportToSVG 函数是否正确调用了")
        print("      convertForeignObjectsToText")
        print()
    else:
        print("✅ 可以安全地将此 SVG 文件拖入 PowerPoint 使用")
        print()
    
    return is_compatible


def main():
    if len(sys.argv) < 2:
        print("用法: python verify_svg_ppt_compatibility.py <svg_file_path>")
        print()
        print("示例:")
        print("  python verify_svg_ppt_compatibility.py infographic_1234567890.svg")
        sys.exit(1)
    
    svg_path = sys.argv[1]
    
    # 支持通配符
    if '*' in svg_path or '?' in svg_path:
        import glob
        files = glob.glob(svg_path)
        if not files:
            print(f"❌ 未找到匹配的文件: {svg_path}")
            sys.exit(1)
        
        print(f"找到 {len(files)} 个文件:\n")
        
        results = []
        for file in files:
            result = analyze_svg_file(file)
            results.append((file, result))
            print()
        
        # 总结
        print("=" * 60)
        print("📊 批量检查总结")
        print("=" * 60)
        compatible_count = sum(1 for _, r in results if r)
        print(f"总文件数: {len(results)}")
        print(f"兼容: {compatible_count}")
        print(f"不兼容: {len(results) - compatible_count}")
        print("=" * 60)
        
    else:
        analyze_svg_file(svg_path)


if __name__ == '__main__':
    main()
