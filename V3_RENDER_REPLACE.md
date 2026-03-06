# ================= v3.0.0 render_ai_director() 函数完整重写 =================

# 使用说明：
# 1. 在 app.py 中找到 "def render_ai_director():" 行（约 line 937）
# 2. 删除该函数到下一个 def 之前的所有内容
# 3. 粘贴以下完整代码
# 4. 测试并提交

def render_ai_director():
    """渲染 Seedance 2.0 AI 全能导演系统 v3.0.0（视听一致性引擎 + 6要素标准化）"""

    st.subheader("🎬 Seedance 2.0 AI 全能导演工作站 v3.0.0")
    st.caption("视听一致性引擎 + 三层导演逻辑 + 6要素标准化剧本")

    st.markdown("---")

    # ================= v3.0.0 全局设定（三层架构 - 第一层） =================

    st.subheader("🌐 第一层：全局设定（视听一致性保证）")
    st.info("💡 这些设定会在所有分镜中保持一致，防止角色变脸和环境跳戏")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        global_character = st.text_input(
            "👤 核心角色（外貌特征）",
            placeholder="例如：复仇者、剑客、情侣",
            help="描述核心角色的外貌特征（发色、服装、性格）"
        )

    with col2:
        global_environment = st.text_input(
            "🏞️ 环境设定（地点 + 时间 + 天气）",
            placeholder="例如：极寒雪原 - 黄昏",
            help="描述空间位置、时间、天气"
        )

    with col3:
        global_lighting_tone = st.selectbox(
            "💡 光影基调",
            ["自然光", "高对比度", "强烈明暗", "暖色调", "冷色调"],
            index=0,
            help="选择整体的光影基调"
        )

    with col4:
        global_visual_style = st.selectbox(
            "🎨 视觉风格",
            ["电影感", "写实", "动画", "赛博朋克", "东方武侠", "唯美"],
            index=0,
            help="选择整体的视觉风格"
        )

    # 全局设定集合
    global_settings = {
        "main_character": global_character,
        "environment": global_environment,
        "lighting_tone": global_lighting_tone,
        "visual_style": global_visual_style
    }

    st.markdown("---")

    # ================= v3.0.0 故事输入 =================

    col1, col2 = st.columns([2, 1])

    with col1:
        story_text = st.text_area(
            "📖 1. 故事/脚本输入（100-300字）",
            placeholder="输入100-300字的故事或场景描述...",
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

    st.markdown("---")

    # ================= v3.0.0 导演控制参数（三层架构 - 第二、三层） =================

    st.subheader("🎥 第二层：导演控制参数")

    col1, col2, col3 = st.columns(3)

    with col1:
        tension_level = st.select_slider(
            "🎭 2. 张力强度调节器（5级）",
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
            help="为分镜添加细腻的表情描述（10种）"
        )

        action_select = st.multiselect(
            "🏃 5. 动作张力（可选）",
            list(ACTION_ENHANCEMENTS.keys()),
            help="为分镜添加爆发性的动作描述（7种）"
        )

    with col3:
        camera_select = st.multiselect(
            "🎥 6. 大师运镜（可选）",
            list(MASTER_CAMERA_MOVES.keys()),
            help="选择大师级镜头语言（7种）"
        )

        lighting_select = st.multiselect(
            "💡 7. 戏剧化光影（可选）",
            list(DRAMATIC_LIGHTING.keys()),
            help="选择戏剧化的光影效果（5种）"
        )

        aspect_ratio = st.selectbox(
            "📐 8. 画幅比例",
            ["16:9 横屏", "21:9 电影宽屏", "9:16 竖屏", "1:1 方图"],
            index=0,
            help="选择视频的画面比例"
        )

    st.markdown("---")

    # ================= v3.0.0 API 模式选择 =================

    col1, col2 = st.columns(2)

    with col1:
        api_mode = st.selectbox(
            "🤖 9. AI 模式选择",
            ["OpenAI GPT-4 (付费 - 最高质量)", "DeepSeek-V3 (免费 - 优秀质量)", "本地模拟 (快速)"],
            index=0,
            help="OpenAI GPT-4 质量最高，DeepSeek-V3 免费但稳定，本地模拟最快"
        )

    with col2:
        if api_mode == "OpenAI GPT-4 (付费 - 最高质量)":
            st.info("💡 OpenAI GPT-4：最高质量，最具文学性和电影感")
        elif api_mode == "DeepSeek-V3 (免费 - 优秀质量)":
            st.info("💡 DeepSeek-V3：免费但稳定，质量优秀")
        else:
            st.info("💡 本地模拟：速度最快，适合快速测试")

    st.markdown("---")

    # ================= v3.0.0 生成按钮 =================

    if st.button("🎬 生成 v3.0.0 导演级分镜（视听一致性 + 6要素标准化剧本）", type="primary", use_container_width=True):
        if not story_text:
            st.warning("⚠️ 请先输入故事或脚本！")
        else:
            with st.spinner("AI 全能导演正在分析故事...（三层导演逻辑）"):

                # ================= v3.0.0 生成逻辑 =================

                if api_mode == "本地模拟 (快速)":
                    # 本地模拟模式
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

                    # 添加 v3.0.0 兼容层（添加 6 要素）
                    for segment in result["segments"]:
                        if "vo" not in segment:
                            segment["vo"] = ""
                        if "sfx" not in segment:
                            segment["sfx"] = ""

                    # 显示 v3.0.0 格式
                    display_v3_result(result, api_mode, story_text, global_settings, tension_level, aspect_ratio)

                else:
                    # API 模式（OpenAI 或 DeepSeek）
                    if api_mode == "DeepSeek-V3 (免费 - 优秀质量)":
                        # DeepSeek API 调用
                        result = call_deepseek_api_director(
                            story_text,
                            tension_level,
                            emotion_filter,
                            expression_select,
                            action_select,
                            camera_select,
                            lighting_select
                        )

                        # 尝试解析为 v3.0.0 格式
                        if "segments" in result and result["segments"]:
                            # 检查是否有 6 要素
                            needs_upgrade = False
                            for segment in result["segments"]:
                                if "vo" not in segment or "sfx" not in segment:
                                    needs_upgrade = True
                                    break

                            if needs_upgrade:
                                # 添加 v3.0.0 兼容层
                                for segment in result["segments"]:
                                    if "vo" not in segment:
                                        segment["vo"] = ""
                                    if "sfx" not in segment:
                                        segment["sfx"] = ""

                        # 显示结果
                        display_v3_result(result, api_mode, story_text, global_settings, tension_level, aspect_ratio)

                    elif api_mode == "OpenAI GPT-4 (付费 - 最高质量)":
                        # OpenAI GPT-4 调用（使用 v3.0.0 System Prompt）
                        try:
                            # 调用 v3.0.0 API 函数
                            result = call_openai_api_director_v3(
                                story_text,
                                api_mode,
                                global_settings,
                                tension_level,
                                emotion_filter,
                                expression_select,
                                action_select,
                                camera_select,
                                lighting_select,
                                aspect_ratio
                            )

                            # 显示 v3.0.0 格式
                            display_v3_result(result, api_mode, story_text, global_settings, tension_level, aspect_ratio)

                        except Exception as e:
                            st.error(f"❌ OpenAI API 调用失败：{str(e)}")
                            st.info("💡 建议：切换到 DeepSeek-V3 模式或本地模拟模式")


def display_v3_result(result, api_mode, story_text, global_settings, tension_level, aspect_ratio):
    """显示 v3.0.0 导演级分镜结果（6要素标准化）"""

    if "error" in result:
        st.error(f"❌ {result['error']}")
    elif "segments" in result and result["segments"]:
        st.success(f"✅ v3.0.0 导演级分镜已生成！({api_mode})")

        # ================= 显示全局设定（第一层） =================

        st.markdown("### 🌐 第一层：全局设定（视听一致性保证）")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("核心角色", result.get("global_settings", {}).get("main_character", global_settings["main_character"]))
        with col2:
            st.metric("环境设定", result.get("global_settings", {}).get("environment", global_settings["environment"]))
        with col3:
            st.metric("光影基调", result.get("global_settings", {}).get("lighting_tone", global_settings["lighting_tone"]))
        with col4:
            st.metric("分镜数量", len(result["segments"]))

        st.markdown("---")

        # ================= 显示分镜剧本（第二层：导演编剧层） =================

        st.markdown("### 🎥 第二层：导演编剧层（6要素标准化剧本）")

        for i, segment in enumerate(result["segments"]):
            with st.expander(f"🎬 分镜 {i+1}: {segment.get('shot_id', 'Shot ' + str(i+1))}"):
                # 分镜信息卡片（4要素）
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(f"**📅 场景：** {segment.get('setting', '未指定')}")
                    st.markdown(f"**🎥 运镜：** {segment.get('camera', '未指定')}")

                with col2:
                    st.markdown(f"**😐 情绪：** {segment.get('emotion', '未指定')}")
                    st.markdown(f"**💪 张力：** {segment.get('tension', '未指定')}")

                with col3:
                    st.markdown(f"**🎤 旁白 (VO):**")
                    vo = segment.get('vo', '无')
                    if vo:
                        st.success(f"\"{vo}\"")
                    else:
                        st.info("（无）")

                with col4:
                    st.markdown(f"**🔊 音效 (SFX):**")
                    sfx = segment.get('sfx', '无')
                    if sfx:
                        st.success(f"\"{sfx}\"")
                    else:
                        st.info("（无）")

                st.markdown("---")

                # 动态画面描述提示词（第三层：Seedance 2.0 适配层）
                st.markdown(f"**🎯 第三层：Seedance 2.0 适配层 - 动态画面描述提示词**")
                st.code(segment.get('visual_prompt', '未指定'), language="text")

        st.markdown("---")

        # ================= 显示完整提示词（第三层） =================

        st.markdown("### 🎯 第三层：Seedance 2.0 适配层 - 完整提示词（复制到 Seedance 使用）")
        st.code(result.get("complete_prompt", ""), language="text")

        # ================= 显示元数据 =================

        st.markdown("### 📊 元数据")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("API 模式", api_mode)
        with col2:
            st.metric("模型", result.get("model", "未知"))
        with col3:
            st.metric("张力强度", tension_level)

        # ================= 下载按钮 =================

        download_content = f"""=== Seedance 2.0 v3.0.0 导演级分镜（视听一致性引擎）===

{result.get("complete_prompt", "")}

=== 元数据 ===
API 模式：{api_mode}
模型：{result.get("model", "未知")}
张力强度：{tension_level}
画幅比例：{aspect_ratio}

=== 第一层：全局设定（视听一致性保证）===
核心角色：{result.get("global_settings", {}).get("main_character", global_settings["main_character"])}
环境设定：{result.get("global_settings", {}).get("environment", global_settings["environment"])}
光影基调：{result.get("global_settings", {}).get("lighting_tone", global_settings["lighting_tone"])}
视觉风格：{result.get("global_settings", {}).get("visual_style", global_settings["visual_style"])}

=== 第二层：导演编剧层（6要素标准化剧本）===
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

        # ================= 保存到历史记录 =================

        save_to_history(
            "AI全能导演v3.0.0",
            story_text,
            result.get("complete_prompt", ""),
            len(result["segments"]) > 0
        )

    else:
        st.warning("⚠️ 未生成任何分镜，请检查输入或 API 配置")
