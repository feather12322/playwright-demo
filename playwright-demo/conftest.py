"""Pytest配置文件"""

import pytest
from datetime import datetime


def pytest_configure(config):
    """配置pytest元数据"""
    # 只有在pytest-html插件存在时才设置元数据
    if hasattr(config, '_metadata'):
        config._metadata.update({
            "项目": "百度搜索自动化测试",
            "环境": "Windows",
            "浏览器": "Chromium",
            "框架": "Playwright + Pytest",
            "执行时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试执行钩子"""
    outcome = yield
    report = outcome.get_result()
    
    # 测试失败时的处理
    if report.when == "call" and report.failed:
        print(f"\n测试失败: {item.name}")
        
        # 尝试获取页面对象并截图
        try:
            if hasattr(item, "funcargs") and "browser_page" in item.funcargs:
                page = item.funcargs["browser_page"]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"failure_{item.name}_{timestamp}.png"
                page.screenshot(path=screenshot_path)
                print(f"失败截图: {screenshot_path}")
        except Exception as e:
            print(f"截图失败: {e}")
