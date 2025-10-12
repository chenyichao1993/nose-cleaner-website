#!/usr/bin/env python3
"""
更新所有页面的Recent Posts，添加新文章并移除最旧的文章
"""

import os
import re
from pathlib import Path

def update_recent_posts_in_file(file_path):
    """更新单个文件的Recent Posts"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 查找Recent Posts部分
        recent_posts_pattern = r'(<ul class="recent-posts">.*?</ul>)'
        match = re.search(recent_posts_pattern, content, re.DOTALL)
        
        if match:
            # 新的Recent Posts内容
            new_recent_posts = '''<ul class="recent-posts">
            <li>
                <a href="/blog/best-way-to-clean-your-nose/">
                    <img src="/images/responsive/best-way-to-clean-your-nose_mobile.webp" alt="Best Way to Clean Your Nose Complete Guide" width="60" height="60">
                    <div>
                        <h4>Best Way to Clean Your Nose Complete Guide</h4>
                        <span>November 15, 2025</span>
                    </div>
                </a>
            </li>
            <li>
                <a href="/blog/adult-nasal-irrigation-complete-guide/">
                    <img src="/images/responsive/adult-nasal-irrigation-complete-guide_mobile.webp" alt="Adult Nasal Irrigation Complete Guide" width="60" height="60">
                    <div>
                        <h4>Adult Nasal Irrigation Complete Guide</h4>
                        <span>October 1, 2025</span>
                    </div>
                </a>
            </li>
            <li>
                <a href="/blog/electric-vs-manual-nasal-aspirators/">
                    <img src="/images/responsive/electric-manual-aspirators_mobile.webp" alt="Electric vs Manual Nasal Aspirators" width="60" height="60">
                    <div>
                        <h4>Electric vs Manual Nasal Aspirators</h4>
                        <span>August 15, 2025</span>
                    </div>
                </a>
            </li>
            <li>
                <a href="/blog/baby-nasal-congestion-remedies/">
                    <img src="/images/responsive/baby-congestion-remedies_mobile.webp" alt="Baby Nasal Congestion Remedies" width="60" height="60">
                    <div>
                        <h4>Baby Nasal Congestion Remedies</h4>
                        <span>June 22, 2025</span>
                    </div>
                </a>
            </li>
            <li>
                <a href="/blog/navage-vs-neilmed-detailed-comparison/">
                    <img src="/images/responsive/comparison-chart_mobile.webp" alt="Naväge vs NeilMed Comparison" width="60" height="60">
                    <div>
                        <h4>Naväge vs NeilMed Comparison</h4>
                        <span>April 8, 2025</span>
                    </div>
                </a>
            </li>
        </ul>'''
            
            # 替换Recent Posts内容
            content = re.sub(recent_posts_pattern, new_recent_posts, content, flags=re.DOTALL)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已更新Recent Posts: {file_path}")
            return True
        else:
            print(f"⏭️ 无需更新: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ 更新文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("🔄 开始更新所有页面的Recent Posts...")
    
    # 需要更新的页面列表（排除已经手动更新的页面）
    pages_to_update = [
        'blog/category/baby-care/index.html',
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
            if update_recent_posts_in_file(page_path):
                updated_pages += 1
        else:
            print(f"⚠️ 文件不存在: {page_path}")
    
    print(f"\n🎉 Recent Posts更新完成！共更新了 {updated_pages} 个页面")
    print("📋 现在所有页面的Recent Posts都包含最新的文章列表")

if __name__ == "__main__":
    main()


