# 即梦（Seedance）提示词工具 - Streamlit Web 应用

import streamlit as st
import json
from datetime import datetime
from pathlib import Path
import os

# 页面配置
st.set_page_config(
    page_title="即梦提示词工具",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .success-btn {
        background-color: #4CAF50;
        color: white;
    }
    .copy-btn {
        background-color: #2196F3;
        color: white;
    }
    h1 {
        color: #1f77b4;
    }
    h2, h3 {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# 初始化 session state
if 'history' not in st.session_state:
    st.session_state.history = []
    st.session_state.history_file = Path.home() / ".seedance_streamlit_history.json"

# 加载历史记录
def load_history():
    if st.session_state.history_file.exists():
        try:
            with open(st.session_state.history_file, 'r', encoding='utf-8') as f:
                st.session_state.history = json.load(f)
        except:
            st.session_state.history = []

# 保存历史记录
def save_to_history(tool_type, prompt, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_entry = {
        "timestamp": timestamp,
        "tool": tool_type,
        "prompt": prompt,
        "result": result
    }
    st.session_state.history.append(history_entry)

    # 保存到文件
    try:
        with open(st.session_state.history_file, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"保存历史记录失败：{e}")

# 计算时间轴分段
def calculate_time_segments(duration):
    if duration <= 5:
        return [(0, duration)]
    elif duration <= 10:
        return [(0, duration // 2), (duration // 2, duration)]
    elif duration <= 15:
        segment_length = duration // 3
        return [
            (0, segment_length),
            (segment_length, segment_length * 2),
            (segment_length * 2, duration)
        ]
    else:
        segment_length = duration // 4
        return [
            (0, segment_length),
            (segment_length, segment_length * 2),
            (segment_length * 2, segment_length * 3),
            (segment_length * 3, duration)
        ]

# 侧边栏
with st.sidebar:
    st.title("🎬 即梦提示词工具")
    st.markdown("---")

    # 页面选择
    page = st.radio(
        "选择功能",
        ["📝 分镜生成器", "⚡ 提示词生成器", "📚 历史记录", "ℹ️ 关于"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 📊 统计")
    if st.session_state.history:
        st.metric("总生成次数", len(st.session_state.history))
        storyboard_count = sum(1 for h in st.session_state.history if h['tool'] == '分镜生成')
        prompt_count = sum(1 for h in st.session_state.history if h['tool'] == '提示词生成')
        st.metric("分镜生成", storyboard_count)
        st.metric("提示词生成", prompt_count)
    else:
        st.info("暂无使用记录")

# 主内容区域
if page == "📝 分镜生成器":
    st.header("📝 分镜生成器")
    st.markdown("根据你的创意描述，生成分镜提示词和时间轴")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📋 输入设置")

        # 创意描述
        prompt = st.text_area(
            "创意描述",
            placeholder="例如：仙侠战斗，主角持剑迎战魔兵",
            height=150,
            help="描述你想创建的视频内容"
        )

        # 参数设置
        st.markdown("### ⚙️ 参数设置")

        duration = st.slider(
            "视频时长（秒）",
            min_value=4,
            max_value=15,
            value=15,
            step=1,
            help="Seedance 2.0 支持 4-15 秒视频"
        )

        ratio = st.selectbox(
            "画面比例",
            ["16:9 横屏", "9:16 竖屏", "2.35:1 电影宽屏"],
            index=0,
            help="选择视频的画面比例"
        )

        style = st.selectbox(
            "视觉风格",
            ["电影感", "青春校园", "赛博朋克", "仙侠奇幻", "写实", "动画", "复古", "科幻"],
            index=0,
            help="选择视频的整体视觉风格"
        )

        references = st.text_input(
            "参考素材（可选）",
            value="无",
            placeholder="例如：@图片1 人物图, @视频1 参考运镜"
        )

        # 生成按钮
        generate_btn = st.button("🎬 生成分镜", type="primary", use_container_width=True)

    with col2:
        st.subheader("📤 生成结果")

        if generate_btn:
            if not prompt:
                st.warning("⚠️ 请输入创意描述！")
            else:
                with st.spinner("正在生成分镜..."):
                    # 计算时间轴分段
                    segments = calculate_time_segments(duration)

                    # 构建提示词
                    result = f"{duration}秒{style}视频，{ratio}。\n\n"
                    result += "时间轴：\n"

                    for i, (start, end) in enumerate(segments):
                        if i == 0:
                            desc = f"{start}-{end}秒：{prompt}，镜头缓慢推近"
                        elif i == len(segments) - 1:
                            desc = f"{start}-{end}秒：{prompt}的高潮部分，镜头拉远定格"
                        else:
                            desc = f"{start}-{end}秒：{prompt}的发展，环绕拍摄"
                        result += f"- {desc}\n"

                    if references != "无":
                        result += f"\n参考素材：\n- {references}\n"

                    # 显示结果
                    st.success("✅ 分镜生成完成！")
                    st.code(result, language="text")

                    # 保存到历史
                    save_to_history("分镜生成", prompt, result)

                    # 下载按钮
                    st.download_button(
                        label="💾 下载提示词",
                        data=result,
                        file_name=f"seedance_storyboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
        else:
            st.info("👆 在左侧输入参数并生成")

elif page == "⚡ 提示词生成器":
    st.header("⚡ 提示词生成器")
    st.markdown("根据场景类型，生成多个版本的 Seedance 提示词")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📋 输入设置")

        # 场景类型
        scene_type = st.selectbox(
            "场景类型",
            ["动作/打斗", "剧情/对话", "商业广告", "风景/环境", "产品展示", "奇幻/仙侠", "科幻/未来"],
            index=0,
            help="选择你要生成的视频类型"
        )

        # 场景描述
        description = st.text_area(
            "场景描述",
            placeholder="例如：男女主角在夕阳下对视，准备表白",
            height=120,
            help="详细描述视频内容"
        )

        # 参数设置
        st.markdown("### ⚙️ 参数设置")

        duration = st.slider(
            "视频时长（秒）",
            min_value=4,
            max_value=15,
            value=15,
            step=1
        )

        ratio = st.selectbox(
            "画面比例",
            ["16:9 横屏", "9:16 竖屏"],
            index=0
        )

        version_count = st.slider(
            "生成版本数",
            min_value=1,
            max_value=5,
            value=3,
            step=1,
            help="生成多个不同版本的提示词供选择"
        )

        references = st.text_input(
            "参考素材（可选）",
            value="无",
            placeholder="例如：@图片1 产品图"
        )

        # 生成按钮
        generate_btn = st.button("🚀 生成提示词", type="primary", use_container_width=True)

    with col2:
        st.subheader("📤 生成结果")

        if generate_btn:
            if not description:
                st.warning("⚠️ 请输入场景描述！")
            else:
                with st.spinner(f"正在生成 {version_count} 个版本的提示词..."):
                    # 计算时间轴分段
                    segments = calculate_time_segments(duration)

                    # 版本风格
                    version_styles = {
                        1: "标准版",
                        2: "更具创意",
                        3: "简洁高效",
                        4: "氛围强化",
                        5: "电影质感"
                    }

                    # 生成多个版本
                    results = []
                    for i in range(version_count):
                        version = i + 1
                        style_desc = version_styles.get(version, "标准版")

                        result = f"--- 版本 {version}（{style_desc}）---\n"
                        result += f"{duration}秒{scene_type}场景，{style_desc}风格，{ratio}。\n\n"
                        result += "时间轴：\n"

                        for j, (start, end) in enumerate(segments):
                            if j == 0:
                                desc = f"{start}-{end}秒：{description}的引入，特写"
                            elif j == len(segments) - 1:
                                desc = f"{start}-{end}秒：{description}的高潮，拉远定格"
                            else:
                                desc = f"{start}-{end}秒：{description}的发展，中景跟随"
                            result += f"- {desc}\n"

                        # 添加音效设计
                        result += "\n音效设计：\n"
                        result += "- 背景音乐：根据场景类型调整\n"
                        result += "- 音效：环境音、动作音效\n"

                        if references != "无":
                            result += f"\n参考素材：\n- {references}\n"

                        results.append(result)

                    # 合并结果
                    final_result = f"场景类型：{scene_type}\n时长：{duration}秒\n比例：{ratio}\n\n{''.join(results)}"

                    # 显示结果
                    st.success(f"✅ 已生成 {version_count} 个版本的提示词！")

                    # 使用标签页显示不同版本
                    tabs = st.tabs([f"版本 {i+1}" for i in range(version_count)])
                    for i, tab in enumerate(tabs):
                        with tab:
                            st.code(results[i], language="text")

                    # 合并下载
                    st.download_button(
                        label="💾 下载所有版本",
                        data=final_result,
                        file_name=f"seedance_prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                    # 保存到历史
                    save_to_history("提示词生成", description, final_result)
        else:
            st.info("👆 在左侧输入参数并生成")

elif page == "📚 历史记录":
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
            with st.expander(f"{entry['timestamp']} - {entry['tool']}"):
                st.markdown(f"**输入：**\n{entry['prompt']}")
                st.markdown(f"\n**输出：**")
                st.code(entry['result'], language="text")

        # 清除历史按钮
        if st.button("🗑️ 清除所有历史记录"):
            if st.session_state.get('confirm_clear', False):
                st.session_state.history = []
                if st.session_state.history_file.exists():
                    st.session_state.history_file.unlink()
                st.success("✅ 历史记录已清除！")
                st.session_state.confirm_clear = False
                st.rerun()
            else:
                st.warning("⚠️ 确认要清除所有历史记录吗？")
                st.session_state.confirm_clear = True
                st.rerun()

elif page == "ℹ️ 关于":
    st.header("ℹ️ 关于")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("版本", "1.0.0")
        st.metric("发布日期", "2026-03-04")

    with col2:
        st.metric("开发者", "Seedance Tool Team")
        st.metric("框架", "Streamlit")

    with col3:
        st.metric("许可证", "MIT")
        st.metric("状态", "✅ 正常运行")

    st.markdown("---")

    st.subheader("🎯 功能特性")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📝 分镜生成器
        - ✅ 创意描述输入
        - ✅ 自动时间轴分段
        - ✅ 多种视觉风格
        - ✅ 参考素材支持
        """)

    with col2:
        st.markdown("""
        ### ⚡ 提示词生成器
        - ✅ 多种场景类型
        - ✅ 多版本生成
        - ✅ 智能音效设计
        - ✅ 一键下载
        """)

    st.markdown("---")

    st.subheader("🚀 使用建议")
    st.markdown("""
    1. **快速生成** - 直接使用内置模板，无需配置
    2. **多版本对比** - 生成多个版本，选择最佳方案
    3. **历史记录** - 随时查看之前的生成结果
    4. **批量导出** - 支持下载所有版本的提示词
    """)

    st.markdown("---")

    st.subheader("💡 技术栈")
    st.markdown("""
    - **Streamlit** - Web 应用框架
    - **Python 3.8+** - 编程语言
    - **JSON** - 数据存储
    """)

    st.markdown("---")

    st.subheader("📞 获取帮助")
    st.markdown("""
    - 查看 [README](/README.md) 了解详细使用方法
    - 提交 [Issue](https://github.com/your-repo/issues) 报告问题
    """)

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>🎬 即梦提示词工具 v1.0.0 | Made with ❤️ using Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
