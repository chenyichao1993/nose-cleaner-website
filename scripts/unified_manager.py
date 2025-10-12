#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一网站管理脚本 - 一个脚本搞定所有事情
"""

import os
import json
import re
import glob
from datetime import datetime

def load_article_data():
    """加载文章数据"""
    with open('data/articles.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def update_components(article_data):
    """更新所有组件文件"""
    print("🔄 更新组件文件...")
    
    # 更新Categories组件
    categories_html = """<!-- Categories Widget -->
<div class="sidebar-widget">
    <h3>Categories</h3>
    <ul class="category-list" id="categories-list">"""
    
    for category, data in article_data['categories'].items():
        categories_html += f'\n        <li><a href="{data["url"]}">{category} <span>({data["count"]})</span></a></li>'
    
    categories_html += """
    </ul>
</div>"""
    
    with open('components/categories.html', 'w', encoding='utf-8') as f:
        f.write(categories_html)
    print("✅ 已更新 Categories 组件")
    
    # 更新Recent Posts组件
    recent_posts = sorted(article_data['articles'], key=lambda x: x['date'], reverse=True)[:5]
    recent_posts_html = """<!-- Recent Posts Widget -->
<div class="sidebar-widget">
    <h3>Recent Posts</h3>
    <ul class="recent-posts" id="recent-posts-list">"""
    
    for post in recent_posts:
        recent_posts_html += f"""
        <li>
            <a href="{post['url']}">
                <img src="/images/responsive/{post['image']['mobile']}" alt="{post['shortTitle']}" width="60" height="60">
                <div>
                    <h4>{post['shortTitle']}</h4>
                </div>
            </a>
        </li>"""
    
    recent_posts_html += """
    </ul>
</div>"""
    
    with open('components/recent-posts.html', 'w', encoding='utf-8') as f:
        f.write(recent_posts_html)
    print("✅ 已更新 Recent Posts 组件")
    
    # 更新完整侧边栏组件
    sidebar_html = f"""<!-- Sidebar -->
<aside class="blog-sidebar">
    <!-- Categories Widget -->
    <div class="sidebar-widget">
        <h3>Categories</h3>
        <ul class="category-list">
"""
    
    for category, data in article_data['categories'].items():
        sidebar_html += f'            <li><a href="{data["url"]}">{category} <span>({data["count"]})</span></a></li>\n'
    
    sidebar_html += """        </ul>
    </div>
    
    <!-- Recent Posts Widget -->
    <div class="sidebar-widget">
        <h3>Recent Posts</h3>
        <ul class="recent-posts">"""
    
    for post in recent_posts:
        sidebar_html += f"""
            <li>
                <a href="{post['url']}">
                    <img src="/images/responsive/{post['image']['mobile']}" alt="{post['shortTitle']}" width="60" height="60">
                    <div>
                        <h4>{post['shortTitle']}</h4>
                    </div>
                </a>
            </li>"""
    
    sidebar_html += """
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
    </div>
</aside>"""
    
    with open('components/sidebar.html', 'w', encoding='utf-8') as f:
        f.write(sidebar_html)
    print("✅ 已更新完整侧边栏组件")

def remove_all_dates():
    """删除所有页面的日期"""
    print("🗑️ 删除所有页面的日期...")
    
    html_files = glob.glob('blog/**/*.html', recursive=True)
    updated_count = 0
    
    for filepath in html_files:
        if 'blog/_layouts' in filepath:
            continue
            
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
            r'<span>[^<]*(?:January|February|March|April|May|June|July|August|September|October|November|December)[^<]*</span>',
            r'<span>[^<]*(?:2024|2025)[^<]*</span>',
        ]
        
        for pattern in date_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        # 清理多余的空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1
    
    print(f"✅ 已删除 {updated_count} 个文件的日期")

def fix_all_sidebars():
    """修复所有页面的侧边栏"""
    print("🔧 修复所有页面的侧边栏...")
    
    # 读取侧边栏内容
    with open('components/sidebar.html', 'r', encoding='utf-8') as f:
        sidebar_content = f.read()
    
    html_files = glob.glob('blog/**/*.html', recursive=True)
    updated_count = 0
    
    for filepath in html_files:
        if 'blog/_layouts' in filepath:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 替换空的侧边栏组件
        empty_sidebar_pattern = r'<aside class="blog-sidebar"><div id="sidebar-component"></div></aside>'
        if re.search(empty_sidebar_pattern, content):
            content = re.sub(empty_sidebar_pattern, sidebar_content, content)
            updated_count += 1
        
        # 替换其他形式的空侧边栏
        empty_sidebar_pattern2 = r'<div id="sidebar-component"></div>'
        if re.search(empty_sidebar_pattern2, content):
            content = re.sub(empty_sidebar_pattern2, sidebar_content, content)
            updated_count += 1
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print(f"✅ 已修复 {updated_count} 个文件的侧边栏")

def sync_sidebar_data(article_data):
    """同步所有页面的侧边栏数据"""
    print("🔄 同步所有页面的侧边栏数据...")
    
    html_files = glob.glob('blog/**/*.html', recursive=True)
    updated_count = 0
    
    for filepath in html_files:
        if 'blog/_layouts' in filepath:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 更新分类数量
        for category, data in article_data['categories'].items():
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
            updated_count += 1
    
    print(f"✅ 已同步 {updated_count} 个文件的侧边栏数据")

def add_new_article():
    """添加新文章"""
    print("\n📝 添加新文章")
    
    title = input("文章标题: ").strip()
    if not title:
        print("❌ 标题不能为空")
        return
    
    short_title = input("短标题 (用于Recent Posts): ").strip()
    if not short_title:
        short_title = title[:50] + "..." if len(title) > 50 else title
    
    category = input("分类 (Baby Care/Adult Care/Product Reviews/Safety Tips): ").strip()
    if category not in ['Baby Care', 'Adult Care', 'Product Reviews', 'Safety Tips']:
        print("❌ 无效的分类")
        return
    
    excerpt = input("文章摘要: ").strip()
    if not excerpt:
        print("❌ 摘要不能为空")
        return
    
    # 生成slug
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
    slug = re.sub(r'\s+', '-', slug).strip('-')
    
    # 生成图片文件名
    image_base = slug
    image_desktop = f"{image_base}_desktop.webp"
    image_mobile = f"{image_base}_mobile.webp"
    
    # 创建文章数据
    new_article = {
        "slug": slug,
        "title": title,
        "shortTitle": short_title,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "displayDate": datetime.now().strftime("%B %d, %Y"),
        "excerpt": excerpt,
        "image": {
            "desktop": image_desktop,
            "mobile": image_mobile
        },
        "url": f"/blog/{slug}/"
    }
    
    # 更新文章数据
    article_data = load_article_data()
    article_data['articles'].insert(0, new_article)
    article_data['categories'][category]['count'] += 1
    
    # 保存数据
    with open('data/articles.json', 'w', encoding='utf-8') as f:
        json.dump(article_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 已添加新文章: {title}")
    print(f"📁 文章URL: /blog/{slug}/")
    print(f"🖼️ 图片文件: {image_desktop}, {image_mobile}")
    
    return new_article

def main():
    """主函数"""
    print("🚀 统一网站管理脚本")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 完整同步 (更新组件 + 删除日期 + 修复侧边栏 + 同步数据)")
        print("2. 添加新文章")
        print("3. 只删除所有日期")
        print("4. 只修复侧边栏")
        print("5. 只同步数据")
        print("6. 退出")
        
        choice = input("\n请输入选择 (1-6): ").strip()
        
        if choice == '1':
            # 完整同步
            article_data = load_article_data()
            print(f"\n📊 文章数据统计:")
            for category, data in article_data['categories'].items():
                print(f"  {category}: {data['count']} 篇")
            
            update_components(article_data)
            remove_all_dates()
            fix_all_sidebars()
            sync_sidebar_data(article_data)
            
            print("\n🎉 完整同步完成！")
            
        elif choice == '2':
            # 添加新文章
            new_article = add_new_article()
            if new_article:
                # 自动同步
                article_data = load_article_data()
                update_components(article_data)
                remove_all_dates()
                fix_all_sidebars()
                sync_sidebar_data(article_data)
                print("✅ 新文章已添加并同步完成")
                
        elif choice == '3':
            # 只删除日期
            remove_all_dates()
            
        elif choice == '4':
            # 只修复侧边栏
            fix_all_sidebars()
            
        elif choice == '5':
            # 只同步数据
            article_data = load_article_data()
            sync_sidebar_data(article_data)
            
        elif choice == '6':
            print("👋 再见！")
            break
            
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()
