#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seedance-Tool v3.0.0 AI 全能导演工作站 - 完整模块
独立模块，包含所有 v3.0.0 的核心功能
"""

import streamlit as st
import json
import logging
from datetime import datetime
from openai import OpenAI
import requests
import re

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================= v3.0.0 Director System Prompt (视听一致性引擎）===================

DIRECTOR_SYSTEM_PROMPT = """你是一位顶级的电影导演、影视工业专家和 AI 视频专家。

## 你的角色
1. **视觉导演** - 负责镜头语言、运镜设计、光影构图
2. **情感分析师** - 负责识别故事的情绪转折点和冲突爆发点
3. **分镜编剧** - 负责将故事拆分为逻辑连贯的导演级分镜

## 你的任务
将用户的文字稿转化为具有**空间逻辑一致性**和**前后分镜连续**的 Seedance 2.0 专业分镜。

## 三层导演逻辑

### 第一层：全局逻辑层（一致性保证）
在生成任何分镜之前，必须先提取并锁定以下全局设定：

1. **核心角色设定**：
   - 外貌特征（发型、发色、面部特征）
   - 服装风格（颜色、材质、风格）
   - 性格特点（冷酷、温柔、坚毅等）

2. **环境设定**：
   - 空间位置（室内/室外、具体地点）
   - 时间（清晨/黄昏/夜晚/深夜）
   - 天气（晴天/雨天/雪天/暴风雨）

3. **光影基调**：
   - 整体色调（冷/暖）
   - 对比度（高/低）
   - 光效风格（自然/戏剧）

**重要性**：这些设定在所有分镜中必须保持一致，防止"角色变脸"或"环境跳戏"。

### 第二层：导演编剧层（标准化剧本）
根据故事的情绪逻辑，生成 3-5 个逻辑连贯的分镜。每个分镜必须包含以下 6 个标准化要素：

1. **镜号 (Shot ID)**：明确序列顺序（如：Shot 01, Shot 02）
2. **场景 (Setting)**：定义空间位置与时间（如：破旧小酒馆 - 深夜）
3. **运镜 (Camera)**：专业摄影机语言（如：低角度推近特写、荷兰斜角、希区柯克变焦）
4. **动态画面描述提示词 (Visual Prompt)**：核心输出，包含：
   - 电影级画质标签（8K, 超高清）
   - 主体描述（外貌 + 服装，必须一致）
   - 表情微操（瞳孔微动、汗水滑落、肌肉颤抖等）
   - 爆发性动作（慢动作爆发、碎屑飞溅、衣物撕裂、剧烈喘息等）
   - 环境特效（水花溅射、烟雾扩散、光效闪烁）
   - 运镜描述（推、拉、摇、移、跟、环绕、变焦等）
5. **旁白 (VO)**：叙事台词或内心独白
6. **音效 (SFX)**：环境音、动作音、情绪转场音

### 第三层：Seedance 2.0 适配层
将场景转化为高张力、细致表情和物理动态的动态描述，并添加 Seedance 2.0 参数。

## 空间连续性要求
- 必须保持同一场景内的方位逻辑一致
- 如果 Shot 1 角色在左侧，Shot 2 的转场必须符合视觉逻辑
- 角色的位置、朝向、动作必须连续，不能跳跃

## 角色一致性要求
- 在所有分镜提示词中，必须使用相同的外貌特征描述
- 服装、发型、面部特征必须保持一致
- 避免使用"然后"、"接着"等简单的过渡词
- 使用具有画面感的连续性描述

## Seedance 2.0 优化要求
- **细致表情**：必须包含（如：瞳孔收缩、嘴角抽搐、泪水盈眶、咬紧牙关）
- **高张力动作**：必须包含（如：肌肉发力、衣物随风摆动、物理碰撞效果）
- **物理交互**：必须包含（如：水花溅射、烟雾扩散、粒子特效）

## 张力强度调节
根据用户的张力选择，调整描述的激烈程度：
- 3 (温和)：平静、温和、低强度
- 5 (中等)：明显起伏、中等强度
- 7 (强烈)：紧张刺激、高强度
- 9 (极致)：极端冲突、极高强度
- 10 (史诗)：史诗级冲突、最高强度

## 情绪滤镜应用
根据用户选择的情绪滤镜，调整整体氛围：
- 忧郁：冷色调、低饱和度、阴影沉重、氛围压抑
- 惊悚：高对比度、强烈明暗、锐利线条、不安感
- 热血：暖色调、高饱和度、红色为主、燃烧感
- 赛博：霓虹色彩、冷蓝色调、光效绚烂、科技感
- 国风：水墨色调、留白艺术、金色点缀、古雅感
- 治愈：暖色调、柔和光线、高亮度、温馨感
- 悬疑：低亮度、强烈对比、阴影深重、神秘感
- 浪漫：粉色系、柔光效果、朦胧美感、氛围甜蜜

## 输出格式（必须严格遵守）
请以 JSON 格式输出，格式如下：

```json
{
  "global_settings": {
    "main_character": "角色外貌特征描述（简短）",
    "environment": "环境设定（地点 + 时间 + 天气）",
    "lighting_tone": "光影基调",
    "visual_style": "视觉风格"
  },
  "segments": [
    {
      "shot_id": "Shot 01",
      "setting": "场景（地点 + 时间）",
      "camera": "运镜方式（专业摄影语言）",
      "visual_prompt": "完整的 Seedance 2.0 提示词，包含：电影级画质 + 主体 + 表情微操 + 爆发动作 + 环境特效 + 运镜 + 参数",
      "vo": "旁白或台词",
      "sfx": "音效描述",
      "emotion": "情绪类型",
      "tension": "张力等级"
    }
  ],
  "complete_prompt": "所有分镜的完整 Seedance 2.0 提示词（用于直接复制）",
  "metadata": {
    "total_shots": 3-5,
    "avg_tension": "平均张力等级",
    "dominant_emotion": "主导情绪"
  }
}
```

## 重要提醒
1. **空间连续性**是第一优先级，确保角色和环境的逻辑连贯
2. **角色一致性**是第二优先级，确保外貌描述完全一致
3. **张力强度**根据用户选择动态调整
4. **情绪滤镜**应用到所有分镜，保持氛围统一
5. **输出格式**必须严格遵循 JSON 格式
6. **6 要素**每个分镜必须包含：镜号、场景、运镜、提示词、旁白、音效

现在，请根据用户输入的故事和参数，生成符合上述要求的导演级分镜。
"""

# ================= OpenAI API 配置 =================

OPENAI_API_KEY = None  # 将从 st.secrets 中读取
OPENAI_BASE_URL = "https://api.openai.com/v1"  # 默认值，可从 st.secrets 中读取

# ================= OpenAI API 调用函数 =================

def call_openai_api_director(story_text, global_settings, api_mode, tension_level, emotion_filter, expression_select, action_select, camera_select, lighting_select, aspect_ratio):
    """调用 OpenAI API (GPT-4) 生成导演级分镜"""

    # 转换为 DeepSeek/OpenAI 兼容的格式
    if "deepseek" in api_mode.lower():
        # DeepSeek 格式
        api_key = "sk-6297255fd0f84e7cb39ad48de10bf14e"
        base_url = "https://api.deepseek.com/v1"
        model_name = "deepseek-chat"
    else:
        # OpenAI 格式
        api_key = OPENAI_API_KEY if OPENAI_API_KEY else "sk-6297255fd0f84e7cb39ad48de10bf14e"
        base_url = OPENAI_BASE_URL if OPENAI_BASE_URL else "https://api.openai.com/v1"
        model_name = "gpt-4-turbo"

    try:
        # 创建客户端
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        # 转换张力等级为数字
        tension_map = {
            "平淡叙事 (温和)": 3,
            "轻微波动 (平静)": 5,
            "明显起伏 (中等)": 7,
            "紧张刺激 (强烈)": 9,
            "史诗冲突 (极致)": 10
        }
        tension_val = tension_map.get(tension_level, 5)

        # 转换画幅比例
        ar_map = {
            "16:9 横屏": "--ar 16:9",
            "21:9 电影宽屏": "--ar 21:9",
            "9:16 竖屏": "--ar 9:16",
            "1:1 方图": "--ar 1:1"
        }
        ar_param = ar_map.get(aspect_ratio, "--ar 16:9")

        # 构建用户提示词
        global_settings_str = json.dumps(global_settings, ensure_ascii=False, indent=2) if global_settings else "{}"

        user_prompt = f"""请为以下故事生成 3-5 个导演级分镜脚本：

故事描述：{story_text}

全局设定（全局逻辑层）：
{global_settings_str}

导演参数：
- 张力强度：{tension_level} (数值: {tension_val})
- 情绪滤镜：{', '.join(emotion_filter) if emotion_filter else '无'}
- 表情微操：{', '.join(expression_select) if expression_select else '无'}
- 动作张力：{', '.join(action_select) if action_select else '无'}
- 大师运镜：{', '.join(camera_select) if camera_select else '无'}
- 戏剧化光影：{', '.join(lighting_select) if lighting_select else '无'}
- 画幅比例：{aspect_ratio}

要求：
1. 根据故事的情绪转折点，生成 3-5 个逻辑连贯的分镜
2. 每个分镜必须包含以下 6 个要素：
   - 镜号 (Shot ID)
   - 场景 (Setting)
   - 运镜 (Camera)
   - 动态画面描述提示词 (Visual Prompt)
   - 旁白 (VO)
   - 音效 (SFX)
3. 确保空间连续性和角色一致性
4. 使用电影级、文学性的中文描述
5. 极致张力和细腻表情

请以 JSON 格式输出。
"""

        # 构建 API 请求
        messages = [
            {
                "role": "system",
                "content": DIRECTOR_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        # 调用 GPT-4 API
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.7,
            top_p=0.9,
            max_tokens=3000
        )

        # 解析响应
        content = response.choices[0].message.content

        # 尝试提取 JSON
        try:
            json_start = content.find("{")
            json_end = content.rfind("}") + 1

            if json_start != -1 and json_end > json_start:
                json_str = content[json_start:json_end]
                segments_data = json.loads(json_str)

                return {
                    "api_mode": api_mode,
                    "model": model_name,
                    "global_settings": segments_data.get("global_settings", {}),
                    "segments": segments_data.get("segments", []),
                    "complete_prompt": content
                }

        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"解析 OpenAI 响应失败：{e}")

        # 如果 JSON 解析失败，返回原始内容
        return {
            "api_mode": api_mode,
            "model": model_name,
            "global_settings": {},
            "segments": [],
            "complete_prompt": content,
            "raw_response": True
        }

    except Exception as e:
        logger.error(f"OpenAI API 调用失败：{e}")
        return {
            "error": f"API 调用失败：{str(e)}",
            "api_mode": api_mode,
            "segments": []
        }


# ================= v3.0.0 完整故事板生成函数 =================

def generate_full_storyboard(story_text, api_mode, global_settings, tension_level, emotion_filter, expression_select, action_select, camera_select, lighting_select, aspect_ratio):
    """v3.0.0 完整故事板生成函数（三层架构）"""

    # 调用 API
    result = call_openai_api_director(
        story_text,
        global_settings,
        api_mode,
        tension_level,
        emotion_filter,
        expression_select,
        action_select,
        camera_select,
        lighting_select,
        aspect_ratio
    )

    # 如果出错，返回
    if "error" in result:
        return result

    # 如果没有 segments，返回
    if not result["segments"]:
        return result

    # 转换为标准格式
    segments = result["segments"]

    # 添加完整提示词（包含所有分镜）
    complete_prompt_lines = ["电影级画质，极致细节"]

    for i, segment in enumerate(segments):
        shot_id = segment.get("shot_id", f"Shot {i+1:02d}")
        setting = segment.get("setting", "")
        camera = segment.get("camera", "")
        visual_prompt = segment.get("visual_prompt", "")
        vo = segment.get("vo", "")
        sfx = segment.get("sfx", "")

        # 组装完整提示词
        complete_prompt_lines.append(f"{shot_id}：{visual_prompt}")

        # 添加旁白
        if vo:
            complete_prompt_lines.append(f"旁白：{vo}")

        # 添加音效
        if sfx:
            complete_prompt_lines.append(f"音效：{sfx}")

    # 添加 Seedance 2.0 参数
    tension_map = {
        "平淡叙事 (温和)": 3,
        "轻微波动 (平静)": 5,
        "明显起伏 (中等)": 7,
        "紧张刺激 (强烈)": 9,
        "史诗冲突 (极致)": 10
    }
    tension_val = tension_map.get(tension_level, 5)

    ar_map = {
        "16:9 横屏": "--ar 16:9",
        "21:9 电影宽屏": "--ar 21:9",
        "9:16 竖屏": "--ar 9:16",
        "1:1 方图": "--ar 1:1"
    }
    ar_param = ar_map.get(aspect_ratio, "--ar 16:9")

    complete_prompt_lines.append(f"--motion {tension_val} {ar_param}")

    # 组合成最终字符串
    final_prompt = "\n".join(complete_prompt_lines)

    return {
        "api_mode": result["api_mode"],
        "model": result["model"],
        "global_settings": result.get("global_settings", {}),
        "segments": segments,
        "complete_prompt": final_prompt,
        "metadata": {
            "total_shots": len(segments),
            "tension_level": tension_level,
            "aspect_ratio": aspect_ratio,
            "api_used": result["api_mode"]
        }
    }


# ================= v3.0.0 UI 渲染函数 =================

def render_v3_ai_director():
    """渲染 Seedance 2.0 AI 全能导演系统 v3.0.0"""

    st.subheader("🎬 Seedance 2.0 AI 全能导演工作站 v3.0.0")
    st.caption("视听一致性引擎 + 三层导演逻辑 + 6 要素标准化剧本")

    st.markdown("---")

    # API 模式切换
    col1, col2 = st.columns(2)

    with col1:
        api_mode = st.selectbox(
            "🤖 AI 模式选择",
            ["OpenAI GPT-4 (付费)", "DeepSeek-V3 (免费)", "本地模拟 (快速)"],
            index=0,
            help="OpenAI GPT-4 质量最高，DeepSeek-V3 免费但稳定，本地模拟最快"
        )

    with col2:
        if api_mode == "OpenAI GPT-4 (付费)":
            st.info("💡 OpenAI GPT-4 会生成最高质量、最具文学性的分镜")
        elif api_mode == "DeepSeek-V3 (免费)":
            st.info("💡 DeepSeek-V3 免费但稳定，质量优秀")
        else:
            st.info("💡 本地模拟速度最快，适合快速测试")

    st.markdown("---")

    # 第一部分：故事输入
    col1, col2 = st.columns([2, 1])

    with col1:
        story_text = st.text_area(
            "📖 1. 故事/脚本输入（100-300字）",
            placeholder="输入故事或场景描述...",
            height=120,
            help="系统将自动分析文本中的情绪高点，生成导演级分镜"
        )

    with col2:
        st.info("💡 输入提示")
        st.markdown("""
        - 系统会自动识别：
          • 情绪转折点
          • 冲突爆发点
          • 情绪高潮点
        - 推荐长度：100-300字
        """)

    st.divider()

    # 第二部分：全局设定（三层逻辑 - 第一层）
    st.subheader("🌐 2. 全局设定（一致性保证）")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        global_character = st.text_input(
            "核心角色（可选）",
            placeholder="例如：复仇者、剑客、情侣",
            help="描述核心角色的外貌特征（发色、服装、性格）"
        )

    with col2:
        global_environment = st.text_input(
            "环境设定（可选）",
            placeholder="例如：极寒雪原黄昏、破旧小酒馆深夜",
            help="描述空间位置、时间、天气"
        )

    with col3:
        global_lighting = st.selectbox(
            "光影基调（可选）",
            ["自然光", "高对比度", "强烈明暗", "暖色调", "冷色调"],
            index=0,
            help="选择整体的光影基调"
        )

    with col4:
        global_style = st.selectbox(
            "视觉风格（可选）",
            ["电影感", "写实", "动画", "赛博朋克", "东方武侠", "唯美"],
            index=0,
            help="选择整体的视觉风格"
        )

    # 全局设定集合
    global_settings = {
        "main_character": global_character,
        "environment": global_environment,
        "lighting_tone": global_lighting,
        "visual_style": global_style
    }

    st.divider()

    # 第三部分：导演控制参数（三层逻辑 - 第二、三层）
    st.subheader("🎥 3. 导演控制参数")

    col1, col2, col3 = st.columns(3)

    with col1:
        tension_level = st.select_slider(
            "🎭 张力强度调节器",
            options=list(TENSION_MOTION_MAP.keys()),
            value="明显起伏 (中等)",
            help="从平淡叙事到史诗冲突，调节整体张力（5级）"
        )

        emotion_filter = st.multiselect(
            "🎨 情绪滤镜",
            list(EMOTION_FILTERS.keys()),
            help="选择情绪基调，可多选"
        )

    with col2:
        expression_select = st.multiselect(
            "😐 表情微操（可选）",
            list(EXPRESSION_ENHANCEMENTS.keys()),
            help="为分镜添加细腻的表情描述（10种）"
        )

        action_select = st.multiselect(
            "🏃 动作张力（可选）",
            list(ACTION_ENHANCEMENTS.keys()),
            help="为分镜添加爆发性的动作描述（7种）"
        )

    with col3:
        camera_select = st.multiselect(
            "🎥 大师运镜（可选）",
            list(MASTER_CAMERA_MOVES.keys()),
            help="选择大师级镜头语言（7种）"
        )

        lighting_select = st.multiselect(
            "💡 戏剧化光影（可选）",
            list(DRAMATIC_LIGHTING.keys()),
            help="选择戏剧化的光影效果（5种）"
        )

        aspect_ratio = st.selectbox(
            "📐 画幅比例",
            ["16:9 横屏", "21:9 电影宽屏", "9:16 竖屏", "1:1 方图"],
            help="选择视频的画面比例"
        )

    st.divider()

    # 生成按钮
    if st.button("🎬 生成 v3.0.0 导演级分镜（6 要素标准化剧本）", type="primary", use_container_width=True):
        if not story_text:
            st.warning("⚠️ 请先输入故事或脚本！")
        else:
            with st.spinner("AI 全能导演正在分析故事..."):

                # API 模式
                if api_mode == "OpenAI GPT-4 (付费)":
                    with st.spinner("正在调用 OpenAI GPT-4 API 生成最高质量分镜..."):
                        result = generate_full_storyboard(
                            story_text,
                            "openai",
                            global_settings,
                            tension_level,
                            emotion_filter,
                            expression_select,
                            action_select,
                            camera_select,
                            lighting_select,
                            aspect_ratio
                        )

                elif api_mode == "DeepSeek-V3 (免费)":
                    with st.spinner("正在调用 DeepSeek-V3 API 生成高质量分镜..."):
                        result = generate_full_storyboard(
                            story_text,
                            "deepseek",
                            global_settings,
                            tension_level,
                            emotion_filter,
                            expression_select,
                            action_select,
                            camera_select,
                            lighting_select,
                            aspect_ratio
                        )

                else:
                    # 本地模拟
                    result = generate_dramatic_storyboard(
                        story_text,
                        tension_level,
                        emotion_filter,
                        expression_select,
                        action_select,
                        camera_select,
                        lighting_select,
                        aspect_ratio
                    )
                    # 模拟添加 6 要素
                    for segment in result["segments"]:
                        if "vo" not in segment:
                            segment["vo"] = ""
                        if "sfx" not in segment:
                            segment["sfx"] = ""

                # 显示结果
                display_v3_director_result(result, api_mode, story_text, global_settings, tension_level, aspect_ratio)


def display_v3_director_result(result, api_mode, story_text, global_settings, tension_level, aspect_ratio):
    """显示 v3.0.0 导演级分镜结果"""

    if "error" in result:
        st.error(f"❌ {result['error']}")
    elif "segments" in result and result["segments"]:
        st.success("✅ v3.0.0 导演级分镜已生成！")

        # 显示全局设定
        st.markdown("### 🌐 全局设定（一致性保证）")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("核心角色", result.get("global_settings", {}).get("main_character", "未指定"))
        with col2:
            st.metric("环境设定", result.get("global_settings", {}).get("environment", "未指定"))
        with col3:
            st.metric("光影基调", result.get("global_settings", {}).get("lighting_tone", "未指定"))
        with col4:
            st.metric("分镜数量", len(result["segments"]))

        st.markdown("---")

        # 显示分镜卡片
        st.markdown("### 🎬 分镜剧本（6 要素标准化）")

        for i, segment in enumerate(result["segments"]):
            with st.expander(f"🎬 分镜 {i+1}: {segment.get('shot_id', 'Shot ' + str(i+1))}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"**⏱️ 时间/场景：** {segment.get('setting', '未指定')}")
                    st.markdown(f"**🎥 运镜：** {segment.get('camera', '未指定')}")

                with col2:
                    st.markdown(f"**😐 情绪：** {segment.get('emotion', '未指定')}")
                    st.markdown(f"**💪 张力：** {segment.get('tension', '未指定')}")

                st.markdown("---")
                st.markdown(f"**🎯 动态画面描述提示词：**")
                st.code(segment.get('visual_prompt', '未指定'), language="text")

                # 新增：旁白和音效
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**🎤 旁白 (VO):**")
                    vo = segment.get('vo', '无')
                    if vo:
                        st.success(f"\"{vo}\"")
                    else:
                        st.info("（无）")

                with col2:
                    st.markdown("**🔊 音效 (SFX):**")
                    sfx = segment.get('sfx', '无')
                    if sfx:
                        st.success(f"\"{sfx}\"")
                    else:
                        st.info("（无）")

        st.markdown("---")

        # 显示完整提示词
        st.markdown("### 🎯 完整 Seedance 2.0 提示词（复制到 Seedance 使用）")
        st.code(result.get("complete_prompt", ""), language="text")

        # 显示元数据
        st.markdown("### 📊 元数据")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("API 模式", result.get("api_mode", "未知"))
        with col2:
            st.metric("模型", result.get("model", "未知"))
        with col3:
            st.metric("张力强度", tension_level)

        # 下载按钮
        download_content = f"""=== Seedance 2.0 v3.0.0 导演级分镜 ===

{result.get("complete_prompt", "")}

=== 元数据 ===
API 模式：{result.get("api_mode", "未知")}
模型：{result.get("model", "未知")}
张力强度：{tension_level}
画幅比例：{aspect_ratio}

=== 全局设定 ===
核心角色：{result.get("global_settings", {}).get("main_character", "未指定")}
环境设定：{result.get("global_settings", {}).get("environment", "未指定")}
光影基调：{result.get("global_settings", {}).get("lighting_tone", "未指定")}
视觉风格：{result.get("global_settings", {}).get("visual_style", "未指定")}

=== 分镜详情（6 要素）===
"""

        for i, seg in enumerate(result["segments"]):
            download_content += f"""
分镜 {i+1}：
镜号：{seg.get('shot_id', 'Shot ' + str(i+1))}
场景：{seg.get('setting', '未指定')}
运镜：{seg.get('camera', '未指定')}
动态画面描述提示词：{seg.get('visual_prompt', '未指定')}
旁白：{seg.get('vo', '（无）')}
音效：{seg.get('sfx', '（无）')}
情绪：{seg.get('emotion', '未指定')}
张力：{seg.get('tension', '未指定')}

"""

        st.download_button(
            label="💾 下载 v3.0.0 导演级分镜配置",
            data=download_content,
            file_name=f"seedance_v3.0.0_director_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

        # 保存到历史记录
        save_to_history(
            "AI全能导演v3.0.0",
            story_text,
            result.get("complete_prompt", ""),
            len(result["segments"]) > 0
        )

    else:
        st.warning("⚠️ 未生成任何分镜，请检查输入或 API 配置")
