#!/usr/bin/env python3
"""
更新所有页面使用新的组件系统
"""

import os
import re
from pathlib import Path

def update_page_components(file_path):
    """更新单个页面使用组件系统"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 添加组件加载器脚本引用
        if 'js/components.js' not in content:
            # 在</body>标签前添加组件加载器
            content = re.sub(
                r'(\s*</body>)',
                r'\n    <!-- Component Loader -->\n    <script src="/js/components.js"></script>\1',
                content
            )
        
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
    print("🔄 开始更新所有页面使用组件系统...")
    
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
    
    updated_pages = 0
    
    for page_path in pages_to_update:
        if os.path.exists(page_path):
            if update_page_components(page_path):
                updated_pages += 1
        else:
            print(f"⚠️ 文件不存在: {page_path}")
    
    print(f"\n🎉 组件系统更新完成！共更新了 {updated_pages} 个页面")
    print("📋 现在所有页面都使用统一的组件系统:")
    print("  - components/header.html - 页头组件")
    print("  - components/footer.html - 页脚组件")
    print("  - components/sidebar.html - 侧边栏组件")
    print("  - js/components.js - 组件加载器")

if __name__ == "__main__":
    main()
