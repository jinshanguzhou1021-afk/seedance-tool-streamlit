#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v3.0.0 补丁文件：display_v3_director_result() 函数
将此函数添加到 app.py 的末尾，在 if __name__ == "__main__": 之前
"""

def display_v3_director_result(result, api_mode, story_text, global_settings, tension_level, aspect_ratio):
    """显示 v3.0.0 导演级分镜结果（6要素：镜号、场景、运镜、提示词、旁白、音效）"""

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
        # 注意：这里需要导入 save_to_history 函数
        # 如果 save_to_history 是 app.py 中的函数，可以直接调用
        # 如果是独立模块，需要确保正确导入
        try:
            save_to_history(
                "AI全能导演v3.0.0" if api_mode else "AI全能导演v3.0.0(DeepSeek)",
                story_text,
                result.get("complete_prompt", ""),
                len(result["segments"]) > 0
            )
        except NameError:
            # save_to_history 未定义，忽略
            pass

    else:
        st.warning("⚠️ 未生成任何分镜，请检查输入或 API 配置")
