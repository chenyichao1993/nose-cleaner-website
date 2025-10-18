#!/usr/bin/env python3
"""
批量更新侧边栏 - 简单方法
"""

import os
import re

def update_file(file_path):
    """更新单个文件"""
    print(f"🔄 更新: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经更新过
    if 'sidebar-container' in content:
        print(f"⏭️  跳过: 已经更新过")
        return False
    
    # 使用正则表达式替换侧边栏
    pattern = r'<aside class="blog-sidebar">.*?</aside>'
    replacement = '''<!-- Sidebar Component -->
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
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        print(f"⏭️  跳过: 未找到侧边栏")
        return False
    
    # 添加CSS链接
    if 'sidebar.css' not in new_content:
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
    print("🚀 批量更新侧边栏...")
    
    # 需要更新的文件
    files = [
        'blog/baby-nasal-congestion-remedies/index.html',
        'blog/best-way-to-clean-your-nose/index.html',
        'blog/category/baby-care/index.html',
        'blog/category/product-reviews/index.html',
        'blog/category/safety-tips/index.html',
        'blog/electric-vs-manual-nasal-aspirators/index.html'
    ]
    
    updated = 0
    skipped = 0
    
    for file_path in files:
        if os.path.exists(file_path):
            if update_file(file_path):
                updated += 1
            else:
                skipped += 1
        else:
            print(f"⏭️  跳过: 文件不存在 {file_path}")
            skipped += 1
    
    print(f"\n🎉 批量更新完成！")
    print(f"📊 统计: 更新 {updated} 个文件，跳过 {skipped} 个文件")

if __name__ == "__main__":
    main()
