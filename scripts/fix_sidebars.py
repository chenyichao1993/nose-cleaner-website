#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有页面的侧边栏
"""

import os
import re
import glob

def fix_sidebar_in_file(filepath):
    """修复文件中的侧边栏"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 读取侧边栏内容
    with open('components/sidebar.html', 'r', encoding='utf-8') as f:
        sidebar_content = f.read()
    
    # 替换空的侧边栏组件
    empty_sidebar_pattern = r'<aside class="blog-sidebar"><div id="sidebar-component"></div></aside>'
    if re.search(empty_sidebar_pattern, content):
        content = re.sub(empty_sidebar_pattern, sidebar_content, content)
        print(f"✅ 已修复侧边栏: {filepath}")
        return True
    
    # 替换其他形式的空侧边栏
    empty_sidebar_pattern2 = r'<div id="sidebar-component"></div>'
    if re.search(empty_sidebar_pattern2, content):
        content = re.sub(empty_sidebar_pattern2, sidebar_content, content)
        print(f"✅ 已修复侧边栏: {filepath}")
        return True
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    else:
        print(f"⏭️ 无需更新: {filepath}")
        return False

def main():
    """主函数"""
    print("🔧 开始修复所有页面的侧边栏...")
    
    # 获取所有HTML文件
    html_files = glob.glob('blog/**/*.html', recursive=True)
    updated_count = 0
    
    for filepath in html_files:
        if 'blog/_layouts' in filepath:  # 跳过布局文件
            continue
        if fix_sidebar_in_file(filepath):
            updated_count += 1
    
    print(f"\n🎉 完成！共更新了 {updated_count} 个文件")

if __name__ == "__main__":
    main()
