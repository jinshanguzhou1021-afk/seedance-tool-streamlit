# 🚀 V3.1.0 Streamlit Cloud 部署指南

**部署时间**：2026-03-06 14:46
**版本**：V3.1.0（功能整合版）
**状态**：✅ 已推送到 GitHub，准备部署到 Streamlit Cloud

---

## 📋 前置条件

### 1. 账户准备

- ✅ GitHub 账户（已有）
- ✅ Streamlit Cloud 账户（需要注册）
- ✅ 仓库已推送到 GitHub

### 2. 仓库信息

- **GitHub 仓库**：https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit.git
- **主分支**：main
- **主文件**：app_v3.1.0_integrated.py
- **本地领先**：6 个提交

---

## 🌐 方法 1：通过 Streamlit Cloud 部署（推荐）

### 步骤 1：登录 Streamlit Cloud

1. 打开浏览器，访问：https://streamlit.io/cloud
2. 点击"Sign up"或"Log in"
3. 使用你的 GitHub 账户登录

### 步骤 2：创建新应用

1. 登录后，点击"New app"
2. 填写应用信息：
   - **App name**：seedance-tool-v3.1.0
   - **Repository**：jinshanguzhou1021-afk/seedance-tool-streamlit
   - **Branch**：main
   - **Main file path**：app_v3.1.0_integrated.py
3. 点击"Deploy"

### 步骤 3：配置 Secrets（API Key）

1. 应用部署后，点击应用名称进入设置
2. 点击"Secrets"
3. 添加新的 Secret：
   - **Key**：`DEEPSEEK_API_KEY`
   - **Value**：`sk-2f2c80b0af064d2a8ef04990630c8d7d`
4. 点击"Save"

### 步骤 4：重新部署

1. 配置完成后，点击"Deploy"
2. 等待部署完成
3. 部署完成后，点击应用 URL 访问

---

## 🌐 方法 2：通过 GitHub 部署

### 步骤 1：推送代码到 GitHub

**方式 1：使用 HTTPS（如果 SSH 不可用）**

```bash
# 更改远程仓库为 HTTPS
cd /workspace/projects/workspace
git remote set-url origin https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit.git

# 推送代码
git push origin main
```

**方式 2：使用 SSH（如果配置了 SSH 密钥）**

```bash
cd /workspace/projects/workspace
git push origin main
```

### 步骤 2：在 GitHub 上创建 Streamlit Cloud 应用

1. 打开你的 GitHub 仓库：https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit
2. 点击仓库顶部的"..."
3. 选择"Import repository"或"Deploy"
4. 选择"Streamlit"或"Deploy to Streamlit"
5. 点击"Create App"

### 步骤 3：配置应用

1. 填写应用信息：
   - **App name**：seedance-tool-v3.1.0
   - **Main file path**：app_v3.1.0_integrated.py
2. 点击"Create"

### 步骤 4：配置 Secrets

1. 部署完成后，进入应用设置
2. 点击"Secrets"
3. 添加 Secret：
   - **Key**：`DEEPSEEK_API_KEY`
   - **Value**：`sk-2f2c80b0af064d2a8ef04990630c8d7d`
4. 点击"Save"

---

## 🔧 方法 3：手动推送（解决 SSH 问题）

### 步骤 1：检查 SSH 配置

```bash
cd /workspace/projects/workspace
git remote -v
```

**如果 SSH 配置错误**，你会看到类似：
```
fatal: cannot run ssh: No such file or directory
```

### 步骤 2：更改远程仓库为 HTTPS

```bash
cd /workspace/projects/workspace
git remote set-url origin https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit.git
```

### 步骤 3：推送代码

```bash
cd /workspace/projects/workspace
git push origin main
```

**如果需要 GitHub 认证**，你需要：
1. 创建 GitHub Personal Access Token
2. 输入用户名和 Token（不是密码）

---

## 📊 配置文件

### requirements.txt

确保仓库中有 `requirements.txt` 文件：

```txt
streamlit>=1.55.0
python-dotenv>=1.0.0
openai>=1.52.0
requests>=2.31.0
```

### .streamlit/config.toml

如果需要，可以创建 `.streamlit/config.toml` 文件：

```toml
[theme]
primaryColor="#F63366"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[logger]
level = "info"
```

---

## 🚀 部署后访问

### 应用 URL

部署完成后，Streamlit Cloud 会提供一个应用 URL，格式如下：

```
https://[your-app-name]-[random-string].streamlit.app
```

### 示例 URL

```
https://seedance-tool-v3.1.0-xyz123.streamlit.app
```

---

## 🔑 Secrets 配置

### 必需的 Secrets

在 Streamlit Cloud 中配置以下 Secret：

| Key | Value | 说明 |
|-----|-------|------|
| **DEEPSEEK_API_KEY** | sk-2f2c80b0af064d2a8ef04990630c8d7d | DeepSeek V3 API Key |

### 可选的 Secrets

| Key | Value | 说明 |
|-----|-------|------|
| **OPENAI_API_KEY** | 你的 OpenAI API Key | OpenAI API（可选） |
| **OPENAI_BASE_URL** | https://api.openai.com/v1 | OpenAI API 地址（可选） |

---

## 🎯 环境变量

### 在 Streamlit Cloud 中配置环境变量

如果你需要使用环境变量而不是 Secrets：

1. 进入应用设置
2. 点击"Advanced settings"
3. 在"Environment variables"中添加：

```bash
DEEPSEEK_API_KEY=sk-2f2c80b0af064d2a8ef04990630c8d7d
```

---

## 📱 部署后测试

### 测试步骤

1. **访问应用**
   - 打开应用 URL
   - 等待应用加载

2. **测试分镜生成器**
   - 切换到"📝 分镜生成器"
   - 输入创意描述
   - 点击生成
   - 验证输出结果

3. **测试分镜提示词**
   - 切换到"🧩 分镜提示词"
   - 测试手动模式
   - 测试 AI 专业模式
   - 验证输出结果

4. **测试历史记录**
   - 查看历史记录
   - 测试搜索功能

5. **测试关于页面**
   - 查看版本信息
   - 验证所有信息正确

---

## 🔍 故障排除

### 问题 1：部署失败

**可能原因**：
- 主文件路径错误
- 依赖缺失
- 代码错误

**解决方案**：
1. 检查主文件路径是否为 `app_v3.1.0_integrated.py`
2. 检查 `requirements.txt` 是否存在
3. 检查代码是否有语法错误
4. 查看部署日志

### 问题 2：API 调用失败

**可能原因**：
- API Key 未配置
- API Key 错误
- API 额度不足

**解决方案**：
1. 检查 Secrets 中是否配置了 `DEEPSEEK_API_KEY`
2. 验证 API Key 是否正确
3. 检查 API 额度是否充足

### 问题 3：应用无法启动

**可能原因**：
- 依赖冲突
- 端口冲突
- 环境不兼容

**解决方案**：
1. 检查 `requirements.txt` 是否正确
2. 查看应用日志
3. 尝试重新部署

---

## 💡 最佳实践

### 1. 版本管理

- 使用 Git 标签标记版本
- 保持 main 分支稳定
- 使用 feature 分支开发新功能

### 2. Secrets 管理

- 不要将 API Key 写在代码中
- 使用 Streamlit Secrets 管理敏感信息
- 定期更新 API Key

### 3. 日志管理

- 使用 `logging` 模块记录日志
- 设置合适的日志级别
- 避免在生产环境输出过多日志

### 4. 错误处理

- 使用 try-except 捕获异常
- 提供友好的错误信息
- 记录错误日志

---

## 📊 监控和维护

### 监控指标

- 应用访问量
- API 调用次数
- 错误率
- 响应时间

### 维护任务

- 定期更新依赖
- 监控 API 使用量
- 优化性能
- 修复 bug

---

## 📞 技术支持

### 文档

- **版本说明**：V3.1.0_发布说明_功能整合版.md
- **测试报告**：V3.1.0_测试报告.md
- **代码分析**：代码分析报告_功能重合与整合建议.md

### GitHub 仓库

https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit.git

### Streamlit Cloud 文档

https://docs.streamlit.io/streamlit-cloud/get-started

---

## 🎉 部署成功

### 部署检查清单

- [ ] 代码已推送到 GitHub
- [ ] 已在 Streamlit Cloud 创建应用
- [ ] 已配置 Secrets（DEEPSEEK_API_KEY）
- [ ] 应用已成功部署
- [ ] 应用 URL 可访问
- [ ] 所有功能测试通过

### 部署确认

**状态**：✅ 准备部署到 Streamlit Cloud

**下一步**：
1. 选择部署方式
2. 配置 Secrets
3. 部署应用
4. 测试所有功能
5. 收集用户反馈

---

**🚀 准备部署到 Streamlit Cloud！**

选择以下方式之一开始部署：
- 方法 1：通过 Streamlit Cloud 部署（推荐）
- 方法 2：通过 GitHub 部署
- 方法 3：手动推送（解决 SSH 问题）

详细步骤请参考上文！
