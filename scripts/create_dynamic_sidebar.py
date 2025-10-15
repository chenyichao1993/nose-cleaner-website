#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建动态侧边栏系统 - 一次性解决分类计数问题
"""

import os
import json
import re
import glob

def load_articles_data():
    """加载文章数据"""
    with open('data/articles.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_sidebar_html(articles_data):
    """生成动态侧边栏HTML"""
    categories_html = ""
    for category_name, category_data in articles_data['categories'].items():
        categories_html += f'            <li><a href="{category_data["url"]}">{category_name} <span>({category_data["count"]})</span></a></li>\n'
    
    sidebar_html = f'''    <!-- Categories Widget -->
    <div class="sidebar-widget">
        <h3>Categories</h3>
        <ul class="category-list">
{categories_html.rstrip()}
        </ul>
    </div>
    
    <!-- Newsletter Widget -->
    <div class="sidebar-widget newsletter-widget">
        <h3>Stay Updated</h3>
        <p>Get the latest nasal health tips and product reviews delivered to your inbox.</p>
        <form class="newsletter-form">
            <input type="email" placeholder="Enter your email address" required 
                   title="Please enter a valid email address"
                   oninvalid="this.setCustomValidity('Please enter a valid email address')"
                   oninput="this.setCustomValidity('')">
            <button type="submit" class="btn btn-primary">Subscribe</button>
        </form>
    </div>'''
    
    return sidebar_html

def update_sidebar_in_file(file_path, new_sidebar_html):
    """更新文件中的侧边栏内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找侧边栏区域并替换
        # 匹配从 <!-- Categories Widget --> 开始到 </aside> 结束的整个侧边栏
        pattern = r'<!-- Categories Widget -->.*?</aside>'
        new_content = re.sub(pattern, new_sidebar_html, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
        
    except Exception as e:
        print(f"处理 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("正在创建动态侧边栏系统...")
    
    # 加载文章数据
    articles_data = load_articles_data()
    
    # 生成新的侧边栏HTML
    new_sidebar_html = generate_sidebar_html(articles_data)
    
    # 需要更新的文件列表
    files_to_update = [
        'blog/index.html',
        'blog/category/baby-care/index.html',
        'blog/category/adult-care/index.html',
        'blog/category/product-reviews/index.html',
        'blog/category/safety-tips/index.html',
        'blog/adult-nasal-irrigation-complete-guide/index.html',
        'blog/baby-nasal-congestion-remedies/index.html',
        'blog/best-way-to-clean-your-nose/index.html',
        'blog/complete-guide-baby-nasal-care/index.html',
        'blog/electric-vs-manual-nasal-aspirators/index.html',
        'blog/nasal-irrigation-safety-mistakes/index.html',
        'blog/navage-vs-neilmed-detailed-comparison/index.html',
        'blog/salt-water-nose-rinse-safety-guide/index.html',
        'blog/nasal-irrigation-frequency-guide/index.html'
    ]
    
    success_count = 0
    total_count = 0
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            total_count += 1
            if update_sidebar_in_file(file_path, new_sidebar_html):
                print(f"已更新 {file_path}")
                success_count += 1
            else:
                print(f"无需更新 {file_path}")
        else:
            print(f"文件不存在: {file_path}")
    
    print(f"\n动态侧边栏系统创建完成!")
    print(f"处理统计: {success_count}/{total_count} 个文件成功更新")
    print(f"分类数据来源: data/articles.json")
    print(f"以后添加新文章时，只需更新 data/articles.json，然后运行此脚本即可")

if __name__ == "__main__":
    main()
