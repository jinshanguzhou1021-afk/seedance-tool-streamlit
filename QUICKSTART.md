# 🚀 快速开始指南

5 分钟快速上手即梦提示词工具 Streamlit 版本。

---

## 步骤 1：检查环境（30秒）

```bash
# 进入项目目录
cd seedance-tool-streamlit

# 运行环境测试
python3 test_env.py
```

确保所有测试都通过 ✅

---

## 步骤 2：安装依赖（1分钟）

```bash
# 方式 A：使用启动脚本（自动安装）
bash run.sh    # Linux/Mac
# 或
run.bat       # Windows

# 方式 B：手动安装
pip3 install -r requirements.txt
```

---

## 步骤 3：启动应用（10秒）

```bash
# 方式 A：使用启动脚本
bash run.sh    # Linux/Mac
run.bat       # Windows

# 方式 B：直接启动
streamlit run app.py
```

应用会自动打开浏览器，访问：**http://localhost:8501**

---

## 步骤 4：使用应用（2分钟）

### 使用分镜生成器

1. 点击侧边栏的"📝 分镜生成器"
2. 在"创意描述"框中输入：
   ```
   仙侠战斗，主角持剑迎战魔兵
   ```
3. 设置参数：
   - 视频时长：15秒
   - 画面比例：16:9 横屏
   - 视觉风格：仙侠奇幻
4. 点击"🎬 生成分镜"
5. 查看结果，点击"💾 下载提示词"

### 使用提示词生成器

1. 点击侧边栏的"⚡ 提示词生成器"
2. 选择场景类型：剧情/对话
3. 在"场景描述"框中输入：
   ```
   男女主角在夕阳下对视，准备表白
   ```
4. 设置参数：
   - 视频时长：10秒
   - 画面比例：16:9 横屏
   - 生成版本数：3个
5. 点击"🚀 生成提示词"
6. 查看多个版本，选择最佳的，点击"💾 下载所有版本"

---

## 步骤 5：查看历史记录（可选）

1. 点击侧边栏的"📚 历史记录"
2. 查看所有生成的记录
3. 使用搜索框查找特定的记录

---

## 🌐 部署到 Streamlit Cloud（可选）

### 1. 准备代码

```bash
# 初始化 Git 仓库（如果还没有）
git init
git add .
git commit -m "Initial commit"

# 连接到 GitHub
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

### 2. 部署到 Streamlit Cloud

1. 访问 https://share.streamlit.io
2. 点击"New app"
3. 连接 GitHub 账号
4. 选择仓库
5. 设置主文件路径：`app.py`
6. 点击"Deploy"

### 3. 访问应用

部署完成后，你会得到一个类似这样的 URL：
```
https://your-app.streamlit.app
```

---

## 🎨 自定义主题（可选）

编辑 `.streamlit/config.toml`：

```toml
[theme]
primaryColor = "#1f77b4"              # 主色调
backgroundColor = "#ffffff"           # 背景色
secondaryBackgroundColor = "#f0f2f6" # 次要背景色
textColor = "#262730"                # 文字颜色
```

---

## 📱 使用手机访问

如果你在本地运行应用：

1. 确保手机和电脑在同一网络
2. 查看电脑的 IP 地址：
   ```bash
   # macOS/Linux:
   ifconfig | grep "inet "

   # Windows:
   ipconfig
   ```
3. 在手机浏览器访问：
   ```
   http://<电脑IP>:8501
   ```

---

## 💡 常用命令

```bash
# 启动应用
streamlit run app.py

# 指定端口
streamlit run app.py --server.port=8502

# 开启调试模式
streamlit run app.py --logger.level=debug

# 重新加载文件（自动监听文件变化）
streamlit run app.py --server.fileWatcherType=auto

# 运行环境测试
python3 test_env.py
```

---

## 🐛 遇到问题？

### 应用无法启动

```bash
# 运行环境测试
python3 test_env.py

# 重新安装依赖
pip3 install --upgrade -r requirements.txt
```

### 端口被占用

```bash
# 使用其他端口
streamlit run app.py --server.port=8502
```

### 页面显示异常

1. 清除浏览器缓存
2. 使用无痕模式
3. 更新浏览器版本

---

## 📚 更多信息

- 完整文档：查看 [README.md](README.md)
- Streamlit 文档：https://docs.streamlit.io
- Seedance 平台：https://jimeng.jianying.com

---

**开始使用即梦提示词工具，快速生成高质量的视频提示词！** 🚀
