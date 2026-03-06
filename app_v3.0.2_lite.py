#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即梦提示词工具 - Streamlit Web 应用（AI 全能导演工作站 - Lite 版本）
集成分镜生成器 + 提示词生成器 + AI 视觉导演 + DeepSeek-V3 API + JSON 强制输出
版本: 3.0.2-Lite
"""

import streamlit as st
import json
import logging
import os
from datetime import datetime
from pathlib import Path
import time
from openai import OpenAI

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================= 1. API 安全配置 =================

# 优先级：st.secrets > 环境变量 > 内置 fallback

# 方式 1：Streamlit Secrets（生产环境推荐）
try:
    API_KEY = st.secrets["DEEPSEEK_API_KEY"]
    API_MODE = "Secrets"
except (KeyError, FileNotFoundError):
    # 方式 2：环境变量
    API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    if API_KEY:
        API_MODE = "环境变量"
    else:
        # 方式 3：内置 fallback（仅用于本地开发测试）
        API_KEY = "sk-2f2c80b0af064d2a8ef04990630c8d7d"
        API_MODE = "内置 fallback"
        st.sidebar.warning("⚠️ 正在使用硬编码的 API Key，请尽快迁移到 st.secrets")

# API 配置
API_BASE_URL = "https://api.deepseek.com"
API_MODEL = "deepseek-chat"

# 初始化 OpenAI 客户端（完美兼容 DeepSeek）
try:
    client = OpenAI(
        api_key=API_KEY,
        base_url=API_BASE_URL
    )
except Exception as e:
    st.error(f"❌ API 客户端初始化失败：{str(e)}")
    client = None

# ================= 2. 核心系统提示词（三层导演逻辑）===================

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
   - 时间（清晨、黄昏、夜晚、深夜）
   - 天气（晴天、雨天、雪天、暴风雨）

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
6. **音效 (SFX)**：环境音、动作音、情绪转场音（如：暴雨击打窗户声、沉重的拔刀声）

### 第三层：Seedance 2.0 适配层
将场景转化为高张力、细致表情和物理动态的动态描述，并添加 Seedance 2.0 参数。

## 输出格式要求
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
      "visual_prompt": "Seedance 2.0 画质+主体+表情+动作+特效+运镜",
      "vo": "旁白内容",
      "sfx": "音效描述",
      "emotion": "情绪",
      "tension": "张力"
    }
  ]
}

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
"""

# ================= 3. 张力和风格配置 =================

# 张力等级映射
TENSION_MAP = {
    "低 (日常)": 3,
    "中 (剧情)": 5,
    "高 (动作/爆发)": 7
}

# 视觉风格库
VISUAL_STYLES = {
    "赛博朋克": "霓虹灯光、冷色调、未来科技感、高对比度",
    "唯美日系": "柔和光线、低饱和度、治愈感、清新自然",
    "暗黑废土": "粗粝质感、暖色调、废墟风格、低饱和度",
    "王家卫质感": "暖色灯光、高对比度、电影感、情绪化"
}

# ================= 4. AI 调用与解析 =================

def call_deepseek_api(story_text, params):
    """调用 DeepSeek 接口并严格解析 JSON"""
    if not client:
        return {"error": "API 客户端未初始化"}

    user_prompt = f"""
请根据以下输入生成导演级分镜：

【故事描述】：{story_text}
【附加参数】：{params}

请严格按照 JSON 格式输出。
"""

    try:
        response = client.chat.completions.create(
            model=API_MODEL,
            messages=[
                {"role": "system", "content": DIRECTOR_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            # 强化 JSON 输出，非常关键的一步！
            response_format={"type": "json_object"}
        )

        # 解析返回的 JSON 字符串为 Python 字典
        result_content = response.choices[0].message.content
        result_json = json.loads(result_content)
        return result_json

    except json.JSONDecodeError as e:
        logger.error(f"JSON 解析失败: {e}")
        return {"error": "AI 返回的数据格式有误，请重试。"}
    except Exception as e:
        logger.error(f"API 调用失败: {e}")
        return {"error": str(e)}

def build_final_prompt(segments, motion_val=5, ar_param="16:9"):
    """将 AI 生成的 JSON 分镜组装成最终可复制的纯文本提示词"""
    prompt_parts = ["🎬 【完整 Seedance 复制版】\n参数: 电影级画质，极致细节\n"]

    for segment in segments:
        shot = f"[{segment.get('shot_id')}] 镜头:{segment.get('camera')} | 画面:{segment.get('visual_prompt')}"
        prompt_parts.append(shot)

    prompt_parts.append(f"\n--motion {motion_val} --ar {ar_param}")
    return "\n".join(prompt_parts)

# ================= 5. UI 渲染主函数 =================

def render_ai_director():
    """渲染 AI 导演控制台 UI"""

    st.subheader("🎬 Seedance 2.0 AI 视觉导演系统")
    st.caption("通过三层导演逻辑，生成极致张力、细腻表情和戏剧化冲突的全中文分镜提示词")
    st.markdown("---")

    # 显示 API 模式
    st.info(f"🔑 API Key 来源：{API_MODE}")

    col1, col2 = st.columns([2, 1])

    with col1:
        story_text = st.text_area(
            "📖 1. 故事/脚本输入",
            placeholder="输入100字左右的故事或场景描述...",
            height=120
        )

    with col2:
        st.info("💡 系统会自动分析：情绪转折点、冲突爆发点")
        st.markdown("""
        - 推荐长度：50-150字
        - 包含：核心角色、环境、情绪转折
        """)

    st.divider()

    # 导演控制参数
    st.subheader("🎛️ 2. 导演控制参数")

    col1, col2, col3 = st.columns(3)

    with col1:
        tension_level = st.selectbox(
            "张力等级",
            list(TENSION_MAP.keys()),
            index=1  # 默认"中 (剧情)"
        )

        visual_style = st.selectbox(
            "视觉风格",
            list(VISUAL_STYLES.keys()),
            index=0  # 默认"赛博朋克"
        )

    with col2:
        aspect_ratio = st.selectbox(
            "画面比例",
            ["16:9 横屏", "9:16 竖屏", "1:1 方形", "2.35:1 电影宽屏"],
            index=0
        )

        motion_param = st.slider(
            "画面动态程度 (--motion)",
            1, 10, 5
        )

    with col3:
        st.markdown("**风格说明：**")
        st.caption(VISUAL_STYLES.get(visual_style, ""))

    st.divider()

    # 生成按钮
    if st.button("🚀 开始生成导演分镜", use_container_width=True, type="primary"):
        if not story_text.strip():
            st.warning("⚠️ 请输入故事文本！")
            return

        # 构建参数字符串
        tension_val = TENSION_MAP.get(tension_level, 5)
        ar_param = aspect_ratio.split()[0]  # 提取 "16:9" 等部分
        style_desc = VISUAL_STYLES.get(visual_style, "")

        params = f"张力:{tension_level}({tension_val}), 风格:{visual_style}, {style_desc}, 画面比例:{ar_param}"

        # 显示生成状态
        with st.spinner("🧠 视觉导演正在构思分镜..."):
            # 调用 DeepSeek API
            ai_result = call_deepseek_api(story_text, params)

        if "error" in ai_result:
            st.error(f"❌ 生成失败：{ai_result['error']}")
        else:
            st.success("🎉 分镜生成成功！")

            # 模块一：展示全局设定
            st.markdown("### 🌍 全局设定（一致性保证）")
            cols = st.columns(4)
            cols[0].metric("核心角色", ai_result["global_settings"].get("main_character", "无"))
            cols[1].metric("环境", ai_result["global_settings"].get("environment", "无"))
            cols[2].metric("光影", ai_result["global_settings"].get("lighting_tone", "无"))
            cols[3].metric("风格", ai_result["global_settings"].get("visual_style", "无"))

            st.markdown("---")

            # 模块二：展示分镜详情
            st.markdown("### 🎞️ 分镜剧本（6 要素标准化）")

            for index, segment in enumerate(ai_result.get("segments", [])):
                with st.expander(f"{segment['shot_id']} : {segment['setting']}", expanded=(index == 0)):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"**🎥 运镜：** {segment['camera']}")
                        st.markdown(f"**😐 情绪：** {segment.get('emotion', '无')}")
                        st.markdown(f"**💪 张力：** {segment.get('tension', '无')}")

                    with col2:
                        st.markdown(f"**🔊 音效：** {segment.get('sfx', '无')}")
                        st.markdown(f"**🗣️ 旁白：** {segment.get('vo', '无')}")

                    st.markdown("---")
                    st.markdown(f"**🎯 动态画面描述提示词：**")
                    st.code(segment.get('visual_prompt', '无'), language="text")

            st.markdown("---")

            # 模块三：一键复制整合版提示词
            st.markdown("### 📋 一键复制到 Seedance")
            final_text = build_final_prompt(
                ai_result.get("segments", []),
                motion_param,
                ar_param
            )
            st.code(final_text, language="text")

            # 下载按钮
            download_content = f"""=== Seedance 2.0 V3.0.2-Lite 导演级分镜 ===

{final_text}

=== 全局设定 ===
核心角色：{ai_result["global_settings"].get("main_character", "无")}
环境：{ai_result["global_settings"].get("environment", "无")}
光影：{ai_result["global_settings"].get("lighting_tone", "无")}
风格：{ai_result["global_settings"].get("visual_style", "无")}

=== 分镜详情（6 要素）===
"""

            for i, seg in enumerate(ai_result.get("segments", []), 1):
                download_content += f"""
分镜 {i}：
镜号：{seg['shot_id']}
场景：{seg['setting']}
运镜：{seg['camera']}
动态画面描述提示词：{seg['visual_prompt']}
旁白：{seg.get('vo', '无')}
音效：{seg.get('sfx', '无')}
情绪：{seg.get('emotion', '无')}
张力：{seg.get('tension', '无')}
"""

            st.download_button(
                label="💾 下载 v3.0.2-Lite 导演级分镜配置",
                data=download_content,
                file_name=f"seedance_v3.0.2_lite_director_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

            # 保存到历史记录（如果函数存在）
            try:
                # 这里可以添加保存历史记录的逻辑
                pass
            except Exception as e:
                logger.warning(f"保存历史记录失败: {e}")

# ================= 6. 主函数入口 =================

def main():
    """主函数"""
    render_ai_director()

if __name__ == "__main__":
    main()
