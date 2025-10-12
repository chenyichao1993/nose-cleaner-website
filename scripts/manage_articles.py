#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一文章管理脚本
- 更新组件内容
- 同步所有页面
- 管理文章数据
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
                    <span>{post['displayDate']}</span>
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
    sidebar_html = """<!-- Sidebar -->
<aside class="blog-sidebar" id="sidebar-component">
    <div id="categories-component"></div>
    <div id="recent-posts-component"></div>
    <div id="newsletter-component"></div>
</aside>"""
    
    with open('components/sidebar.html', 'w', encoding='utf-8') as f:
        f.write(sidebar_html)
    print("✅ 已更新完整侧边栏组件")

def update_pages():
    """更新所有页面以使用组件系统"""
    print("\n🔄 更新页面...")
    
    # 获取所有HTML文件
    html_files = glob.glob('blog/**/*.html', recursive=True)
    updated_count = 0
    
    for filepath in html_files:
        if 'blog/_layouts' in filepath:  # 跳过布局文件
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = False
        
        # 替换侧边栏为组件
        sidebar_pattern = r'<!-- Sidebar -->\s*<aside class="blog-sidebar">.*?<!-- Newsletter -->\s*<div class="sidebar-widget newsletter-widget">.*?</div>\s*</aside>'
        if re.search(sidebar_pattern, content, re.DOTALL):
            content = re.sub(sidebar_pattern, '<aside class="blog-sidebar"><div id="sidebar-component"></div></aside>', content, flags=re.DOTALL)
            updated = True
        
        # 添加组件加载脚本
        if 'js/components.js' not in content:
            script_tag = '    <script src="/js/components.js"></script>'
            content = content.replace('</body>', f'{script_tag}\n</body>')
            updated = True
        
        if updated:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已更新: {filepath}")
            updated_count += 1
        else:
            print(f"⏭️ 无需更新: {filepath}")
    
    return updated_count

def add_new_article():
    """添加新文章的交互式工具"""
    print("\n📝 添加新文章")
    
    # 获取用户输入
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
    article_data['articles'].insert(0, new_article)  # 添加到开头
    
    # 更新分类计数
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
    print("🚀 统一文章管理脚本")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 同步所有组件和页面")
        print("2. 添加新文章")
        print("3. 退出")
        
        choice = input("\n请输入选择 (1-3): ").strip()
        
        if choice == '1':
            # 同步所有组件和页面
            article_data = load_article_data()
            print(f"\n📊 文章数据统计:")
            for category, data in article_data['categories'].items():
                print(f"  {category}: {data['count']} 篇")
            
            update_components(article_data)
            updated_count = update_pages()
            
            print(f"\n🎉 同步完成！共更新了 {updated_count} 个页面")
            
        elif choice == '2':
            # 添加新文章
            new_article = add_new_article()
            if new_article:
                # 自动同步
                article_data = load_article_data()
                update_components(article_data)
                update_pages()
                print("✅ 新文章已添加并同步完成")
                
        elif choice == '3':
            print("👋 再见！")
            break
            
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()
