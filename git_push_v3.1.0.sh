#!/bin/bash
# V3.1.0 Git 推送脚本

echo "=========================================="
echo "🚀 V3.1.0 - Git 推送脚本"
echo "=========================================="
echo ""

cd /workspace/projects/apps/seedance-tool-streamlit

echo "📌 Git 状态"
echo "-" * 60

# 检查 Git 状态
git status --short

echo ""
echo "📌 本地提交历史"
echo "-" * 60

git log --oneline -5

echo ""
echo "📌 远程仓库信息"
echo "-" * 60

git remote -v

echo ""
echo "📌 推送状态检查"
echo "-" * 60

# 检查本地是否领先远程
LOCAL=$(git rev-parse main)
REMOTE=$(git rev-parse origin/main 2>/dev/null)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "✅ 本地已与远程同步"
else
    echo "⚠️  本地领先远程"
    echo "  本地提交：$LOCAL"
    echo "  远程提交：${REMOTE:-无}"
fi

echo ""
echo "📌 推送方式选择"
echo "-" * 60

echo "由于 SSH 不可用，需要使用 HTTPS 推送"
echo "请选择以下方式之一："
echo ""
echo "方式 1：使用 GitHub Token（推荐）"
echo "方式 2：手动推送（如果方式 1 失败）"
echo ""

# 方式 1：使用 GitHub Token
echo "📌 方式 1：使用 GitHub Token"
echo "-" * 60

echo "请按以下步骤操作："
echo ""
echo "1. 创建 GitHub Personal Access Token"
echo "   - 访问：https://github.com/settings/tokens"
echo "   - 点击\"Generate new token\""
echo "   - 选择权限：repo（full control of private repositories）"
echo "   - 生成 Token 并复制"
echo ""
echo "2. 配置 Git 凭证"
echo "   - 执行以下命令："
echo "     git config --global credential.helper store"
echo "     git config --global user.name \"你的用户名\""
echo "     git config --global user.email \"你的邮箱\""
echo ""
echo "3. 推送代码"
echo "   - 执行以下命令："
echo "     git push origin main"
echo ""
echo "或者使用以下方式一次性推送："
echo ""
echo " git push https://YOUR_USERNAME:YOUR_TOKEN@github.com/jinshanguzhou1021-afk/seedance-tool-streamlit.git main"
echo ""
echo "⚠️  注意：将 YOUR_USERNAME 替换为你的 GitHub 用户名"
echo "⚠️  注意：将 YOUR_TOKEN 替换为你刚刚创建的 Token"
echo ""

# 方式 2：手动推送
echo "📌 方式 2：手动推送"
echo "-" * 60

echo "如果方式 1 失败，请按以下步骤手动推送："
echo ""
echo "1. 在浏览器中打开 GitHub"
echo "   - 访问：https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit"
echo ""
echo "2. 登录到 GitHub"
echo "   - 如果未登录，点击右上角的\"Sign in\""
echo ""
echo "3. 创建 Pull Request 或直接推送"
echo "   - 由于你有推送权限，可以直接推送"
echo "   - 或者使用 GitHub 网页界面的推送功能"
echo ""

# 生成推送脚本
echo "📌 自动推送脚本（需要配置 Token）"
echo "-" * 60

PUSH_SCRIPT="push_with_token.sh"

cat > "$PUSH_SCRIPT" << 'EOF'
#!/bin/bash
# V3.1.0 自动推送脚本

cd /workspace/projects/apps/seedance-tool-streamlit

# 配置你的 GitHub Token
GITHUB_USERNAME="YOUR_USERNAME"
GITHUB_TOKEN="YOUR_TOKEN"

# 推送代码
git push https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/jinshanguzhou1021-afk/seedance-tool-streamlit.git main
EOF

chmod +x "$PUSH_SCRIPT"

echo "已生成自动推送脚本：$PUSH_SCRIPT"
echo ""
echo "使用方法："
echo "1. 编辑 $PUSH_SCRIPT"
echo "2. 替换 YOUR_USERNAME 为你的 GitHub 用户名"
echo "3. 替换 YOUR_TOKEN 为你的 GitHub Token"
echo "4. 运行：bash $PUSH_SCRIPT"
echo ""

# 生成完整的手动推送说明
echo "📌 完整的手动推送说明"
echo "-" * 60

cat << 'EOF'

## 完整的手动推送步骤

### 步骤 1：创建 GitHub Personal Access Token

1. 访问：https://github.com/settings/tokens
2. 点击"Generate new token (classic)"
3. 输入 Token 描述：V3.1.0 - Seedance Tool
4. 选择权限：
   - repo（full control of private repositories）
5. 点击"Generate token"
6. 复制生成的 Token（只显示一次，请妥善保存）

### 步骤 2：配置 Git 凭证

#### 方式 A：全局配置（推荐）

```bash
git config --global credential.helper store
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"
```

#### 方式 B：配置 HTTPS 凭证

```bash
git config --global credential.helper store
```

然后推送时输入用户名和 Token：
```bash
git push https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit.git main
```

### 步骤 3：推送代码

#### 方式 A：全局配置后推送

```bash
cd /workspace/projects/apps/seedance-tool-streamlit
git push origin main
```

#### 方式 B：使用 Token URL 推送（一次性）

```bash
cd /workspace/projects/apps/seedance-tool-streamlit
git push https://YOUR_USERNAME:YOUR_TOKEN@github.com/jinshanguzhou1021-afk/seedance-tool-streamlit.git main
```

替换 `YOUR_USERNAME` 和 `YOUR_TOKEN` 为你的实际值。

### 步骤 4：验证推送

1. 打开浏览器
2. 访问：https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit
3. 检查最新的提交是否已推送到远程仓库

---

## Streamlit Cloud 部署

推送成功后，参考以下文档进行 Streamlit Cloud 部署：

Streamlit_Cloud_部署指南_V3.1.0.md

---

EOF

echo ""
echo "=========================================="
echo "📊 Git 推送总结"
echo "=========================================="
echo ""
echo "状态：⚠️ 需要手动推送"
echo "原因：SSH 不可用，HTTPS 需要认证"
echo ""
echo "📋 推送方式："
echo "  方式 1：使用 GitHub Token（推荐）"
echo "  方式 2：手动推送"
echo ""
echo "📄 相关文件："
echo "  - push_with_token.sh - 自动推送脚本"
echo "  - Streamlit_Cloud_部署指南_V3.1.0.md - Streamlit Cloud 部署指南"
echo ""
echo "🚀 下一步："
echo "  1. 选择一种推送方式"
echo "  2. 推送代码到 GitHub"
echo "  3. 在 Streamlit Cloud 部署应用"
echo "  4. 更新 Streamlit Cloud URL"
echo ""
echo "=========================================="
