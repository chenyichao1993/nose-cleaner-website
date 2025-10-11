#!/usr/bin/env python3
"""
组件同步脚本 - 自动更新所有页面的共享组件
"""

import os
import json
import re
from pathlib import Path

def load_article_data():
    """加载文章数据"""
    try:
        with open('data/articles.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 加载文章数据失败: {e}")
        return None

def update_categories_component(data):
    """更新Categories组件"""
    categories_html = []
    for category_name, category_data in data['categories'].items():
        categories_html.append(
            f'        <li><a href="{category_data["url"]}">{category_name} <span>({category_data["count"]})</span></a></li>'
        )
    
    categories_content = f"""<!-- Categories Widget -->
<div class="sidebar-widget">
    <h3>Categories</h3>
    <ul class="category-list">
{chr(10).join(categories_html)}
    </ul>
</div>"""
    
    # 写入组件文件
    with open('components/categories.html', 'w', encoding='utf-8') as f:
        f.write(categories_content)
    
    print("✅ 已更新 Categories 组件")

def update_recent_posts_component(data):
    """更新Recent Posts组件"""
    recent_articles = data['articles'][:5]  # 取最新5篇
    
    posts_html = []
    for article in recent_articles:
        posts_html.append(f"""        <li>
            <a href="{article['url']}">
                <img src="/images/responsive/{article['image']['mobile']}" alt="{article['shortTitle']}" width="60" height="60">
                <div>
                    <h4>{article['shortTitle']}</h4>
                    <span>{article['displayDate']}</span>
                </div>
            </a>
        </li>""")
    
    recent_posts_content = f"""<!-- Recent Posts Widget -->
<div class="sidebar-widget">
    <h3>Recent Posts</h3>
    <ul class="recent-posts">
{chr(10).join(posts_html)}
    </ul>
</div>"""
    
    # 写入组件文件
    with open('components/recent-posts.html', 'w', encoding='utf-8') as f:
        f.write(recent_posts_content)
    
    print("✅ 已更新 Recent Posts 组件")

def update_sidebar_component(data):
    """更新完整侧边栏组件"""
    # 生成Categories HTML
    categories_html = []
    for category_name, category_data in data['categories'].items():
        categories_html.append(
            f'            <li><a href="{category_data["url"]}">{category_name} <span>({category_data["count"]})</span></a></li>'
        )
    
    # 生成Recent Posts HTML
    recent_articles = data['articles'][:5]
    posts_html = []
    for article in recent_articles:
        posts_html.append(f"""            <li>
                <a href="{article['url']}">
                    <img src="/images/responsive/{article['image']['mobile']}" alt="{article['shortTitle']}" width="60" height="60">
                    <div>
                        <h4>{article['shortTitle']}</h4>
                        <span>{article['displayDate']}</span>
                    </div>
                </a>
            </li>""")
    
    sidebar_content = f"""<!-- Sidebar -->
<aside class="blog-sidebar">
    <!-- Categories -->
    <div class="sidebar-widget">
        <h3>Categories</h3>
        <ul class="category-list">
{chr(10).join(categories_html)}
        </ul>
    </div>

    <!-- Recent Posts -->
    <div class="sidebar-widget">
        <h3>Recent Posts</h3>
        <ul class="recent-posts">
{chr(10).join(posts_html)}
        </ul>
    </div>

    <!-- Newsletter -->
    <div class="sidebar-widget newsletter-widget">
        <h3>Stay Updated</h3>
        <p>Get the latest nasal health tips and product reviews delivered to your inbox.</p>
        <form class="newsletter-form" id="newsletter-form">
            <input type="email" placeholder="Enter your email address" required 
                   title="Please enter a valid email address"
                   oninvalid="this.setCustomValidity('Please enter a valid email address')"
                   oninput="this.setCustomValidity('')">
            <button type="submit" class="btn btn-primary">Subscribe</button>
        </form>
    </div>
</aside>"""
    
    # 写入组件文件
    with open('components/sidebar.html', 'w', encoding='utf-8') as f:
        f.write(sidebar_content)
    
    print("✅ 已更新完整侧边栏组件")

def update_page_components(file_path, data):
    """更新单个页面的组件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 更新Categories部分
        categories_pattern = r'(<div class="sidebar-widget">\s*<h3>Categories</h3>\s*<ul class="category-list">).*?(</ul>\s*</div>)'
        categories_replacement = f'\\1\n'
        for category_name, category_data in data['categories'].items():
            categories_replacement += f'            <li><a href="{category_data["url"]}">{category_name} <span>({category_data["count"]})</span></a></li>\n'
        categories_replacement += '        \\2'
        
        content = re.sub(categories_pattern, categories_replacement, content, flags=re.DOTALL)
        
        # 更新Recent Posts部分
        recent_articles = data['articles'][:5]
        posts_html = []
        for article in recent_articles:
            posts_html.append(f"""            <li>
                <a href="{article['url']}">
                    <img src="/images/responsive/{article['image']['mobile']}" alt="{article['shortTitle']}" width="60" height="60">
                    <div>
                        <h4>{article['shortTitle']}</h4>
                        <span>{article['displayDate']}</span>
                    </div>
                </a>
            </li>""")
        
        recent_posts_pattern = r'(<div class="sidebar-widget">\s*<h3>Recent Posts</h3>\s*<ul class="recent-posts">).*?(</ul>\s*</div>)'
        recent_posts_replacement = f'\\1\n{chr(10).join(posts_html)}\n        \\2'
        
        content = re.sub(recent_posts_pattern, recent_posts_replacement, content, flags=re.DOTALL)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已更新: {file_path}")
            return True
        else:
            print(f"⏭️ 无需更新: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ 更新文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("🔄 开始同步组件...")
    
    # 加载文章数据
    data = load_article_data()
    if not data:
        return
    
    print("📊 文章数据统计:")
    for category_name, category_data in data['categories'].items():
        print(f"  {category_name}: {category_data['count']} 篇")
    
    # 更新组件文件
    update_categories_component(data)
    update_recent_posts_component(data)
    update_sidebar_component(data)
    
    # 需要更新的页面列表
    pages_to_update = [
        'blog/index.html',
        'blog/category/baby-care/index.html',
        'blog/category/adult-care/index.html',
        'blog/category/product-reviews/index.html',
        'blog/category/safety-tips/index.html',
        'blog/electric-vs-manual-nasal-aspirators/index.html',
        'blog/baby-nasal-congestion-remedies/index.html',
        'blog/navage-vs-neilmed-detailed-comparison/index.html',
        'blog/nasal-irrigation-safety-mistakes/index.html',
        'blog/complete-guide-baby-nasal-care/index.html',
        'blog/adult-nasal-irrigation-complete-guide/index.html'
    ]
    
    print("\n🔄 开始更新页面...")
    updated_pages = 0
    
    for page_path in pages_to_update:
        if os.path.exists(page_path):
            if update_page_components(page_path, data):
                updated_pages += 1
        else:
            print(f"⚠️ 文件不存在: {page_path}")
    
    print(f"\n🎉 组件同步完成！共更新了 {updated_pages} 个页面")
    print("📋 组件文件已更新:")
    print("  - components/categories.html")
    print("  - components/recent-posts.html") 
    print("  - components/sidebar.html")

if __name__ == "__main__":
    main()
