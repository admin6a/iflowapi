#!/usr/bin/env python3
"""
自动更新iFlow API密钥的脚本
通过GitHub Actions定时执行，实现API密钥的自动更新
每日凌晨0:00固定执行 (UTC+8)
"""

import os
import requests
import json
import time
import random
from datetime import datetime
import logging
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 配置UTC+8时区
UTC8 = pytz.timezone('Asia/Shanghai')

# 配置日志
class UTC8Formatter(logging.Formatter):
    """自定义日志格式化器，使用UTC+8时区"""
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=UTC8)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()

# 配置日志处理器
handler = logging.StreamHandler()
handler.setFormatter(UTC8Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# 配置根日志记录器
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)
logger = logging.getLogger(__name__)

class AntiDetectionMechanism:
    """反检测机制实现"""
    
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
        ]
    
    def get_random_user_agent(self):
        """获取随机User-Agent"""
        return random.choice(self.user_agents)
    
    def random_delay(self, min_seconds=2, max_seconds=10):
        """随机延迟"""
        delay = random.uniform(min_seconds, max_seconds)
        logger.info(f"随机延迟 {delay:.2f} 秒")
        time.sleep(delay)
    
    def human_like_delay(self):
        """模拟人类操作的延迟"""
        # 随机短延迟，模拟人类思考时间
        short_delay = random.uniform(0.5, 2.0)
        time.sleep(short_delay)

class APIManager:
    """API管理器，处理API密钥的获取和重置"""
    
    def __init__(self):
        """初始化反检测机制"""
        self.anti_detection = AntiDetectionMechanism()
    
    def _get_headers(self):
        """获取请求头，包含随机User-Agent"""
        return {
            'User-Agent': self.anti_detection.get_random_user_agent(),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/json'
        }
    
    def get_api_key_info(self):
        """获取API密钥信息"""
        cookie = os.getenv('IFLOW_COOKIE')
        if not cookie:
            raise ValueError("IFLOW_COOKIE环境变量未设置")
        
        url = "https://platform.iflow.cn/api/openapi/apikey"
        headers = self._get_headers()
        headers['Cookie'] = cookie
        
        self.anti_detection.random_delay(1, 3)
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"API响应: {json.dumps(data, ensure_ascii=False)}")
            
            return data
            
        except requests.RequestException as e:
            logger.error(f"API请求失败: {e}")
            raise
    
    def simulate_browser_reset(self):
        """模拟浏览器操作重置API密钥"""
        cookie = os.getenv('IFLOW_COOKIE')
        if not cookie:
            raise ValueError("IFLOW_COOKIE环境变量未设置")
        
        logger.info("开始模拟浏览器操作重置API密钥...")
        
        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument(f'--user-agent={self.anti_detection.get_random_user_agent()}')
        
        driver = None
        try:
            # 初始化WebDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 设置cookie并访问页面
            driver.get("https://platform.iflow.cn")
            
            # 解析cookie并设置
            for cookie_item in cookie.split('; '):
                if '=' in cookie_item:
                    name, value = cookie_item.split('=', 1)
                    driver.add_cookie({
                        'name': name.strip(),
                        'value': value.strip(),
                        'domain': 'platform.iflow.cn'
                    })
            
            # 访问API密钥页面
            driver.get("https://platform.iflow.cn/profile?tab=apiKey")
            
            # 等待页面加载
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 增加等待时间，确保页面完全加载
            logger.info("等待页面完全加载...")
            time.sleep(10)
            
            self.anti_detection.human_like_delay()
            
            # 查找并点击按钮 - 基于提供的HTML结构
            button_selectors = [
                ".btn_ib1Q",  # 主要按钮类名
                "div[class*='btn']",  # 包含btn的div
                "button:contains('重置API密钥')",  # 包含特定文本的按钮
                "button:contains('重置')",
                "button:contains('重新生成')",
                "button:contains('生成')",
                "button:contains('Reset')",
                "button:contains('Regenerate')",
                "button:contains('Generate')",
                "button[type='submit']",
                ".btn",
                "button.btn"
            ]
            
            button_found = False
            for selector in button_selectors:
                try:
                    buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                    if buttons:
                        logger.info(f"使用选择器 '{selector}' 找到按钮，准备点击...")
                        # 确保按钮可见且可点击
                        WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        buttons[0].click()
                        button_found = True
                        break
                except Exception as e:
                    logger.debug(f"选择器 '{selector}' 未找到按钮或不可点击: {e}")
            
            if not button_found:
                # 如果所有CSS选择器都失败，尝试XPath查找
                xpath_selectors = [
                    "//div[contains(@class, 'btn') and contains(text(), '重置API密钥')]",
                    "//button[contains(text(), '重置API密钥')]",
                    "//div[contains(text(), '重置API密钥')]",
                    "//*[contains(text(), '重置API密钥')]",
                    "//button[contains(text(), '重置')]",
                    "//button[contains(text(), '重新生成')]"
                ]
                
                for xpath in xpath_selectors:
                    try:
                        buttons = driver.find_elements(By.XPATH, xpath)
                        if buttons:
                            logger.info(f"使用XPath '{xpath}' 找到按钮，准备点击...")
                            WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, xpath))
                            )
                            buttons[0].click()
                            button_found = True
                            break
                    except Exception as e:
                        logger.debug(f"XPath '{xpath}' 查找按钮失败: {e}")
            
            if button_found:
                # 等待操作完成
                logger.info("等待操作完成...")
                time.sleep(8)  # 增加等待时间确保操作完成
                
                # 重新获取API密钥信息
                self.anti_detection.random_delay(3, 7)
                api_info = self.get_api_key_info()
                
                # 修复逻辑：hasExpired为false表示未过期，true表示已过期
                data = api_info.get('data', {})
                has_expired = data.get('hasExpired', True)
                
                if not has_expired:
                    logger.info("API密钥重置成功")
                    return True
                else:
                    logger.warning("重新生成后API仍然过期")
                    return False
            else:
                logger.warning("未找到按钮元素，尝试截图保存页面状态")
                # 保存页面截图和HTML源码用于调试
                try:
                    driver.save_screenshot("page_debug.png")
                    with open("page_source.html", "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    logger.info("页面截图和源码已保存用于调试")
                except Exception as e:
                    logger.error(f"保存调试信息失败: {e}")
                return False
                
        except Exception as e:
            logger.error(f"浏览器模拟操作失败: {e}")
            return False
        finally:
            if driver:
                driver.quit()
    
    def check_api_expiration(self, api_data):
        """检查API是否过期"""
        if not api_data:
            logger.error("API响应数据为空")
            return False
            
        data = api_data.get('data', {})
        has_expired = data.get('hasExpired', True)
        
        logger.info(f"API过期状态: {has_expired}")
        
        # 修复逻辑：hasExpired为false表示未过期，true表示已过期
        if has_expired:
            logger.info("API密钥已过期，需要重置")
            return True
        else:
            logger.info("API密钥未过期，无需重置")
            return False
    
    def run_auto_update(self):
        """执行自动更新流程"""
        logger.info("开始执行自动更新流程...")
        
        try:
            # 步骤1: 获取API密钥信息
            api_info = self.get_api_key_info()
            
            # 步骤2: 检查是否过期
            is_expired = self.check_api_expiration(api_info)
            
            if is_expired:
                # API已过期，执行浏览器模拟重置操作
                logger.info("API密钥已过期，开始模拟浏览器操作重置...")
                success = self.simulate_browser_reset()
                
                if success:
                    logger.info("浏览器模拟重置操作成功，API密钥已更新")
                    logger.info("下次执行：每日凌晨0:00 (UTC+8)")
                    return True
                else:
                    logger.error("浏览器模拟重置操作失败")
                    return False
            else:
                # 检查API是否即将过期（expireTime与今天日期相同）
                data = api_info.get('data', {})
                expire_time = data.get('expireTime', '')
                
                if expire_time:
                    try:
                        # 解析expireTime格式：yyyy-MM-dd HH:mm
                        expire_date = datetime.strptime(expire_time, '%Y-%m-%d %H:%M').date()
                        # 获取当前系统日期（UTC+8）
                        current_date = datetime.now(UTC8).date()
                        
                        if expire_date == current_date:
                            logger.info("API密钥即将过期，开始模拟浏览器操作重置...")
                            success = self.simulate_browser_reset()
                            
                            if success:
                                logger.info("浏览器模拟重置操作成功，API密钥已更新")
                                logger.info("下次执行：每日凌晨0:00 (UTC+8)")
                                return True
                            else:
                                logger.error("浏览器模拟重置操作失败")
                                return False
                    except ValueError as e:
                        logger.debug(f"解析expireTime失败: {e}")
                
                # API未过期，不执行重置操作
                logger.info("API密钥未过期，跳过重置操作")
                logger.info("下次执行：每日凌晨0:00 (UTC+8)")
                return True
                    
        except Exception as e:
            logger.error(f"自动更新流程执行失败: {e}")
            return False

def main():
    """主函数"""
    try:
        api_manager = APIManager()
        success = api_manager.run_auto_update()
        
        if success:
            logger.info("自动更新流程执行成功")
            exit(0)
        else:
            logger.error("自动更新流程执行失败")
            exit(1)
            
    except Exception as e:
        logger.error(f"程序执行异常: {e}")
        exit(1)

if __name__ == "__main__":
    main()
