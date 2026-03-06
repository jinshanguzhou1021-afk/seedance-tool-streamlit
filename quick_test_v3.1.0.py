#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V3.1.0 快速测试和发布脚本
"""

import sys
import json
import ast
import time
from datetime import datetime
from openai import OpenAI

print("=" * 70)
print("🧪 V3.1.0 - 快速测试和发布")
print("=" * 70)
print()

# 版本信息
VERSION = "V3.1.0"
VERSION_DATE = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"版本：{VERSION}")
print(f"日期：{VERSION_DATE}")
print()

# 1. 模块导入测试
print("📌 1. 模块导入测试")
print("-" * 70)

modules_tested = 0
modules_passed = 0

try:
    import streamlit as st
    print("✓ streamlit")
    modules_tested += 1
    modules_passed += 1
except ImportError as e:
    print(f"✗ streamlit: {e}")
    modules_tested += 1

try:
    from openai import OpenAI
    print("✓ openai")
    modules_tested += 1
    modules_passed += 1
except ImportError as e:
    print(f"✗ openai: {e}")
    modules_tested += 1

try:
    import json
    print("✓ json")
    modules_tested += 1
    modules_passed += 1
except ImportError as e:
    print(f"✗ json: {e}")
    modules_tested += 1

try:
    import logging
    print("✓ logging")
    modules_tested += 1
    modules_passed += 1
except ImportError as e:
    print(f"✗ logging: {e}")
    modules_tested += 1

try:
    import os
    print("✓ os")
    modules_tested += 1
    modules_passed += 1
except ImportError as e:
    print(f"✗ os: {e}")
    modules_tested += 1

try:
    from datetime import datetime
    print("✓ datetime")
    modules_tested += 1
    modules_passed += 1
except ImportError as e:
    print(f"✗ datetime: {e}")
    modules_tested += 1

try:
    from pathlib import Path
    print("✓ pathlib")
    modules_tested += 1
    modules_passed += 1
except ImportError as e:
    print(f"✗ pathlib: {e}")
    modules_tested += 1

try:
    import time
    print("✓ time")
    modules_tested += 1
    modules_passed += 1
except ImportError as e:
    print(f"✗ time: {e}")
    modules_tested += 1

print()
module_pass_rate = (modules_passed / modules_tested * 100) if modules_tested > 0 else 0
print(f"模块导入测试：{modules_passed}/{modules_tested} 通过 ({module_pass_rate:.1f}%)")
print()

# 2. 应用文件测试
print("📌 2. 应用文件测试")
print("-" * 70)

try:
    with open('app_v3.1.0_integrated.py', 'r', encoding='utf-8') as f:
        code = f.read()
        ast.parse(code)
    print("✓ 应用文件语法检查通过")
    print(f"  文件大小：{len(code)} 字节（{len(code)/1024:.1f} KB）")
    print(f"  代码行数：{len(code.split(chr(10)))} 行")
    file_test_passed = True
except Exception as e:
    print(f"✗ 应用文件测试失败：{e}")
    file_test_passed = False

print()

# 3. 函数定义测试
print("📌 3. 函数定义测试")
print("-" * 70)

required_functions = [
    'load_history',
    'save_to_history',
    'calculate_time_segments',
    'generate_with_deepseek',
    'generate_locally',
    'render_storyboard_generator',
    'render_prompt_builder',
    'render_manual_mode',
    'render_ai_professional_mode',
    'render_history',
    'render_about',
    'main'
]

with open('app_v3.1.0_integrated.py', 'r', encoding='utf-8') as f:
    code = f.read()

functions_tested = len(required_functions)
functions_passed = 0

for func in required_functions:
    if f'def {func}(' in code:
        print(f"✓ {func}")
        functions_passed += 1
    else:
        print(f"✗ {func} 缺失")

print()
function_pass_rate = (functions_passed / functions_tested * 100) if functions_tested > 0 else 0
print(f"函数定义测试：{functions_passed}/{functions_tested} 通过 ({function_pass_rate:.1f}%)")
print()

# 4. API 配置测试
print("📌 4. API 配置测试")
print("-" * 70)

api_config_tests = {
    "ASPECT_RATIOS": "画面比例",
    "VISUAL_STYLES": "视觉风格",
    "SCENE_TYPES": "场景类型",
    "CAMERA_MOVES": "运镜语言",
    "LIGHTING_STYLES": "光影效果",
    "QUALITY_TAGS": "画质标签",
    "API_KEY": "API Key",
    "API_BASE_URL": "API 地址",
    "API_MODEL": "API 模型"
}

config_tested = len(api_config_tests)
config_passed = 0

for config, desc in api_config_tests.items():
    if f'{config} ' in code or f'{config}=' in code:
        print(f"✓ {desc}")
        config_passed += 1
    else:
        print(f"✗ {desc} 缺失")

print()
config_pass_rate = (config_passed / config_tested * 100) if config_tested > 0 else 0
print(f"API 配置测试：{config_passed}/{config_tested} 通过 ({config_pass_rate:.1f}%)")
print()

# 5. API 功能测试
print("📌 5. API 功能测试")
print("-" * 70)

API_KEY = "sk-2f2c80b0af064d2a8ef04990630c8d7d"
API_BASE_URL = "https://api.deepseek.com"

api_test_passed = False

try:
    client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)

    print("正在测试 API 连接...")
    start_time = time.time()

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": "你好"}
        ],
        max_tokens=20
    )

    api_time = time.time() - start_time
    result = response.choices[0].message.content

    print(f"✓ API 测试成功！")
    print(f"  模型：{response.model}")
    print(f"  回答：{result}")
    print(f"  响应时间：{api_time:.2f} 秒")
    api_test_passed = True

except Exception as e:
    print(f"✗ API 测试失败：{str(e)}")
    api_test_passed = False

print()

# 6. 综合测试总结
print("=" * 70)
print("📊 测试总结")
print("=" * 70)
print()

tests = [
    ("模块导入", modules_passed, modules_tested),
    ("应用文件", 1 if file_test_passed else 0, 1),
    ("函数定义", functions_passed, functions_tested),
    ("API 配置", config_passed, config_tested),
    ("API 功能", 1 if api_test_passed else 0, 1)
]

total_passed = sum(t[1] for t in tests)
total_tests = sum(t[2] for t in tests)

print("测试项：")
for name, passed, total in tests:
    rate = (passed / total * 100) if total > 0 else 0
    print(f"  {name:15} {passed:2}/{total:2} ({rate:5.1f}%)")

print()
overall_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
print(f"总计：{total_passed}/{total_tests} 通过 ({overall_rate:.1f}%)")
print()

if overall_rate == 100:
    print("🎉 所有测试通过！V3.1.0 可以投入使用！")
    print()
    print("🚀 启动方式：")
    print("  cd /workspace/projects/apps/seedance-tool-streamlit")
    print("  streamlit run app_v3.1.0_integrated.py")
    print()
    print("🌐 访问地址：")
    print("  本地：http://localhost:8501")
    print("  远程：http://[服务器IP]:8501")
else:
    print("⚠️ 部分测试失败，请检查错误信息")
    sys.exit(1)

print()
print("=" * 70)
