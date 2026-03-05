# 🚀 Streamlit Cloud 自动部署指南

本文档说明如何将 `seedance-tool-streamlit` 部署到 Streamlit Cloud。

---

## 📊 当前状态

| 检查项 | 状态 | 说明 |
|--------|------|------|
| **GitHub 仓库** | ✅ | https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit |
| **代码** | ✅ | 最新代码已推送 |
| **Streamlit Cloud** | ⏳ | **尚未部署**（需要手动首次配置） |

---

## 🎯 部署步骤（首次）

### 方式 1：网页部署（推荐，1 分钟完成）

#### 步骤 1：访问 Streamlit Cloud

打开浏览器，访问：
```
https://share.streamlit.io
```

#### 步骤 2：登录 GitHub

- 点击右上角 **"New app"**
- 使用 **GitHub 账号**登录

#### 步骤 3：配置应用

填写以下信息：

```
Repository:    jinshanguzhou1021-afk/seedance-tool-streamlit
Branch:        main
Main file:     app.py
Python:        3.9+ (默认即可)
```

#### 步骤 4：部署

- 点击 **"Deploy"** 按钮
- 等待 **1-3 分钟**部署完成

#### 步骤 5：访问应用

部署完成后，你会得到一个 URL：
```
https://seedance-tool-streamlit.streamlit.app
```

---

### 方式 2：使用部署脚本（自动推送）

```bash
# 进入项目目录
cd /workspace/projects/apps/seedance-tool-streamlit

# 运行自动部署脚本
./auto-deploy.sh
```

脚本会：
1. ✅ 检查代码更改
2. ✅ 自动提交
3. ✅ 推送到 GitHub
4. ✅ 检查部署状态

**注意**：首次仍需在 Streamlit Cloud 网页上手动配置应用。

---

## 🔄 自动部署（首次配置后）

### 自动重新部署

一旦在 Streamlit Cloud 上配置了应用，**每次推送到 GitHub 都会自动触发重新部署**。

### 使用自动部署脚本

```bash
cd /workspace/projects/apps/seedance-tool-streamlit

# 自动提交并推送
./auto-deploy.sh

# 检查部署状态
python3 check_deployment.py
```

### 自动部署流程

```
1. 检测代码更改
   ↓
2. 自动提交到 Git
   ↓
3. 推送到 GitHub
   ↓
4. Streamlit Cloud 自动检测到更新
   ↓
5. 自动重新部署（1-3 分钟）
   ↓
6. ✅ 部署完成
```

---

## 📋 快速命令

| 命令 | 说明 |
|------|------|
| `./auto-deploy.sh` | 自动提交并推送（触发自动部署） |
| `python3 check_deployment.py` | 检查部署状态 |
| `streamlit run app.py` | 本地运行应用 |
| `git push origin main` | 手动推送代码 |

---

## 🔍 检查部署状态

### 使用脚本检查

```bash
python3 check_deployment.py
```

输出示例：

**已部署：**
```
=========================================
  部署状态：✅ 已部署
=========================================

🌐 应用地址：
   https://seedance-tool-streamlit.streamlit.app

📊 查看部署日志：
   https://share.streamlit.io
```

**未部署：**
```
=========================================
  部署状态：⏳ 未部署
=========================================

请按照上面的步骤进行首次部署
```

### 手动检查

1. 访问应用 URL：
   ```
   https://seedance-tool-streamlit.streamlit.app
   ```

2. 如果看到应用界面 → ✅ 已部署
3. 如果看到 404 错误 → ⏳ 未部署或正在部署

---

## 🌐 访问应用

部署成功后，访问：

```
https://seedance-tool-streamlit.streamlit.app
```

---

## 📊 查看部署日志

### 方式 1：Streamlit Cloud 控制台

1. 访问：https://share.streamlit.io
2. 点击你的应用
3. 点击 "Settings" → "Logs"

### 方式 2：应用内查看

在应用页面，右上角菜单 → "Settings" → "Logs"

---

## ⚠️ 常见问题

### 问题 1：部署失败

**症状**：
```
Error: Deployment failed
```

**解决**：
1. 检查 `requirements.txt` 是否正确
2. 检查 `app.py` 语法是否正确
3. 查看部署日志了解详细错误

### 问题 2：应用无法访问（404）

**症状**：
```
404 Not Found
```

**解决**：
1. 确认已在 Streamlit Cloud 上配置了应用
2. 检查仓库名称和分支是否正确
3. 等待 1-3 分钟，可能正在部署

### 问题 3：依赖安装失败

**症状**：
```
ERROR: Could not find a version...
```

**解决**：
```bash
# 本地测试
pip install -r requirements.txt

# 如果成功，Streamlit Cloud 也会成功
```

### 问题 4：部署后功能异常

**症状**：某些功能不工作

**解决**：
1. 检查本地是否正常运行
2. 查看部署日志
3. 检查是否有硬编码的本地路径

---

## 💡 部署优化

### 1. 缩短部署时间

- 使用 `@st.cache_data` 缓存重复计算
- 减少 `requirements.txt` 中的依赖数量
- 使用 `.gitignore` 排除不必要的文件

### 2. 提升性能

- 使用 Streamlit 的缓存机制
- 优化数据库查询（如果有）
- 使用 CDN 加速静态资源

### 3. 监控部署

- 设置 GitHub Actions 监控推送
- 使用第三方工具监控可用性
- 定期检查部署日志

---

## 🎯 总结

### 部署流程

1. **首次**：手动在 Streamlit Cloud 网页配置（1 分钟）
2. **后续**：自动部署，推送即部署（1-3 分钟）

### 自动化工具

- ✅ `auto-deploy.sh` - 自动提交和推送
- ✅ `check_deployment.py` - 检查部署状态

### 关键链接

- **Streamlit Cloud**: https://share.streamlit.io
- **GitHub 仓库**: https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit
- **应用 URL**: https://seedance-tool-streamlit.streamlit.app（部署后）

---

**开始部署吧！** 🚀
