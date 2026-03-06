# ================= DeepSeek/OpenAI API 配置管理 =================

# ⚠️ 安全提示：
# 1. API Key 已内置到代码中，仅供个人学习和测试使用
# 2. 生产环境强烈建议使用 Streamlit Secrets 或环境变量管理 API Key
# 3. 不要将包含真实 API Key 的代码上传到公共仓库

# ================= API Key 配置 =================

# DeepSeek API 配置（内置）
DEEPSEEK_API_KEY = "sk-62a693ae5cb24574bd9df2a9bb53cd99"  # 用户提供的 API Key
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

# OpenAI API 配置（用于 v3.0.0 AI 全能导演工作站）
OPENAI_API_KEY = None  # 将从 st.secrets 中读取
OPENAI_BASE_URL = "https://api.openai.com/v1"  # 默认值，可从 st.secrets 中读取
OPENAI_MODEL = "gpt-4-turbo"

# ================= API 模式选择 =================

API_MODES = {
    "DeepSeek-V3 (免费)": "deepseek",
    "OpenAI GPT-4 (付费)": "openai"
}

# ================= API 配置函数 =================

def get_api_config(api_mode):
    """根据 API 模式获取 API 配置"""

    if "deepseek" in api_mode.lower():
        return {
            "api_key": DEEPSEEK_API_KEY,
            "base_url": "https://api.deepseek.com/v1",
            "model": DEEPSEEK_MODEL,
            "provider": "deepseek"
        }
    else:
        return {
            "api_key": OPENAI_API_KEY if OPENAI_API_KEY else DEEPSEEK_API_KEY,
            "base_url": OPENAI_BASE_URL if OPENAI_BASE_URL else "https://api.openai.com/v1",
            "model": OPENAI_MODEL,
            "provider": "openai"
        }

def is_api_key_valid(api_key):
    """检查 API Key 是否有效（基本格式检查）"""
    return api_key and api_key.startswith("sk-") and len(api_key) > 20

# ================= 环境变量支持 =================

import os

# 支持从环境变量读取 API Key（优先级最高）
if os.getenv("DEEPSEEK_API_KEY"):
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if os.getenv("OPENAI_API_KEY"):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if os.getenv("OPENAI_BASE_URL"):
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
