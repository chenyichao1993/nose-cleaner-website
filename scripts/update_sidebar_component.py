#!/usr/bin/env python3
"""
更新所有页面的侧边栏为统一组件
"""

import os
import glob
import re

def update_sidebar_in_file(file_path):
    """更新单个文件中的侧边栏"""
    print(f"🔄 更新文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找侧边栏开始和结束位置
    sidebar_start = content.find('<aside class="blog-sidebar">')
    if sidebar_start == -1:
        print(f"⏭️  跳过: 未找到侧边栏")
        return False
    
    # 找到对应的结束标签
    sidebar_end = content.find('</aside>', sidebar_start)
    if sidebar_end == -1:
        print(f"❌ 错误: 未找到侧边栏结束标签")
        return False
    
    sidebar_end += len('</aside>')
    
    # 替换侧边栏内容
    new_sidebar = '''<!-- Sidebar Component -->
    <div id="sidebar-container"></div>
    <script>
        // 动态加载侧边栏组件
        fetch('/components/sidebar.html')
            .then(response => response.text())
            .then(html => {
                document.getElementById('sidebar-container').innerHTML = html;
            })
            .catch(error => console.error('Error loading sidebar:', error));
    </script>'''
    
    # 替换内容
    new_content = content[:sidebar_start] + new_sidebar + content[sidebar_end:]
    
    # 检查是否需要添加CSS链接
    if 'sidebar.css' not in new_content:
        # 在head部分添加CSS链接
        css_link = '<link rel="stylesheet" href="/css/sidebar.css">'
        head_end = new_content.find('</head>')
        if head_end != -1:
            new_content = new_content[:head_end] + f'    {css_link}\n' + new_content[head_end:]
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 更新完成: {file_path}")
    return True

def main():
    """主函数"""
    print("🚀 开始更新所有页面的侧边栏组件...")
    
    # 查找所有需要更新的HTML文件
    html_files = []
    
    # 博客相关页面
    blog_files = glob.glob('blog/**/*.html', recursive=True)
    html_files.extend(blog_files)
    
    # 其他页面
    other_files = glob.glob('*.html')
    html_files.extend(other_files)
    
    updated_count = 0
    skipped_count = 0
    
    for file_path in html_files:
        if update_sidebar_in_file(file_path):
            updated_count += 1
        else:
            skipped_count += 1
    
    print(f"\n🎉 侧边栏组件更新完成！")
    print(f"📊 统计: 更新 {updated_count} 个文件，跳过 {skipped_count} 个文件")
    print(f"📁 侧边栏组件: components/sidebar.html")
    print(f"🎨 样式文件: css/sidebar.css")
    print(f"📊 数据源: data/articles.json (通过 js/categories.js 动态加载)")

if __name__ == "__main__":
    main()
