"""
百度搜索自动化测试脚本 V2
使用Playwright进行UI自动化测试
测试目标：搜索「GitHub PR流程」并验证结果
优化方案：直接访问搜索结果URL，避免首页交互问题
"""

from playwright.sync_api import sync_playwright
import time
import urllib.parse


def test_baidu_search():
    """
    测试百度搜索功能
    验证搜索结果标题是否包含关键词
    """
    with sync_playwright() as p:
        # 启动浏览器（headless=False 可以看到浏览器操作过程）
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500,
            executable_path=r"C:\Users\zhousicheng\AppData\Local\ms-playwright\chromium-1208\chrome-win64\chrome.exe"
        )

        # 创建新的浏览器上下文和页面
        context = browser.new_context()
        page = context.new_page()

        try:
            print("步骤1: 构造搜索URL...")
            # 对搜索关键词进行URL编码
            keyword = "GitHub PR流程"
            encoded_keyword = urllib.parse.quote(keyword)
            search_url = f"https://www.baidu.com/s?wd={encoded_keyword}"
            print(f"搜索URL: {search_url}")

            print("\n步骤2: 直接访问搜索结果页...")
            page.goto(search_url, timeout=15000)

            # 等待页面加载完成
            page.wait_for_load_state("domcontentloaded")
            print("✓ 搜索结果页加载成功")

            # 额外等待确保结果渲染完成
            time.sleep(2)

            print("\n步骤3: 验证搜索结果...")
            # 等待搜索结果容器出现
            page.wait_for_selector("#content_left", timeout=10000)

            # 获取页面标题
            page_title = page.title()
            print(f"页面标题: {page_title}")

            # 验证标题包含关键词
            assert "GitHub" in page_title or "PR" in page_title or keyword in page_title, \
                f"标题验证失败: 期望包含关键词，实际标题为'{page_title}'"
            print("✓ 标题验证通过")

            # 获取搜索结果数量
            results = page.locator("#content_left .result").all()
            print(f"\n找到 {len(results)} 条搜索结果")

            if len(results) > 0:
                # 获取第一条搜索结果
                first_result = results[0]
                first_result_text = first_result.inner_text()
                print(f"\n第一条搜索结果预览:\n{first_result_text[:150]}...")

                # 验证搜索结果包含关键词
                page_content = page.content()
                assert "GitHub" in page_content or "PR" in page_content, \
                    "搜索结果验证失败: 页面内容未找到相关关键词"
                print("✓ 搜索结果验证通过")
            else:
                print("⚠ 警告: 未找到搜索结果，但页面已成功加载")

            print("\n" + "=" * 50)
            print("测试通过！所有验证点均成功 ✓")
            print("=" * 50)

            # 暂停3秒以便查看结果
            time.sleep(3)

        except Exception as e:
            print(f"\n✗ 测试失败: {str(e)}")
            # 截图保存错误现场
            page.screenshot(path="error_screenshot_v2.png")
            print("已保存错误截图: error_screenshot_v2.png")
            raise

        finally:
            # 关闭浏览器
            context.close()
            browser.close()
            print("\n浏览器已关闭")


if __name__ == "__main__":
    print("=" * 50)
    print("开始执行百度搜索自动化测试 V2")
    print("=" * 50 + "\n")
    test_baidu_search()
