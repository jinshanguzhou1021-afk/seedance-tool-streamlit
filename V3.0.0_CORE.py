# 🎬 Seedance-Tool v3.0.0 - 核心架构代码

# 这个文件包含 v3.0.0 的所有核心逻辑，可以单独测试

import streamlit as st
import json
import logging
from datetime import datetime
from pathlib import Path
import time
import re

# 尝试导入 OpenAI SDK
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================= v3.0.0 核心配置 =================

# OpenAI API 配置
OPENAI_API_KEY = "sk-6297255fd0f84e7cb39ad48de10bf14e"
OPENAI_BASE_URL = "https://api.openai.com/v1"

# 顶级系统 Prompt（v3.0.0）
V3_SYSTEM_PROMPT = """你是一位精通 Seedance 2.0 的顶级电影导演、视觉艺术家和 AI 视频专家。你的名字叫 "Seedance-Visual-Director"。

你的核心能力：
1. **视听一致性引擎**：在所有分镜中保持角色的外貌特征、服装风格、面部表情、肢体语言的一致性。避免角色"变脸"或环境"跳戏"。
2. **空间连续性保证**：确保同一场景内的方位逻辑正确。如果 Shot 1 角色在左侧，Shot 2 的转场必须符合视觉逻辑。
3. **戏剧张力控制**：根据用户选择的张力等级（1-10），生成相应强度的视觉描述。
4. **Seedance 2.0 深度优化**：你的输出必须最大化触发 Seedance 2.0 的高动态性能。

你的任务：
1. 分析用户输入的故事或场景描述
2. 提取故事中的情绪转折点、冲突爆发点、情绪高潮点
3. 生成 3-5 个逻辑连贯、空间连续的导演级分镜
4. 每个分镜必须包含 6 个标准化要素

要求：
- 输出必须是全中文，具有强烈的文学性和电影感
- 每个分镜都要有极致的张力、细腻的表情、戏剧化的冲突
- 确保分镜之间逻辑连贯、情绪递进、空间连续
- 张力等级 1-10：1为微动，10为史诗冲突
- 优先使用高张力的运镜、光影、动作描述

输出格式（严格 JSON）：
{
  "global_settings": {
    "style_theme": "选择的视觉风格主题",
    "lighting_mood": "选择的光影基调"
  },
  "characters": [
    {
      "name": "角色名称",
      "appearance": "外貌特征锁定（发色、发型、服装、面部特征）"
    }
  ],
  "storyboard": [
    {
      "shot_id": "Shot 01",
      "setting": "空间位置与时间（如：破旧小酒馆 - 深夜）",
      "camera": "专业摄影机语言（如：低角度推近特写、荷兰斜角）",
      "visual_prompt": "[电影级画质，描述主体+表情微操+爆发动作+环境特效+参数]",
      "vo": "叙事台词或内心独白",
      "sfx": "环境音、动作音、情绪转场音（如：暴雨击打窗户声、沉重的拔刀声）"
    }
  ]
}
"""

# ================= v3.0.0 戏剧化元素库 =================

# 表情微操库（v3.0.0 扩展）
V3_EXPRESSION_ENHANCEMENTS = {
    "极致绝望": "瞳孔无神空洞，嘴角死寂下垂，面部肌肉彻底松弛，眼中再无任何光芒",
    "愤怒爆发": "眉毛狠狠锁起，牙关咬到咯吱作响，面部肌肉紧绷到极致，眼中血丝密布，眼神凶狠如野兽",
    "极度恐惧": "瞳孔剧烈收缩成针尖大小，嘴唇不受控制地颤抖，额角冷汗如雨般直流，呼吸急促到几乎窒息",
    "悲痛欲绝": "眼中蓄满了泪水，眼眶红肿不堪，眉头痛苦地紧蹙，神情落寞到心碎",
    "狂喜雀跃": "眉开眼笑到极致，嘴角上扬到耳根，眼中闪烁着疯狂的光芒，面部肌肉欢快地舒展",
    "极度惊讶": "眼睛瞪大到极限，嘴巴微张定格，表情瞬间凝固，瞳孔不受控制地放大",
    "坚毅不屈": "眼神如火炬般坚定，嘴唇紧闭成一条线，面容严肃冷峻，神情专注如一",
    "疯狂失智": "瞳孔震颤失控，嘴角不受控制地抽搐，面部扭曲变形，眼神狂乱无神",
    "极致温柔": "眼神柔和如水，嘴角含着温暖的笑意，表情平静美好，气质温婉如玉",
    "冷漠如冰": "目光冰冷刺骨，面无任何表情，眼神空洞如深渊，神情淡漠如冰"
    "复杂矛盾": "眼神中同时流露出希望与绝望，嘴角既有上扬的笑意又有下撇的苦涩，面部表情复杂矛盾"
    "阴险狠毒": "眼中闪烁着阴险的光芒，嘴角勾起一抹冷笑，面容透着狠毒与算计",
    "纯净无暇": "眼神清澈如泉，嘴角纯真微笑，表情美好如天使，气质纯净无瑕"
}

# 动作张力库（v3.0.0 扩展）
V3_ACTION_ENHANCEMENTS = {
    "慢动作爆发": "极致慢放镜头，捕捉每一个粒子运动的轨迹，时间被拉伸到近乎静止",
    "爆炸冲击波": "物体破碎瞬间的爆炸冲击波，能量波向四周疯狂扩散，视觉冲击力极强",
    "衣物撕裂慢放": "衣物被撕裂的极致慢放，布料纤维一根根分离的细节清晰可见",
    "剧烈喘息声": "胸口剧烈起伏如破风箱，粗重的呼吸声清晰可闻，喉结不受控制地滚动",
    "肌肉剧烈抽搐": "肌肉不受控制地剧烈抽搐，青筋如蚯蚓般暴起，力量感爆发到极限",
    "突然爆发性转身": "猛然转身带起狂风，头发和衣摆在风中狂乱飞扬，气场瞬间爆发",
    "动作残影": "动作快到留下残影，视觉上呈现多个重叠的影像，速度感极强",
    "物理飞溅": "血液、水珠、碎片等物理物质四溅飞射，粒子特效绚丽真实"
    "冲击波扩散": "动作产生强大的冲击波，周围的空气被压缩然后向四周扩散"
}

# 大师运镜库（v3.0.0 扩展）
V3_MASTER_CAMERA_MOVES = {
    "希区柯克变焦": "镜头完全不动，推镜头与拉镜头同时反向运动，营造极度的眩晕不安感",
    "荷兰斜角极端": "镜头极度倾斜构图，画面严重失衡，营造极其强烈的紧张不安感",
    "手持剧烈晃动": "镜头剧烈晃动，呼吸感强烈到令人头晕，营造极致的真实临场感",
    "低角度极端仰拍": "极端低角度仰拍，主体显得高大威猛如神，压迫感极强",
    "高角度极致俯拍": "极高角度俯拍，主体显得渺小脆弱如尘埃，孤独感极强",
    "环绕螺旋拍摄": "镜头螺旋上升环绕主体运动，全方位展示，空间感和眩晕感极强",
    "快速跟拍 + 晃动": "镜头快速跟随主体运动并剧烈晃动，代入感极强，动感极强"
}

# 情绪滤镜库（v3.0.0 扩展）
V3_EMOTION_FILTERS = {
    "极致忧郁": "极致的冷色调，极低的饱和度，阴影沉重如铅，氛围压抑到窒息",
    "极致惊悚": "极高的对比度，极端强烈的明暗对比，锐利线条到刺眼，不安感极强",
    "极致热血": "极致的暖色调，极高的饱和度，红色为主色调，燃烧感极强",
    "极致赛博": "极致的霓虹色彩，极端的冷蓝色调，光效绚烂到刺眼，科技感极强",
    "极致国风": "极致的水墨色调，极致的留白艺术，金色点缀点缀，古雅感极强",
    "极致治愈": "极致的暖色调，极致的柔和光线，极高的亮度，温馨感极强",
    "极致悬疑": "极低的亮度，极端强烈的对比，阴影深重如墨，神秘感极强",
    "极致浪漫": "极致的粉色系，极致的柔光效果，极致的朦胧美感，氛围甜蜜到腻",
    "史诗悲壮": "史诗般的壮丽色调，黄金比例构图，恢弘大气的配乐，悲壮感极强",
    "黑暗压抑": "黑暗压抑的色调，阴沉沉重的氛围，绝望感和恐怖感极强"
}

# 戏剧化光影库（v3.0.0 扩展）
V3_DRAMATIC_LIGHTING = {
    "极致侧逆光": "极致强烈的侧逆光，勾勒出人物如剪影般的轮廓，明暗对比极端",
    "极致丁达尔效应": "极致强烈的光束穿透尘埃，形成极致的丁达尔效应，神圣庄严",
    "极致霓虹灯效": "极致绚烂的霓虹灯光闪烁，色彩丰富到极点，光晕弥漫，赛博朋克",
    "极致黄金时刻": "极致金色的暖光沐浴，色调温暖柔和到极致，时间凝固感极强",
    "极致雷光闪烁": "背景极致强烈的雷光闪电般闪烁，瞬间强光照亮一切，戏剧化极强",
    "极致冷暖对比": "画面中冷暖色块的极致对比，营造强烈的视觉冲突和戏剧性"
}

# ================= v3.0.0 核心功能函数 =================

def v3_analyze_story_with_characters(story_text):
    """分析故事并提取角色设定"""
    
    # 情绪关键词
    emotion_keywords = {
        "绝望": ["绝望", "沉重", "痛苦", "黑暗", "死亡"],
        "转折": ["突然", "但是", "然而", "意外", "转折"],
        "爆发": ["爆发", "冲突", "争吵", "打斗", "愤怒"],
        "高潮": ["高潮", "顶点", "极致", "巅峰", "最后"],
        "悲伤": ["悲伤", "痛苦", "流泪", "难过", "哀伤"],
        "愤怒": ["愤怒", "生气", "怒火", "憎恨", "复仇"],
        "恐惧": ["恐惧", "害怕", "惊恐", "担心", "害怕"],
        "喜悦": ["喜悦", "快乐", "开心", "幸福", "快乐"],
        "复仇": ["复仇", "报应", "仇恨", "仇视", "复仇者"]
    }
    
    # 角色关键词
    character_keywords = {
        "男性": ["男人", "男生", "他", "男子", "少年", "男孩"],
        "女性": ["女人", "女生", "她", "女子", "少女", "女孩"],
        "剑客": ["剑客", "剑者", "武士", "武者", "侠客"],
        "复仇者": ["复仇者", "报应者", "复仇"],
        "主角": ["主角", "主人公", "领衔"],
        "反派": ["反派", "坏人", "敌人", "对手"]
    }
    
    # 分析情绪
    emotions = []
    text_lower = story_text.lower()
    for emotion, keywords in emotion_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            emotions.append(emotion)
    
    # 提取角色
    characters = []
    for char_type, keywords in character_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            characters.append({
                "name": char_type,
                "appearance": f"一个{char_type}，根据故事描述确定具体外貌和服装"
            })
    
    # 如果没有识别到角色，创建默认角色
    if not characters:
        characters = [{
            "name": "主角",
            "appearance": "根据故事描述确定主角的外貌和服装"
        }]
    
    return {
        "emotions": emotions if emotions else ["平静"],
        "characters": characters
    }


def v3_generate_dramatic_storyboard(
    story_text,
    tension_level,
    emotion_filter,
    expression_select,
    action_select,
    camera_select,
    lighting_select,
    aspect_ratio,
    global_style_theme,
    global_lighting_mood
):
    """v3.0.0 三层架构生成戏剧化分镜"""
    
    # 第一层：全局逻辑层（角色、环境、基调）
    analysis = v3_analyze_story_with_characters(story_text)
    
    # 第二层：导演编剧层（分镜生成）
    segments = []
    story_sentences = split_story_to_segments(story_text)
    
    # 获取物理参数
    tension_motion_map = {
        "平淡叙事 (温和)": 3,
        "轻微波动 (平静)": 5,
        "明显起伏 (中等)": 7,
        "紧张刺激 (强烈)": 9,
        "史诗冲突 (极致)": 10
    }
    motion_val = tension_motion_map.get(tension_level, 7)
    
    # 转换画幅比例
    ar_map = {
        "16:9 横屏": "--ar 16:9",
        "21:9 电影宽屏": "--ar 21:9",
        "9:16 竖屏": "--ar 9:16",
        "1:1 方图": "--ar 1:1"
    }
    ar_param = ar_map.get(aspect_ratio, "--ar 16:9")
    
    # 根据情绪和故事生成分镜
    for i, sentence in enumerate(story_sentences):
        # 确定情节和情绪
        if i == 0:
            plot_type = "起"
            emotion = analysis["emotions"][0] if analysis["emotions"] else "平静"
        elif i == len(story_sentences) - 1:
            plot_type = "合"
            emotion = analysis["emotions"][-1] if analysis["emotions"] else "平静"
        else:
            plot_type = "承/转"
            emotion = analysis["emotions"][1] if len(analysis["emotions"]) > 1 else (analysis["emotions"][0] if analysis["emotions"] else "平静")
        
        # 第二层：戏剧化扩充
        visual_prompt = v3_build_visual_prompt(
            sentence,
            emotion,
            expression_select,
            action_select,
            camera_select,
            lighting_select
        )
        
        # 确定时间范围
        num_shots = len(story_sentences)
        if num_shots == 3:
            time_ranges = ["0-5秒", "5-10秒", "10-15秒"]
        elif num_shots == 4:
            time_ranges = ["0-4秒", "4-8秒", "8-12秒", "12-15秒"]
        elif num_shots == 5:
            time_ranges = ["0-3秒", "3-6秒", "6-9秒", "9-12秒", "12-15秒"]
        else:
            time_ranges = [f"{i*3}-{(i+1)*3}秒" for i in range(num_shots)]
        
        # 生成旁白和音效
        vo = generate_vo_for_shot(sentence, emotion)
        sfx = generate_sfx_for_shot(sentence, emotion, action_select)
        
        segments.append({
            "shot_id": f"Shot {i+1:02d}",
            "setting": f"根据故事描述确定的场景 - 时间：{time_ranges[i].split('-')[0]}",
            "camera": v3_select_camera(camera_select, plot_type, emotion),
            "visual_prompt": visual_prompt,
            "vo": vo,
            "sfx": sfx
        })
    
    # 第三层：Seedance 适配层（组装最终提示词）
    final_prompt = v3_assemble_final_prompt(segments, motion_val, ar_param)
    
    return {
        "global_settings": {
            "style_theme": global_style_theme,
            "lighting_mood": global_lighting_mood
        },
        "characters": analysis["characters"],
        "storyboard": segments,
        "final_prompt": final_prompt
    }


def v3_build_visual_prompt(sentence, emotion, expression_select, action_select, camera_select, lighting_select):
    """v3.0.0 戏剧化扩充引擎"""
    
    description_parts = []
    
    # 基础场景描述
    description_parts.append(sentence)
    
    # 添加表情微操
    if emotion in expression_select:
        description_parts.append(V3_EXPRESSION_ENHANCEMENTS[emotion])
    
    # 添加动作张力
    if action_select:
        for action in action_select:
            description_parts.append(V3_ACTION_ENHANCEMENTS[action])
    
    # 添加运镜
    if camera_select:
        for camera in camera_select:
            description_parts.append(V3_MASTER_CAMERA_MOVES[camera])
    
    # 添加光影
    if lighting_select:
        for lighting in lighting_select:
            description_parts.append(V3_DRAMATIC_LIGHTING[lighting])
    
    # 组合成视觉提示词
    visual_prompt = f"[电影级画质，极致细节，{', '.join(description_parts)}]"
    
    # 如果有选择的情绪滤镜，也添加到提示词中
    if emotion_select and len(emotion_select) > 0:
        emotion_desc = ', '.join([V3_EMOTION_FILTERS[e] for e in emotion_select])
        visual_prompt += f", {emotion_desc}"
    
    return visual_prompt


def v3_select_camera(camera_select, plot_type, emotion):
    """智能选择运镜"""
    
    if camera_select:
        # 如果用户选择了运镜，使用第一个
        return camera_select[0]
    
    # 否则根据情节和情绪智能选择
    if plot_type == "起":
        return "低角度推近特写"
    elif plot_type == "合":
        if emotion in ["愤怒", "爆发", "复仇"]:
            return "低角度极端仰拍"
        else:
            return "高角度极致俯拍"
    else:
        return "手持晃动感"


def generate_vo_for_shot(sentence, emotion):
    """生成分镜的旁白"""
    
    # 简单的旁白生成逻辑
    if not sentence:
        return ""
    
    # 检查是否是对话
    if '"' in sentence or '"' in sentence or "说" in sentence:
        return f"(旁白)：{sentence}"
    else:
        return f"(内心独白)：{sentence}"


def generate_sfx_for_shot(sentence, emotion, action_select):
    """生成分镜的音效"""
    
    sfx_list = []
    
    # 根据情绪添加基础音效
    if emotion == "恐惧":
        sfx_list.append("心跳声")
        sfx_list.append("呼吸声")
    elif emotion == "愤怒":
        sfx_list.append("怒吼声")
        sfx_list.append("拳头紧握声")
    elif emotion == "悲伤":
        sfx_list.append("呜咽声")
        sfx_list.append("风声")
    
    # 添加动作音效
    if action_select:
        if "慢动作" in action_select[0]:
            sfx_list.append("慢动作音效")
        elif "爆发" in action_select[0]:
            sfx_list.append("爆炸声")
        elif "撕裂" in action_select[0]:
            sfx_list.append("撕裂声")
    
    return ', '.join(sfx_list) if sfx_list else "环境音"


def v3_assemble_final_prompt(segments, motion_val, ar_param):
    """v3.0.0 Seedance 适配层"""
    
    prompt_parts = []
    
    # 添加全局画质
    prompt_parts.append("电影级画质，极致细节，高动态")
    
    # 添加所有分镜
    for i, segment in enumerate(segments):
        prompt_parts.append(f"{segment['shot_id']}：{segment['setting']} - {segment['camera']} - {segment['visual_prompt']} - VO:{segment['vo']} - SFX:{segment['sfx']}")
    
    # 添加 Seedance 2.0 物理参数
    prompt_parts.append(f"--motion {motion_val} {ar_param}")
    
    # 组合成最终字符串
    final_prompt = "\n".join(prompt_parts)
    
    return final_prompt


# ================= v3.0.0 OpenAI API 调用函数 =================

def v3_call_openai_api(story_text, user_instructions):
    """调用 OpenAI API 生成 v3.0.0 导演级分镜"""
    
    if not OPENAI_AVAILABLE:
        return {
            "error": "OpenAI SDK 未安装，请先安装：pip install openai",
            "segments": []
        }
    
    try:
        # 初始化 OpenAI 客户端
        client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )
        
        # 构建 API 请求
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": V3_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"""
请将这段故事转化为专业连贯分镜：

故事描述：{story_text}

用户指令：{user_instructions}

要求：
1. 提取故事中的核心角色、环境设定
2. 生成 3-5 个逻辑连贯、空间连续的导演级分镜
3. 每个分镜包含 6 个标准化要素：镜号、场景、运镜、动态画面描述提示词、旁白、音效
4. 输出为严格的 JSON 格式
5. 确保角色一致性、空间连续性
6. 最大化 Seedance 2.0 的动态性能
"""
                }
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        # 解析响应
        result = response.choices[0].message.content
        
        # 尝试提取 JSON
        try:
            json_start = result.find("{")
            json_end = result.rfind("}") + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = result[json_start:json_end]
                data = json.loads(json_str)
                
                return {
                    "global_settings": data.get("global_settings", {}),
                    "characters": data.get("characters", []),
                    "storyboard": data.get("storyboard", []),
                    "final_prompt": result,
                    "raw_response": result,
                    "parsed": True
                }
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"解析 OpenAI 响应失败：{e}")
        
        # 如果 JSON 解析失败，返回原始内容
        return {
            "error": "无法解析 API 响应为标准格式",
            "raw_response": result,
            "segments": []
        }
    
    except Exception as e:
        logger.error(f"OpenAI API 调用失败：{e}")
        return {
            "error": f"API 调用失败：{str(e)}",
            "segments": []
        }


# ================= v3.0.0 渲染函数 =================

def v3_render_director_console():
    """渲染 v3.0.0 AI 全能导演工作站"""
    
    st.subheader("🎬 Seedance 2.0 AI 全能导演工作站 v3.0.0")
    st.caption("三层导演逻辑 + 六要素标准化剧本 + 视听一致性引擎")
    
    st.markdown("---")
    
    # API 模式切换
    api_mode = st.toggle("🤖 使用 OpenAI GPT-4o API", value=True, help="开启后使用 OpenAI API 进行智能生成，关闭后使用本地模拟")
    
    if not api_mode and not OPENAI_AVAILABLE:
        st.warning("⚠️ 本地模拟模式需要 OpenAI SDK，但当前环境未安装 OpenAI SDK")
        st.info("💡 提示：安装 OpenAI SDK 后可以使用完整的本地模拟功能")
    
    st.markdown("---")
    
    # 第一部分：全局逻辑层配置
    st.markdown("### 🎭 全局逻辑层 (Global Settings)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        story_text = st.text_area(
            "📖 1. 故事/脚本输入",
            placeholder="输入 100-300 字的故事或完整剧本...",
            height=150,
            help="系统将自动分析角色、环境、情绪，生成导演级分镜"
        )
    
    with col2:
        st.info("💡 输入建议")
        st.markdown("""
        - 包含核心角色（外貌、服装）
        - 包含环境描述（时间、地点）
        - 包含冲突或转折点
        - 推荐长度：100-300字
        """)
    
    st.divider()
    
    # 全局风格配置
    col1, col2, col3 = st.columns(3)
    
    with col1:
        global_style_theme = st.selectbox(
            "🎨 2. 视觉风格主题",
            ["赛博朋克", "东方武侠", "史诗战争", "唯美爱情", "悬疑惊悚", "治愈温暖", "极简主义"],
            help="选择全局的视觉风格主题"
        )
        
        global_lighting_mood = st.selectbox(
            "💡 3. 光影基调",
            ["高对比度", "柔和光影", "冷暖对比", "戏剧化光影", "自然光"],
            help="选择全局的光影基调"
        )
    
    with col2:
        tension_level = st.select_slider(
            "🎭 4. 物理强度控制",
            options=list(TENSION_MOTION_MAP.keys()),
            value="明显起伏 (中等)",
            help="控制 Seedance 2.0 的 --motion 参数，影响动态强度"
        )
        
        aspect_ratio = st.selectbox(
            "📐 5. 画幅比例",
            ["16:9 横屏", "21:9 电影宽屏", "9:16 竖屏"],
            help="选择视频的画面比例"
        )
    
    with col3:
        expression_select = st.multiselect(
            "😐 6. 表情微操（可选）",
            list(V3_EXPRESSION_ENHANCEMENTS.keys()),
            help="选择要添加的细腻表情（可多选）"
        )
        
        action_select = st.multiselect(
            "🏃 7. 动作张力（可选）",
            list(V3_ACTION_ENHANCEMENTS.keys()),
            help="选择要添加的动作张力（可多选）"
        )
    
    st.divider()
    
    # 导演编剧层配置
    st.markdown("### 🎬 导演编剧层 (Director Layer)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        camera_select = st.multiselect(
            "🎥 8. 大师运镜（可选）",
            list(V3_MASTER_CAMERA_MOVES.keys()),
            help="选择大师级镜头语言（可多选）"
        )
        
        lighting_select = st.multiselect(
            "💡 9. 戏剧化光影（可选）",
            list(V3_DRAMATIC_LIGHTING.keys()),
            help="选择戏剧化的光影效果（可多选）"
        )
    
    with col2:
        emotion_filter = st.multiselect(
            "🎨 10. 情绪滤镜（可选）",
            list(V3_EMOTION_FILTERS.keys()),
            help="选择情绪基调（可多选）"
        )
    
    with col3:
        st.markdown("**提示**")
        st.markdown("""
        - 表情、动作、运镜、光影将应用到所有分镜
        - 情绪滤镜将影响整体的色调和氛围
        - 全局设置将覆盖单分镜的设置
        """)
    
    st.divider()
    
    # 用户指令输入
    user_instructions = st.text_area(
        "📝 11. 导演指令（可选）",
        placeholder="输入额外的导演指令，如：'增加更多慢动作'、'使用更多特写'...",
        height=80,
        help="输入额外的导演指令，用于指导 AI 生成更符合你需求的分镜"
    )
    
    st.divider()
    
    # 生成按钮
    generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])
    
    with generate_col2:
        if st.button("🎬 生成 v3.0.0 导演级分镜", type="primary", use_container_width=True):
            if not story_text:
                st.warning("⚠️ 请先输入故事或脚本！")
            else:
                if api_mode and OPENAI_AVAILABLE:
                    # 使用 OpenAI API 模式
                    with st.spinner("OpenAI GPT-4o 正在分析故事并生成分镜..."):
                        result = v3_call_openai_api(story_text, user_instructions)
                        display_v3_result(result, api_mode=True)
                else:
                    # 使用本地模拟模式
                    with st.spinner("本地模拟正在生成分镜..."):
                        result = v3_generate_dramatic_storyboard(
                            story_text,
                            tension_level,
                            emotion_filter,
                            expression_select,
                            action_select,
                            camera_select,
                            lighting_select,
                            aspect_ratio,
                            global_style_theme,
                            global_lighting_mood
                        )
                        display_v3_result(result, api_mode=False)


def display_v3_result(result, api_mode):
    """显示 v3.0.0 结果"""
    
    if "error" in result:
        st.error(f"❌ {result['error']}")
        return
    
    if api_mode and result.get("parsed", False):
        # API 模式且解析成功
        st.success("✅ OpenAI GPT-4o 已生成导演级分镜！")
        
        # 显示全局设置
        st.markdown("---")
        st.markdown("### 🎭 全局逻辑层")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**视觉风格主题**")
            st.code(result["global_settings"].get("style_theme", "未设置"), language="text")
        
        with col2:
            st.markdown("**光影基调**")
            st.code(result["global_settings"].get("lighting_mood", "未设置"), language="text")
        
        # 显示角色设定
        st.markdown("---")
        st.markdown("### 👤 角色设定")
        
        for char in result["characters"]:
            with st.expander(f"👤 {char['name']}"):
                st.markdown(f"**外貌特征锁定**：")
                st.code(char['appearance'], language="text")
        
        # 显示分镜
        st.markdown("---")
        st.markdown("### 🎬 导演编剧层")
        
        if result["storyboard"]:
            tabs = st.tabs([seg['shot_id'] for seg in result["storyboard"]])
            
            for i, tab in enumerate(tabs):
                with tab:
                    segment = result["storyboard"][i]
                    
                    # 分镜卡片
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"**{segment['shot_id']}**")
                        st.markdown(f"**场景**：{segment['setting']}")
                    
                    with col2:
                        st.markdown(f"**运镜**：{segment['camera']}")
                        st.markdown(f"**旁白 (VO)**：{segment['vo']}")
                    
                    with col3:
                        st.markdown(f"**音效 (SFX)**：{segment['sfx']}")
                    
                    st.markdown("---")
                    st.markdown(f"**动态画面描述提示词 (Visual Prompt)**")
                    st.code(segment['visual_prompt'], language="text")
        
        # 显示完整提示词
        st.markdown("---")
        st.markdown("### 🎯 完整 Seedance 2.0 提示词（复制到 Seedance 使用）")
        st.code(result["final_prompt"], language="text")
        
        # 下载按钮
        download_content = f"""=== Seedance 2.0 v3.0.0 导演级分镜 ===

{result['final_prompt']}

=== 导演信息 ===
使用模式：OpenAI GPT-4o API
模型：gpt-4o
全局风格：{result['global_settings'].get('style_theme', '未设置')}
光影基调：{result['global_settings'].get('lighting_mood', '未设置')}
物理强度：{result['global_settings'].get('physical_strength', '未设置')}
画幅比例：{result['global_settings'].get('aspect_ratio', '未设置')}

=== 角色设定 ===
"""
        for char in result["characters"]:
            download_content += f"""
{char['name']}：{char['appearance']}
"""

        download_content += f"""
=== 分镜详情 ===
"""
        for seg in result["storyboard"]:
            download_content += f"""
{seg['shot_id']}：
场景：{seg['setting']}
运镜：{seg['camera']}
视觉提示词：{seg['visual_prompt']}
旁白：{seg['vo']}
音效：{seg['sfx']}

"""

        st.download_button(
            label="💾 下载导演级分镜配置",
            data=download_content,
            file_name=f"seedance_v3_director_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    else:
        # 本地模拟模式或 API 模式但解析失败
        mode_name = "OpenAI API (原始响应)" if api_mode else "本地模拟"
        st.success(f"✅ {mode_name} 已生成分镜！")
        
        if result.get("storyboard"):
            # 有分镜数据
            tabs = st.tabs([seg['shot_id'] for seg in result["storyboard"]])
            
            for i, tab in enumerate(tabs):
                with tab:
                    segment = result["storyboard"][i]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"**{segment['shot_id']}**")
                        st.markdown(f"**场景**：{segment['setting']}")
                    
                    with col2:
                        st.markdown(f"**运镜**：{segment['camera']}")
                        st.markdown(f"**旁白**：{segment['vo']}")
                    
                    with col3:
                        st.markdown(f"**音效**：{segment['sfx']}")
                    
                    st.markdown("---")
                    st.markdown(f"**动态画面描述提示词**")
                    st.code(segment['visual_prompt'], language="text")
            
            # 显示完整提示词
            st.markdown("---")
            st.markdown("### 🎯 完整 Seedance 2.0 提示词")
            st.code(result["final_prompt"], language="text")
            
            # 下载按钮
            download_content = f"""=== Seedance 2.0 v3.0.0 导演级分镜 ===

{result['final_prompt']}

=== 导演信息 ===
使用模式：{mode_name}
全局风格：{result.get('global_settings', {}).get('style_theme', '未设置')}
光影基调：{result.get('global_settings', {}).get('lighting_mood', '未设置')}
"""

            for seg in result["storyboard"]:
                download_content += f"""
{seg['shot_id']}：
场景：{seg['setting']}
运镜：{seg['camera']}
视觉提示词：{seg['visual_prompt']}
旁白：{seg['vo']}
音效：{seg['sfx']}

"""
        else:
            # 只有原始响应
            st.markdown("---")
            st.markdown("### 🎯 API 原始响应")
            st.code(result.get("raw_response", ""), language="text")
            
            download_content = f"""=== Seedance 2.0 v3.0.0 API 原始响应 ===

{result.get('raw_response', '')}
"""

        st.download_button(
            label="💾 下载配置",
            data=download_content,
            file_name=f"seedance_v3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )


# 主函数（用于测试）
if __name__ == "__main__":
    v3_render_director_console()
