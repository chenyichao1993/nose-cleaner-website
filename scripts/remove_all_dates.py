#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除所有页面的日期
"""

import os
import re
import glob

def remove_dates_from_file(filepath):
    """从文件中删除所有日期"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 删除各种日期格式
    date_patterns = [
        r'<span class="post-date">[^<]*</span>',
        r'<span class="article-date">[^<]*</span>',
        r'<span class="date">[^<]*</span>',
        r'<span class="meta-date">[^<]*</span>',
        r'<time[^>]*>[^<]*</time>',
        r'<span[^>]*class="[^"]*date[^"]*"[^>]*>[^<]*</span>',
        # 删除Recent Posts中的日期
        r'<span>[^<]*(?:January|February|March|April|May|June|July|August|September|October|November|December)[^<]*</span>',
        # 删除任何包含日期的span
        r'<span>[^<]*(?:2024|2025)[^<]*</span>',
    ]
    
    for pattern in date_patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # 清理多余的空行
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已删除日期: {filepath}")
        return True
    else:
        print(f"⏭️ 无需更新: {filepath}")
        return False

def main():
    """主函数"""
    print("🗑️ 开始删除所有页面的日期...")
    
    # 获取所有HTML文件
    html_files = glob.glob('blog/**/*.html', recursive=True)
    updated_count = 0
    
    for filepath in html_files:
        if 'blog/_layouts' in filepath:  # 跳过布局文件
            continue
        if remove_dates_from_file(filepath):
            updated_count += 1
    
    print(f"\n🎉 完成！共更新了 {updated_count} 个文件")

if __name__ == "__main__":
    main()
