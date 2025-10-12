#!/usr/bin/env python3
"""
文章管理系统 - 自动化处理文章添加、更新和同步
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

class ArticleManager:
    def __init__(self):
        self.articles_file = 'data/articles.json'
        self.articles_data = self.load_articles_data()
        
    def load_articles_data(self):
        """加载文章数据"""
        try:
            with open(self.articles_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"articles": []}
    
    def save_articles_data(self):
        """保存文章数据"""
        with open(self.articles_file, 'w', encoding='utf-8') as f:
            json.dump(self.articles_data, f, indent=2, ensure_ascii=False)
    
    def add_article(self, article_data):
        """添加新文章"""
        # 验证必需字段
        required_fields = ['slug', 'title', 'shortTitle', 'category', 'date', 'displayDate', 'excerpt', 'image', 'url']
        for field in required_fields:
            if field not in article_data:
                raise ValueError(f"缺少必需字段: {field}")
        
        # 检查文章是否已存在
        existing_slugs = [article['slug'] for article in self.articles_data['articles']]
        if article_data['slug'] in existing_slugs:
            raise ValueError(f"文章已存在: {article_data['slug']}")
        
        # 添加到文章列表开头（最新文章在前）
        self.articles_data['articles'].insert(0, article_data)
        self.save_articles_data()
        
        print(f"✅ 文章已添加到数据源: {article_data['title']}")
        return article_data
    
    def get_category_counts(self):
        """获取各分类的文章数量"""
        category_counts = {}
        for article in self.articles_data['articles']:
            category_slug = article['category'].lower().replace(' ', '-')
            category_counts[category_slug] = category_counts.get(category_slug, 0) + 1
        return category_counts
    
    def get_recent_posts(self, limit=5):
        """获取最新文章列表"""
        return self.articles_data['articles'][:limit]
    
    def update_blog_index(self):
        """更新博客首页"""
        file_path = 'blog/index.html'
        if not os.path.exists(file_path):
            print(f"⚠️ 文件不存在: {file_path}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新文章列表（添加新文章到开头）
        articles = self.articles_data['articles']
        new_articles_html = ""
        
        for i, article in enumerate(articles[:6]):  # 显示前6篇文章
            if i == 0:
                # 第一篇文章作为featured post
                new_articles_html += f'''
                        <article class="featured-post">
                            <div class="featured-post-image">
                                <picture>
                                    <source media="(min-width: 768px)" srcset="/images/responsive/{article['image']['desktop']}">
                                    <img src="/images/responsive/{article['image']['mobile']}" 
                                         alt="{article['shortTitle']}" 
                                         loading="lazy">
                                </picture>
                            </div>
                            <div class="featured-post-content">
                                <div class="post-meta">
                                    <span class="post-category">{article['category']}</span>
                                    <span class="post-date">{article['displayDate']}</span>
                                </div>
                                <h2><a href="{article['url']}">{article['title']}</a></h2>
                                <p>{article['excerpt']}</p>
                                <a href="{article['url']}" class="read-more">Read More →</a>
                            </div>
                        </article>
                '''
            else:
                # 其他文章作为blog posts
                new_articles_html += f'''
                        <article class="blog-post">
                            <div class="post-image">
                                <picture>
                                    <source media="(min-width: 768px)" srcset="/images/responsive/{article['image']['desktop']}">
                                    <img src="/images/responsive/{article['image']['mobile']}" 
                                         alt="{article['shortTitle']}" 
                                         loading="lazy"
                                         width="400" 
                                         height="300">
                                </picture>
                            </div>
                            <div class="post-content">
                                <div class="post-meta">
                                    <span class="post-category">{article['category']}</span>
                                    <span class="post-date">{article['displayDate']}</span>
                                </div>
                                <h3><a href="{article['url']}">{article['title']}</a></h3>
                                <p>{article['excerpt']}</p>
                                <a href="{article['url']}" class="read-more">Read More →</a>
                            </div>
                        </article>
                '''
        
        # 替换featured post和blog posts
        featured_pattern = r'(<article class="featured-post">.*?</article>)'
        blog_posts_pattern = r'(<div class="blog-posts">.*?</div>)'
        
        content = re.sub(featured_pattern, new_articles_html.split('</article>')[0] + '</article>', content, flags=re.DOTALL)
        
        # 更新blog posts部分
        blog_posts_html = f'''<div class="blog-posts">
{new_articles_html.split('</article>')[1:]}
                </div>'''
        content = re.sub(blog_posts_pattern, blog_posts_html, content, flags=re.DOTALL)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新博客首页: {file_path}")
    
    def update_category_pages(self):
        """更新所有分类页面"""
        category_counts = self.get_category_counts()
        
        for category_slug, count in category_counts.items():
            category_file = f'blog/category/{category_slug}/index.html'
            if not os.path.exists(category_file):
                print(f"⚠️ 分类页面不存在: {category_file}")
                continue
            
            with open(category_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 获取该分类的文章
            category_articles = [article for article in self.articles_data['articles'] 
                               if article['category'].lower().replace(' ', '-') == category_slug]
            
            if not category_articles:
                # 如果没有文章，显示空状态
                content = self.update_empty_category_page(content, category_slug)
            else:
                # 更新文章列表
                content = self.update_category_articles(content, category_articles)
            
            # 更新分类计数
            content = self.update_category_counts_in_content(content, category_counts)
            
            with open(category_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已更新分类页面: {category_file}")
    
    def update_category_articles(self, content, articles):
        """更新分类页面的文章列表"""
        if not articles:
            return content
        
        # 第一篇文章作为featured post
        featured_article = articles[0]
        featured_html = f'''
                <article class="featured-post">
                    <div class="featured-post-image">
                        <picture>
                            <source media="(min-width: 768px)" srcset="/images/responsive/{featured_article['image']['desktop']}">
                            <img src="/images/responsive/{featured_article['image']['mobile']}" 
                                 alt="{featured_article['shortTitle']}" 
                                 loading="lazy">
                        </picture>
                    </div>
                    <div class="featured-post-content">
                        <div class="post-meta">
                            <span class="post-category">{featured_article['category']}</span>
                            <span class="post-date">{featured_article['displayDate']}</span>
                        </div>
                        <h2><a href="{featured_article['url']}">{featured_article['title']}</a></h2>
                        <p>{featured_article['excerpt']}</p>
                        <a href="{featured_article['url']}" class="read-more">Read More →</a>
                    </div>
                </article>
        '''
        
        # 其他文章作为blog posts
        if len(articles) > 1:
            additional_articles_html = ""
            for article in articles[1:]:
                additional_articles_html += f'''
                    <article class="blog-post">
                        <div class="post-image">
                            <picture>
                                <source media="(min-width: 768px)" srcset="/images/responsive/{article['image']['desktop']}">
                                <img src="/images/responsive/{article['image']['mobile']}" 
                                     alt="{article['shortTitle']}" 
                                     loading="lazy">
                            </picture>
                        </div>
                        <div class="post-content">
                            <div class="post-meta">
                                <span class="post-category">{article['category']}</span>
                                <span class="post-date">{article['displayDate']}</span>
                            </div>
                            <h3><a href="{article['url']}">{article['title']}</a></h3>
                            <p>{article['excerpt']}</p>
                            <a href="{article['url']}" class="read-more">Read More →</a>
                        </div>
                    </article>
                '''
            
            featured_html += f'''
                <!-- Additional Posts -->
                <div class="blog-posts">
                    {additional_articles_html}
                </div>
            '''
        
        # 替换featured post
        featured_pattern = r'(<article class="featured-post">.*?</article>)'
        content = re.sub(featured_pattern, featured_html, content, flags=re.DOTALL)
        
        return content
    
    def update_empty_category_page(self, content, category_slug):
        """更新空分类页面"""
        empty_html = '''
                <div class="no-posts-message">
                    <h2>No articles yet</h2>
                    <p>We're working on adding great content for this category. Check back soon!</p>
                </div>
        '''
        
        # 替换主要内容区域
        main_pattern = r'(<main class="blog-main">.*?</main>)'
        content = re.sub(main_pattern, f'<main class="blog-main">{empty_html}</main>', content, flags=re.DOTALL)
        
        return content
    
    def update_category_counts_in_content(self, content, category_counts):
        """更新内容中的分类计数"""
        for category_slug, count in category_counts.items():
            category_name = self.get_category_name(category_slug)
            pattern = rf'(<li><a href="/blog/category/{re.escape(category_slug)}/">.*?<span>)\(\d+\)(</span></a></li>)'
            replacement = rf'\g<1>({count})\g<2>'
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def get_category_name(self, category_slug):
        """根据slug获取分类名称"""
        category_map = {
            'baby-care': 'Baby Care',
            'adult-care': 'Adult Care',
            'product-reviews': 'Product Reviews',
            'safety-tips': 'Safety Tips'
        }
        return category_map.get(category_slug, category_slug.title())
    
    def update_recent_posts_in_all_pages(self):
        """更新所有页面的Recent Posts"""
        recent_posts = self.get_recent_posts(5)
        
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
            'blog/adult-nasal-irrigation-complete-guide/index.html',
            'blog/best-way-to-clean-your-nose/index.html'
        ]
        
        recent_posts_html = '<ul class="recent-posts">\n'
        for post in recent_posts:
            recent_posts_html += f'''            <li>
                <a href="{post['url']}">
                    <img src="/images/responsive/{post['image']['mobile']}" alt="{post['shortTitle']}" width="60" height="60">
                    <div>
                        <h4>{post['shortTitle']}</h4>
                        <span>{post['displayDate']}</span>
                    </div>
                </a>
            </li>
'''
        recent_posts_html += '        </ul>'
        
        for page_path in pages_to_update:
            if not os.path.exists(page_path):
                continue
            
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换Recent Posts
            recent_posts_pattern = r'(<ul class="recent-posts">.*?</ul>)'
            content = re.sub(recent_posts_pattern, recent_posts_html, content, flags=re.DOTALL)
            
            # 更新分类计数
            category_counts = self.get_category_counts()
            content = self.update_category_counts_in_content(content, category_counts)
            
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已更新Recent Posts: {page_path}")
    
    def update_sitemaps(self):
        """更新sitemap文件"""
        # 更新sitemap.xml
        sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <!-- Main Pages -->
    <url>
        <loc>https://nosecleaner.online/</loc>
        <lastmod>2025-01-06</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    
    <url>
        <loc>https://nosecleaner.online/blog/</loc>
        <lastmod>2025-01-06</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    
    <url>
        <loc>https://nosecleaner.online/reviews</loc>
        <lastmod>2025-01-06</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    
    <url>
        <loc>https://nosecleaner.online/guide</loc>
        <lastmod>2025-01-06</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    
    <url>
        <loc>https://nosecleaner.online/baby</loc>
        <lastmod>2025-01-06</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    
    <url>
        <loc>https://nosecleaner.online/about</loc>
        <lastmod>2025-01-06</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    
    <!-- Blog Category Pages -->'''
        
        # 添加分类页面
        category_counts = self.get_category_counts()
        for category_slug in category_counts.keys():
            sitemap_content += f'''
    <url>
        <loc>https://nosecleaner.online/blog/category/{category_slug}/</loc>
        <lastmod>2025-01-06</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>'''
        
        # 添加文章页面
        sitemap_content += '''
    
    <!-- Blog Articles -->'''
        for article in self.articles_data['articles']:
            sitemap_content += f'''
    <url>
        <loc>https://nosecleaner.online{article['url']}</loc>
        <lastmod>{article['date']}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>'''
        
        sitemap_content += '''

</urlset>'''
        
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        print("✅ 已更新sitemap.xml")
        
        # 更新sitemap-images.xml
        self.update_sitemap_images()
    
    def update_sitemap_images(self):
        """更新sitemap-images.xml"""
        sitemap_images_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
    
    <!-- Main page images -->'''
        
        # 添加主页面图片
        main_pages = [
            ('/', 'homepage', 'Nose Cleaner Homepage'),
            ('/reviews', 'reviews', 'Product Reviews'),
            ('/guide', 'guide', 'Usage Guide'),
            ('/baby', 'baby-care', 'Baby Care Guide'),
            ('/about', 'about', 'About Us')
        ]
        
        for url, image_name, title in main_pages:
            sitemap_images_content += f'''
    <url>
        <loc>https://nosecleaner.online{url}</loc>
        <image:image>
            <image:loc>https://nosecleaner.online/images/responsive/{image_name}_desktop.webp</image:loc>
            <image:title>{title}</image:title>
            <image:caption>Professional nasal health guidance and product reviews</image:caption>
        </image:image>
    </url>'''
        
        # 添加博客文章图片
        sitemap_images_content += '''
    
    <!-- Blog article images -->'''
        for article in self.articles_data['articles']:
            sitemap_images_content += f'''
    <url>
        <loc>https://nosecleaner.online{article['url']}</loc>
        <image:image>
            <image:loc>https://nosecleaner.online/images/responsive/{article['image']['desktop']}</image:loc>
            <image:title>{article['shortTitle']}</image:title>
            <image:caption>{article['excerpt']}</image:caption>
        </image:image>
    </url>'''
        
        sitemap_images_content += '''

</urlset>'''
        
        with open('sitemap-images.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap_images_content)
        
        print("✅ 已更新sitemap-images.xml")
    
    def create_article_template(self, article_data):
        """创建文章页面模板"""
        template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article_data['title']} | Nose Cleaner</title>
    <meta name="description" content="{article_data['excerpt']}">
    <meta name="keywords" content="nasal hygiene, nose cleaning, nasal irrigation, nasal health">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://nosecleaner.online{article_data['url']}">
    <meta property="og:title" content="{article_data['title']}">
    <meta property="og:description" content="{article_data['excerpt']}">
    <meta property="og:image" content="https://nosecleaner.online/images/responsive/{article_data['image']['desktop']}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:site_name" content="Nose Cleaner">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://nosecleaner.online{article_data['url']}">
    <meta property="twitter:title" content="{article_data['title']}">
    <meta property="twitter:description" content="{article_data['excerpt']}">
    <meta property="twitter:image" content="https://nosecleaner.online/images/responsive/{article_data['image']['desktop']}">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://nosecleaner.online{article_data['url']}">
    
    <!-- Favicon -->
    <link rel="icon" type="image/webp" href="/images/webp/favicon.webp">
    <link rel="apple-touch-icon" href="/images/webp/apple-touch-icon.webp">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/blog/css/blog.css">
    
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-XXXXXXXXXX');
    </script>
    
    <!-- Microsoft Clarity -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){{
            c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        }})(window, document, "clarity", "script", "XXXXXXXXXX");
    </script>
    
    <!-- Baidu Analytics -->
    <script>
        var _hmt = _hmt || [];
        (function() {{
            var hm = document.createElement("script");
            hm.src = "https://hm.baidu.com/hm.js?XXXXXXXXXX";
            var s = document.getElementsByTagName("script")[0]; 
            s.parentNode.insertBefore(hm, s);
        }})();
    </script>
    
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-TRQ8QLR9');</script>
    
    <style>
        /* 文章页面样式 - 与其他文章页面保持一致 */
        .article-layout {{
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 3rem;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }}
        
        .article-main {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            overflow: hidden;
        }}
        
        .article-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }}
        
        .article-title {{
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0 0 1rem 0;
            line-height: 1.2;
        }}
        
        .article-meta {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            margin-top: 1.5rem;
        }}
        
        .article-category {{
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
        }}
        
        .article-date {{
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.9rem;
        }}
        
        .article-content {{
            padding: 3rem 2rem;
        }}
        
        .article-image {{
            margin-bottom: 2rem;
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .article-image img {{
            width: 100%;
            height: auto;
            border-radius: 8px;
        }}
        
        .article-excerpt {{
            font-size: 1.2rem;
            color: #64748b;
            line-height: 1.6;
            margin-bottom: 2rem;
            font-style: italic;
        }}
        
        .article-body h2 {{
            color: #1e293b;
            font-size: 1.8rem;
            font-weight: 600;
            margin: 2.5rem 0 1rem 0;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 0.5rem;
        }}
        
        .article-body h3 {{
            color: #334155;
            font-size: 1.4rem;
            font-weight: 600;
            margin: 2rem 0 1rem 0;
        }}
        
        .article-body p {{
            color: #475569;
            line-height: 1.7;
            margin-bottom: 1.5rem;
        }}
        
        .article-body ul, .article-body ol {{
            margin: 1.5rem 0;
            padding-left: 2rem;
        }}
        
        .article-body li {{
            color: #475569;
            line-height: 1.6;
            margin-bottom: 0.5rem;
        }}
        
        .highlight-box {{
            background: #f8fafc;
            border-left: 4px solid #3b82f6;
            padding: 1.5rem;
            margin: 2rem 0;
            border-radius: 0 8px 8px 0;
        }}
        
        .warning-box {{
            background: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 1.5rem;
            margin: 2rem 0;
            border-radius: 0 8px 8px 0;
        }}
        
        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .comparison-table th,
        .comparison-table td {{
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .comparison-table th {{
            background: #f8fafc;
            font-weight: 600;
            color: #1e293b;
        }}
        
        .comparison-table tr:hover {{
            background: #f8fafc;
        }}
        
        /* 侧边栏样式 */
        .blog-sidebar {{
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }}
        
        .sidebar-widget {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        
        .sidebar-widget h3 {{
            color: #1e293b;
            font-size: 1.2rem;
            font-weight: 600;
            margin: 0 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #e2e8f0;
        }}
        
        .category-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .category-list li {{
            margin-bottom: 0.75rem;
        }}
        
        .category-list a {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: #64748b;
            text-decoration: none;
            padding: 0.5rem 0;
            transition: color 0.3s ease;
        }}
        
        .category-list a:hover {{
            color: #3b82f6;
        }}
        
        .recent-posts {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .recent-posts li {{
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .recent-posts li:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}
        
        .recent-posts a {{
            display: flex;
            gap: 0.75rem;
            text-decoration: none;
            color: inherit;
        }}
        
        .recent-posts img {{
            width: 60px;
            height: 60px;
            object-fit: cover;
            border-radius: 6px;
            flex-shrink: 0;
        }}
        
        .recent-posts h4 {{
            color: #1e293b;
            font-size: 0.9rem;
            font-weight: 500;
            margin: 0 0 0.25rem 0;
            line-height: 1.3;
        }}
        
        .recent-posts span {{
            color: #64748b;
            font-size: 0.8rem;
        }}
        
        .newsletter-widget {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .newsletter-widget h3 {{
            color: white;
            border-bottom-color: rgba(255, 255, 255, 0.2);
        }}
        
        .newsletter-widget p {{
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 1rem;
        }}
        
        .newsletter-form {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }}
        
        .newsletter-form input {{
            padding: 0.75rem;
            border: none;
            border-radius: 6px;
            font-size: 0.9rem;
        }}
        
        .newsletter-form button {{
            background: white;
            color: #667eea;
            border: none;
            padding: 0.75rem;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .newsletter-form button:hover {{
            background: #f8fafc;
            transform: translateY(-1px);
        }}
        
        /* 面包屑导航 */
        .breadcrumb {{
            background: #f8fafc;
            padding: 1rem 0;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .breadcrumb-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }}
        
        .breadcrumb-list {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            list-style: none;
            margin: 0;
            padding: 0;
        }}
        
        .breadcrumb-item {{
            color: #64748b;
            font-size: 0.9rem;
        }}
        
        .breadcrumb-item:not(:last-child)::after {{
            content: "›";
            margin-left: 0.5rem;
            color: #94a3b8;
        }}
        
        .breadcrumb-item a {{
            color: #3b82f6;
            text-decoration: none;
        }}
        
        .breadcrumb-item a:hover {{
            text-decoration: underline;
        }}
        
        /* 返回顶部按钮 */
        .back-to-top {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #3b82f6;
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            transition: all 0.3s ease;
            opacity: 0;
            visibility: hidden;
            z-index: 1000;
        }}
        
        .back-to-top.show {{
            opacity: 1;
            visibility: visible;
        }}
        
        .back-to-top:hover {{
            background: #2563eb;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
        }}
        
        @media (max-width: 768px) {{
            .article-layout {{
                grid-template-columns: 1fr;
                gap: 2rem;
            }}
            
            .article-title {{
                font-size: 2rem;
            }}
            
            .article-content {{
                padding: 2rem 1rem;
            }}
            
            .article-excerpt {{
                font-size: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TRQ8QLR9"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

    <!-- Header -->
    <header class="header">
        <div id="header-component"></div>
    </header>

    <!-- Breadcrumb -->
    <nav class="breadcrumb">
        <div class="breadcrumb-container">
            <ol class="breadcrumb-list">
                <li class="breadcrumb-item"><a href="/">Home</a></li>
                <li class="breadcrumb-item"><a href="/blog/">Blog</a></li>
                <li class="breadcrumb-item"><a href="/blog/category/{article_data['category'].lower().replace(' ', '-')}/">{article_data['category']}</a></li>
                <li class="breadcrumb-item">{article_data['shortTitle']}</li>
            </ol>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="main">
        <div class="container">
            <div class="article-layout">
                <article class="article-main">
                    <header class="article-header">
                        <h1 class="article-title">{article_data['title']}</h1>
                        <div class="article-meta">
                            <span class="article-category">{article_data['category']}</span>
                            <span class="article-date">{article_data['displayDate']}</span>
                        </div>
                    </header>
                    
                    <div class="article-content">
                        <div class="article-image">
                            <picture>
                                <source media="(max-width: 768px)" srcset="/images/responsive/{article_data['image']['mobile']}">
                                <img src="/images/responsive/{article_data['image']['desktop']}" 
                                     alt="{article_data['shortTitle']}" 
                                     loading="eager">
                            </picture>
                        </div>
                        
                        <div class="article-excerpt">
                            {article_data['excerpt']}
                        </div>
                        
                        <div class="article-body">
                            <!-- 在这里添加文章内容 -->
                            <p>请在这里添加您的文章内容...</p>
                        </div>
                    </div>
                </article>
                
                <!-- Sidebar -->
                <aside class="blog-sidebar">
                    <div id="sidebar-component"></div>
                </aside>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div id="footer-component"></div>
    </footer>

    <!-- Back to Top Button -->
    <button class="back-to-top" id="back-to-top" aria-label="Back to top">
        ↑
    </button>

    <!-- Scripts -->
    <script src="/js/main.js"></script>
    <script src="/js/components.js"></script>
    
    <!-- Schema.org structured data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{article_data['title']}",
        "description": "{article_data['excerpt']}",
        "image": "https://nosecleaner.online/images/responsive/{article_data['image']['desktop']}",
        "author": {{
            "@type": "Organization",
            "name": "Nose Cleaner Team"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "Nose Cleaner",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://nosecleaner.online/images/webp/logo.webp"
            }}
        }},
        "datePublished": "{article_data['date']}",
        "dateModified": "{article_data['date']}",
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "https://nosecleaner.online{article_data['url']}"
        }}
    }}
    </script>
    
    <script>
        // Back to Top Button
        document.addEventListener('DOMContentLoaded', function() {{
            const backToTopButton = document.getElementById('back-to-top');
            
            // Show/hide button based on scroll position
            window.addEventListener('scroll', function() {{
                if (window.pageYOffset > 300) {{
                    backToTopButton.classList.add('show');
                }} else {{
                    backToTopButton.classList.remove('show');
                }}
            }});
            
            // Smooth scroll to top when clicked
            backToTopButton.addEventListener('click', function() {{
                window.scrollTo({{
                    top: 0,
                    behavior: 'smooth'
                }});
            }});
            
            // Update current year in footer
            const currentYear = new Date().getFullYear();
            const yearElement = document.getElementById('current-year-footer');
            if (yearElement) {{
                yearElement.textContent = currentYear;
            }}
        }});
    </script>
</body>
</html>'''
        
        return template
    
    def create_article_page(self, article_data):
        """创建文章页面文件"""
        article_dir = f"blog/{article_data['slug']}"
        os.makedirs(article_dir, exist_ok=True)
        
        article_file = f"{article_dir}/index.html"
        template = self.create_article_template(article_data)
        
        with open(article_file, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"✅ 已创建文章页面: {article_file}")
        return article_file
    
    def sync_all_data(self):
        """同步所有数据 - 一键更新所有页面"""
        print("🔄 开始同步所有数据...")
        
        # 1. 更新博客首页
        self.update_blog_index()
        
        # 2. 更新所有分类页面
        self.update_category_pages()
        
        # 3. 更新所有页面的Recent Posts和分类计数
        self.update_recent_posts_in_all_pages()
        
        # 4. 更新sitemap文件
        self.update_sitemaps()
        
        print("🎉 所有数据同步完成！")

def main():
    """主函数 - 演示如何使用"""
    manager = ArticleManager()
    
    # 示例：添加新文章
    new_article = {
        "slug": "test-article",
        "title": "Test Article Title",
        "shortTitle": "Test Article",
        "category": "Adult Care",
        "date": "2025-11-15",
        "displayDate": "November 15, 2025",
        "excerpt": "This is a test article excerpt.",
        "image": {
            "desktop": "test-article_desktop.webp",
            "mobile": "test-article_mobile.webp"
        },
        "url": "/blog/test-article/"
    }
    
    # 添加文章到数据源
    # manager.add_article(new_article)
    
    # 创建文章页面
    # manager.create_article_page(new_article)
    
    # 同步所有数据
    manager.sync_all_data()

if __name__ == "__main__":
    main()


