#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同步所有页面的侧边栏数据，确保都引用 data/articles.json
"""

import os
import json
import re
import glob

def load_article_data():
    """加载文章数据"""
    with open('data/articles.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def update_sidebar_in_file(filepath, article_data):
    """更新文件中的侧边栏数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 更新分类数量
    for category, data in article_data['categories'].items():
        # 匹配各种可能的格式
        patterns = [
            f'{category} <span>\\(\\d+\\)</span>',
            f'{category} <span>\\([0-9]+\\)</span>',
            f'{category}.*<span>\\(\\d+\\)</span>',
        ]
        
        for pattern in patterns:
            replacement = f'{category} <span>({data["count"]})</span>'
            content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已更新侧边栏数据: {filepath}")
        return True
    else:
        print(f"⏭️ 无需更新: {filepath}")
        return False

def main():
    """主函数"""
    print("🔄 开始同步所有页面的侧边栏数据...")
    
    # 加载文章数据
    article_data = load_article_data()
    print(f"📊 正确的分类数量:")
    for category, data in article_data['categories'].items():
        print(f"  {category}: {data['count']} 篇")
    
    # 获取所有HTML文件
    html_files = glob.glob('blog/**/*.html', recursive=True)
    updated_count = 0
    
    for filepath in html_files:
        if 'blog/_layouts' in filepath:  # 跳过布局文件
            continue
        if update_sidebar_in_file(filepath, article_data):
            updated_count += 1
    
    print(f"\n🎉 完成！共更新了 {updated_count} 个文件")

if __name__ == "__main__":
    main()
