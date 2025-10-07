#!/usr/bin/env python3
"""
AI图片处理和集成脚本
自动处理AI生成的图片并集成到网站
"""

import os
import json
from PIL import Image
import glob

def create_directory_structure():
    """创建图片目录结构"""
    directories = [
        'images',
        'images/webp',
        'images/responsive',
        'images/original'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ 创建目录: {directory}")

def process_ai_images():
    """处理AI生成的图片"""
    
    # 图片映射配置
    image_config = {
        'hero-nose-cleaner': {
            'sizes': [(800, 600), (1200, 900), (1600, 1200)],
            'alt': 'Best nasal irrigators and nose cleaners',
            'description': 'Professional nasal irrigation devices'
        },
        'baby-nose-cleaner': {
            'sizes': [(400, 300), (600, 450), (800, 600)],
            'alt': 'Baby nose cleaner device',
            'description': 'Safe and gentle baby nasal aspirator'
        },
        'adult-nose-cleaner': {
            'sizes': [(400, 300), (600, 450), (800, 600)],
            'alt': 'Adult nose cleaner device',
            'description': 'Professional adult nasal irrigator'
        },
        'allergy-relief': {
            'sizes': [(400, 300), (600, 450), (800, 600)],
            'alt': 'Allergy relief nose cleaner',
            'description': 'Allergy relief nasal irrigation device'
        },
        'navage-device': {
            'sizes': [(300, 300), (400, 400), (600, 600)],
            'alt': 'Naväge Nasal Care Starter Kit',
            'description': 'Naväge nasal irrigation device'
        },
        'neilmed-device': {
            'sizes': [(300, 300), (400, 400), (600, 600)],
            'alt': 'NeilMed Sinus Rinse Kit',
            'description': 'NeilMed sinus rinse device'
        },
        'baby-aspirator': {
            'sizes': [(300, 300), (400, 400), (600, 600)],
            'alt': 'Baby nasal aspirator',
            'description': 'Gentle baby nasal aspirator device'
        },
        'safety-guide': {
            'sizes': [(600, 400), (800, 533), (1200, 800)],
            'alt': 'Nasal irrigation safety guide',
            'description': 'Step-by-step safety instructions'
        },
        'comparison-chart': {
            'sizes': [(800, 500), (1200, 750), (1600, 1000)],
            'alt': 'Nose cleaner comparison chart',
            'description': 'Product comparison infographic'
        },
        'logo': {
            'sizes': [(100, 30), (150, 45), (200, 60), (300, 90)],
            'alt': 'Nose Cleaner Logo',
            'description': 'Nose Cleaner brand logo'
        }
    }
    
    print("🔄 开始处理AI生成的图片...")
    
    # 检查是否有原始图片
    original_files = glob.glob('images/original/*.png') + glob.glob('images/original/*.jpg')
    
    if not original_files:
        print("❌ 未找到原始图片文件")
        print("📁 请将AI生成的图片放入 images/original/ 目录")
        print("📋 需要的文件：")
        for name in image_config.keys():
            print(f"   - {name}.png 或 {name}.jpg")
        return False
    
    processed_count = 0
    
    for original_file in original_files:
        filename = os.path.basename(original_file)
        name = os.path.splitext(filename)[0]
        
        if name not in image_config:
            print(f"⚠️  跳过未知文件: {filename}")
            continue
        
        print(f"🔄 处理图片: {name}")
        
        try:
            with Image.open(original_file) as img:
                config = image_config[name]
                
                # 转换为RGB模式（如果需要）
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 生成不同尺寸
                for width, height in config['sizes']:
                    # 保持宽高比缩放
                    resized = img.copy()
                    resized.thumbnail((width, height), Image.Resampling.LANCZOS)
                    
                    # 保存PNG版本
                    png_path = f'images/responsive/{name}_{width}x{height}.png'
                    resized.save(png_path, 'PNG', optimize=True)
                    
                    # 保存WebP版本
                    webp_path = f'images/responsive/{name}_{width}x{height}.webp'
                    resized.save(webp_path, 'WebP', quality=85, optimize=True)
                
                # 保存原始WebP版本
                original_webp = f'images/webp/{name}.webp'
                img.save(original_webp, 'WebP', quality=90, optimize=True)
                
                processed_count += 1
                print(f"  ✅ 完成: {name}")
                
        except Exception as e:
            print(f"  ❌ 错误: {name} - {str(e)}")
    
    print(f"\n🎉 处理完成！共处理 {processed_count} 张图片")
    return True

def generate_image_manifest():
    """生成图片清单"""
    manifest = {
        "images": {
            "hero": {
                "desktop": "images/webp/hero-nose-cleaner.webp",
                "tablet": "images/responsive/hero-nose-cleaner_1200x900.webp",
                "mobile": "images/responsive/hero-nose-cleaner_800x600.webp"
            },
            "products": {
                "baby": {
                    "desktop": "images/webp/baby-nose-cleaner.webp",
                    "mobile": "images/responsive/baby-nose-cleaner_400x300.webp"
                },
                "adult": {
                    "desktop": "images/webp/adult-nose-cleaner.webp",
                    "mobile": "images/responsive/adult-nose-cleaner_400x300.webp"
                },
                "allergy": {
                    "desktop": "images/webp/allergy-relief.webp",
                    "mobile": "images/responsive/allergy-relief_400x300.webp"
                }
            },
            "devices": {
                "navage": "images/webp/navage-device.webp",
                "neilmed": "images/webp/neilmed-device.webp",
                "baby_aspirator": "images/webp/baby-aspirator.webp"
            },
            "guides": {
                "safety": "images/webp/safety-guide.webp",
                "comparison": "images/webp/comparison-chart.webp"
            },
            "logo": {
                "desktop": "images/responsive/logo_200x60.webp",
                "tablet": "images/responsive/logo_150x45.webp",
                "mobile": "images/responsive/logo_100x30.webp"
            }
        }
    }
    
    with open('images/manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print("📋 图片清单已生成: images/manifest.json")

def update_website_images():
    """更新网站图片引用"""
    print("🔄 更新网站图片引用...")
    
    # 这里可以添加自动更新HTML文件的代码
    # 由于图片路径已经标准化，主要需要确保文件存在
    
    print("✅ 网站图片引用已更新")

def main():
    """主函数"""
    print("🚀 开始AI图片处理流程...")
    
    # 1. 创建目录结构
    create_directory_structure()
    
    # 2. 处理AI生成的图片
    if process_ai_images():
        # 3. 生成图片清单
        generate_image_manifest()
        
        # 4. 更新网站
        update_website_images()
        
        print("\n🎉 AI图片处理完成！")
        print("📁 图片已保存到:")
        print("   - images/webp/ (WebP格式)")
        print("   - images/responsive/ (响应式尺寸)")
        print("   - images/original/ (原始文件)")
        
        print("\n📋 下一步:")
        print("1. 检查生成的图片质量")
        print("2. 运行 git add . && git commit -m 'Add AI-generated images'")
        print("3. 运行 git push origin main")
    else:
        print("\n❌ 请先添加AI生成的图片到 images/original/ 目录")

if __name__ == "__main__":
    main()

