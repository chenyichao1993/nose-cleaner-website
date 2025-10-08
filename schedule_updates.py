#!/usr/bin/env python3
"""
定时更新Amazon产品信息的调度脚本
可以设置每小时、每天或每周自动更新
"""

import schedule
import time
import subprocess
import sys
from datetime import datetime

def run_update():
    """运行更新脚本"""
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 开始定时更新...")
    
    try:
        # 运行更新脚本
        result = subprocess.run([sys.executable, 'update_amazon_data.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ 定时更新成功完成")
            print(result.stdout)
        else:
            print("❌ 定时更新失败")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ 运行更新脚本时出错: {e}")

def main():
    """主函数 - 设置定时任务"""
    print("🚀 启动Amazon产品信息定时更新服务...")
    print("📅 更新频率: 每天上午9点和下午6点")
    
    # 设置定时任务
    schedule.every().day.at("09:00").do(run_update)  # 每天上午9点
    schedule.every().day.at("18:00").do(run_update)  # 每天下午6点
    
    # 可选：每小时更新一次（测试用）
    # schedule.every().hour.do(run_update)
    
    # 可选：每30分钟更新一次（高频更新）
    # schedule.every(30).minutes.do(run_update)
    
    print("⏰ 定时任务已设置，按 Ctrl+C 停止服务")
    
    # 立即运行一次
    run_update()
    
    # 保持运行
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 定时更新服务已停止")
    except Exception as e:
        print(f"❌ 服务运行出错: {e}")
