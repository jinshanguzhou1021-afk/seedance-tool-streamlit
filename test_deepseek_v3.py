#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek V3 API 测试和分析脚本
"""

import json
from openai import OpenAI

# API 配置
API_KEY = "sk-2f2c80b0af064d2a8ef04990630c8d7d"
API_BASE_URL = "https://api.deepseek.com"
API_MODEL = "deepseek-chat"

# 初始化客户端
client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)

print("=" * 60)
print("🧪 DeepSeek V3 API 测试脚本")
print("=" * 60)
print()

# 测试用例 1：基础对话
print("📌 测试 1：基础对话能力")
print("-" * 60)

try:
    response = client.chat.completions.create(
        model=API_MODEL,
        messages=[
            {"role": "system", "content": "你是一位专业的视频导演和 AI 视频专家。"},
            {"role": "user", "content": "你好，请用一句话介绍一下你自己。"}
        ],
        temperature=0.7
    )
    result = response.choices[0].message.content
    print("✅ 基础对话测试通过")
    print(f"回答：{result}")
    print()
except Exception as e:
    print(f"❌ 基础对话测试失败：{str(e)}")
    print()

# 测试用例 2：分镜生成（简单）
print("📌 测试 2：简单分镜生成")
print("-" * 60)

simple_story = "一对情侣在夕阳下对视，准备表白"

system_prompt = """你是一位顶级的电影导演、影视工业专家和 AI 视频专家。

你的任务：将用户的文字稿转化为具有空间逻辑一致性和前后分镜连续的 Seedance 2.0 专业分镜。

要求：
1. 将对话转化为具体的画面描述（面部表情、肢体动作、眼神交流）
2. 包含具体的专业运镜术语（如：特写、慢推、环绕、平移）
3. 音效必须具体

输出格式：
15秒🎭 剧情/对话场景，🎬 电影感，16:9。

时间轴（AI 增强）：
- 0-5秒：[分镜1：角色外貌、动作、环境光影描述] + [具体运镜方式]
- 5-10秒：[分镜2：神态变化、肢体动作描述] + [具体运镜方式]
- 10-15秒：[分镜3：情节高潮动作描述] + [具体运镜方式]

音效设计（AI 建议）：
- 背景音乐：[具体的乐器、节奏]
- 音效：[具体的环境摩擦音]
"""

try:
    response = client.chat.completions.create(
        model=API_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请结合以上要求，将这段内容改为完美的视频画面分镜：\n{simple_story}"}
        ],
        temperature=0.7
    )
    result = response.choices[0].message.content
    print("✅ 简单分镜生成测试通过")
    print(f"结果：\n{result}")
    print()
except Exception as e:
    print(f"❌ 简单分镜生成测试失败：{str(e)}")
    print()

# 测试用例 3：分镜生成（复杂）
print("📌 测试 3：复杂分镜生成")
print("-" * 60)

complex_story = """在极寒的雪原夜晚，一名身着黑色斗篷的复仇者孤独地前行。他手持一把泛着寒光的古剑，剑刃上满是陈年的血痕。前方是一座破败的古城，城墙在风雪中若隐若现。复仇者停下脚步，凝视着城门，眼中燃烧着复仇的火焰。他猛然拔剑，剑尖指向夜空，发出无声的嘶吼。"""

try:
    response = client.chat.completions.create(
        model=API_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请结合以上要求，将这段内容改为完美的视频画面分镜：\n{complex_story}"}
        ],
        temperature=0.7
    )
    result = response.choices[0].message.content
    print("✅ 复杂分镜生成测试通过")
    print(f"结果：\n{result}")
    print()
except Exception as e:
    print(f"❌ 复杂分镜生成测试失败：{str(e)}")
    print()

# 测试用例 4：JSON 输出
print("📌 测试 4：JSON 输出格式")
print("-" * 60)

json_system_prompt = """你是一位顶级的电影导演和 AI 视频专家。

你的任务：将用户的文字稿转化为 Seedance 2.0 专业分镜。

你必须且只能返回合法的 JSON 格式，结构如下：
{
  "global_settings": {
    "main_character": "角色外貌描述",
    "environment": "环境设定",
    "lighting_tone": "光影基调",
    "visual_style": "视觉风格"
  },
  "segments": [
    {
      "shot_id": "Shot 01",
      "setting": "场景",
      "camera": "运镜描述",
      "visual_prompt": "画面描述提示词",
      "vo": "旁白",
      "sfx": "音效描述",
      "emotion": "情绪",
      "tension": "张力"
    }
  ]
}

不要添加任何其他文字，只返回 JSON。
"""

try:
    response = client.chat.completions.create(
        model=API_MODEL,
        messages=[
            {"role": "system", "content": json_system_prompt},
            {"role": "user", "content": f"请将以下故事转化为 JSON 格式的分镜：\n{simple_story}"}
        ],
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    json_data = json.loads(result)
    print("✅ JSON 输出格式测试通过")
    print(f"JSON 结构：")
    print(json.dumps(json_data, indent=2, ensure_ascii=False))
    print()
except json.JSONDecodeError as e:
    print(f"❌ JSON 解析失败：{str(e)}")
    print(f"原始输出：{result}")
    print()
except Exception as e:
    print(f"❌ JSON 输出格式测试失败：{str(e)}")
    print()

# 测试总结
print("=" * 60)
print("📊 测试总结")
print("=" * 60)
print(f"API 模型：{API_MODEL}")
print(f"API 版本：V3")
print(f"测试状态：完成")
print()

# 分析结果
print("🎯 分析建议：")
print("1. 检查生成的分镜质量是否符合预期")
print("2. 评估视觉化描述的准确性和细节")
print("3. 检查运镜术语是否专业")
print("4. 验证音效建议是否具体")
print("5. 评估 JSON 输出的稳定性")
print()

print("=" * 60)
