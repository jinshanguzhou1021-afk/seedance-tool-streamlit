#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即梦提示词工具 - Streamlit Web 应用（AI 视觉导演版）
集成分镜生成器 + 提示词生成器 + 高级构建器 + AI 视觉导演 + 智能模板库
版本: 2.3.0
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
    "突然转身": "猛然转身带起风声，头发飞扬，衣摆猎猎"
}

# 大师运镜库
MASTER_CAMERA_MOVES = {
    "希区柯克变焦": "镜头不动，推镜头与拉镜头反向运动，营造眩晕不安",
    "荷兰斜角": "镜头倾斜构图，画面失衡，营造紧张不安感",
    "手持晃动感": "镜头轻微晃动，呼吸感强烈，营造真实临场感",
    "低角度仰拍": "低角度仰拍，主体显得高大威猛，压迫感强烈",
    "高角度俯拍": "高角度俯拍，主体显得渺小脆弱，孤独感十足",
    "环绕拍摄": "镜头环绕主体运动，全方位展示，空间感强烈"
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

# 页面配置
st.set_page_config(
    page_title="即梦提示词工具 v2.3.0",
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


# 主界面
def main():
    # 加载历史记录
    load_history()
    
    # 标题
    st.title("🎬 即梦提示词工具 v2.3.0")
    st.markdown("集成 **分镜生成器** + **提示词生成器** + **高级构建器** + **AI 视觉导演** + **智能模板库**")
    
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
        ["📝 分镜生成器", "⚡ 提示词生成器", "🧩 高级构建器", "🎬 AI 视觉导演", "📚 历史记录", "ℹ️ 关于"],
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

    # 功能 3：高级构建器
    elif page == "🧩 高级构建器":
        st.header("🧩 高级分镜提示词构建器")
        st.markdown("模块化构建专业级 Seedance 提示词，支持中英双语和精确参数控制")

        render_prompt_builder()

    # 功能 4：AI 视觉导演
    elif page == "🎬 AI 视觉导演":
        st.header("🎬 Seedance 2.0 AI 视觉导演系统")
        st.markdown("三层导演逻辑，生成极致张力、细腻表情和戏剧化冲突的全中文分镜提示词")

        render_ai_director()

    # 功能 5：历史记录
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
    
    # 功能 5：关于
    elif page == "ℹ️ 关于":
        st.header("ℹ️ 关于")
        st.markdown("---")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("版本", "2.3.0")
            st.metric("发布日期", "2026-03-05")

        with col2:
            st.metric("开发者", "Seedance Tool Team")
            st.metric("框架", "Streamlit 1.55.0")

        with col3:
            st.metric("状态", "✅ 正常运行")
            st.metric("新增", "AI 视觉导演")

        st.markdown("---")

        st.subheader("🎯 功能特性")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            ### 📝 分镜生成器
            - ✅ 创意描述输入
            - ✅ 智能时间轴分段
            - ✅ 15+ 视觉风格
            - ✅ AI 增强模式
            - ✅ 深色模式支持
            """)

        with col2:
            st.markdown("""
            ### ⚡ 提示词生成器
            - ✅ 12种场景类型
            - ✅ 多版本生成
            - ✅ AI 增强模式
            - ✅ 版本对比查看
            - ✅ 深色模式支持
            """)

        with col3:
            st.markdown("""
            ### 🧩 高级构建器
            - ✅ 模块化提示词构建
            - ✅ 7种专业运镜
            - ✅ 5种光影氛围
            - ✅ 4种画质特效
            - ✅ 中英双语支持
            - ✅ 专业反向提示词
            """)

        st.markdown("---")

        st.subheader("🎬 AI 视觉导演系统")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            ### 核心特性
            - ✅ 三层导演逻辑
            - ✅ 情感语义解析
            - ✅ 戏剧化扩充引擎
            - ✅ Seedance 2.0 适配
            - ✅ 极致张力控制
            """)

        with col2:
            st.markdown("""
            ### 戏剧化元素
            - ✅ 10种细腻表情
            - ✅ 6种动作张力
            - ✅ 6种大师运镜
            - ✅ 8种情绪滤镜
            - ✅ 5种戏剧光影
            """)

        with col3:
            st.markdown("""
            ### 专业输出
            - ✅ 全中文文学性描述
            - ✅ 张力强度调节（5级）
            - ✅ 情绪滤镜（8种）
            - ✅ 导演级分镜卡片
            - ✅ 完整提示词配置
            """)

        st.markdown("---")

        st.subheader("💡 AI 增强功能")
        st.markdown("""
        开启 **🤖 使用 OpenClaw AI 技能** 后：

        - **场景智能理解** - 根据场景类型（动作、剧情、广告等）自动生成更具体的描述
        - **运镜智能匹配** - 自动匹配最合适的运镜方式
        - **音效智能设计** - 自动推荐背景音乐和音效
        - **专业级提示词** - 生成电影级别的视频描述

        **v2.2.0 新增功能**：
        - **高级构建器** - 模块化构建专业级 Seedance 提示词
        - **专业运镜** - 7种专业运镜方式（推、拉、全景、特写、跟随、无人机、FPV）
        - **光影控制** - 5种专业光影氛围（电影级、丁达尔效应、霓虹灯、黄金时刻、自然光）
        - **画质特效** - 4种专业画质标签（8K、虚幻引擎5、胶片质感、高帧率）
        - **中英双语** - 支持中英文双语词库，兼容各种 AI 视频引擎
        - **反向提示词** - 专业防崩坏反向词，避免生成错误
        - **精确参数** - 精确控制 motion 强度和画幅比例

        **v2.1.1 优化**：
        - **智能输入解析** - 自动区分指令和场景描述，支持简单需求输入
        - **关键词提取** - 从用户输入中提取关键词，生成合适的场景
        - **默认场景生成** - 根据场景类型自动生成专业的默认描述
        - **缓存机制** - 重复计算自动缓存，大幅提升性能
        - **深色模式** - 支持深色/浅色主题切换
        - **扩展风格** - 视觉风格扩展至 15+ 种，场景类型扩展至 12 种

        对比：
        - **分镜生成器** - 适合快速生成，AI 智能辅助
        - **提示词生成器** - 适合多版本对比，批量生成
        - **高级构建器** - 适合专业需求，精确控制每个参数
        - **v2.2.0 全能版** - 三种模式 + 深色模式 + 智能解析 + 专业构建
        """)
        
        st.markdown("---")
        
        st.subheader("📚 使用指南")
        st.markdown("""
        1. **快速开始** - 关闭 AI 技能，使用标准模式快速生成
        2. **专业生成** - 开启 AI 技能，获得智能增强的提示词
        3. **版本对比** - 提示词生成器可以生成多个版本供选择
        4. **历史管理** - 所有生成记录自动保存，随时查看
        5. **深色模式** - 点击侧边栏的 🌙 切换主题

        **v2.1.1 新功能：智能输入解析**
        - 输入'情侣' → 自动生成'一对情侣在夕阳下对视，准备表白'
        - 输入'动作' → 自动生成'武侠高手在竹林中与敌人激烈对战'
        - 输入'帮我生成' → 自动识别为指令，生成合适的默认场景
        - 输入完整的场景描述 → 直接使用你的描述

        **提示**：
        - 分镜生成器适合需要精确时间轴控制的场景
        - 提示词生成器适合需要多版本对比的场景
        - AI 增强模式会利用缓存机制，第二次生成相同内容会更快
        - 深色模式适合夜间使用，保护眼睛
        - 智能输入解析让你可以用简单的关键词生成专业场景
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
            <p>🎬 即梦提示词工具 v2.3.0（AI 视觉导演版）| Made with ❤️ using Streamlit</p>
            <p>集成分镜生成器 + 提示词生成器 + 高级构建器 + AI 视觉导演 + 智能模板库</p>
            <p><small>🎬 v2.3.0 重磅：AI 视觉导演系统、三层导演逻辑、戏剧化分镜、极致张力控制</small></p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
