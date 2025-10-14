#!/usr/bin/env python3
"""
完整的添加新文章脚本
包含所有必要的步骤，确保新文章在所有页面正确显示
"""

import json
import os
import shutil
from datetime import datetime
import re

def load_articles_data():
    """加载文章数据"""
    with open('data/articles.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_articles_data(data):
    """保存文章数据"""
    with open('data/articles.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def optimize_images():
    """优化图片"""
    print("🔄 优化图片...")
    os.system('python scripts/optimize_images.py')
    print("✅ 图片优化完成")

def update_blog_homepage(new_article):
    """更新博客首页"""
    print("🔄 更新博客首页...")
    
    # 读取博客首页
    with open('blog/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建新文章卡片HTML
    new_article_html = f'''                        <article class="blog-post">
                            <div class="post-image">
                                <picture>
                                    <source media="(min-width: 768px)" srcset="/images/responsive/{new_article['image']['desktop']}">
                                    <img src="/images/responsive/{new_article['image']['mobile']}" 
                                         alt="{new_article['shortTitle']}" 
                                         loading="lazy"
                                         width="400" 
                                         height="300">
                                </picture>
                            </div>
                            <div class="post-content">
                                <div class="post-meta">
                                    <span class="post-category">{new_article['category']}</span>
                                    
                                </div>
                                <h3><a href="{new_article['url']}">{new_article['title']}</a></h3>
                                <p>{new_article['excerpt']}</p>
                                <a href="{new_article['url']}" class="read-more">Read More →</a>
                            </div>
                        </article>'''
    
    # 在第一个blog-post后面插入新文章
    pattern = r'(<article class="blog-post">.*?</article>)'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    if matches:
        # 在第一个文章后面插入新文章
        insert_pos = matches[0].end()
        content = content[:insert_pos] + '\n\n' + new_article_html + content[insert_pos:]
        
        # 保存更新后的内容
        with open('blog/index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ 博客首页已更新")
    else:
        print("❌ 未找到插入位置")

def update_category_page(new_article):
    """更新分类页面"""
    print(f"🔄 更新 {new_article['category']} 分类页面...")
    
    category_slug = new_article['category'].lower().replace(' ', '-')
    category_file = f'blog/category/{category_slug}/index.html'
    
    if not os.path.exists(category_file):
        print(f"❌ 分类页面不存在: {category_file}")
        return
    
    # 读取分类页面
    with open(category_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建新文章卡片HTML
    new_article_html = f'''                        <article class="blog-post">
                            <div class="post-image">
                                <picture>
                                    <source media="(min-width: 768px)" srcset="/images/responsive/{new_article['image']['desktop']}">
                                    <img src="/images/responsive/{new_article['image']['mobile']}" 
                                         alt="{new_article['shortTitle']}" 
                                         loading="lazy"
                                         width="400" 
                                         height="300">
                                </picture>
                            </div>
                            <div class="post-content">
                                <div class="post-meta">
                                    <span class="post-category">{new_article['category']}</span>
                                    
                                </div>
                                <h3><a href="{new_article['url']}">{new_article['title']}</a></h3>
                                <p>{new_article['excerpt']}</p>
                                <a href="{new_article['url']}" class="read-more">Read More →</a>
                            </div>
                        </article>'''
    
    # 在第一个blog-post后面插入新文章
    pattern = r'(<article class="blog-post">.*?</article>)'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    if matches:
        # 在第一个文章后面插入新文章
        insert_pos = matches[0].end()
        content = content[:insert_pos] + '\n\n' + new_article_html + content[insert_pos:]
        
        # 保存更新后的内容
        with open(category_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {new_article['category']} 分类页面已更新")
    else:
        print(f"❌ 未找到插入位置: {category_file}")


def update_sidebar_categories():
    """更新侧边栏分类计数"""
    print("🔄 更新侧边栏分类计数...")
    
    # 加载文章数据
    data = load_articles_data()
    
    # 需要更新的文件列表
    files_to_update = [
        'blog/index.html',
        'blog/category/baby-care/index.html',
        'blog/category/adult-care/index.html',
        'blog/category/product-reviews/index.html',
        'blog/category/safety-tips/index.html'
    ]
    
    for file_path in files_to_update:
        if not os.path.exists(file_path):
            continue
            
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新每个分类的计数
        for category, info in data['categories'].items():
            old_pattern = f'{category} \\(\\d+\\)'
            new_text = f'{category} ({info["count"]})'
            content = re.sub(old_pattern, new_text, content)
        
        # 保存更新后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新 {file_path} 的分类计数")

def create_article_page(article_data):
    """创建文章页面"""
    print(f"🔄 创建文章页面: {article_data['slug']}...")
    
    # 使用模板页面
    template_file = 'blog/electric-vs-manual-nasal-aspirators/index.html'
    
    if not os.path.exists(template_file):
        print(f"❌ 模板文件不存在: {template_file}")
        return
    
    # 创建目录
    article_dir = f"blog/{article_data['slug']}"
    os.makedirs(article_dir, exist_ok=True)
    
    # 复制模板文件
    shutil.copy2(template_file, f"{article_dir}/index.html")
    
    # 读取并修改文章页面
    with open(f"{article_dir}/index.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换文章特定内容
    replacements = {
        'Electric vs Manual Nasal Aspirators: Which is Better for Your Baby? - Nose Cleaner Blog': f"{article_data['title']} - Nose Cleaner Blog",
        'Compare electric and manual nasal aspirators for babies. Learn the pros, cons, and best use cases for each type to make the right choice for your family.': article_data['excerpt'],
        'https://nosecleaner.online/images/responsive/baby-aspirator_800x600.webp': f"https://nosecleaner.online/images/responsive/{article_data['slug']}_800x600.webp",
        'https://nosecleaner.online/blog/electric-vs-manual-nasal-aspirators/': f"https://nosecleaner.online{article_data['url']}",
        'Electric vs Manual Nasal Aspirators: Which is Better for Your Baby?': article_data['title'],
        'Compare electric and manual nasal aspirators for babies. Learn the pros, cons, and best use cases for each type to make the right choice for your family.': article_data['excerpt'],
        '/blog/electric-vs-manual-nasal-aspirators/': article_data['url'],
        'electric-manual-aspirators_desktop.webp': article_data['image']['desktop'],
        'electric-manual-aspirators_mobile.webp': article_data['image']['mobile'],
        'Electric vs Manual Nasal Aspirators: Which is Better for Your Baby?': article_data['title'],
        'Product Reviews': article_data['category'],
        '/blog/category/product-reviews/': f"/blog/category/{article_data['category'].lower().replace(' ', '-')}/",
        'Electric vs Manual Nasal Aspirators': article_data['shortTitle']
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # 保存更新后的内容
    with open(f"{article_dir}/index.html", 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 文章页面已创建: {article_dir}/index.html")

def main():
    """主函数"""
    print("🚀 开始添加新文章流程...")
    
    # 获取用户输入
    print("\n📝 请输入新文章信息:")
    slug = input("文章slug (URL路径): ").strip()
    title = input("文章标题: ").strip()
    short_title = input("文章短标题: ").strip()
    category = input("文章分类: ").strip()
    excerpt = input("文章摘要: ").strip()
    
    # 生成文章数据
    article_data = {
        "slug": slug,
        "title": title,
        "shortTitle": short_title,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "displayDate": datetime.now().strftime("%B %d, %Y"),
        "excerpt": excerpt,
        "image": {
            "desktop": f"{slug}_desktop.webp",
            "mobile": f"{slug}_mobile.webp"
        },
        "url": f"/blog/{slug}/"
    }
    
    print(f"\n📊 文章信息:")
    print(f"  Slug: {article_data['slug']}")
    print(f"  标题: {article_data['title']}")
    print(f"  分类: {article_data['category']}")
    print(f"  URL: {article_data['url']}")
    
    # 确认继续
    confirm = input("\n确认添加这篇文章? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ 操作已取消")
        return
    
    try:
        # 1. 优化图片
        optimize_images()
        
        # 2. 更新文章数据
        print("🔄 更新文章数据...")
        data = load_articles_data()
        data['articles'].insert(0, article_data)  # 插入到开头
        
        # 更新分类计数
        if category in data['categories']:
            data['categories'][category]['count'] += 1
        else:
            data['categories'][category] = {
                "slug": category.lower().replace(' ', '-'),
                "count": 1,
                "url": f"/blog/category/{category.lower().replace(' ', '-')}/"
            }
        
        save_articles_data(data)
        print("✅ 文章数据已更新")
        
        # 3. 创建文章页面
        create_article_page(article_data)
        
        # 4. 更新博客首页
        update_blog_homepage(article_data)
        
        # 5. 更新分类页面
        update_category_page(article_data)
        
        # 6. 更新侧边栏分类计数
        update_sidebar_categories()
        
        print("\n🎉 新文章添加完成！")
        print(f"📄 文章页面: {article_data['url']}")
        print("📝 请检查文章内容并根据需要修改")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
