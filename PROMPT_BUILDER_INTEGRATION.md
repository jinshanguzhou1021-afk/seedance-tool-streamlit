# 🧩 Prompt Builder 集成到 app.py 的代码

# ================= 插入到 app.py 的指定位置 =================

# 1. 在文件开头，import 之后添加词库定义（约第 20 行之后）

# ================= Prompt Builder 词库定义 =================
CAMERA_MOVES = {
    "默认 (Default)": "",
    "推镜头 (Dolly In)": "dolly in, moving forward slowly",
    "拉镜头 (Dolly Out)": "dolly out, moving backward",
    "全景/大远景 (Wide Shot)": "extreme wide shot, panoramic view",
    "特写 (Close-up)": "extreme close-up shot, macro detail",
    "跟随镜头 (Tracking Shot)": "tracking shot, following of subject",
    "无人机航拍 (Drone View)": "drone shot, sweeping aerial view",
    "第一人称视角 (FPV)": "FPV, first person view, dynamic motion"
}

LIGHTING_STYLES = {
    "电影级打光": "cinematic lighting, dramatic shadows",
    "丁达尔效应": "volumetric lighting, god rays",
    "霓虹灯效": "cyberpunk neon lights, glowing ambiance",
    "黄金时刻 (日落/日出)": "golden hour light, warm and soft tone",
    "自然光": "natural ambient light, realistic lighting"
}

QUALITY_TAGS = {
    "8K 超高清": "8k resolution, ultra-detailed",
    "虚幻引擎5渲染": "Unreal Engine 5 render, octane render",
    "胶片质感": "35mm film grain, vintage film aesthetic",
    "极高帧率(慢动作)": "120fps, smooth slow motion, fluid physics"
}

ASPECT_RATIOS = {
    "横屏 (16:9)": "--ar 16:9",
    "竖屏 (9:16)": "--ar 9:16",
    "方图 (1:1)": "--ar 1:1"
}

# 2. 添加 Prompt Builder 渲染函数（在 main() 函数之前，约第 460 行之前）

# ================= Prompt Builder 渲染函数 =================
def render_prompt_builder():
    """渲染高级分镜提示词构建器"""

    st.subheader("🧩 高级分镜提示词构建器 (Prompt Builder)")
    st.caption("按模块选择，自动生成符合 Seedance 引擎底层逻辑的专业英文/中文提示词")

    st.markdown("---")

    # 第一部分：主体与核心动作
    col_main1, col_main2 = st.columns([2, 1])
    with col_main1:
        base_prompt = st.text_area(
            "🎬 1. 画面主体与动作 (Base Prompt)",
            placeholder="例如：一个穿着黑色风衣的赛博朋克女孩，在下雨的霓虹街道上奔跑...",
            height=100,
            help="描述你想创建的视频内容，越具体越好"
        )
    with col_main2:
        st.info("💡 提示：主体描述越具体越好，包含人物外观、服装、正在做的具体动作。")

    motion_strength = st.slider(
        "🏃‍♂️ 动态强度 (Motion)",
        min_value=1,
        max_value=10,
        value=5,
        help="1为微动，10为剧烈运动"
    )

    st.divider()

    # 第二部分：专业控制参数
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_camera = st.selectbox(
            "🎥 2. 镜头语言 (Camera)",
            list(CAMERA_MOVES.keys()),
            help="选择镜头运动方式"
        )
        aspect_ratio = st.selectbox(
            "📐 3. 画幅比例 (Ratio)",
            list(ASPECT_RATIOS.keys()),
            help="选择视频的画面比例"
        )

    with col2:
        selected_lighting = st.multiselect(
            "💡 4. 光影氛围 (Lighting)",
            list(LIGHTING_STYLES.keys()),
            help="选择光影效果（可多选）"
        )
        selected_quality = st.multiselect(
            "✨ 5. 画质与特效 (Quality)",
            list(QUALITY_TAGS.keys()),
            help="选择画质和特效（可多选）"
        )

    with col3:
        use_negative = st.toggle("🛡️ 启用专业反向提示词", value=True)
        if use_negative:
            st.caption("防崩坏反向词已开启")

    st.divider()

    # 生成按钮
    if st.button("🚀 生成专业级 Seedance 提示词", type="primary", use_container_width=True):
        if not base_prompt:
            st.warning("⚠️ 请先输入「画面主体与动作」！")
        else:
            with st.spinner("正在组合提示词..."):
                # 基础组合数组
                prompt_parts = []

                # 1. 插入主体
                prompt_parts.append(base_prompt)

                # 2. 插入运镜（如果有）
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
                st.success("✅ 提示词构建完成！请复制下方内容使用：")

                st.markdown("### 🎯 正向提示词 (Prompt)")
                st.code(final_prompt, language="text")

                if use_negative:
                    st.markdown("### 🚫 反向提示词 (Negative Prompt)")
                    st.code(negative_prompt, language="text")

                # 保存到历史记录
                save_to_history("高级构建器", base_prompt, f"Prompt: {final_prompt}\nNegative: {negative_prompt}", use_negative)

                # 下载按钮
                download_content = f"=== Seedance 提示词 ===\n\n正向提示词：\n{final_prompt}\n\n反向提示词：\n{negative_prompt}\n\n=== 生成信息 ===\n工具：高级构建器\n镜头：{selected_camera}\n光影：{', '.join(selected_lighting)}\n画质：{', '.join(selected_quality)}\n动态强度：{motion_strength}\n"
                st.download_button(
                    label="💾 下载提示词配置",
                    data=download_content,
                    file_name=f"seedance_prompt_builder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

# 3. 修改侧边栏选项卡（找到 page 变量定义的位置，约第 360 行）

# 修改前：
# page = st.sidebar.radio(
#     "选择功能",
#     ["📝 分镜生成器", "⚡ 提示词生成器", "📚 历史记录", "ℹ️ 关于"],
#     label_visibility="collapsed"
# )

# 修改后：
page = st.sidebar.radio(
    "选择功能",
    ["📝 分镜生成器", "⚡ 提示词生成器", "🧩 高级构建器", "📚 历史记录", "ℹ️ 关于"],
    label_visibility="collapsed"
)

# 4. 添加新的页面处理（在 main() 函数内，历史记录页面之前，约第 580 行）

# 在 elif page == "📚 历史记录": 之前添加：
elif page == "🧩 高级构建器":
    render_prompt_builder()

# 5. 更新关于页面（更新功能列表）

# 在"功能特性"部分添加（约第 770 行）：
st.markdown("""
### 🧩 高级构建器
- ✅ 模块化提示词构建
- ✅ 7种专业运镜
- ✅ 5种光影氛围
- ✅ 4种画质特效
- ✅ 中英双语支持
- ✅ 专业反向提示词
- ✅ 精确参数控制（motion、ar）
""")

# 6. 更新版本号和发布日期

# 修改页面配置（约第 22 行）：
st.set_page_config(
    page_title="即梦提示词工具 v2.2.0",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io',
        'Report a bug': 'https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit/issues',
    }
)

# 修改标题（约第 330 行）：
st.title("🎬 即梦提示词工具 v2.2.0")

# 修改版本号（关于页面，约第 750 行）：
st.metric("版本", "2.2.0")
st.metric("发布日期", "2026-03-05")

# 修改页脚（约第 830 行）：
st.markdown(
    """
    <div style='text-align: center'>
        <p>🎬 即梦提示词工具 v2.2.0（AI 增强版）| Made with ❤️ using Streamlit</p>
        <p>集成分镜生成器 + 提示词生成器 + 高级构建器 + 智能模板库</p>
        <p><small>🚀 v2.2.0 新增：高级构建器、专业参数控制、反向提示词</small></p>
    </div>
    """,
    unsafe_allow_html=True
)
