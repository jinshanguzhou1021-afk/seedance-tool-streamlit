#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即梦提示词工具 - Streamlit Web 应用（整合版）
两个核心功能：分镜生成器 + 分镜提示词
版本: V3.1.0
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

# ================= API 配置 =================

# DeepSeek API 配置
try:
    API_KEY = st.secrets["DEEPSEEK_API_KEY"]
    API_MODE = "Secrets"
except (KeyError, FileNotFoundError):
    API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    if API_KEY:
        API_MODE = "环境变量"
    else:
        API_KEY = "sk-2f2c80b0af064d2a8ef04990630c8d7d"
        API_MODE = "内置 fallback"
        st.sidebar.warning("⚠️ 正在使用硬编码的 API Key，请尽快迁移到 st.secrets")

# API 配置
API_BASE_URL = "https://api.deepseek.com"
API_MODEL = "deepseek-chat"

# 初始化 OpenAI 客户端
try:
    client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)
except Exception as e:
    st.error(f"❌ API 客户端初始化失败：{str(e)}")
    client = None

# ================= 参数配置 =================

# 画面比例
ASPECT_RATIOS = {
    "16:9 横屏": "--ar 16:9",
    "9:16 竖屏": "--ar 9:16",
    "1:1 方形": "--ar 1:1",
    "2.35:1 电影宽屏": "--ar 2.35:1"
}

# 视觉风格
VISUAL_STYLES = {
    "🎬 电影感": "电影级质感，高对比度，专业摄影",
    "🌸 青春校园": "明亮色调，青春气息，清新自然",
    "🤖 赛博朋克": "霓虹灯光，冷色调，未来科技感",
    "⚔️ 仙侠奇幻": "柔和光影，古雅风格，水墨质感",
    "📷 写实": "真实质感，自然光线，细节丰富",
    "🎨 动画": "色彩鲜明，扁平化风格，卡通感",
    "🎞️ 复古": "胶片质感，暖色调，怀旧感",
    "🚀 科幻": "冷色调，科技感，未来主义",
    "🌊 水墨风": "黑白灰，留白，东方美学",
    "🎭 国潮": "中国红，金色，传统纹样",
    "🚂 蒸汽朋克": "黄铜质感，齿轮，维多利亚风格",
    "🎥 纪录片": "手持摄影，自然光，真实感",
    "📱 短视频": "明快节奏，流行色调，网红感",
    "🌟 网红风": "高饱和度，滤镜感，时尚感",
    "🎪 狂欢节": "色彩丰富，活泼，节日氛围"
}

# 场景类型
SCENE_TYPES = {
    "⚔️ 动作/打斗": "动作场景，战斗，激烈",
    "🎭 剧情/对话": "剧情展开，对话，情感",
    "📢 商业广告": "产品展示，营销，商业",
    "🏞️ 风景/环境": "自然风光，环境展示，唯美",
    "📦 产品展示": "产品特写，360度，细节",
    "🌟 奇幻/仙侠": "奇幻场景，魔法，仙侠",
    "🚀 科幻/未来": "未来世界，科技，科幻",
    "🎵 音乐MV": "音乐画面，节奏感，情感",
    "😄 喜剧搞笑": "幽默，搞笑，轻松",
    "💕 情感爱情": "浪漫，爱情，甜蜜",
    "🔍 悬疑惊悚": "紧张，悬疑，惊悚",
    "🌈 治愈温暖": "温暖，治愈，平静"
}

# 运镜语言
CAMERA_MOVES = {
    "📸 静态镜头": "固定机位，稳定",
    "🔍 特写": "Close-up",
    "👥 中景": "Medium Shot",
    "🏞️ 全景": "Wide Shot",
    "🎥 慢推": "Slow Zoom In",
    "⬆️ 快推": "Fast Zoom In",
    "⬇️ 拉远": "Zoom Out",
    "↔️ 平移": "Pan",
    "🔄 环绕": "Orbit",
    "🚶 跟拍": "Tracking",
    "🎢 摇镜": "Tilt"
}

# 光影效果
LIGHTING_STYLES = {
    "💡 自然光": "自然光线，柔和",
    "🌅 黄金时刻": "暖色调，夕阳",
    "🌙 月光": "冷色调，夜晚",
    "🔆 高对比度": "强明暗对比，戏剧化",
    "🌈 柔和光": "柔和光线，均匀",
    "⚡ 戏剧光": "戏剧化光效，强烈",
    "🌫️ 逆光": "背光，剪影效果",
    "✨ 侧光": "侧光，立体感",
    "🎆 顶光": "顶光，神秘感"
}

# 画质标签
QUALITY_TAGS = {
    "8K 超高清": "8K, ultra HD, cinematic",
    "4K 高清": "4K, high quality",
    "电影级画质": "cinematic quality",
    "极致细节": "ultra detailed",
    "专业摄影": "professional photography",
    "光影完美": "perfect lighting"
}

# ================= 辅助函数 =================

def load_history():
    """加载历史记录"""
    if "history" not in st.session_state:
        st.session_state.history = []

def save_to_history(tool_type, prompt, result, use_ai):
    """保存到历史记录"""
    st.session_state.history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tool": tool_type,
        "prompt": prompt,
        "result": result,
        "use_ai": use_ai
    })

def calculate_time_segments(duration):
    """计算时间分段"""
    if duration <= 5:
        return [(0, duration)]
    elif duration <= 10:
        return [(0, 5), (5, duration)]
    else:
        return [(0, 5), (5, 10), (10, duration)]

# ================= AI 生成函数 =================

def generate_with_deepseek(story_text, duration, ratio, style, scene_type):
    """使用 DeepSeek API 生成分镜"""

    system_instruction = f"""你是一位顶尖的 AI 视频提示词专家（精通 Seedance, Runway, Kling）。

你的任务：将用户的文字稿转化为具有空间逻辑一致性和前后分镜连续的 Seedance 2.0 专业分镜。

## 核心要求

1. **视觉化要求**
   - 绝对不要直接复制用户的原话！
   - 将对话转化为具体的画面描述（面部表情、肢体动作、眼神交流、光影变幻）

2. **运镜术语**
   - 必须包含具体的专业运镜术语（特写、慢推、环绕、平移等）

3. **音效设计**
   - 音效必须具体，不要写"根据场景调整"
   - 例如："舒缓大提琴带有轻微混响"、"微风吹拂树叶声"

## 目标规格
- 时长：{duration}秒
- 画幅：{ratio}
- 视觉风格：{style}
- 场景类型：{scene_type}

## 输出格式（严格按此格式）

{duration}秒🎭 {scene_type}场景，🎬 {style}，{ratio}。

时间轴（AI 增强）：
- 0-5秒：[分镜1：角色外貌、动作、环境光影描述] + [具体运镜方式]
- 5-10秒：[分镜2：神态变化、肢体动作描述] + [具体运镜方式]
- 10-{duration}秒：[分镜3：情节高潮动作描述] + [具体运镜方式]

音效设计（AI 建议）：
- 背景音乐：[具体的乐器、节奏]
- 音效：[具体的环境摩擦音]
"""

    if not client:
        return "🚨 API 客户端未初始化，请检查配置"

    try:
        response = client.chat.completions.create(
            model=API_MODEL,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"请将这段内容改为完美的视频画面分镜：\n{story_text}"}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"🚨 AI 生成遇到问题：{str(e)}\n请检查 API Key 或网络状态。"

def generate_locally(story_text, duration, ratio, style, scene_type):
    """本地生成分镜（简化版）"""

    segments = calculate_time_segments(duration)

    result = f"{duration}秒{scene_type}场景，{style}风格，{ratio}。\n\n时间轴：\n"

    for i, (start, end) in enumerate(segments):
        if i == 0:
            desc = f"{start}-{end}秒：{story_text}的引入，镜头缓慢推近，建立场景"
        elif i == len(segments) - 1:
            desc = f"{start}-{end}秒：{story_text}的高潮部分，{style}风格，拉远定格"
        else:
            desc = f"{start}-{end}秒：{story_text}的发展，{style}风格，环绕拍摄"
        result += f"- {desc}\n"

    # 添加音效建议
    result += "\n音效设计：\n"
    result += f"- 背景音乐：根据{style}风格选择合适的音乐\n"
    result += f"- 音效：根据场景添加环境音效\n"

    return result

# ================= 模块 1：分镜生成器 =================

def render_storyboard_generator():
    """渲染分镜生成器（整合分镜生成器 + 提示词生成器）"""

    st.header("📝 分镜生成器")
    st.markdown("快速生成分镜提示词，支持单个/多个版本，可选择 AI 增强")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📋 输入设置")

        # 创意描述
        story_input = st.text_area(
            "创意描述/故事内容",
            placeholder="例如：一对情侣在夕阳下对视，准备表白",
            height=150,
            help="描述你想创建的视频内容"
        )

        st.markdown("### ⚙️ 参数设置")

        # 视频时长
        duration = st.slider(
            "视频时长（秒）",
            min_value=4,
            max_value=15,
            value=15,
            step=1,
            help="Seedance 2.0 支持 4-15 秒视频"
        )

        # 画面比例
        ratio = st.selectbox(
            "画面比例",
            list(ASPECT_RATIOS.keys()),
            index=0,
            help="选择视频的画面比例"
        )

        # 视觉风格
        style = st.selectbox(
            "视觉风格",
            list(VISUAL_STYLES.keys()),
            index=0,
            help="选择视频的整体视觉风格"
        )

        # 场景类型
        scene_type = st.selectbox(
            "场景类型",
            list(SCENE_TYPES.keys()),
            index=0,
            help="选择视频类型"
        )

        # 多版本生成
        version_count = st.slider(
            "生成版本数",
            min_value=1,
            max_value=5,
            value=1,
            step=1,
            help="生成多个不同版本的提示词供选择"
        )

        # AI 增强
        use_ai = st.toggle("🤖 使用 DeepSeek AI 增强", value=True,
                           help="开启后使用 DeepSeek AI 进行智能生成，关闭后使用本地模拟")

        # 生成按钮
        generate_btn = st.button("🎬 生成分镜", type="primary", use_container_width=True)

    with col2:
        st.subheader("📤 生成结果")

        if generate_btn:
            if not story_input:
                st.warning("⚠️ 请输入创意描述！")
            else:
                with st.spinner(f"正在生成 {version_count} 个版本的提示词（{'AI 增强' if use_ai else '本地'}）..."):
                    results = []

                    for i in range(version_count):
                        version = i + 1

                        if use_ai:
                            result = generate_with_deepseek(story_input, duration, ratio, style, scene_type)
                        else:
                            result = generate_locally(story_input, duration, ratio, style, scene_type)

                        results.append(result)

                # 显示结果
                st.success(f"✅ 已生成 {version_count} 个版本的提示词！（{'AI 增强' if use_ai else '本地'}）")

                # 使用标签页显示不同版本
                if version_count > 1:
                    tabs = st.tabs([f"版本 {i+1}" for i in range(version_count)])
                    for i, tab in enumerate(tabs):
                        with tab:
                            st.code(results[i], language="text")
                else:
                    st.code(results[0], language="text")

                # 下载所有版本
                all_results = "\n\n=== 版本分隔 ===\n\n".join([f"版本 {i+1}：\n{r}" for i, r in enumerate(results)])

                st.download_button(
                    label="💾 下载所有版本",
                    data=all_results,
                    file_name=f"seedance_storyboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

                # 保存到历史
                save_to_history("分镜生成器", story_input, all_results, use_ai)

        else:
            st.info("👆 在左侧输入参数并生成")

# ================= 模块 2：分镜提示词 =================

def render_prompt_builder():
    """渲染分镜提示词（整合高级构建器 + AI 视觉导演）"""

    st.header("🧩 分镜提示词")
    st.markdown("专业级分镜提示词构建器，支持手动/AI 双模式")

    # 模式切换
    mode = st.radio(
        "选择模式",
        ["手动模式", "AI 专业模式"],
        horizontal=True,
        help="手动模式：模块化构建 | AI 专业模式：三层导演逻辑"
    )

    st.markdown("---")

    if mode == "手动模式":
        render_manual_mode()
    else:
        render_ai_professional_mode()

def render_manual_mode():
    """手动模式渲染"""

    st.subheader("🔧 手动模式 - 模块化构建")

    col1, col2 = st.columns([2, 1])

    with col1:
        # 画面主体
        base_prompt = st.text_area(
            "🎬 1. 画面主体与动作",
            placeholder="例如：一个穿着黑色风衣的赛博朋克女孩，在下雨的霓虹街道上奔跑...",
            height=100,
            help="描述你想创建的视频内容，越具体越好"
        )

        # 动态强度
        motion_strength = st.slider(
            "🏃‍♂️ 动态强度",
            min_value=1,
            max_value=10,
            value=5,
            help="1为微动，10为剧烈运动"
        )

    with col2:
        st.info("💡 提示")
        st.markdown("""
        - 主体描述越具体越好
        - 包含人物外观、服装
        - 描述具体动作
        """)

    st.divider()

    # 专业控制参数
    col1, col2, col3 = st.columns(3)

    with col1:
        # 镜头语言
        selected_camera = st.selectbox(
            "🎥 2. 镜头语言",
            list(CAMERA_MOVES.keys()),
            help="选择镜头运动方式"
        )

        # 画面比例
        aspect_ratio = st.selectbox(
            "📐 3. 画面比例",
            list(ASPECT_RATIOS.keys()),
            help="选择视频的画面比例"
        )

    with col2:
        # 光影氛围
        selected_lighting = st.multiselect(
            "💡 4. 光影氛围",
            list(LIGHTING_STYLES.keys()),
            help="选择光影效果（可多选）"
        )

        # 画质与特效
        selected_quality = st.multiselect(
            "✨ 5. 画质与特效",
            list(QUALITY_TAGS.keys()),
            help="选择画质和特效（可多选）"
        )

    with col3:
        # 反向提示词
        use_negative = st.toggle("🛡️ 启用反向提示词", value=True)

        if use_negative:
            st.caption("防崩坏反向词已开启")

    st.divider()

    # 生成按钮
    if st.button("🚀 生成提示词", type="primary", use_container_width=True):
        if not base_prompt:
            st.warning("⚠️ 请先输入「画面主体与动作」！")
        else:
            with st.spinner("正在组合提示词..."):
                # 基础组合数组
                prompt_parts = []

                # 1. 插入主体
                prompt_parts.append(base_prompt)

                # 2. 插入运镜
                if CAMERA_MOVES[selected_camera]:
                    prompt_parts.append(CAMERA_MOVES[selected_camera])

                # 3. 插入光影
                for lighting in selected_lighting:
                    prompt_parts.append(LIGHTING_STYLES[lighting])

                # 4. 插入画质
                for quality in selected_quality:
                    prompt_parts.append(QUALITY_TAGS[quality])

                # 组合成最终字符串
                final_prompt = ", ".join(prompt_parts)

                # 加上 Seedance/通用引擎参数后缀
                final_prompt += f" --motion {motion_strength} {ASPECT_RATIOS[aspect_ratio]}"

                # 标准视频防崩坏反向提示词
                negative_prompt = "mutated limbs, bad anatomy, deformed, jerky movement, flickering, text, watermark, low resolution, static image"

                # 结果展示
                st.success("✅ 提示词构建完成！")

                st.markdown("### 🎯 正向提示词")
                st.code(final_prompt, language="text")

                if use_negative:
                    st.markdown("### 🚫 反向提示词")
                    st.code(negative_prompt, language="text")

                # 下载按钮
                download_content = f"""=== Seedance 提示词 ===

正向提示词：
{final_prompt}

反向提示词：
{negative_prompt}

=== 生成信息 ===
模式：手动模式
镜头：{selected_camera}
光影：{', '.join(selected_lighting)}
画质：{', '.join(selected_quality)}
动态强度：{motion_strength}
"""

                st.download_button(
                    label="💾 下载提示词配置",
                    data=download_content,
                    file_name=f"seedance_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

                # 保存到历史
                save_to_history("分镜提示词（手动）", base_prompt, final_prompt, False)

def render_ai_professional_mode():
    """AI 专业模式渲染（整合 AI 视觉导演）"""

    st.subheader("🤖 AI 专业模式 - 三层导演逻辑")
    st.caption("通过三层导演逻辑，生成极致张力、细腻表情和戏剧化冲突的全中文分镜提示词")

    st.markdown("---")

    # 故事输入
    col1, col2 = st.columns([2, 1])

    with col1:
        story_text = st.text_area(
            "📖 故事/脚本输入",
            placeholder="输入100字左右的故事或场景描述...",
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
        - 推荐长度：50-150字
        """)

    st.divider()

    # 导演控制参数
    col1, col2, col3 = st.columns(3)

    with col1:
        # 视觉风格
        visual_style = st.selectbox(
            "🎨 视觉风格",
            list(VISUAL_STYLES.keys()),
            index=0,
            help="选择视频的整体视觉风格"
        )

        # 画面比例
        aspect_ratio = st.selectbox(
            "📐 画面比例",
            list(ASPECT_RATIOS.keys()),
            index=0,
            help="选择视频的画面比例"
        )

    with col2:
        # 动态程度
        motion_param = st.slider(
            "画面动态程度 (--motion)",
            1, 10, 5
        )

        # 场景类型
        scene_type = st.selectbox(
            "🎭 场景类型",
            list(SCENE_TYPES.keys()),
            index=0,
            help="选择视频类型"
        )

    with col3:
        st.markdown("**风格说明：**")
        st.caption(VISUAL_STYLES.get(visual_style, ""))

    st.divider()

    # 生成按钮
    if st.button("🎬 生成 AI 导演分镜", type="primary", use_container_width=True):
        if not story_text:
            st.warning("⚠️ 请输入故事或脚本！")
        else:
            # 构建参数
            ratio_param = ASPECT_RATIOS[aspect_ratio]

            with st.spinner("🧠 视觉导演正在构思分镜..."):
                # 调用 DeepSeek API
                result = generate_with_deepseek(story_text, 15, aspect_ratio, visual_style, scene_type)

            if "🚨" in result:
                st.error(result)
            else:
                st.success("🎉 AI 导演级分镜已生成！")

                # 显示结果
                st.markdown("### 🎬 AI 生成的分镜提示词")
                st.code(result, language="text")

                # 下载按钮
                download_content = f"""=== Seedance 2.0 AI 导演级分镜 ===

{result}

=== 元数据 ===
模式：AI 专业模式
风格：{visual_style}
场景类型：{scene_type}
画面比例：{aspect_ratio}
动态程度：{motion_param}
"""

                st.download_button(
                    label="💾 下载 AI 导演分镜配置",
                    data=download_content,
                    file_name=f"seedance_ai_director_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

                # 保存到历史
                save_to_history("分镜提示词（AI）", story_text, result, True)

# ================= 历史记录 =================

def render_history():
    """渲染历史记录"""

    st.header("📚 历史记录")
    st.markdown("查看之前的生成记录")

    load_history()

    if not st.session_state.history:
        st.info("暂无历史记录，开始生成第一个提示词吧！")
    else:
        # 搜索框
        search = st.text_input("🔍 搜索历史记录", placeholder="输入关键词搜索...")

        # 过滤历史
        if search:
            filtered_history = [
                h for h in st.session_state.history
                if search.lower() in h['prompt'].lower() or search.lower() in h['result'].lower()
            ]
        else:
            filtered_history = st.session_state.history

        # 显示历史
        for i, entry in enumerate(reversed(filtered_history)):
            with st.expander(f"📅 {entry['timestamp']} - {entry['tool']}{' 🤖' if entry.get('use_ai', False) else ''}"):
                st.markdown(f"**输入：**\n{entry['prompt']}")
                st.markdown(f"\n**输出：**")
                st.code(entry['result'], language="text")

        # 清除历史按钮
        if st.button("🗑️ 清除所有历史记录"):
            if st.session_state.get('confirm_clear', False):
                st.session_state.history = []
                st.success("✅ 历史记录已清除！")
                st.session_state.confirm_clear = False
                st.rerun()
            else:
                st.warning("⚠️ 确认要清除所有历史记录吗？")
                st.session_state.confirm_clear = True
                st.rerun()

        st.info("💡 提示：在本地运行时，历史记录会保存；在 Streamlit Cloud 上，历史记录仅在当前会话有效。")

# ================= 关于 =================

def render_about():
    """渲染关于页面"""

    st.header("ℹ️ 关于")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("版本", "3.1.0")
        st.metric("发布日期", "2026-03-06")

    with col2:
        st.metric("核心功能", "2 个")
        st.metric("框架", "Streamlit + DeepSeek V3")

    with col3:
        st.metric("状态", "✅ 正常运行")
        st.metric("新增", "功能整合")

    st.markdown("---")

    st.markdown("### 📝 核心功能")

    st.markdown("""
    **1. 分镜生成器**（整合分镜生成器 + 提示词生成器）
    - 快速生成分镜提示词
    - 支持单个/多个版本
    - 标准/AI 模式切换

    **2. 分镜提示词**（整合高级构建器 + AI 视觉导演）
    - 手动模式：模块化构建
    - AI 专业模式：三层导演逻辑
    - 专业级参数控制
    """)

    st.markdown("---")

    st.markdown("### 🔑 API 配置")

    st.markdown(f"""
    - **API 模式**：{API_MODE}
    - **API 模型**：{API_MODEL}
    - **API 地址**：{API_BASE_URL}
    """)

    st.markdown("---")

    st.markdown("### 💡 使用建议")

    st.markdown("""
    - **快速生成**：使用「分镜生成器」，选择 AI 增强模式
    - **手动控制**：使用「分镜提示词」的手动模式，精确控制每个参数
    - **专业创作**：使用「分镜提示词」的 AI 专业模式，获取导演级分镜
    """)

# ================= 主函数 =================

def main():
    # 加载历史记录
    load_history()

    # 标题
    st.title("🎬 即梦提示词工具 v3.1.0")
    st.markdown("两个核心功能：**分镜生成器** + **分镜提示词** | 整合版 | DeepSeek V3 AI | 三层导演逻辑")

    # 侧边栏
    with st.sidebar:
        st.markdown("### ⚙️ 设置")

        # API 状态
        st.info(f"🔑 API 模式：{API_MODE}")

        # 深色模式
        dark_mode = st.toggle("🌙 深色模式", value=False)

    # 功能选择
    page = st.radio(
        "选择功能",
        ["📝 分镜生成器", "🧩 分镜提示词", "📚 历史记录", "ℹ️ 关于"],
        label_visibility="collapsed"
    )

    # 统计
    st.sidebar.markdown("### 📊 统计")
    if st.session_state.history:
        total = len(st.session_state.history)
        ai_used = sum(1 for h in st.session_state.history if h.get('use_ai', False))
        st.metric("总生成次数", total)
        st.metric("AI 增强次数", ai_used)

    # 功能渲染
    if page == "📝 分镜生成器":
        render_storyboard_generator()
    elif page == "🧩 分镜提示词":
        render_prompt_builder()
    elif page == "📚 历史记录":
        render_history()
    elif page == "ℹ️ 关于":
        render_about()

if __name__ == "__main__":
    main()
