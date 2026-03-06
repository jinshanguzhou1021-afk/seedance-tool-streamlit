#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V3.1.0 快速验证脚本
"""

import sys

print("=" * 60)
print("🧪 V3.1.0 整合版 - 快速验证")
print("=" * 60)
print()

# 1. 模块导入测试
print("📌 1. 模块导入测试")
print("-" * 60)

try:
    import streamlit as st
    print("✅ Streamlit 导入成功")
except ImportError as e:
    print(f"❌ Streamlit 导入失败: {e}")
    sys.exit(1)

try:
    from openai import OpenAI
    print("✅ OpenAI 导入成功")
except ImportError as e:
    print(f"❌ OpenAI 导入失败: {e}")
    sys.exit(1)

try:
    import json
    print("✅ json 导入成功")
except ImportError as e:
    print(f"❌ json 导入失败: {e}")
    sys.exit(1)

try:
    import logging
    print("✅ logging 导入成功")
except ImportError as e:
    print(f"❌ logging 导入失败: {e}")
    sys.exit(1)

try:
    import os
    print("✅ os 导入成功")
except ImportError as e:
    print(f"❌ os 导入失败: {e}")
    sys.exit(1)

try:
    from datetime import datetime
    print("✅ datetime 导入成功")
except ImportError as e:
    print(f"❌ datetime 导入失败: {e}")
    sys.exit(1)

try:
    from pathlib import Path
    print("✅ pathlib 导入成功")
except ImportError as e:
    print(f"❌ pathlib 导入失败: {e}")
    sys.exit(1)

try:
    import time
    print("✅ time 导入成功")
except ImportError as e:
    print(f"❌ time 导入失败: {e}")
    sys.exit(1)

print()
print("✅ 所有模块导入成功")
print()

# 2. 应用文件测试
print("📌 2. 应用文件测试")
print("-" * 60)

try:
    import ast
    with open('app_v3.1.0_integrated.py', 'r', encoding='utf-8') as f:
        code = f.read()
    ast.parse(code)
    print("✅ 应用文件语法检查通过")
    print(f"  文件大小：{len(code)} 字节")
except Exception as e:
    print(f"❌ 应用文件检查失败: {e}")
    sys.exit(1)

print()

# 3. API 配置测试
print("📌 3. API 配置测试")
print("-" * 60)

try:
    from openai import OpenAI

    API_KEY = "sk-2f2c80b0af064d2a8ef04990630c8d7d"
    API_BASE_URL = "https://api.deepseek.com"

    client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)
    print("✅ API 客户端初始化成功")
    print(f"  API 地址：{API_BASE_URL}")
    print(f"  API 模型：deepseek-chat")
except Exception as e:
    print(f"❌ API 配置失败: {str(e)}")
    sys.exit(1)

print()

# 4. 快速 API 测试
print("📌 4. 快速 API 测试")
print("-" * 60)

try:
    from openai import OpenAI

    API_KEY = "sk-2f2c80b0af064d2a8ef04990630c8d7d"

    client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

    print("正在测试 API 连接...")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": "你好"}
        ],
        max_tokens=50
    )

    result = response.choices[0].message.content
    print(f"✅ API 测试成功！")
    print(f"  回答：{result}")

except Exception as e:
    print(f"❌ API 测试失败: {str(e)}")
    sys.exit(1)

print()

# 5. 总结
print("=" * 60)
print("📊 验证总结")
print("=" * 60)
print()
print("✅ 模块导入测试：通过")
print("✅ 应用文件测试：通过")
print("✅ API 配置测试：通过")
print("✅ API 功能测试：通过")
print()
print("🎉 所有验证通过！")
print()
print("🚀 启动方式：")
print("   streamlit run app_v3.1.0_integrated.py")
print()
print("🌐 访问地址：")
print("   本地：http://localhost:8501")
print("   远程：http://[服务器IP]:8501")
print()
print("=" * 60)
