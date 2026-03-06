#!/bin/bash
# V3.0.2-Lite 快速启动脚本

echo "=========================================="
echo "🎬 Seedance Tool V3.0.2-Lite 启动"
echo "=========================================="
echo ""

cd /workspace/projects/apps/seedance-tool-streamlit

echo "📌 版本信息"
echo "版本：V3.0.2-Lite"
echo "特性：整合优化版 API 安全 + V3.0.0 三层导演逻辑"
echo ""

echo "📌 API 配置"
echo "优先级：st.secrets > 环境变量 > 内置"
echo ""

echo "📌 启动应用..."
echo ""
echo "⚠️  注意：应用将在后台启动，可以通过以下方式访问："
echo "   - 本地访问：http://localhost:8501"
echo "   - 如果在云服务器，需要配置端口转发"
echo ""
echo "🚀 启动中..."
streamlit run app_v3.0.2_lite.py --server.port=8501 --server.address=0.0.0.0
