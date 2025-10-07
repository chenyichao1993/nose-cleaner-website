#!/usr/bin/env python3
"""
自动为所有HTML页面添加favicon代码的脚本
使用方法: python add_favicon.py
"""

import os
import re
import glob
from pathlib import Path

# Favicon代码模板
FAVICON_CODE = '''    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
    <link rel="icon" type="image/png" sizes="48x48" href="favicon-48.png">
    <link rel="icon" type="image/png" sizes="64x64" href="favicon-64.png">
    <link rel="icon" type="image/png" sizes="128x128" href="favicon-128.png">
    <link rel="icon" type="image/png" sizes="256x256" href="favicon-256.png">
    <link rel="apple-touch-icon" href="apple-touch-icon.png">'''

def check_favicon_exists(html_content):
    """检查HTML内容是否已经包含favicon代码"""
    # 检查是否已经有favicon相关的链接
    favicon_patterns = [
        r'<link[^>]*rel=["\']icon["\'][^>]*>',
        r'<link[^>]*rel=["\']apple-touch-icon["\'][^>]*>',
        r'<link[^>]*href=["\']favicon\.ico["\'][^>]*>'
    ]
    
    for pattern in favicon_patterns:
        if re.search(pattern, html_content, re.IGNORECASE):
            return True
    return False

def find_insertion_point(html_content):
    """找到插入favicon代码的最佳位置"""
    lines = html_content.split('\n')
    
    # 寻找canonical链接之后的位置
    for i, line in enumerate(lines):
        if '<link rel="canonical"' in line:
            return i + 1
    
    # 如果没有canonical链接，寻找stylesheet之后的位置
    for i, line in enumerate(lines):
        if '<link rel="stylesheet"' in line:
            return i + 1
    
    # 如果都没有，在head标签内寻找合适位置
    for i, line in enumerate(lines):
        if '<head>' in line:
            return i + 1
    
    return 0

def add_favicon_to_file(file_path):
    """为单个HTML文件添加favicon代码"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有favicon
        if check_favicon_exists(content):
            print(f"⏭️  {file_path} - 已有favicon，跳过")
            return "skipped"
        
        # 找到插入位置
        lines = content.split('\n')
        insert_pos = find_insertion_point(content)
        
        # 插入favicon代码
        favicon_lines = FAVICON_CODE.split('\n')
        for i, favicon_line in enumerate(favicon_lines):
            lines.insert(insert_pos + i, favicon_line)
        
        # 写回文件
        new_content = '\n'.join(lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ {file_path} - 已添加favicon")
        return "added"
        
    except Exception as e:
        print(f"❌ {file_path} - 处理失败: {e}")
        return "failed"

def main():
    """主函数"""
    print("🚀 开始自动添加favicon...")
    print("=" * 50)
    
    # 查找所有HTML文件
    html_files = glob.glob("*.html")
    
    if not html_files:
        print("❌ 未找到HTML文件")
        return
    
    print(f"📁 找到 {len(html_files)} 个HTML文件:")
    for file in html_files:
        print(f"   - {file}")
    print()
    
    # 统计结果
    processed = 0
    skipped = 0
    failed = 0
    
    # 处理每个HTML文件
    for html_file in html_files:
        result = add_favicon_to_file(html_file)
        if result == "added":
            processed += 1
        elif result == "skipped":
            skipped += 1
        else:
            failed += 1
    
    print()
    print("=" * 50)
    print("📊 处理结果:")
    print(f"   ✅ 已添加favicon: {processed} 个文件")
    print(f"   ⏭️  已有favicon: {skipped} 个文件")
    print(f"   ❌ 处理失败: {failed} 个文件")
    
    if processed > 0:
        print()
        print("🎉 完成！请检查修改后的文件，然后提交到Git。")
        print("💡 提示: 以后添加新页面后，只需运行此脚本即可自动添加favicon。")

if __name__ == "__main__":
    main()
