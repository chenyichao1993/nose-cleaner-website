#!/usr/bin/env python3
"""
多产品Amazon信息自动更新脚本
支持同时更新多个Amazon产品的价格、评分等信息
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time

class MultiProductUpdater:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 产品配置
        self.products = {
            'neilmed': {
                'name': 'NeilMed Sinus Rinse Kit',
                'url': 'https://www.amazon.com/NeilMed-100-Sinus-Rinse-Complete/dp/B000RDZFZ0',
                'html_selector': 'neilmed',  # 用于在HTML中定位
                'asin': 'B000RDZFZ0'
            },
            'nosefrida': {
                'name': 'NoseFrida Baby Nasal Aspirator',
                'url': 'https://www.amazon.com/Fridababy-NoseFrida-Aspirator-Hygiene-Filters/dp/B00RP0GHBO',
                'html_selector': 'nosefrida',
                'asin': 'B00RP0GHBO'
            },
            'navage': {
                'name': 'Naväge Nasal Care Starter Kit',
                'url': 'https://www.amazon.com/Naväge-Nasal-Care-Starter-Kit/dp/B000FOBMOC',
                'html_selector': 'navage',
                'asin': 'B000FOBMOC'
            }
        }
        
    def get_product_data(self, product_key):
        """从Amazon页面获取产品数据"""
        product = self.products[product_key]
        url = product['url']
        
        try:
            print(f"🔄 正在获取 {product['name']} 的数据...")
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 提取产品数据
            data = {
                'product_key': product_key,
                'name': product['name'],
                'url': url,
                'asin': product['asin'],
                'last_updated': datetime.now().isoformat()
            }
            
            # 提取价格信息
            price_data = self.extract_price(soup)
            data.update(price_data)
            
            # 提取评分信息
            rating_data = self.extract_rating(soup)
            data.update(rating_data)
            
            # 提取产品标题
            title = self.extract_title(soup)
            if title:
                data['title'] = title
            
            print(f"✅ 成功获取 {product['name']} 数据")
            return data
            
        except Exception as e:
            print(f"❌ 获取 {product['name']} 数据失败: {e}")
            return None
    
    def extract_price(self, soup):
        """提取价格信息"""
        price_data = {
            'current_price': None,
            'original_price': None,
            'discount': None
        }
        
        # 多种价格选择器
        price_selectors = [
            '.a-price-whole',
            '.a-price .a-offscreen',
            '#price_inside_buybox',
            '.a-price-range .a-offscreen',
            '.a-price .a-price-whole'
        ]
        
        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                price_text = price_elem.get_text().strip()
                price_match = re.search(r'[\d,]+\.?\d*', price_text)
                if price_match:
                    price_data['current_price'] = f"${price_match.group()}"
                    break
        
        # 查找原价
        original_selectors = [
            '.a-text-price .a-offscreen',
            '.a-price-was .a-offscreen',
            '.a-price .a-text-price .a-offscreen'
        ]
        
        for selector in original_selectors:
            original_elem = soup.select_one(selector)
            if original_elem:
                original_text = original_elem.get_text().strip()
                price_match = re.search(r'[\d,]+\.?\d*', original_text)
                if price_match:
                    price_data['original_price'] = f"${price_match.group()}"
                    break
        
        # 查找折扣
        discount_selectors = [
            '.a-badge-text',
            '.a-size-large .a-color-price',
            '.a-color-price'
        ]
        
        for selector in discount_selectors:
            discount_elem = soup.select_one(selector)
            if discount_elem:
                discount_text = discount_elem.get_text().strip()
                discount_match = re.search(r'-?\d+%', discount_text)
                if discount_match:
                    price_data['discount'] = discount_match.group()
                    break
        
        return price_data
    
    def extract_rating(self, soup):
        """提取评分信息"""
        rating_data = {
            'rating': None,
            'review_count': None,
            'stars': None
        }
        
        # 查找评分
        rating_selectors = [
            '.a-icon-alt',
            '.a-icon-star .a-icon-alt',
            '#acrPopover .a-icon-alt'
        ]
        
        for selector in rating_selectors:
            rating_elem = soup.select_one(selector)
            if rating_elem:
                rating_text = rating_elem.get_text().strip()
                rating_match = re.search(r'(\d+\.?\d*)\s+out\s+of\s+5', rating_text)
                if rating_match:
                    rating_data['rating'] = rating_match.group(1)
                    
                    # 生成星级
                    rating_float = float(rating_match.group(1))
                    full_stars = int(rating_float)
                    half_star = 1 if rating_float - full_stars >= 0.5 else 0
                    empty_stars = 5 - full_stars - half_star
                    
                    stars = '★' * full_stars + '☆' * half_star + '☆' * empty_stars
                    rating_data['stars'] = stars
                    break
        
        # 查找评论数量
        review_selectors = [
            '#acrCustomerReviewText',
            '.a-size-base .a-link-normal',
            '.a-size-base'
        ]
        
        for selector in review_selectors:
            review_elem = soup.select_one(selector)
            if review_elem:
                review_text = review_elem.get_text().strip()
                review_match = re.search(r'([\d,]+)', review_text)
                if review_match:
                    rating_data['review_count'] = review_match.group(1)
                    break
        
        return rating_data
    
    def extract_title(self, soup):
        """提取产品标题"""
        title_selectors = [
            '#productTitle',
            '.product-title',
            'h1'
        ]
        
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                return title_elem.get_text().strip()
        return None
    
    def update_html_file(self, all_products_data, html_file='index.html'):
        """更新HTML文件中的产品信息 - 只更新价格、评分、评论数量"""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            updated_count = 0
            
            for product_data in all_products_data:
                if not product_data:
                    continue
                
                product_key = product_data['product_key']
                print(f"🔄 更新HTML中的 {product_data['name']}...")
                
                # 只更新价格、评分、评论数量，不更新标题和描述
                if product_key == 'neilmed':
                    # 更新NeilMed产品信息
                    if product_data['price']:
                        content = re.sub(
                            r'<span class="price">\$[\d,]+\.?\d*</span>',
                            f'<span class="price">{product_data["price"]}</span>',
                            content
                        )
                    
                    if product_data['original_price']:
                        content = re.sub(
                            r'<span class="original-price">\$[\d,]+\.?\d*</span>',
                            f'<span class="original-price">{product_data["original_price"]}</span>',
                            content
                        )
                    
                    if product_data['discount']:
                        content = re.sub(
                            r'<span class="discount">-\d+%</span>',
                            f'<span class="discount">{product_data["discount"]}</span>',
                            content
                        )
                    
                    if product_data['rating'] and product_data['review_count']:
                        rating_pattern = r'<span class="rating-text">\d+\.?\d*/5 \([\d,]+ reviews\)</span>'
                        replacement = f'<span class="rating-text">{product_data["rating"]}/5 ({product_data["review_count"]} reviews)</span>'
                        content = re.sub(rating_pattern, replacement, content)
                    
                    if product_data['stars']:
                        content = re.sub(
                            r'<span class="stars">[★☆]+</span>',
                            f'<span class="stars">{product_data["stars"]}</span>',
                            content
                        )
                
                elif product_key == 'nosefrida':
                    # 更新NoseFrida产品信息
                    if product_data['price']:
                        content = re.sub(
                            r'<span class="price">\$[\d,]+\.?\d*</span>',
                            f'<span class="price">{product_data["price"]}</span>',
                            content
                        )
                    
                    if product_data['original_price']:
                        content = re.sub(
                            r'<span class="original-price">\$[\d,]+\.?\d*</span>',
                            f'<span class="original-price">{product_data["original_price"]}</span>',
                            content
                        )
                    
                    if product_data['discount']:
                        content = re.sub(
                            r'<span class="discount">-\d+%</span>',
                            f'<span class="discount">{product_data["discount"]}</span>',
                            content
                        )
                    
                    if product_data['rating'] and product_data['review_count']:
                        rating_pattern = r'<span class="rating-text">\d+\.?\d*/5 \([\d,]+ reviews\)</span>'
                        replacement = f'<span class="rating-text">{product_data["rating"]}/5 ({product_data["review_count"]} reviews)</span>'
                        content = re.sub(rating_pattern, replacement, content)
                    
                    if product_data['stars']:
                        content = re.sub(
                            r'<span class="stars">[★☆]+</span>',
                            f'<span class="stars">{product_data["stars"]}</span>',
                            content
                        )
                
                updated_count += 1
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 成功更新 {updated_count} 个产品的价格和评分信息")
            return True
            
        except Exception as e:
            print(f"❌ 更新HTML文件失败: {e}")
            return False
    
    def save_data_to_json(self, all_products_data, filename='all_products_data.json'):
        """保存所有产品数据到JSON文件"""
        try:
            data = {
                'last_updated': datetime.now().isoformat(),
                'products': all_products_data
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ 所有产品数据已保存到 {filename}")
        except Exception as e:
            print(f"❌ 保存数据失败: {e}")
    
    def run_update(self):
        """运行完整更新流程"""
        print("🚀 开始更新所有Amazon产品数据...")
        print(f"📅 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        all_products_data = []
        
        # 获取所有产品数据
        for product_key in self.products.keys():
            product_data = self.get_product_data(product_key)
            if product_data:
                all_products_data.append(product_data)
            
            # 添加延迟避免被Amazon限制
            time.sleep(2)
        
        if all_products_data:
            # 更新HTML文件
            self.update_html_file(all_products_data)
            
            # 保存数据到JSON
            self.save_data_to_json(all_products_data)
            
            print("✅ 所有产品更新完成!")
            
            # 显示更新摘要
            print("\n📊 更新摘要:")
            for data in all_products_data:
                print(f"  {data['name']}: {data.get('current_price', 'N/A')} ({data.get('rating', 'N/A')}/5)")
        else:
            print("❌ 没有成功获取任何产品数据")

def main():
    """主函数"""
    updater = MultiProductUpdater()
    updater.run_update()

if __name__ == "__main__":
    main()
