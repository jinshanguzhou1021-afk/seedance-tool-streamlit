# AI 视觉导演系统 - 完整函数代码

# 这个文件包含 AI 视觉导演系统的所有函数，可以复制到 app.py 中

def render_ai_director():
    """渲染 Seedance 2.0 AI 视觉导演系统"""

    st.subheader("🎬 Seedance 2.0 AI 视觉导演系统")
    st.caption("通过三层导演逻辑，生成极致张力、细腻表情和戏剧化冲突的全中文分镜提示词")

    st.markdown("---")

    # 第一部分：故事输入与情感分析
    col1, col2 = st.columns([2, 1])

    with col1:
        story_text = st.text_area(
            "📖 1. 故事/脚本输入",
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

    # 第二部分：导演控制参数
    col1, col2, col3 = st.columns(3)

    with col1:
        tension_level = st.select_slider(
            "🎭 2. 张力强度调节器",
            options=list(TENSION_MOTION_MAP.keys()),
            value="明显起伏 (中等)",
            help="从平淡叙事到史诗冲突，调节整体张力"
        )

        emotion_filter = st.multiselect(
            "🎨 3. 情绪滤镜",
            list(EMOTION_FILTERS.keys()),
            help="选择情绪基调，可多选"
        )

    with col2:
        expression_select = st.multiselect(
            "😐 4. 表情微操（可选）",
            list(EXPRESSION_ENHANCEMENTS.keys()),
            help="为分镜添加细腻的表情描述"
        )

        action_select = st.multiselect(
            "🏃 5. 动作张力（可选）",
            list(ACTION_ENHANCEMENTS.keys()),
            help="为分镜添加爆发性的动作描述"
        )

    with col3:
        camera_select = st.multiselect(
            "🎥 6. 大师运镜（可选）",
            list(MASTER_CAMERA_MOVES.keys()),
            help="选择大师级镜头语言"
        )

        lighting_select = st.multiselect(
            "💡 7. 戏剧化光影（可选）",
            list(DRAMATIC_LIGHTING.keys()),
            help="选择戏剧化的光影效果"
        )

        aspect_ratio = st.selectbox(
            "📐 8. 画幅比例",
            ["16:9 横屏", "21:9 电影宽屏", "9:16 竖屏", "1:1 方图"],
            help="选择视频的画面比例"
        )

    st.divider()

    # 生成按钮
    if st.button("🎬 生成导演级分镜提示词", type="primary", use_container_width=True):
        if not story_text:
            st.warning("⚠️ 请先输入故事或脚本！")
        else:
            with st.spinner("AI 视觉导演正在分析故事..."):
                # 三层导演逻辑
                dramatic_storyboard = generate_dramatic_storyboard(
                    story_text,
                    tension_level,
                    emotion_filter,
                    expression_select,
                    action_select,
                    camera_select,
                    lighting_select,
                    aspect_ratio
                )

                # 显示结果
                st.success("✅ 导演级分镜已生成！")

                # 使用标签页展示不同分镜
                tabs = st.tabs([f"分镜 {i+1}" for i in range(len(dramatic_storyboard['segments']))])

                for i, tab in enumerate(tabs):
                    with tab:
                        st.markdown(f"### 🎬 分镜 {i+1}")

                        # 分镜信息卡片
                        segment = dramatic_storyboard['segments'][i]

                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**时间：** {segment['time']}")
                            st.markdown(f"**情节：** {segment['plot']}")

                        with col2:
                            st.markdown(f"**情绪：** {segment['emotion']}")
                            st.markdown(f"**张力：** {segment['tension']}")

                        st.markdown("---")
                        st.markdown(f"**📝 分镜描述：**")
                        st.code(segment['description'], language="text")

                # 显示完整提示词
                st.markdown("---")
                st.markdown("### 🎯 完整 Seedance 2.0 提示词（复制到 Seedance 使用）")
                st.code(dramatic_storyboard['final_prompt'], language="text")

                # 下载按钮
                download_content = f"""=== Seedance 2.0 导演级分镜 ===

{dramatic_storyboard['final_prompt']}

=== 导演信息 ===
张力强度：{tension_level}
情绪滤镜：{', '.join(emotion_filter) if emotion_filter else '无'}
表情微操：{', '.join(expression_select) if expression_select else '无'}
动作张力：{', '.join(action_select) if action_select else '无'}
大师运镜：{', '.join(camera_select) if camera_select else '无'}
戏剧光影：{', '.join(lighting_select) if lighting_select else '无'}
画幅比例：{aspect_ratio}

=== 分镜详情 ===
"""
                for i, seg in enumerate(dramatic_storyboard['segments']):
                    download_content += f"""
分镜 {i+1}：
时间：{seg['time']}
情节：{seg['plot']}
情绪：{seg['emotion']}
张力：{seg['tension']}
描述：{seg['description']}

"""

                st.download_button(
                    label="💾 下载导演级分镜配置",
                    data=download_content,
                    file_name=f"seedance_director_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

                # 保存到历史记录
                save_to_history(
                    "AI视觉导演",
                    story_text,
                    dramatic_storyboard['final_prompt'],
                    len(dramatic_storyboard['segments']) > 0
                )


# ================= AI 视觉导演核心逻辑 =================

def analyze_story_emotion(text):
    """第一层：情感语义解析器"""

    # 情绪关键词映射
    emotion_keywords = {
        "压抑": ["压抑", "沉重", "痛苦", "绝望", "黑暗"],
        "转折": ["突然", "但是", "然而", "意外", "转折"],
        "爆发": ["爆发", "冲突", "争吵", "打斗", "愤怒"],
        "高潮": ["高潮", "顶点", "极致", "巅峰", "最后"],
        "悲伤": ["悲伤", "痛苦", "流泪", "难过", "哀伤"],
        "愤怒": ["愤怒", "生气", "怒火", "憎恨", "仇恨"],
        "恐惧": ["恐惧", "害怕", "惊恐", "担心", "害怕"],
        "喜悦": ["喜悦", "快乐", "开心", "幸福", "快乐"],
        "绝望": ["绝望", "放弃", "无望", "崩溃", "绝望"]
    }

    emotions = []
    text_lower = text.lower()

    # 检测情绪
    for emotion, keywords in emotion_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            emotions.append(emotion)

    return emotions if emotions else ["平静"]


def generate_dramatic_storyboard(
    story_text,
    tension_level,
    emotion_filter,
    expression_select,
    action_select,
    camera_select,
    lighting_select,
    aspect_ratio
):
    """三层导演逻辑生成戏剧化分镜"""

    # 第一层：情感语义解析
    emotions = analyze_story_emotion(story_text)

    # 根据情绪和故事生成分镜
    segments = []

    # 获取物理参数
    motion_val = TENSION_MOTION_MAP[tension_level]

    # 分解故事为3-5个分镜
    story_sentences = split_story_to_segments(story_text)

    for i, sentence in enumerate(story_sentences):
        # 确定每个分镜的情绪和情节
        if i == 0:
            plot_type = "起"
            emotion = emotions[0] if emotions else "平静"
            tension = "温和"
        elif i == len(story_sentences) - 1:
            plot_type = "合"
            emotion = emotions[-1] if emotions else "平静"
            tension = "强烈"
        else:
            plot_type = "承/转"
            emotion = emotions[1] if len(emotions) > 1 else (emotions[0] if emotions else "平静")
            tension = "中等"

        # 第二层：戏剧化扩充
        dramatic_description = build_dramatic_description(
            sentence,
            emotion,
            tension,
            expression_select,
            action_select,
            camera_select,
            lighting_select
        )

        # 确定时间范围
        if len(story_sentences) == 3:
            if i == 0:
                time_range = "0-5秒"
            elif i == 1:
                time_range = "5-10秒"
            else:
                time_range = "10-15秒"
        elif len(story_sentences) == 4:
            if i == 0:
                time_range = "0-4秒"
            elif i == 1:
                time_range = "4-8秒"
            elif i == 2:
                time_range = "8-12秒"
            else:
                time_range = "12-15秒"
        elif len(story_sentences) == 5:
            if i == 0:
                time_range = "0-3秒"
            elif i == 1:
                time_range = "3-6秒"
            elif i == 2:
                time_range = "6-9秒"
            elif i == 3:
                time_range = "9-12秒"
            else:
                time_range = "12-15秒"
        else:
            time_range = f"{i*3}-{(i+1)*3}秒"

        segments.append({
            "time": time_range,
            "plot": plot_type,
            "emotion": emotion,
            "tension": tension,
            "description": dramatic_description
        })

    # 第三层：组装最终提示词
    final_prompt = build_final_director_prompt(
        segments,
        motion_val,
        aspect_ratio
    )

    return {
        "segments": segments,
        "final_prompt": final_prompt
    }


def split_story_to_segments(story_text):
    """将故事切分为3-5个逻辑连贯的分镜"""

    # 按标点符号切分
    import re
    sentences = re.split(r'[。！？]', story_text)

    # 过滤空字符串
    sentences = [s.strip() for s in sentences if s.strip()]

    # 限制在3-5个分镜
    if len(sentences) > 5:
        sentences = sentences[:5]
    elif len(sentences) < 3:
        # 如果分镜太少，按长度切分
        words = story_text.split()
        if len(words) <= 20:
            sentences = [story_text]
        elif len(words) <= 40:
            mid = len(words) // 2
            sentences = [' '.join(words[:mid]), ' '.join(words[mid:])]
        else:
            third = len(words) // 3
            sentences = [
                ' '.join(words[:third]),
                ' '.join(words[third:2*third]),
                ' '.join(words[2*third:])
            ]

    return sentences


def build_dramatic_description(
    sentence,
    emotion,
    tension,
    expression_select,
    action_select,
    camera_select,
    lighting_select
):
    """第二层：戏剧化扩充引擎"""

    description_parts = []

    # 基础场景描述
    description_parts.append(sentence)

    # 添加表情微操
    if emotion in expression_select:
        description_parts.append(EXPRESSION_ENHANCEMENTS[emotion])

    # 添加动作张力
    if action_select:
        for action in action_select:
            description_parts.append(ACTION_ENHANCEMENTS[action])

    # 添加运镜
    if camera_select:
        for camera in camera_select:
            description_parts.append(MASTER_CAMERA_MOVES[camera])

    # 添加光影
    if lighting_select:
        for lighting in lighting_select:
            description_parts.append(DRAMATIC_LIGHTING[lighting])

    # 组合成描述
    return "。".join(description_parts)


def build_final_director_prompt(segments, motion_val, aspect_ratio):
    """第三层：Seedance 2.0 适配器"""

    # 转换画幅比例
    ar_map = {
        "16:9 横屏": "--ar 16:9",
        "21:9 电影宽屏": "--ar 21:9",
        "9:16 竖屏": "--ar 9:16",
        "1:1 方图": "--ar 1:1"
    }
    ar_param = ar_map.get(aspect_ratio, "--ar 16:9")

    # 组装完整提示词
    prompt_parts = []

    # 添加电影级画质
    prompt_parts.append("电影级画质，极致细节")

    # 添加所有分镜
    for i, segment in enumerate(segments):
        prompt_parts.append(f"{segment['time']}：{segment['description']}")

    # 添加 Seedance 2.0 物理参数
    prompt_parts.append(f"--motion {motion_val} {ar_param}")

    # 组合成最终字符串
    final_prompt = "\n".join(prompt_parts)

    return final_prompt
