#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即梦提示词工具 - Streamlit Web 应用（AI 增强版）
集成分镜生成器 + 提示词生成器 + 智能模板库
版本: 2.1.0
"""

import streamlit as st
import json
import logging
from datetime import datetime
from pathlib import Path
import time

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 页面配置
st.set_page_config(
    page_title="即梦提示词工具 v2.1",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io',
        'Report a bug': 'https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit/issues',
    }
)

# 初始化 session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'use_ai_skill' not in st.session_state:
    st.session_state.use_ai_skill = False
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# 主题切换 CSS
def get_theme_css():
    if st.session_state.dark_mode:
        return """
        <style>
            .stApp {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            .stTextInput>div>div>input,
            .stSelectbox>div>div>select,
            .stTextArea>div>div>textarea {
                color: #ffffff !important;
                background-color: #2d2d2d !important;
            }
            .stButton>button {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            .main {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            h1, h2, h3 {
                color: #ffffff;
            }
            .stMetricLabel {
                color: #cccccc;
            }
        </style>
        """
    else:
        return """
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
            .warning-box {
                background-color: #fff3cd;
                padding: 1rem;
                border-left: 5px solid #ffc107;
                margin: 1rem 0;
            }
        </style>
        """

st.markdown(get_theme_css(), unsafe_allow_html=True)

# 加载历史记录（仅使用 session state）
def load_history():
    # Streamlit Cloud 使用只读文件系统，仅使用 session state
    pass

# 复制到剪贴板
def copy_to_clipboard(text):
    """复制文本到剪贴板"""
    st.code(text, language="text")
    st.button("📋 复制到剪贴板", key=f"copy_{id(text)}", help="复制文本")

# 保存到历史记录（仅使用 session state）
def save_to_history(tool_type, prompt, result, use_ai):
    """保存到历史记录（不使用缓存，因为修改会话状态）"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = {
            "timestamp": timestamp,
            "tool": tool_type,
            "prompt": prompt,
            "result": result,
            "use_ai": use_ai
        }
        st.session_state.history.append(history_entry)
        logger.info(f"已保存历史记录：{tool_type} (AI: {use_ai})")
    except Exception as e:
        logger.error(f"保存历史记录失败：{e}")
        st.warning("历史记录保存失败，但不影响生成结果")

# 计算时间轴分段（缓存优化）
@st.cache_data(show_spinner=False)
def calculate_time_segments(duration):
    """计算时间轴分段，使用缓存提升性能"""
    try:
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
    except Exception as e:
        logger.error(f"计算时间轴分段失败：{e}")
        return [(0, duration)]

# 标准版提示词生成
def generate_standard_storyboard(prompt, duration, ratio, style, references):
    # 智能解析用户输入
    parsed_prompt = smart_parse_input("🎭 剧情/对话", prompt)

    segments = calculate_time_segments(duration)

    result = f"{duration}秒{style}视频，{ratio}。\n\n时间轴：\n"

    for i, (start, end) in enumerate(segments):
        if i == 0:
            desc = f"{start}-{end}秒：{parsed_prompt}的引入，镜头缓慢推近，建立场景"
        elif i == len(segments) - 1:
            desc = f"{start}-{end}秒：{parsed_prompt}的高潮部分，{style}风格，拉远定格"
        else:
            desc = f"{start}-{end}秒：{parsed_prompt}的发展，{style}风格，环绕拍摄"
        result += f"- {desc}\n"

    if references != "无":
        result += f"\n参考素材：\n- {references}\n"

    return result

# AI 增强版提示词生成（模拟 OpenClaw 技能）
def generate_ai_storyboard(prompt, duration, ratio, style, scene_type, references):
    """模拟 OpenClaw 技能的智能生成"""

    # 智能解析用户输入（仅在fallback时使用）
    parsed_prompt = smart_parse_input(scene_type, prompt)

    segments = calculate_time_segments(duration)
    
    # 根据场景类型生成更具体的描述
    scene_descriptions = {
        "动作/打斗": [
            "低角度特写主角，衣袍被风/能量吹动，握紧武器，眼神凝视前方",
            "环绕拍摄主角出招，武器发光/能量爆发，特效冲击，敌人被击飞",
            "慢放定格终极一击，冲击波横扫，主角屹立不倒，背景燃烧"
        ],
        "剧情/对话": [
            "远景展示环境，主角或主要角色登场，建立场景氛围",
            "中景展示对话或互动，面部表情特写，肢体语言展现",
            "近景或特写关键瞬间，情感高潮，拉远定格或淡出"
        ],
        "商业广告": [
            "产品展示镜头，360度旋转或特写细节，光影突出质感",
            "功能演示，产品应用场景，使用效果对比",
            "品牌LOGO和slogan定格，高端质感，营销氛围"
        ],
        "奇幻/仙侠": [
            "俯拍云海或仙境全景，镜头缓缓下推，营造神秘氛围",
            "主角登场，特写或中景，特效光环，背景音乐响起",
            "慢放定格主角持剑/施法，画面震撼，音效高潮"
        ],
        "科幻/未来": [
            "俯拍未来城市或宇宙全景，霓虹灯光，赛博朋克氛围",
            "主角或装备特写，科技感，机械结构，全息投影",
            "慢放定格能量爆发或穿越，震撼特效，史诗感"
        ],
        "风景/环境": [
            "大远景展示自然环境，云层、山峰、海洋等",
            "镜头移动（推/拉/摇），展现细节变化，光影流转",
            "拉远或定点，风景全景或特写细节，意境悠远"
        ],
        "产品展示": [
            "产品360度旋转展示，全角度展示细节",
            "分解展示，产品拆分展示内部结构或材质",
            "合成定格，产品完整展示，背景简洁或高级"
        ]
    }
    
    # 获取对应场景的描述
    descriptions = scene_descriptions.get(scene_type, [
        f"{parsed_prompt}的引入，建立场景",
        f"{parsed_prompt}的发展，{style}风格",
        f"{parsed_prompt}的高潮，拉远定格"
    ])
    
    result = f"{duration}秒{scene_type}场景，{style}风格，{ratio}。\n\n时间轴（AI 增强）：\n"
    
    for i, (start, end) in enumerate(segments):
        desc = descriptions[i] if i < len(descriptions) else f"{start}-{end}秒：结尾"
        camera_movement = get_camera_movement(i, len(segments))
        result += f"- {start}-{end}秒：{desc}，{camera_movement}\n"
    
    # 添加音效设计
    result += "\n音效设计（AI 建议）：\n"
    result += f"- 背景音乐：{get_music_style(scene_type)}\n"
    result += f"- 音效：{get_sound_effects(scene_type)}\n"
    
    if references != "无":
        result += f"\n参考素材：\n- {references}\n"
    
    return result

def get_camera_movement(index, total):
    """根据位置返回运镜"""
    movements = ["镜头缓慢推近", "中景跟随", "环绕拍摄", "拉远定格", "推拉组合", "摇镜+跟拍"]
    return movements[min(index, len(movements) - 1)]

def get_music_style(scene_type):
    """根据场景类型返回音乐风格"""
    music_styles = {
        "动作/打斗": "紧张、史诗、管弦乐",
        "剧情/对话": "根据情绪调整（温馨/悲伤/悬疑）",
        "商业广告": "动感、欢快、高级",
        "奇幻/仙侠": "仙侠音乐、古琴、管弦乐",
        "科幻/未来": "电子、科幻、史诗",
        "风景/环境": "轻音乐、自然音",
        "产品展示": "欢快、高级、节奏感强"
    }
    return music_styles.get(scene_type, "根据场景类型调整")

def get_sound_effects(scene_type):
    """根据场景类型返回音效"""
    sound_effects = {
        "动作/打斗": "打击声、爆炸声、能量波动声、刀剑声",
        "剧情/对话": "环境音、脚步声、衣物摩擦声",
        "商业广告": "产品使用音效、科技音效",
        "奇幻/仙侠": "法阵音、能量音、风声、雷声",
        "科幻/未来": "机械音、能量音、电子音",
        "风景/环境": "自然音、风声、水声、鸟鸣",
        "产品展示": "开箱声、机械音、高级音效"
    }
    return sound_effects.get(scene_type, "环境音、动作音效")

# 智能解析用户输入
def smart_parse_input(scene_type, user_input):
    """智能解析用户输入，区分指令和场景描述"""

    # 检查是否为空输入
    if not user_input or user_input.strip() == "":
        return generate_default_scene(scene_type)

    # 检查是否为指令（如"帮我生成"、"请生成"等）
    instruction_patterns = [
        "帮我生成", "请生成", "生成", "制作", "创建",
        "我想看", "我想做", "我要", "需要",
        "分镜", "提示词"
    ]

    input_lower = user_input.lower().strip()

    # 如果输入包含指令关键词，认为是请求而非场景描述
    if any(pattern in input_lower for pattern in instruction_patterns):
        # 尝试提取关键词（如"情侣"）
        keywords = extract_keywords(user_input, scene_type)
        if keywords:
            return generate_scene_from_keywords(scene_type, keywords)
        else:
            return generate_default_scene(scene_type)

    # 如果输入很短（<5个字），可能是用户还没输入完整
    if len(user_input) < 5:
        return generate_default_scene(scene_type)

    # 正常的场景描述，直接返回
    return user_input.strip()

# 提取关键词
def extract_keywords(user_input, scene_type):
    """从用户输入中提取关键词"""

    # 常见关键词映射
    keyword_patterns = {
        "情侣": ["情侣", "恋人", "男女", "两人", "一对"],
        "动作": ["打斗", "战斗", "武打", "动作", "格斗"],
        "风景": ["风景", "景色", "山水", "自然", "风景"],
        "产品": ["产品", "商品", "展示", "广告", "推广"],
        "喜剧": ["喜剧", "搞笑", "幽默", "有趣", "好玩"],
        "音乐": ["音乐", "歌曲", "MV", "演唱", "歌舞"],
        "悬疑": ["悬疑", "惊悚", "恐怖", "神秘", "紧张"],
        "治愈": ["治愈", "温暖", "温馨", "感人", "正能量"]
    }

    # 场景类型对应的主题关键词
    scene_keywords = {
        "⚔️ 动作/打斗": ["打斗", "战斗", "武术", "格斗", "对决"],
        "🎭 剧情/对话": ["情侣", "恋人", "两人", "对话", "交谈"],
        "📢 商业广告": ["产品", "商品", "品牌", "推广", "展示"],
        "🏞️ 风景/环境": ["风景", "景色", "自然", "山水", "美景"],
        "📦 产品展示": ["产品", "商品", "展示", "介绍", "演示"],
        "🌟 奇幻/仙侠": ["仙侠", "奇幻", "魔法", "修炼", "江湖"],
        "🚀 科幻/未来": ["科幻", "未来", "科技", "宇宙", "飞船"],
        "🎵 音乐MV": ["音乐", "歌曲", "MV", "演唱", "舞蹈"],
        "😄 喜剧搞笑": ["喜剧", "搞笑", "幽默", "有趣", "好笑"],
        "💕 情感爱情": ["情侣", "恋人", "爱情", "浪漫", "表白"],
        "🔍 悬疑惊悚": ["悬疑", "惊悚", "恐怖", "神秘", "紧张"],
        "🌈 治愈温暖": ["治愈", "温暖", "温馨", "感人", "正能量"]
    }

    # 优先查找场景类型相关的关键词
    if scene_type in scene_keywords:
        for keyword in scene_keywords[scene_type]:
            if keyword in user_input:
                return keyword

    # 查找通用关键词
    for category, patterns in keyword_patterns.items():
        for pattern in patterns:
            if pattern in user_input:
                return category

    return None

# 根据关键词生成场景
def generate_scene_from_keywords(scene_type, keywords):
    """根据关键词生成合适的场景描述"""

    scene_templates = {
        "情侣": "一对情侣在夕阳下对视，准备表白",
        "动作": "主角在废墟中与敌人展开激烈战斗",
        "风景": "无人机俯拍壮丽的山川湖海，云雾缭绕",
        "产品": "360度旋转展示产品细节，光影突出质感",
        "喜剧": "主角滑稽地摔倒，周围人忍不住大笑",
        "音乐": "歌手在舞台上深情演唱，灯光绚丽",
        "悬疑": "主角在黑暗中探索，突然发现神秘线索",
        "治愈": "温暖阳光洒在小女孩脸上，她开心地笑着"
    }

    # 查找匹配的模板
    for key, template in scene_templates.items():
        if key in keywords or keywords in key:
            return template

    # 如果没有匹配，返回场景类型相关的默认场景
    return generate_default_scene(scene_type)

# 生成默认场景
def generate_default_scene(scene_type):
    """根据场景类型生成默认场景描述"""

    default_scenes = {
        "⚔️ 动作/打斗": "武侠高手在竹林中与敌人激烈对战，剑气纵横",
        "🎭 剧情/对话": "一对情侣在咖啡馆里温馨交谈，氛围浪漫",
        "📢 商业广告": "产品特写镜头，展示细节和质感，高端大气",
        "🏞️ 风景/环境": "无人机航拍壮丽的自然风光，云海、雪山、森林",
        "📦 产品展示": "360度旋转展示产品，展示多个角度和使用场景",
        "🌟 奇幻/仙侠": "修仙者在云端飞舞，身后仙气缭绕，宛如仙境",
        "🚀 科幻/未来": "宇航员在宇宙空间站探索，窗外是绚丽的星云",
        "🎵 音乐MV": "歌手在舞台上深情演唱，灯光绚丽，观众欢呼",
        "😄 喜剧搞笑": "主角滑稽地绊倒，周围朋友忍不住大笑",
        "💕 情感爱情": "一对情侣在夕阳下对视，准备表白，氛围浪漫",
        "🔍 悬疑惊悚": "主角在废弃工厂中探索，突然发现神秘线索",
        "🌈 治愈温暖": "温暖阳光洒在脸上，小女孩开心地笑着，温馨治愈"
    }

    return default_scenes.get(scene_type, "美丽的自然风光，宁静祥和")

# 标准版提示词生成
def generate_standard_prompt(scene_type, description, duration, ratio, version, references):
    # 智能解析用户输入
    parsed_description = smart_parse_input(scene_type, description)

    segments = calculate_time_segments(duration)

    version_styles = {
        1: "标准版",
        2: "更具创意",
        3: "简洁高效",
        4: "氛围强化",
        5: "电影质感"
    }
    style_desc = version_styles.get(version, "标准版")

    result = f"--- 版本 {version}（{style_desc}）---\n"
    result += f"{duration}秒{scene_type}场景，{style_desc}风格，{ratio}。\n\n时间轴：\n"

    for j, (start, end) in enumerate(segments):
        if j == 0:
            desc = f"{start}-{end}秒：{parsed_description}的引入，特写"
        elif j == len(segments) - 1:
            desc = f"{start}-{end}秒：{parsed_description}的高潮，拉远定格"
        else:
            desc = f"{start}-{end}秒：{parsed_description}的发展，中景跟随"
        result += f"- {desc}\n"

    # 添加音效设计
    result += "\n音效设计：\n"
    result += f"- 背景音乐：{get_music_style(scene_type)}\n"
    result += f"- 音效：{get_sound_effects(scene_type)}\n"

    if references != "无":
        result += f"\n参考素材：\n- {references}\n"

    return result

# 主界面
def main():
    # 加载历史记录
    load_history()
    
    # 标题
    st.title("🎬 即梦提示词工具 v2.1")
    st.markdown("集成 **分镜生成器** + **提示词生成器** + **智能模板库**")
    
    # AI 技能开关
    st.sidebar.markdown("### ⚙️ 设置")
    use_ai = st.sidebar.checkbox("🤖 使用 OpenClaw AI 技能", value=False, help="开启后使用 AI 智能生成，关闭后使用标准模板")
    st.session_state.use_ai_skill = use_ai

    # 深色模式开关
    dark_mode = st.sidebar.toggle("🌙 深色模式", value=False, help="切换深色/浅色主题")
    st.session_state.dark_mode = dark_mode

    # 选项卡
    page = st.sidebar.radio(
        "选择功能",
        ["📝 分镜生成器", "⚡ 提示词生成器", "📚 历史记录", "ℹ️ 关于"],
        label_visibility="collapsed"
    )
    
    # 统计
    st.sidebar.markdown("### 📊 统计")
    if st.session_state.history:
        total = len(st.session_state.history)
        ai_used = sum(1 for h in st.session_state.history if h.get('use_ai', False))
        st.metric("总生成次数", total)
        st.metric("AI 增强次数", ai_used)
    
    # 功能 1：分镜生成器
    if page == "📝 分镜生成器":
        st.header("📝 分镜生成器")
        st.markdown("根据你的创意描述，生成分镜提示词（可选择 AI 增强）")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📋 输入设置")
            
            prompt = st.text_area(
                "创意描述",
                placeholder="例如：一对情侣在夕阳下对视，准备表白",
                height=150,
                help="描述你想创建的视频内容。如果是简单的需求（如'情侣对话'），系统会自动生成合适的场景描述。"
            )
            
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
                ["🎬 电影感", "🌸 青春校园", "🤖 赛博朋克", "⚔️ 仙侠奇幻", "📷 写实",
                 "🎨 动画", "🎞️ 复古", "🚀 科幻", "🌊 水墨风", "🎭 国潮",
                 "🚂 蒸汽朋克", "🎥 纪录片", "📱 短视频", "🌟 网红风", "🎪 狂欢节"],
                index=0,
                help="选择视频的整体视觉风格"
            )
            
            # 场景类型（仅 AI 模式使用）
            scene_type = st.selectbox(
                "场景类型（AI 增强）",
                ["⚔️ 动作/打斗", "🎭 剧情/对话", "📢 商业广告", "🏞️ 风景/环境",
                 "📦 产品展示", "🌟 奇幻/仙侠", "🚀 科幻/未来", "🎵 音乐MV",
                 "😄 喜剧搞笑", "💕 情感爱情", "🔍 悬疑惊悚", "🌈 治愈温暖"],
                index=0,
                help="选择视频类型，AI 会根据类型生成更具体的描述"
            ) if use_ai else "⚔️ 动作/打斗"
            
            references = st.text_input(
                "参考素材（可选）",
                value="无",
                placeholder="例如：@图片1 人物图, @视频1 参考运镜"
            )
            
            generate_btn = st.button("🎬 生成分镜", type="primary", use_container_width=True)
        
        with col2:
            st.subheader("📤 生成结果")
            
            if generate_btn:
                if not prompt:
                    st.warning("⚠️ 请输入创意描述！")
                else:
                    with st.spinner("正在生成分镜（{} AI 增强）...".format("AI" if use_ai else "标准")):
                        if use_ai:
                            result = generate_ai_storyboard(prompt, duration, ratio, style, scene_type, references)
                        else:
                            result = generate_standard_storyboard(prompt, duration, ratio, style, references)
                    
                        # 显示结果
                        st.success("✅ 分镜生成完成！（{} AI 增强）".format("使用" if use_ai else "标准"))
                        st.code(result, language="text")

                        # 保存到历史
                        save_to_history("分镜生成", prompt, result, use_ai)
                        
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
    
    # 功能 2：提示词生成器
    elif page == "⚡ 提示词生成器":
        st.header("⚡ 提示词生成器")
        st.markdown("根据场景类型，生成多个版本的 Seedance 提示词（可选择 AI 增强）")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📋 输入设置")
            
            scene_type = st.selectbox(
                "场景类型",
                ["⚔️ 动作/打斗", "🎭 剧情/对话", "📢 商业广告", "🏞️ 风景/环境",
                 "📦 产品展示", "🌟 奇幻/仙侠", "🚀 科幻/未来", "🎵 音乐MV",
                 "😄 喜剧搞笑", "💕 情感爱情", "🔍 悬疑惊悚", "🌈 治愈温暖"],
                index=0,
                help="选择你要生成的视频类型"
            )
            
            description = st.text_area(
                "场景描述",
                placeholder="例如：一对情侣在夕阳下对视，准备表白",
                height=120,
                help="详细描述视频内容。如果是简单的需求（如'情侣对话'），系统会自动生成合适的场景描述。"
            )
            
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
            
            generate_btn = st.button("🚀 生成提示词", type="primary", use_container_width=True)
        
        with col2:
            st.subheader("📤 生成结果")
            
            if generate_btn:
                if not description:
                    st.warning("⚠️ 请输入场景描述！")
                else:
                    with st.spinner(f"正在生成 {version_count} 个版本的提示词（{'AI 增强' if use_ai else '标准'}）..."):
                        results = []
                        for i in range(version_count):
                            version = i + 1
                            result = generate_standard_prompt(scene_type, description, duration, ratio, version, references)
                            results.append(result)
                        
                        # 合并结果
                        final_result = f"场景类型：{scene_type}\n时长：{duration}秒\n比例：{ratio}\n使用模式：{'AI 增强' if use_ai else '标准'}\n\n{''.join(results)}"
                        
                        # 显示结果
                        st.success(f"✅ 已生成 {version_count} 个版本的提示词！（{'AI 增强' if use_ai else '标准'}）")
                        
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
                        save_to_history("提示词生成", description, final_result, use_ai)
            else:
                st.info("👆 在左侧输入参数并生成")
    
    # 功能 3：历史记录
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

            # Streamlit Cloud 提示
            st.info("💡 提示：在 Streamlit Cloud 上，历史记录仅在当前会话有效，刷新页面后会清空。")
    
    # 功能 4：关于
    elif page == "ℹ️ 关于":
        st.header("ℹ️ 关于")
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("版本", "2.1.0")
            st.metric("发布日期", "2026-03-05")
        
        with col2:
            st.metric("开发者", "Seedance Tool Team")
            st.metric("框架", "Streamlit 1.55.0")
        
        with col3:
            st.metric("状态", "✅ 正常运行")
            st.metric("优化", "缓存+深色模式")
        
        st.markdown("---")
        
        st.subheader("🎯 功能特性")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📝 分镜生成器
            - ✅ 创意描述输入
            - ✅ 智能时间轴分段（缓存优化）
            - ✅ **15+ 视觉风格**（新增：水墨、国潮、蒸汽朋克等）
            - ✅ **AI 增强模式**（场景智能理解）
            - ✅ 参考素材支持
            - ✅ 一键下载
            - ✅ **深色模式**支持
            """)
        
        with col2:
            st.markdown("""
            ### ⚡ 提示词生成器
            - ✅ **12种场景类型**（新增：音乐MV、喜剧、悬疑等）
            - ✅ 一键生成多个版本
            - ✅ **AI 增强模式**（音效智能设计）
            - ✅ 版本对比查看
            - ✅ 批量下载所有版本
            - ✅ **深色模式**支持
            """)
        
        st.markdown("---")
        
        st.subheader("💡 AI 增强功能")
        st.markdown("""
        开启 **🤖 使用 OpenClaw AI 技能** 后：
        
        - **场景智能理解** - 根据场景类型（动作、剧情、广告等）自动生成更具体的描述
        - **运镜智能匹配** - 自动匹配最合适的运镜方式
        - **音效智能设计** - 自动推荐背景音乐和音效
        - **专业级提示词** - 生成电影级别的视频描述
        
        **v2.1 新增优化**：
        - **缓存机制** - 重复计算自动缓存，大幅提升性能
        - **深色模式** - 支持深色/浅色主题切换
        - **扩展风格** - 视觉风格扩展至 15+ 种，场景类型扩展至 12 种
        - **错误处理** - 完善的异常处理和日志记录
        
        对比：
        - **标准模式** - 简单模板，适合快速生成
        - **AI 增强模式** - 智能生成，适合专业需求
        - **v2.1 优化版** - 缓存加速 + 深色模式 + 更多样式
        """)
        
        st.markdown("---")
        
        st.subheader("📚 使用指南")
        st.markdown("""
        1. **快速开始** - 关闭 AI 技能，使用标准模式快速生成
        2. **专业生成** - 开启 AI 技能，获得智能增强的提示词
        3. **版本对比** - 提示词生成器可以生成多个版本供选择
        4. **历史管理** - 所有生成记录自动保存，随时查看
        5. **深色模式** - 点击侧边栏的 🌙 切换主题
        
        **提示**：
        - 分镜生成器适合需要精确时间轴控制的场景
        - 提示词生成器适合需要多版本对比的场景
        - AI 增强模式会利用缓存机制，第二次生成相同内容会更快
        - 深色模式适合夜间使用，保护眼睛
        - 15+ 种视觉风格覆盖各种视频需求
        """)
        
        st.markdown("---")
        
        st.subheader("📞 技术支持")
        st.markdown("""
        - **Streamlit:** https://docs.streamlit.io
        - **OpenClaw:** https://docs.openclaw.com
        - **Seedance 2.0:** https://jimeng.jianying.com
        
        如有问题，请查看日志或提交 Issue。
        """)
    
    # 页脚
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🎬 即梦提示词工具 v2.1.0（AI 增强版）| Made with ❤️ using Streamlit</p>
            <p>集成分镜生成器 + 提示词生成器 + 智能模板库</p>
            <p><small>🚀 已优化：缓存机制、深色模式、15+ 视觉风格</small></p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
