# 即梦提示词工具 - Streamlit 版本

## ✅ 已创建完成！

所有文件已成功创建到：
```
/workspace/projects/apps/seedance-tool-streamlit/
```

---

## 📁 文件清单

| 文件/目录 | 说明 | 大小 |
|-----------|------|------|
| `app.py` | **主程序**（Streamlit Web 应用） | 15 KB |
| `requirements.txt` | Python 依赖列表 | 75 B |
| `run.sh` | Linux/Mac 启动脚本 | 1.2 KB |
| `run.bat` | Windows 启动脚本 | 1.4 KB |
| `test_env.py` | 环境测试脚本 | 5.7 KB |
| `deploy.sh` | Streamlit Cloud 部署脚本 | 1.7 KB |
| `README.md` | 完整使用文档 | 5.9 KB |
| `QUICKSTART.md` | 快速开始指南 | 2.5 KB |
| `.gitignore` | Git 忽略文件 | 211 B |
| `.streamlit/` | Streamlit 配置目录 | - |
| `.streamlit/config.toml` | Streamlit 配置文件 | 319 B |

---

## 🎯 功能特性

### ✅ 分镜生成器
- 创意描述输入
- 智能时间轴分段
- 多种视觉风格
- 参考素材支持
- 一键下载

### ✅ 提示词生成器
- 7种场景类型
- 1-5个版本生成
- 智能音效设计
- 版本对比查看
- 批量下载

### ✅ 历史记录
- 自动保存
- 关键词搜索
- 详细查看
- 一键清除

### ✅ 其他功能
- 响应式设计
- 实时预览
- 无需刷新
- 离线可用
- 数据本地存储

---

## 🚀 快速开始

### 方式 1：使用启动脚本（推荐）

```bash
cd /workspace/projects/apps/seedance-tool-streamlit

# Linux/Mac
bash run.sh

# Windows
run.bat
```

### 方式 2：直接启动

```bash
cd /workspace/projects/apps/seedance-tool-streamlit
streamlit run app.py
```

### 方式 3：使用虚拟环境

```bash
cd /workspace/projects/apps/seedance-tool-streamlit

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run app.py
```

---

## 🌐 访问应用

启动后，应用会自动打开浏览器，访问：

**本地地址：**
- http://localhost:8501

**局域网访问：**
- 查看电脑 IP 地址
- 在手机/其他设备访问：`http://<电脑IP>:8501`

---

## 📊 环境测试结果

✅ **所有测试通过！**

| 测试项 | 状态 |
|-------|------|
| Python 版本 (3.12.3) | ✅ 通过 |
| Streamlit (1.55.0) | ✅ 通过 |
| 应用文件 | ✅ 通过 |
| 配置文件 | ✅ 通过 |
| 历史记录 | ✅ 通过 |
| 网络连接 | ✅ 通过 |
| 端口可用 (8501) | ✅ 通过 |

---

## 🎨 界面预览

```
╔════════════════════════════════════════════════════╗
║  🎬 即梦提示词工具                         [⚙️] ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║  侧边栏              主内容区域                    ║
║  ┌────────────┐      ┌──────────────────────────┐    ║
║  │  选择功能  │      │                          │    ║
║  │            │      │  [输入设置]  [生成结果]  │    ║
║  │ • 分镜    │      │                          │    ║
║  │ • 提示词  │      │  文本框    生成的提示词  │    ║
║  │ • 历史    │      │  滑块                    │    ║
║  │ • 关于    │      │  下拉框                  │    ║
║  │            │      │  按钮                    │    ║
║  └────────────┘      │                          │    ║
║  ┌────────────┐      └──────────────────────────┘    ║
║  │  📊 统计  │                                       ║
║  │  总生成：0│                                       ║
║  │  分镜：0  │                                       ║
║  │  提示词：0│                                       ║
║  └────────────┘                                       ║
╚════════════════════════════════════════════════════╝
```

---

## 📖 使用文档

- **快速开始：** 查看 [QUICKSTART.md](QUICKSTART.md)
- **完整文档：** 查看 [README.md](README.md)

---

## 🌐 部署到 Streamlit Cloud

### 方法 1：使用部署脚本

```bash
cd /workspace/projects/apps/seedance-tool-streamlit
bash deploy.sh
```

### 方法 2：手动部署

```bash
# 1. 初始化 Git 仓库
git init
git add .
git commit -m "Initial commit"

# 2. 连接到 GitHub
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main

# 3. 访问 Streamlit Cloud
# https://share.streamlit.io
# 点击 "New app"，选择仓库，设置主文件为 app.py
```

---

## 🛠️ 常用命令

```bash
# 运行环境测试
python3 test_env.py

# 启动应用
streamlit run app.py

# 指定端口
streamlit run app.py --server.port=8502

# 开启调试模式
streamlit run app.py --logger.level=debug

# 清除缓存
streamlit cache clear

# 查看所有命令
streamlit --help
```

---

## 🎯 下一步

### 你想要：

1. **立即使用** - 运行 `bash run.sh` 启动应用
2. **部署到云端** - 查看 `QUICKSTART.md` 的部署章节
3. **自定义界面** - 编辑 `.streamlit/config.toml`
4. **添加新功能** - 修改 `app.py` 添加新功能
5. **查看示例** - 在浏览器中打开应用试用

---

## 💡 使用建议

### 新手建议

1. **先本地测试** - 在本地运行应用，熟悉功能
2. **使用示例** - 查看文档中的示例输入
3. **尝试多版本** - 提示词生成器尝试生成多个版本
4. **保存历史** - 保存好的提示词，方便复用

### 进阶建议

1. **自定义主题** - 修改 `config.toml` 调整颜色
2. **部署到云端** - 使用 Streamlit Cloud 免费托管
3. **添加 AI 增强** - 集成 OpenAI API 提升质量
4. **批量处理** - 添加批量生成功能

---

## 📞 获取帮助

遇到问题？

1. **查看文档**
   - [QUICKSTART.md](QUICKSTART.md) - 快速开始
   - [README.md](README.md) - 完整文档

2. **运行测试**
   ```bash
   python3 test_env.py
   ```

3. **查看日志**
   - Streamlit 日志在终端输出
   - 检查错误信息

---

## 🎉 开始使用

立即启动应用：

```bash
cd /workspace/projects/apps/seedance-tool-streamlit
bash run.sh
```

浏览器会自动打开，访问：**http://localhost:8501**

---

**开始使用即梦提示词工具，快速生成高质量的视频提示词！** 🚀
