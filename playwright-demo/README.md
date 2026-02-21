# 百度搜索自动化测试脚本

基于Playwright的UI自动化测试，用于测试百度搜索功能。

## 功能说明

- 自动访问百度首页
- 搜索关键词「GitHub PR流程」
- 验证搜索结果标题和内容包含相关关键词
- 自动截图保存错误现场（如果测试失败）

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

如果需要安装所有浏览器（可选）：
```bash
playwright install
```

## 运行测试

### 方式1：直接运行脚本

```bash
python test_baidu_search.py
```

### 方式2：使用pytest运行

```bash
pytest test_baidu_search.py -v -s
```

参数说明：
- `-v`: 显示详细输出
- `-s`: 显示print输出

## 预期结果

测试成功时，你会看到：

```
==================================================
开始执行百度搜索自动化测试
==================================================

步骤1: 访问百度首页...
✓ 百度首页加载成功

步骤2: 输入搜索关键词...
✓ 已输入关键词: GitHub PR流程

步骤3: 点击搜索按钮...
✓ 搜索完成

步骤4: 验证搜索结果...
页面标题: GitHub PR流程_百度搜索
✓ 标题验证通过

第一条搜索结果预览:
...

✓ 搜索结果验证通过

==================================================
测试通过！所有验证点均成功 ✓
==================================================

浏览器已关闭
```

## 验证脚本是否正确运行

### 1. 观察浏览器行为
- 脚本运行时会自动打开Chrome浏览器
- 你可以看到浏览器自动执行以下操作：
  - 打开百度首页
  - 在搜索框输入「GitHub PR流程」
  - 点击搜索按钮
  - 显示搜索结果

### 2. 检查控制台输出
- 每个步骤都会在控制台输出执行状态
- 所有步骤前面都有 ✓ 标记表示成功
- 最后显示"测试通过！所有验证点均成功 ✓"

### 3. 检查退出码
```bash
echo %ERRORLEVEL%  # Windows
echo $?            # Linux/macOS
```
- 返回 0 表示测试成功
- 返回非0 表示测试失败

### 4. 查看错误截图（如果失败）
- 如果测试失败，会在当前目录生成 `error_screenshot.png`
- 打开图片可以看到失败时的页面状态

## 常见问题

### 1. 浏览器未安装
错误信息：`Executable doesn't exist`

解决方法：
```bash
playwright install chromium
```

### 2. 网络连接问题
如果无法访问百度，检查网络连接或修改timeout时间：
```python
page.goto("https://www.baidu.com", timeout=30000)  # 增加到30秒
```

### 3. 元素定位失败
百度页面可能更新，如果定位器失效，可以：
- 打开百度首页
- 按F12打开开发者工具
- 检查搜索框和按钮的实际ID或选择器

## 自定义配置

### 修改为无头模式（后台运行）
```python
browser = p.chromium.launch(headless=True)
```

### 修改搜索关键词
```python
search_input.fill("你的关键词")
```

### 调整操作速度
```python
browser = p.chromium.launch(headless=False, slow_mo=1000)  # 每步延迟1秒
```
