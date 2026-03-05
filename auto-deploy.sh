#!/bin/bash
# Streamlit Cloud 自动部署助手
# 注意：第一次部署需要手动配置，之后会自动更新

set -e

echo "========================================="
echo "  Streamlit Cloud 自动部署助手"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 git
if ! command -v git &> /dev/null; then
    echo -e "${RED}错误：未找到 Git${NC}"
    echo "请先安装 Git：https://git-scm.com/downloads"
    exit 1
fi

echo -e "${GREEN}✓${NC} Git 已安装"
echo ""

# 进入项目目录
cd "$(dirname "$0")"

# 检查是否在 git 仓库中
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}初始化 Git 仓库...${NC}"
    git init
    echo -e "${GREEN}✓${NC} Git 仓库已初始化"
    echo ""
fi

# 检查状态
echo "检查仓库状态..."
if git diff --quiet && git diff --cached --quiet; then
    echo -e "${YELLOW}⚠️ 没有新的更改需要提交${NC}"
else
    echo "发现新的更改，正在提交..."

    # 添加文件
    echo "添加文件到 Git..."
    git add .

    # 提交
    echo "提交更改..."
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    git commit -m "Auto-update: ${TIMESTAMP}" || echo -e "${YELLOW}⚠️ 没有需要提交的更改${NC}"

    echo -e "${GREEN}✓${NC} 更改已提交"
    echo ""
fi

# 检查远程仓库
if git remote get-url origin &> /dev/null; then
    echo -e "${GREEN}✓${NC} 远程仓库已配置"
    REMOTE_URL=$(git remote get-url origin)

    # 隐藏 token
    SAFE_URL=$(echo "$REMOTE_URL" | sed 's/\/\/[^@]*@/\/\/<token>@/')
    echo "  远程地址：$SAFE_URL"
    echo ""

    # 推送
    echo "推送到远程仓库..."
    if git push origin main 2>/dev/null; then
        echo -e "${GREEN}✓${NC} 代码已成功推送到 main 分支"
    elif git push origin master 2>/dev/null; then
        echo -e "${GREEN}✓${NC} 代码已成功推送到 master 分支"
    else
        echo -e "${RED}✗${NC} 推送失败"
        echo "请检查网络连接或认证信息"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} 未配置远程仓库"
    echo ""
    exit 1
fi

echo ""
echo "========================================="
echo "  部署状态"
echo "========================================="
echo ""

# 检查是否已部署
DEPLOYED_FILE=".streamlit_deployed"

if [ -f "$DEPLOYED_FILE" ]; then
    echo -e "${GREEN}✓ 应用已配置为自动部署${NC}"
    echo ""
    echo "Streamlit Cloud 会自动检测到新的推送并重新部署"
    echo ""
    echo "📊 部署进度："
    echo "  1. ✅ 代码已推送"
    echo "  2. 🔄 Streamlit Cloud 正在检测更新..."
    echo "  3. 📦 正在安装依赖..."
    echo "  4. 🔨 正在构建应用..."
    echo "  5. 🚀 正在部署..."
    echo "  6. ✅ 部署完成（预计 1-3 分钟）"
    echo ""
    echo "🌐 访问应用："
    DEPLOY_URL=$(cat "$DEPLOYED_FILE")
    echo "  $DEPLOY_URL"
    echo ""
    echo "💡 提示：你可以访问以下链接查看部署日志"
    echo "  https://share.streamlit.io"
else
    echo -e "${YELLOW}⚠️ 应用尚未在 Streamlit Cloud 上配置${NC}"
    echo ""
    echo "📋 首次部署步骤："
    echo ""
    echo "1. 访问 Streamlit Cloud："
    echo "   ${GREEN}https://share.streamlit.io${NC}"
    echo ""
    echo "2. 点击右上角 ${GREEN}New app${NC}"
    echo ""
    echo "3. 使用 GitHub 账号登录"
    echo ""
    echo "4. 填写配置："
    echo "   Repository: ${GREEN}jinshanguzhou1021-afk/seedance-tool-streamlit${NC}"
    echo "   Branch: ${GREEN}main${NC}"
    echo "   Main file path: ${GREEN}app.py${NC}"
    echo ""
    echo "5. 点击 ${GREEN}Deploy${NC}"
    echo ""
    echo "6. 等待 1-3 分钟部署完成"
    echo ""
    echo "7. 复制生成的应用 URL，并运行以下命令："
    echo "   ${YELLOW}echo 'YOUR_APP_URL' > .streamlit_deployed${NC}"
    echo ""
fi

echo "========================================="
echo "  快速命令"
echo "========================================="
echo ""
echo "查看部署日志："
echo "  ${GREEN}https://share.streamlit.io${NC}"
echo ""
echo "查看代码仓库："
echo "  ${GREEN}https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit${NC}"
echo ""
echo "后续自动部署："
echo "  ${GREEN}./auto-deploy.sh${NC}"
echo ""
echo "========================================="
