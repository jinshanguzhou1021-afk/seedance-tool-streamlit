# 🎬 Seedance 2.0 AI 视觉导演系统 - 集成代码

# ================= 插入到 app.py 的指定位置 =================

# 1. 在词库定义区域添加戏剧化预设库（在 ASPECT_RATIOS 之后，约第 85 行之后）

# ================= AI 视觉导演系统词库定义 =================

# 张力强度映射
TENSION_MOTION_MAP = {
    "平淡叙事 (温和)": 3,
    "轻微波动 (平静)": 5,
    "明显起伏 (中等)": 7,
    "紧张刺激 (强烈)": 9,
    "史诗冲突 (极致)": 10
}

# 表情微操库
EXPRESSION_ENHANCEMENTS = {
    "绝望": "眼神空洞无神，嘴角微微下撇，面部肌肉松弛",
    "愤怒": "眉毛紧锁，牙关咬紧，面部肌肉紧绷，眼中血丝隐现",
    "恐惧": "瞳孔收缩，嘴唇颤抖，额角冷汗直流，呼吸急促",
    "悲伤": "眼中含泪，眼眶发红，眉头微蹙，神情落寞",
    "喜悦": "眉开眼笑，嘴角上扬，眼中闪烁光芒，面部肌肉舒展",
    "惊讶": "眼睛睁大，嘴巴微张，表情定格一瞬，瞳孔放大",
    "坚定": "眼神如炬，嘴唇紧闭，面容严肃，神情专注",
    "疯狂": "瞳孔震颤，嘴角抽搐，面部扭曲，眼神狂乱",
    "温柔": "眼神柔和，嘴角含笑，表情平静，气质温婉",
    "冷漠": "目光冰冷，面无表情，眼神空洞，神情淡漠"
}

# 动作张力库
ACTION_ENHANCEMENTS = {
    "慢动作爆发": "慢放镜头捕捉瞬间，细节清晰可见，时间被拉长",
    "碎屑飞溅": "物体破碎瞬间，碎片四处飞溅，粒子特效绚丽",
    "衣物撕裂": "衣物被撕裂的特写，布料纤维分离，细节清晰",
    "剧烈喘息": "胸口剧烈起伏，呼吸声清晰可闻，喉结滚动",
    "肌肉颤抖": "肌肉微微颤抖，青筋暴起，力量感十足",
    "突然转身": "猛然转身带起风声，头发飞扬，衣摆猎猎",
    "跌倒爬起": "跌倒后艰难爬起，挣扎动作真实，灰尘飞扬"
}

# 大师运镜库
MASTER_CAMERA_MOVES = {
    "希区柯克变焦": "镜头不动，推镜头与拉镜头反向运动，营造眩晕不安",
    "荷兰斜角": "镜头倾斜构图，画面失衡，营造紧张不安感",
    "手持晃动感": "镜头轻微晃动，呼吸感强烈，营造真实临场感",
    "低角度仰拍": "低角度仰拍，主体显得高大威猛，压迫感强烈",
    "高角度俯拍": "高角度俯拍，主体显得渺小脆弱，孤独感十足",
    "环绕拍摄": "镜头环绕主体运动，全方位展示，空间感强烈",
    "跟拍镜头": "镜头跟随主体运动，节奏一致，代入感极强",
    "推拉组合": "推镜头+拉镜头组合，空间变化丰富，张力十足"
}

# 情绪滤镜库
EMOTION_FILTERS = {
    "忧郁": "冷色调，低饱和度，阴影沉重，氛围压抑",
    "惊悚": "高对比度，强烈明暗，锐利线条，不安感",
    "热血": "暖色调，高饱和度，红色为主，燃烧感",
    "赛博": "霓虹色彩，冷蓝色调，光效绚烂，科技感",
    "国风": "水墨色调，留白艺术，金色点缀，古雅感",
    "治愈": "暖色调，柔和光线，高亮度，温馨感",
    "悬疑": "低亮度，强烈对比，阴影深重，神秘感",
    "浪漫": "粉色系，柔光效果，朦胧美感，氛围甜蜜"
}

# 戏剧化光影库
DRAMATIC_LIGHTING = {
    "强烈侧逆光": "强烈的侧逆光，勾勒出人物剪影，明暗对比极端",
    "丁达尔效应": "光束穿透尘埃，形成丁达尔效应，神圣庄严",
    "霓虹灯效": "霓虹灯光闪烁，色彩绚丽，光晕弥漫，赛博朋克",
    "黄金时刻": "金色暖光沐浴，色调温暖柔和，时间凝固感",
    "雷光闪烁": "背景雷光闪烁，瞬间强光，照亮一切，戏剧化"
}

# 2. 添加 AI 视觉导演渲染函数（在 render_prompt_builder() 之后，约第 640 行之后）

# ================= AI 视觉导演渲染函数 =================
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
        "恐惧": ["恐惧", "害怕", "惊恐", "害怕", "担心"],
        "喜悦": ["喜悦", "快乐", "开心", "幸福", "快乐"],
        "绝望": ["绝望", "绝望", "无望", "放弃", "崩溃"]
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
            emotion = emotions[1] if len(emotions) > 1 else emotions[0] if emotions else "平静"
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

    # 按句号、问号、感叹号切分
    import re
    sentences = re.split(r'[。！？]', story_text)

    # 过滤空字符串
    sentences = [s.strip() for s in sentences if s.strip()]

    # 限制在3-5个分镜
    if len(sentences) > 5:
        sentences = sentences[:5]
    elif len(sentences) < 3:
        # 如果分镜太少，按时间切分
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
