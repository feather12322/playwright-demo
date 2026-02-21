# 百度搜索自动化测试脚本

基于Playwright的UI自动化测试，用于测试百度搜索功能。

## 版本说明

- `test_baidu_search.py` - V1: 基础版本，模拟首页输入
- `test_baidu_search_v2.py` - V2: 优化版本，直接访问搜索结果
- `test_baidu_search_v3.py` - V3: 企业级版本，包含测试报告和完整配置

## 功能特性（V3版本）

- ✅ 自动生成HTML测试报告
- ✅ 失败自动截图
- ✅ 完善的超时处理（30秒默认超时）
- ✅ 符合PEP8规范
- ✅ 使用pytest框架和fixture
- ✅ 支持多个测试用例
- ✅ 详细的日志输出

## 环境要求

- Python 3.8 或更高版本
- Windows/Linux/macOS 操作系统

## 安装步骤

### 1. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 2. 安装Playwright浏览器驱动

```bash
playwright install chromium
```

## 运行测试

### 方式1：生成HTML报告（推荐）

```bash
python run_tests.py
```

这会自动运行测试并生成带时间戳的HTML报告，例如：`report_20260221_143000.html`

### 方式2：使用pytest命令

```bash
# 生成HTML报告
pytest test_baidu_search_v3.py -v -s --html=report.html --self-contained-html

# 不生成报告，直接运行
pytest test_baidu_search_v3.py -v -s
```

### 方式3：直接运行脚本

```bash
python test_baidu_search_v3.py
```

## 测试报告说明

HTML报告包含：
- 测试执行时间
- 测试用例通过/失败状态
- 详细的错误信息
- 失败时的自动截图
- 测试环境信息

报告文件可以直接在浏览器中打开查看。

## 配置文件说明

- `pytest.ini` - pytest配置文件
- `conftest.py` - pytest钩子和fixture配置
- `requirements.txt` - Python依赖列表
- `run_tests.py` - 测试运行脚本

## 验证测试是否成功

### 1. 查看控制台输出

成功时会显示：
```
[步骤1] 访问搜索URL: ...
[步骤2] 验证页面标题
  页面标题: GitHub PR流程_百度搜索
[步骤3] 验证搜索结果
  找到 10 条搜索结果
[步骤4] 验证第一条结果
  第一条结果预览: ...

✓ 所有验证通过

PASSED
```

### 2. 查看HTML报告

打开生成的 `report_*.html` 文件，查看：
- 绿色 PASSED 表示测试通过
- 红色 FAILED 表示测试失败
- 点击测试用例可查看详细日志

### 3. 检查退出码

```bash
echo %ERRORLEVEL%  # Windows
echo $?            # Linux/macOS
```
- 返回 0 表示所有测试通过
- 返回非0 表示有测试失败

## V3版本改进

### 1. 测试报告功能
- 使用 pytest-html 生成美观的HTML报告
- 失败时自动截图并附加到报告
- 包含测试环境元数据

### 2. 超时处理优化
- 设置默认超时30秒（`page.set_default_timeout(30000)`）
- 针对不同操作设置合适的超时时间
- 添加显式等待确保页面加载完成

### 3. 代码规范
- 符合PEP8规范
- 使用类组织测试用例
- 使用pytest fixture管理资源
- 注释简洁明了

### 4. 其他改进
- 使用pytest框架，支持更多功能
- 支持多个测试用例
- 更好的错误处理和日志输出
- 配置文件分离，便于维护

## 常见问题

### 1. 浏览器未安装
```bash
playwright install chromium
```

### 2. 依赖包缺失
```bash
pip install -r requirements.txt
```

### 3. 修改浏览器路径
编辑 `test_baidu_search_v3.py`，修改 `executable_path` 参数

### 4. 无头模式运行
将 `headless=False` 改为 `headless=True`

## 扩展功能

### 添加新的测试用例

在 `test_baidu_search_v3.py` 中添加新方法：

```python
def test_your_new_case(self, browser_page: Page):
    """你的测试用例描述"""
    page = browser_page
    # 测试逻辑
    pass
```

### 使用测试标记

```python
@pytest.mark.smoke
def test_smoke_case(self, browser_page: Page):
    """冒烟测试用例"""
    pass
```

运行特定标记的测试：
```bash
pytest -m smoke
```
