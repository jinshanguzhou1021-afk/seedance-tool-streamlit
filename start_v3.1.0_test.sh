#!/bin/bash
# V3.1.0 整合版快速启动和测试脚本

echo "=========================================="
echo "🧪 V3.1.0 整合版 - 快速启动和测试"
echo "=========================================="
echo ""

cd /workspace/projects/apps/seedance-tool-streamlit

echo "📌 版本信息"
echo "版本：V3.1.0（功能整合版）"
echo "核心功能：2 个（分镜生成器 + 分镜提示词）"
echo "主文件：app_v3.1.0_integrated.py"
echo ""

echo "📌 1. 应用文件检查"
if [ -f "app_v3.1.0_integrated.py" ]; then
    echo "✅ 主应用文件存在"
    ls -lh app_v3.1.0_integrated.py
else
    echo "❌ 主应用文件不存在"
    exit 1
fi
echo ""

echo "📌 2. 依赖检查"
python3 -c "
try:
    import streamlit as st
    print('✅ Streamlit 导入成功')
except ImportError:
    print('❌ Streamlit 未安装')
    exit(1)

try:
    from openai import OpenAI
    print('✅ OpenAI 导入成功')
except ImportError:
    print('❌ OpenAI 未安装')
    exit(1)

print('✅ 所有依赖正常')
"
if [ $? -ne 0 ]; then
    echo "❌ 依赖检查失败"
    exit 1
fi
echo ""

echo "📌 3. API 配置检查"
python3 -c "
from openai import OpenAI

API_KEY = 'sk-2f2c80b0af064d2a8ef04990630c8d7d'
API_BASE_URL = 'https://api.deepseek.com'

try:
    client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)
    print('✅ API 客户端初始化成功')
    print(f'  API 模型：deepseek-chat')
    print(f'  API 地址：{API_BASE_URL}')
except Exception as e:
    print(f'❌ API 客户端初始化失败：{e}')
    exit(1)
"
if [ $? -ne 0 ]; then
    echo "❌ API 配置检查失败"
    exit 1
fi
echo ""

echo "📌 4. 应用启动"
echo "⚠️  注意：应用将在后台启动，按 Ctrl+C 停止"
echo ""
echo "🌐 访问地址："
echo "   - 本地访问：http://localhost:8501"
echo "   - 远程访问：http://[服务器IP]:8501"
echo ""
echo "🚀 启动中..."
echo ""

streamlit run app_v3.1.0_integrated.py --server.port=8501 --server.address=0.0.0.0
