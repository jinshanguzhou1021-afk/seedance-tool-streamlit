#!/bin/bash
# Streamlit Cloud 部署脚本

echo "========================================="
echo "  Streamlit Cloud 部署助手"
echo "========================================="
echo ""

# 检查 git
if ! command -v git &> /dev/null; then
    echo "错误：未找到 Git"
    echo "请先安装 Git：https://git-scm.com/downloads"
    exit 1
fi

echo "✓ Git 已安装"
echo ""

# 检查是否在 git 仓库中
if [ ! -d ".git" ]; then
    echo "初始化 Git 仓库..."
    git init
    echo "✓ Git 仓库已初始化"
    echo ""
fi

# 添加文件
echo "添加文件到 Git..."
git add .
echo "✓ 文件已添加"
echo ""

# 提交
echo "提交更改..."
git commit -m "Update Streamlit app" 2>/dev/null || echo "⚠️ 没有新的更改需要提交"
echo ""

# 检查远程仓库
if git remote get-url origin &> /dev/null; then
    echo "✓ 远程仓库已配置"
    REMOTE_URL=$(git remote get-url origin)
    echo "  远程地址：$REMOTE_URL"
    echo ""

    # 推送
    echo "推送到远程仓库..."
    git push origin main 2>/dev/null || git push origin master 2>/dev/null || git push -u origin main
    echo "✓ 代码已推送"
else
    echo "⚠️ 未配置远程仓库"
    echo ""
    echo "请按照以下步骤操作："
    echo ""
    echo "1. 在 GitHub 创建新仓库"
    echo "2. 添加远程仓库："
    echo "   git remote add origin https://github.com/your-username/your-repo.git"
    echo "3. 推送代码："
    echo "   git push -u origin main"
    echo ""
    echo "然后访问 Streamlit Cloud 部署："
    echo "https://share.streamlit.io"
fi

echo ""
echo "========================================="
echo "  部署指南"
echo "========================================="
echo ""
echo "如果已推送到 GitHub，请："
echo ""
echo "1. 访问 https://share.streamlit.io"
echo "2. 点击 'New app'"
echo "3. 连接你的 GitHub 账号"
echo "4. 选择本仓库"
echo "5. 设置主文件路径为：app.py"
echo "6. 点击 'Deploy'"
echo ""
echo "部署完成后，你会得到一个类似这样的 URL："
echo "https://your-app.streamlit.app"
echo ""
