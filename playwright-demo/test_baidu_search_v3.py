"""百度搜索自动化测试 V3 - 企业级版本"""

import time
import urllib.parse
import pytest
from playwright.sync_api import sync_playwright, Page, Browser


class TestBaiduSearch:
    """百度搜索测试套件"""
    
    @pytest.fixture(scope="function")
    def browser_page(self):
        """浏览器和页面fixture"""
        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(
                headless=False,
                slow_mo=300,
                executable_path=r"C:\Users\zhousicheng\AppData\Local\ms-playwright\chromium-1208\chrome-win64\chrome.exe"
            )
            
            # 创建上下文和页面
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                locale="zh-CN"
            )
            page = context.new_page()
            
            # 设置默认超时时间（30秒）
            page.set_default_timeout(30000)
            
            yield page
            
            # 清理资源
            context.close()
            browser.close()
    
    def test_baidu_search_github_pr(self, browser_page: Page):
        """测试搜索GitHub PR流程"""
        page = browser_page
        keyword = "GitHub PR流程"
        
        # 步骤1: 构造并访问搜索URL
        encoded_keyword = urllib.parse.quote(keyword)
        search_url = f"https://www.baidu.com/s?wd={encoded_keyword}"
        
        print(f"\n[步骤1] 访问搜索URL: {search_url}")
        page.goto(search_url, wait_until="domcontentloaded")
        time.sleep(2)  # 等待动态内容加载
        
        # 步骤2: 验证页面标题
        print("[步骤2] 验证页面标题")
        page_title = page.title()
        print(f"  页面标题: {page_title}")
        
        assert any(kw in page_title for kw in ["GitHub", "PR", keyword]), \
            f"标题验证失败: {page_title}"
        
        # 步骤3: 验证搜索结果存在
        print("[步骤3] 验证搜索结果")
        page.wait_for_selector("#content_left", timeout=10000)
        
        results = page.locator("#content_left .result").all()
        result_count = len(results)
        print(f"  找到 {result_count} 条搜索结果")
        
        assert result_count > 0, "未找到任何搜索结果"
        
        # 步骤4: 验证第一条结果内容
        print("[步骤4] 验证第一条结果")
        first_result = results[0]
        result_text = first_result.inner_text()
        print(f"  第一条结果预览: {result_text[:100]}...")
        
        # 验证页面包含关键词
        page_content = page.content()
        assert "GitHub" in page_content or "PR" in page_content, \
            "搜索结果未包含相关关键词"
        
        print("\n✓ 所有验证通过")
    
    def test_baidu_search_with_screenshot(self, browser_page: Page):
        """测试搜索并截图（用于报告）"""
        page = browser_page
        keyword = "Playwright自动化测试"
        
        # 访问搜索结果
        encoded_keyword = urllib.parse.quote(keyword)
        search_url = f"https://www.baidu.com/s?wd={encoded_keyword}"
        
        print(f"\n[测试] 搜索关键词: {keyword}")
        page.goto(search_url, wait_until="domcontentloaded")
        time.sleep(2)
        
        # 截图保存
        screenshot_path = "test_screenshot.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"  截图已保存: {screenshot_path}")
        
        # 验证
        page.wait_for_selector("#content_left", timeout=10000)
        results = page.locator("#content_left .result").all()
        
        assert len(results) > 0, "未找到搜索结果"
        print(f"  找到 {len(results)} 条结果")


if __name__ == "__main__":
    # 直接运行测试（不生成报告）
    pytest.main([__file__, "-v", "-s"])
