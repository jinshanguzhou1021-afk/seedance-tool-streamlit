#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试 DeepSeek V3 API
"""

from openai import OpenAI

# API 配置
API_KEY = "sk-2f2c80b0af064d2a8ef04990630c8d7d"

try:
    client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

    print("🧪 测试 DeepSeek V3 API...")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": "你好，请用一句话介绍你自己。"}
        ],
        max_tokens=100
    )

    print("✅ API 测试成功！")
    print(f"模型：{response.model}")
    print(f"回答：{response.choices[0].message.content}")

except Exception as e:
    print(f"❌ API 测试失败：{str(e)}")
