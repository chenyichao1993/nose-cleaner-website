#!/usr/bin/env python3
"""
修复剩余页面的侧边栏
"""

import os
import glob

def fix_sidebar_in_file(file_path):
    """修复单个文件的侧边栏"""
    print(f"🔄 修复文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经更新过
    if 'sidebar-container' in content:
        print(f"⏭️  跳过: 已经更新过")
        return False
    
    # 查找侧边栏开始位置
    sidebar_start = content.find('<aside class="blog-sidebar">')
    if sidebar_start == -1:
        print(f"⏭️  跳过: 未找到侧边栏")
        return False
    
    # 找到侧边栏结束位置（查找下一个</div>或</aside>）
    sidebar_end = sidebar_start
    depth = 0
    i = sidebar_start
    while i < len(content):
        if content[i:i+6] == '<aside':
            depth += 1
        elif content[i:i+7] == '</aside':
            depth -= 1
            if depth == 0:
                sidebar_end = i + 7
                break
        i += 1
    
    if sidebar_end == sidebar_start:
        print(f"❌ 错误: 未找到侧边栏结束标签")
        return False
    
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
    
    print(f"✅ 修复完成: {file_path}")
    return True

def main():
    """主函数"""
    print("🚀 开始修复剩余页面的侧边栏...")
    
    # 需要修复的文件列表
    files_to_fix = [
        'blog/adult-nasal-irrigation-complete-guide/index.html',
        'blog/baby-nasal-congestion-remedies/index.html',
        'blog/best-way-to-clean-your-nose/index.html',
        'blog/category/baby-care/index.html',
        'blog/category/product-reviews/index.html',
        'blog/category/safety-tips/index.html',
        'blog/electric-vs-manual-nasal-aspirators/index.html'
    ]
    
    updated_count = 0
    skipped_count = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            if fix_sidebar_in_file(file_path):
                updated_count += 1
            else:
                skipped_count += 1
        else:
            print(f"⏭️  跳过: 文件不存在 {file_path}")
            skipped_count += 1
    
    print(f"\n🎉 侧边栏修复完成！")
    print(f"📊 统计: 修复 {updated_count} 个文件，跳过 {skipped_count} 个文件")

if __name__ == "__main__":
    main()
