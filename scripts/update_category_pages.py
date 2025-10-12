#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新所有分类页面的文章卡片样式和背景色
"""

import os
import re
import glob

def update_category_page(filepath):
    """更新分类页面"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. 添加灰色背景
    if '<body>' in content and 'background-color' not in content:
        content = content.replace('<body>', '<body style="background-color: #f5f5f5;">')
    
    # 2. 将所有 blog-post 改为 featured-post 样式
    # 替换 class="blog-post" 为 class="featured-post"
    content = re.sub(r'class="blog-post"', 'class="featured-post"', content)
    
    # 3. 替换 post-image 为 featured-post-image
    content = re.sub(r'class="post-image"', 'class="featured-post-image"', content)
    
    # 4. 替换 post-content 为 featured-post-content
    content = re.sub(r'class="post-content"', 'class="featured-post-content"', content)
    
    # 5. 将 h3 改为 h2（保持标题层级一致）
    content = re.sub(r'<h3><a href="([^"]+)">([^<]+)</a></h3>', r'<h2><a href="\1">\2</a></h2>', content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已更新: {filepath}")
        return True
    else:
        print(f"⏭️ 无需更新: {filepath}")
        return False

def main():
    """主函数"""
    print("🔄 开始更新所有分类页面...")
    
    # 获取所有分类页面
    category_files = glob.glob('blog/category/**/index.html', recursive=True)
    updated_count = 0
    
    for filepath in category_files:
        if update_category_page(filepath):
            updated_count += 1
    
    print(f"\n🎉 完成！共更新了 {updated_count} 个分类页面")

if __name__ == "__main__":
    main()
