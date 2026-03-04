#!/bin/bash
# Streamlit 应用启动脚本

echo "========================================="
echo "  即梦（Seedance）提示词工具"
echo "  Streamlit Web 应用"
echo "========================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到 Python 3"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

echo "✓ Python 版本：$(python3 --version)"
echo ""

# 检查 Streamlit
echo "检查 Streamlit..."
if python3 -c "import streamlit" 2>/dev/null; then
    echo "✓ Streamlit 已安装"
else
    echo "✗ Streamlit 未安装"
    echo ""
    echo "正在安装依赖..."
    pip3 install -r requirements.txt
    echo ""
fi

# 创建 .streamlit 配置目录
mkdir -p .streamlit

# 启动应用
echo "启动 Streamlit 应用..."
echo ""
echo "========================================="
echo "  应用地址：http://localhost:8501"
echo "========================================="
echo ""

streamlit run app.py --server.port=8501 --server.headless=true

# 如果应用异常退出
if [ $? -ne 0 ]; then
    echo ""
    echo "========================================="
    echo "应用异常退出"
    echo "========================================="
    echo ""
    echo "故障排查："
    echo "1. 检查 Python 版本：python3 --version"
    echo "2. 重新安装依赖：pip3 install -r requirements.txt"
    echo "3. 查看完整错误信息"
    echo ""
fi
