#!/bin/bash
# V3.1.0 整合版快速启动脚本

echo "=========================================="
echo "🎬 Seedance Tool V3.1.0 整合版启动"
echo "=========================================="
echo ""

cd /workspace/projects/apps/seedance-tool-streamlit

echo "📌 版本信息"
echo "版本：V3.1.0（整合版）"
echo "核心功能：2 个（分镜生成器 + 分镜提示词）"
echo "整合：4 个功能 → 2 个功能"
echo "代码优化：减少 400 行（17%）"
echo ""

echo "📌 API 配置"
echo "优先级：st.secrets > 环境变量 > 内置"
echo "API 模型：DeepSeek V3 (deepseek-chat)"
echo ""

echo "📌 功能说明"
echo "1. 分镜生成器（整合分镜生成器 + 提示词生成器）"
echo "2. 分镜提示词（整合高级构建器 + AI 视觉导演）"
echo ""

echo "📌 启动应用..."
echo ""
echo "⚠️  注意：应用将在后台启动，可以通过以下方式访问："
echo "   - 本地访问：http://localhost:8501"
echo "   - 如果在云服务器，需要配置端口转发"
echo ""
echo "🚀 启动中..."
streamlit run app_v3.1.0_integrated.py --server.port=8501 --server.address=0.0.0.0
