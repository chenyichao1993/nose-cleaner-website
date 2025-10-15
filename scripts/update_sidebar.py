#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速更新所有页面的侧边栏 - 一键解决分类计数问题
"""

import subprocess
import sys

def main():
    """主函数"""
    print("🔄 正在更新所有页面的侧边栏...")
    
    try:
        # 运行动态侧边栏更新脚本
        result = subprocess.run([sys.executable, 'scripts/create_dynamic_sidebar.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 侧边栏更新完成！")
            print("📋 所有页面的分类计数现在都从 data/articles.json 动态生成")
        else:
            print(f"❌ 更新失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    main()
