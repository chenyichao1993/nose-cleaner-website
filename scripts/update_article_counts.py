#!/usr/bin/env python3
"""
自动更新博客文章数量的脚本
统计各分类的文章数量并更新所有相关页面
"""

import os
import re
import glob
from pathlib import Path

def count_articles_by_category():
    """统计各分类的文章数量"""
    categories = {
        'baby-care': 0,
        'adult-care': 0,
        'product-reviews': 0,
        'safety-tips': 0
    }
    
    # 扫描所有博客文章
    blog_dir = Path('blog')
    for article_dir in blog_dir.glob('*/'):
        if article_dir.name.startswith('_') or article_dir.name == 'category':
            continue
            
        index_file = article_dir / 'index.html'
        if not index_file.exists():
            continue
            
        # 读取文章内容，查找分类信息
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 查找分类信息
            category_match = re.search(r'<span class="[^"]*category[^"]*">([^<]+)</span>', content)
            if category_match:
                category = category_match.group(1).strip()
                # 标准化分类名称
                if 'Baby Care' in category:
                    categories['baby-care'] += 1
                elif 'Adult Care' in category:
                    categories['adult-care'] += 1
                elif 'Product Reviews' in category:
                    categories['product-reviews'] += 1
                elif 'Safety Tips' in category:
                    categories['safety-tips'] += 1
                    
        except Exception as e:
            print(f"⚠️ 读取文章 {article_dir.name} 时出错: {e}")
            continue
    
    return categories

def update_file_counts(file_path, categories):
    """更新文件中的文章数量"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 更新各分类的数量
        for category, count in categories.items():
            # 匹配模式：Baby Care <span>(数字)</span>
            category_names = {
                'baby-care': 'Baby Care',
                'adult-care': 'Adult Care', 
                'product-reviews': 'Product Reviews',
                'safety-tips': 'Safety Tips'
            }
            
            category_name = category_names[category]
            pattern = rf'({re.escape(category_name)} <span>)\d+(</span>)'
            replacement = rf'\g<1>{count}\g<2>'
            content = re.sub(pattern, replacement, content)
        
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
    print("🔄 开始统计文章数量...")
    
    # 统计各分类文章数量
    categories = count_articles_by_category()
    
    print("📊 文章数量统计:")
    for category, count in categories.items():
        print(f"  {category}: {count} 篇")
    
    # 需要更新的文件列表
    files_to_update = [
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
    
    print("\n🔄 开始更新文件...")
    updated_files = 0
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            if update_file_counts(file_path, categories):
                updated_files += 1
        else:
            print(f"⚠️ 文件不存在: {file_path}")
    
    print(f"\n🎉 更新完成！共更新了 {updated_files} 个文件")
    print("📋 各分类文章数量:")
    for category, count in categories.items():
        print(f"  {category}: {count} 篇")

if __name__ == "__main__":
    main()
