#!/bin/bash
# V3.0.0 快速启动测试脚本

echo "=========================================="
echo "🎬 Seedance Tool V3.0.0 启动测试"
echo "=========================================="
echo ""

cd /workspace/projects/apps/seedance-tool-streamlit

echo "📌 1. 环境检查..."
python3 -m py_compile app.py
if [ $? -eq 0 ]; then
    echo "✅ 语法检查通过"
else
    echo "❌ 语法检查失败"
    exit 1
fi

echo ""
echo "📌 2. 功能自检..."
python3 test_v3_functionality.py
if [ $? -ne 0 ]; then
    echo "❌ 功能自检失败"
    exit 1
fi

echo ""
echo "📌 3. 启动 Streamlit 应用..."
echo ""
echo "⚠️  注意：应用将在后台启动，可以通过以下方式访问："
echo "   - 本地访问：http://localhost:8501"
echo "   - 如果在云服务器，需要配置端口转发"
echo ""
echo "🚀 启动中..."
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
