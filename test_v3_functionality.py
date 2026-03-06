#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V3.0.0 功能自检脚本
测试 AI 全能导演工作站的核心功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🎬 V3.0.0 功能自检脚本")
print("=" * 60)

# 测试 1：检查版本号
print("\n📌 测试 1：版本号检查")
try:
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if '版本: 3.0.0' in content:
            print("✓ 版本号正确：3.0.0")
        else:
            print("✗ 版本号不匹配")
            sys.exit(1)
except Exception as e:
    print(f"✗ 版本检查失败: {e}")
    sys.exit(1)

# 测试 2：检查系统 Prompt
print("\n📌 测试 2：系统 Prompt 检查")
try:
    if 'DIRECTOR_SYSTEM_PROMPT' in content:
        print("✓ 导演系统 Prompt 存在")
        if '三层导演逻辑' in content:
            print("✓ 三层导演逻辑已定义")
        else:
            print("✗ 三层导演逻辑未定义")
            sys.exit(1)
    else:
        print("✗ 导演系统 Prompt 不存在")
        sys.exit(1)
except Exception as e:
    print(f"✗ 系统 Prompt 检查失败: {e}")
    sys.exit(1)

# 测试 3：检查核心函数
print("\n📌 测试 3：核心函数检查")
required_functions = [
    'call_openai_api_director_v3',
    'generate_dramatic_storyboard',
    'render_ai_director',
    'display_director_result',
    'analyze_story_emotion',
    'build_dramatic_description',
    'build_final_director_prompt'
]

missing_functions = []
for func in required_functions:
    if f'def {func}(' in content:
        print(f"✓ {func}")
    else:
        print(f"✗ {func} 缺失")
        missing_functions.append(func)

if missing_functions:
    print(f"\n✗ 缺失函数: {', '.join(missing_functions)}")
    sys.exit(1)

# 测试 4：检查 UI 组件
print("\n📌 测试 4：UI 组件检查")
ui_components = [
    'AI 导演控制台',
    '故事输入',
    '张力强度',
    '情绪滤镜',
    '表情微调',
    '动作动态',
    '运镜风格',
    '光影效果',
    '画面比例'
]

missing_ui = []
for component in ui_components:
    if component in content:
        print(f"✓ {component}")
    else:
        print(f"✗ {component} 缺失")
        missing_ui.append(component)

if missing_ui:
    print(f"\n⚠️  部分 UI 组件缺失: {', '.join(missing_ui)}")
    print("提示：这可能不影响核心功能")

# 测试 5：检查标准化输出格式
print("\n📌 测试 5：标准化输出格式检查")
output_elements = [
    '镜号',
    '场景',
    '运镜',
    '动态画面描述提示词',
    '旁白',
    '音效'
]

missing_output = []
for element in output_elements:
    if element in content:
        print(f"✓ {element}")
    else:
        print(f"✗ {element} 缺失")
        missing_output.append(element)

if missing_output:
    print(f"\n✗ 缺失输出元素: {', '.join(missing_output)}")
    sys.exit(1)

# 测试 6：导入测试
print("\n📌 测试 6：模块导入测试")
try:
    import streamlit as st
    print("✓ Streamlit 导入成功")

    from openai import OpenAI
    print("✓ OpenAI 导入成功")

    import json
    import logging
    from datetime import datetime
    from pathlib import Path
    import time
    print("✓ 所有标准库导入成功")

except ImportError as e:
    print(f"✗ 导入失败: {e}")
    sys.exit(1)

# 测试总结
print("\n" + "=" * 60)
print("📊 自检总结")
print("=" * 60)

checks = [
    ("版本号", "✓ 通过"),
    ("系统 Prompt", "✓ 通过"),
    ("核心函数", "✓ 通过"),
    ("UI 组件", "✓ 通过（部分可能缺失）" if missing_ui else "✓ 通过"),
    ("标准化输出", "✓ 通过"),
    ("模块导入", "✓ 通过")
]

for check_name, status in checks:
    print(f"{check_name:20s} {status}")

print("\n✅ V3.0.0 核心功能自检完成！")
print("\n🚀 下一步：")
print("   1. 启动应用: streamlit run app.py")
print("   2. 测试 AI 导演功能")
print("   3. 检查 API 集成")
print("   4. 验证输出格式")
