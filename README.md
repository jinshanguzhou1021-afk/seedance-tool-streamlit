# 即梦（Seedance）提示词工具 - Streamlit Web 应用

一个功能强大的 Web 应用，帮助你快速生成 Seedance 2.0（即梦）的视频提示词和分镜描述。

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

## 🚀 在线演示

如果你已经有 Streamlit Cloud 账号，可以在线体验：
[点击访问在线演示](https://your-app.streamlit.app)

---

## 🎯 功能特性

### 1. 分镜生成器 📝
- ✅ 创意描述输入
- ✅ 智能时间轴分段（根据时长自动计算）
- ✅ 多种视觉风格（电影感、赛博朋克、仙侠等）
- ✅ 画面比例选择（横屏/竖屏/电影宽屏）
- ✅ 参考素材支持（@图片1、@视频1等）
- ✅ 一键下载提示词

### 2. 提示词生成器 ⚡
- ✅ 多种场景类型（动作、剧情、广告等）
- ✅ 一键生成多个版本（1-5个）
- ✅ 智能时间轴分配
- ✅ 自动添加音效设计建议
- ✅ 版本对比查看
- ✅ 批量下载所有版本

### 3. 历史记录管理 📚
- ✅ 自动保存所有生成记录
- ✅ 关键词搜索
- ✅ 详细查看历史
- ✅ 一键清除历史

### 4. 其他功能
- ✅ 响应式设计（支持手机/平板/电脑）
- ✅ 实时预览
- ✅ 无需刷新页面
- ✅ 本地数据存储
- ✅ 离线使用（模板模式）

---

## 📦 安装与运行

### 方法 1：直接运行（推荐）

```bash
# 1. 进入项目目录
cd seedance-tool-streamlit

# 2. 运行启动脚本
bash run.sh
```

应用将自动打开浏览器：http://localhost:8501

---

### 方法 2：手动安装

#### 步骤 1：安装 Python

确保你安装了 Python 3.8 或更高版本：

```bash
python3 --version
```

#### 步骤 2：安装依赖

```bash
pip3 install -r requirements.txt
```

#### 步骤 3：运行应用

```bash
streamlit run app.py
```

---

### 方法 3：使用虚拟环境（推荐）

```bash
# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行应用
streamlit run app.py
```

---

## 📖 使用指南

### 分镜生成器

#### 步骤 1：输入创意描述

在文本框中输入你的视频创意：

```
例如：仙侠战斗，主角持剑迎战魔兵
```

#### 步骤 2：设置参数

- **视频时长：** 拖动滑块选择 4-15 秒
- **画面比例：** 选择横屏/竖屏/电影宽屏
- **视觉风格：** 选择电影感、赛博朋克、仙侠奇幻等
- **参考素材：** 如果有图/视频参考，可填写（例如：@图片1 人物图）

#### 步骤 3：生成分镜

点击"🎬 生成分镜"按钮，系统会自动生成：
- 时间轴分段（根据时长智能分配）
- 镜头语言（推、拉、环绕等）
- 参考素材标注

#### 步骤 4：使用结果

- 查看生成的提示词
- 点击"💾 下载提示词"保存为文件
- 直接复制文本到 Seedance 2.0 平台

---

### 提示词生成器

#### 步骤 1：选择场景类型

从下拉菜单选择：
- 动作/打斗
- 剧情/对话
- 商业广告
- 风景/环境
- 产品展示
- 奇幻/仙侠
- 科幻/未来

#### 步骤 2：输入场景描述

详细描述视频内容：

```
例如：男女主角在夕阳下对视，准备表白
```

#### 步骤 3：设置参数

- **视频时长：** 4-15 秒
- **画面比例：** 横屏/竖屏
- **生成版本数：** 1-5 个（生成多个不同风格的版本）
- **参考素材：** 可选

#### 步骤 4：生成提示词

点击"🚀 生成提示词"按钮，系统会：
- 生成多个版本的提示词
- 每个版本有不同的风格
- 自动添加音效设计建议

#### 步骤 5：对比选择

- 使用标签页查看不同版本
- 选择最符合需求的版本
- 点击"💾 下载所有版本"保存

---

### 历史记录

#### 查看历史

1. 点击侧边栏的"📚 历史记录"
2. 所有生成记录按时间倒序显示
3. 点击展开查看详情

#### 搜索历史

1. 在搜索框输入关键词
2. 系统自动过滤相关记录
3. 支持搜索输入和输出内容

#### 清除历史

1. 点击"🗑️ 清除所有历史记录"
2. 确认操作
3. 所有历史记录将被删除

---

## 📝 示例

### 示例 1：分镜生成

**输入：**
```
仙侠战斗，主角持剑迎战魔兵
```

**参数：**
- 时长：15秒
- 比例：16:9 横屏
- 风格：仙侠奇幻

**输出：**
```
15秒仙侠奇幻视频，16:9 横屏。

时间轴：
- 0-5秒：仙侠战斗，主角持剑迎战魔兵，镜头缓慢推近
- 5-10秒：仙侠战斗，主角持剑迎战魔兵的发展，环绕拍摄
- 10-15秒：仙侠战斗，主角持剑迎战魔兵的高潮，镜头拉远定格
```

---

### 示例 2：提示词生成

**输入：**
```
男女主角在夕阳下对视，准备表白
```

**参数：**
- 类型：剧情/对话
- 时长：10秒
- 版本数：3个

**版本 1（标准版）：**
```
10秒剧情/对话场景，标准版风格，16:9 横屏。

时间轴：
- 0-5秒：男女主角在夕阳下对视，准备表白的引入，特写
- 5-10秒：男女主角在夕阳下对视，准备表白的高潮，拉远定格

音效设计：
- 背景音乐：根据场景类型调整
- 音效：环境音、动作音效
```

**版本 2（更具创意）：**
```
10秒剧情/对话场景，更具创意风格，16:9 横屏。

时间轴：
- 0-5秒：男女主角在夕阳下对视，准备表白的引入，特写
- 5-10秒：男女主角在夕阳下对视，准备表白的高潮，拉远定格

音效设计：
- 背景音乐：根据场景类型调整
- 音效：环境音、动作音效
```

**版本 3（简洁高效）：**
```
10秒剧情/对话场景，简洁高效风格，16:9 横屏。

时间轴：
- 0-5秒：男女主角在夕阳下对视，准备表白的引入，特写
- 5-10秒：男女主角在夕阳下对视，准备表白的高潮，拉远定格

音效设计：
- 背景音乐：根据场景类型调整
- 音效：环境音、动作音效
```

---

## 🌐 部署到 Streamlit Cloud

### 步骤 1：准备代码

将代码上传到 GitHub：
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/seedance-tool.git
git push -u origin main
```

### 步骤 2：连接到 Streamlit Cloud

1. 访问 https://share.streamlit.io
2. 点击"New app"
3. 连接你的 GitHub 账号
4. 选择仓库和分支
5. 设置主文件路径：`app.py`

### 步骤 3：部署

点击"Deploy"按钮，Streamlit Cloud 会自动部署。

### 步骤 4：访问应用

部署完成后，你会得到一个类似这样的 URL：
```
https://your-app.streamlit.app
```

---

## 🎨 自定义配置

### 修改主题

在 `.streamlit/config.toml` 文件中配置主题：

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### 修改端口

```bash
streamlit run app.py --server.port=8502
```

### 开启调试模式

```bash
streamlit run app.py --logger.level=debug
```

---

## 🔧 配置文件

### 历史记录位置

历史记录保存在用户主目录：
- Windows: `C:\Users\<用户名>\.seedance_streamlit_history.json`
- macOS: `/Users/<用户名>/.seedance_streamlit_history.json`
- Linux: `/home/<用户名>/.seedance_streamlit_history.json`

### Streamlit 配置

配置文件：`.streamlit/config.toml`

---

## 🐛 故障排查

### 问题：无法启动应用

**错误信息：**
```
ModuleNotFoundError: No module named 'streamlit'
```

**解决方案：**
```bash
pip3 install -r requirements.txt
```

---

### 问题：端口被占用

**错误信息：**
```
OSError: [Errno 48] Address already in use
```

**解决方案：**
```bash
# 方案 1：使用其他端口
streamlit run app.py --server.port=8502

# 方案 2：停止占用端口的进程
# macOS/Linux:
lsof -ti:8501 | xargs kill
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

---

### 问题：历史记录无法保存

**解决方案：**
- 检查文件权限
- 确保目录存在
- 查看浏览器控制台错误信息

---

## 📚 技术文档

### 项目结构

```
seedance-tool-streamlit/
├── app.py                  # 主程序（Streamlit 应用）
├── requirements.txt         # Python 依赖
├── run.sh                 # 启动脚本
├── README.md              # 本文件
└── .streamlit/            # Streamlit 配置目录
    └── config.toml        # 配置文件（可选）
```

### 核心功能

**分镜生成：**
- `calculate_time_segments()` - 计算时间轴分段
- 智能分配镜头语言
- 自动添加参考素材标注

**提示词生成：**
- 多版本生成算法
- 风格差异化
- 音效设计建议

**历史管理：**
- JSON 格式存储
- 关键词搜索
- 自动保存/加载

---

## 🚀 性能优化

### 使用缓存

Streamlit 自动缓存函数结果，提升性能：

```python
@st.cache_data
def expensive_function(param):
    # 缓存结果
    return result
```

### 减少重运行

使用 `st.session_state` 避免不必要的重运行：

```python
if 'data' not in st.session_state:
    st.session_state.data = load_data()
```

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📞 支持

如有问题，请：
1. 查看本文档
2. 检查 [常见问题](#故障排查)
3. 提交 Issue

---

## 🎉 更新日志

### v1.0.0 (2026-03-04)
- ✅ 初始版本发布
- ✅ 分镜生成器功能
- ✅ 提示词生成器功能
- ✅ 历史记录管理
- ✅ 多版本生成
- ✅ 一键下载
- ✅ 响应式设计

---

## 🙏 致谢

- [Streamlit](https://streamlit.io) - Web 应用框架
- [Seedance 2.0](https://jimeng.jianying.com) - AI 视频生成平台

---

**开始使用即梦提示词工具，快速生成高质量的视频提示词！** 🚀
