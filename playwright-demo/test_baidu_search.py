"""
百度搜索自动化测试脚本
使用Playwright进行UI自动化测试
测试目标：搜索「GitHub PR流程」并验证结果
"""

from playwright.sync_api import sync_playwright, expect
import time


def test_baidu_search():
    """
    测试百度搜索功能
    验证搜索结果标题是否包含关键词
    """
    with sync_playwright() as p:
        # 启动浏览器（headless=False 可以看到浏览器操作过程）
        # 指定浏览器可执行文件路径（适用于离线安装）
        browser = p.chromium.launch(
            headless=False, 
            slow_mo=500,
            executable_path=r"C:\Users\zhousicheng\AppData\Local\ms-playwright\chromium-1208\chrome-win64\chrome.exe"
        )
        
        # 创建新的浏览器上下文和页面
        context = browser.new_context()
        page = context.new_page()
        
        try:
            print("步骤1: 访问百度首页...")
            page.goto("https://www.baidu.com", timeout=15000)
            
            # 等待页面加载完成
            page.wait_for_load_state("domcontentloaded")
            print("✓ 百度首页加载成功")
            
            print("\n步骤2: 输入搜索关键词...")
            # 百度首页可能显示文心一言等特殊版本，搜索框被隐藏
            # 等待元素存在（不要求可见）
            page.wait_for_selector("#kw", state="attached", timeout=5000)
            
            # 使用JavaScript强制显示元素并设置值
            page.evaluate("""
                // 找到搜索框
                const input = document.querySelector('#kw');
                const form = document.querySelector('#form');
                const button = document.querySelector('#su');
                
                // 强制显示所有相关元素
                if (input) {
                    input.style.display = 'block';
                    input.style.visibility = 'visible';
                    input.style.opacity = '1';
                    input.style.position = 'relative';
                    input.value = 'GitHub PR流程';
                }
                
                if (button) {
                    button.style.display = 'block';
                    button.style.visibility = 'visible';
                    button.style.opacity = '1';
                    button.style.position = 'relative';
                }
                
                if (form) {
                    form.style.display = 'block';
                    form.style.visibility = 'visible';
                }
            """)
            
            # 等待一下让页面更新
            time.sleep(1)
            print("✓ 已输入关键词: GitHub PR流程")
            
            print("\n步骤3: 提交搜索...")
            # 尝试多种方式提交搜索
            search_submitted = page.evaluate("""
                () => {
                    const input = document.querySelector('#kw');
                    const button = document.querySelector('#su');
                    const form = document.querySelector('#form');
                    
                    // 方式1: 点击搜索按钮
                    if (button) {
                        try {
                            button.click();
                            return 'button_click';
                        } catch(e) {}
                    }
                    
                    // 方式2: 提交表单
                    if (form) {
                        try {
                            form.submit();
                            return 'form_submit';
                        } catch(e) {}
                    }
                    
                    // 方式3: 模拟回车键
                    if (input) {
                        try {
                            const event = new KeyboardEvent('keydown', {
                                key: 'Enter',
                                code: 'Enter',
                                keyCode: 13,
                                bubbles: true
                            });
                            input.dispatchEvent(event);
                            return 'enter_key';
                        } catch(e) {}
                    }
                    
                    return 'failed';
                }
            """)
            print(f"✓ 搜索提交方式: {search_submitted}")
            
            # 等待搜索结果加载
            page.wait_for_load_state("domcontentloaded")
            # 额外等待确保结果渲染完成
            time.sleep(2)
            print("✓ 搜索完成")
            
            print("\n步骤4: 验证搜索结果...")
            # 等待搜索结果容器出现
            page.wait_for_selector("#content_left", timeout=10000)
            
            # 获取页面标题
            page_title = page.title()
            print(f"页面标题: {page_title}")
            
            # 验证标题包含关键词
            assert "GitHub" in page_title or "PR" in page_title, \
                f"标题验证失败: 期望包含'GitHub'或'PR'，实际标题为'{page_title}'"
            print("✓ 标题验证通过")
            
            # 获取第一条搜索结果
            first_result = page.locator("#content_left .result").first
            first_result_text = first_result.inner_text()
            print(f"\n第一条搜索结果预览:\n{first_result_text[:100]}...")
            
            # 验证搜索结果包含关键词
            assert "GitHub" in first_result_text or "PR" in first_result_text, \
                "搜索结果验证失败: 未找到相关关键词"
            print("✓ 搜索结果验证通过")
            
            print("\n" + "="*50)
            print("测试通过！所有验证点均成功 ✓")
            print("="*50)
            
            # 暂停3秒以便查看结果
            time.sleep(3)
            
        except Exception as e:
            print(f"\n✗ 测试失败: {str(e)}")
            # 截图保存错误现场
            page.screenshot(path="error_screenshot.png")
            print("已保存错误截图: error_screenshot.png")
            raise
            
        finally:
            # 关闭浏览器
            context.close()
            browser.close()
            print("\n浏览器已关闭")


if __name__ == "__main__":
    print("="*50)
    print("开始执行百度搜索自动化测试")
    print("="*50 + "\n")
    test_baidu_search()
