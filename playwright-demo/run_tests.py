"""测试运行脚本 - 生成HTML报告"""

import pytest
import sys
from datetime import datetime


def run_tests_with_report():
    """运行测试并生成HTML报告"""
    
    # 生成报告文件名（带时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"report_{timestamp}.html"
    
    # pytest参数配置
    args = [
        "test_baidu_search_v3.py",  # 测试文件
        "-v",                        # 详细输出
        "-s",                        # 显示print输出
        f"--html={report_file}",     # HTML报告
        "--self-contained-html",     # 单文件报告
        "--tb=short",                # 简短的错误回溯
    ]
    
    print("=" * 60)
    print("开始执行测试...")
    print(f"报告将保存到: {report_file}")
    print("=" * 60 + "\n")
    
    # 运行测试
    exit_code = pytest.main(args)
    
    print("\n" + "=" * 60)
    if exit_code == 0:
        print("✓ 测试全部通过")
    else:
        print("✗ 部分测试失败")
    print(f"详细报告: {report_file}")
    print("=" * 60)
    
    return exit_code


if __name__ == "__main__":
    sys.exit(run_tests_with_report())
