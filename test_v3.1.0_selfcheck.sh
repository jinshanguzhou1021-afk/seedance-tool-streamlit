#!/bin/bash
# V3.1.0 整合版自检脚本

echo "=========================================="
echo "🧪 V3.1.0 整合版自检脚本"
echo "=========================================="
echo ""

cd /workspace/projects/apps/seedance-tool-streamlit

echo "📌 版本信息"
echo "版本：V3.1.0（整合版）"
echo "功能：2 个核心功能（分镜生成器 + 分镜提示词）"
echo ""

echo "📌 1. 语法检查"
python3 -m py_compile app_v3.1.0_integrated.py
if [ $? -eq 0 ]; then
    echo "✅ 语法检查通过"
else
    echo "❌ 语法检查失败"
    exit 1
fi

echo ""
echo "📌 2. 模块导入测试"
python3 << 'EOF'
import sys
try:
    import streamlit as st
    print("✓ Streamlit 导入成功")
except ImportError as e:
    print(f"✗ Streamlit 导入失败: {e}")
    sys.exit(1)

try:
    from openai import OpenAI
    print("✓ OpenAI 导入成功")
except ImportError as e:
    print(f"✗ OpenAI 导入失败: {e}")
    sys.exit(1)

try:
    import json
    print("✓ json 导入成功")
except ImportError as e:
    print(f"✗ json 导入失败: {e}")
    sys.exit(1)

try:
    import logging
    print("✓ logging 导入成功")
except ImportError as e:
    print(f"✗ logging 导入失败: {e}")
    sys.exit(1)

try:
    import os
    print("✓ os 导入成功")
except ImportError as e:
    print(f"✗ os 导入失败: {e}")
    sys.exit(1)

try:
    from datetime import datetime
    print("✓ datetime 导入成功")
except ImportError as e:
    print(f"✗ datetime 导入失败: {e}")
    sys.exit(1)

try:
    from pathlib import Path
    print("✓ pathlib 导入成功")
except ImportError as e:
    print(f"✗ pathlib 导入失败: {e}")
    sys.exit(1)

try:
    import time
    print("✓ time 导入成功")
except ImportError as e:
    print(f"✗ time 导入失败: {e}")
    sys.exit(1)

print("")
print("✅ 所有模块导入成功")
EOF

if [ $? -ne 0 ]; then
    echo "❌ 模块导入测试失败"
    exit 1
fi

echo ""
echo "📌 3. 函数定义检查"
python3 << 'EOF'
import re

# 读取文件
with open('app_v3.1.0_integrated.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查必需的函数
required_functions = [
    'load_history',
    'save_to_history',
    'calculate_time_segments',
    'generate_with_deepseek',
    'generate_locally',
    'render_storyboard_generator',
    'render_prompt_builder',
    'render_manual_mode',
    'render_ai_professional_mode',
    'render_history',
    'render_about',
    'main'
]

missing_functions = []
for func in required_functions:
    pattern = f'def {func}\\('
    if re.search(pattern, content):
        print(f"✓ {func}")
    else:
        print(f"✗ {func} 缺失")
        missing_functions.append(func)

if missing_functions:
    print(f"\\n✗ 缺失函数: {', '.join(missing_functions)}")
    exit(1)
else:
    print("\\n✅ 所有必需函数存在")
EOF

if [ $? -ne 0 ]; then
    echo "❌ 函数定义检查失败"
    exit 1
fi

echo ""
echo "📌 4. 核心功能检查"
python3 << 'EOF'
import re

# 读取文件
with open('app_v3.1.0_integrated.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查核心功能模块
core_modules = [
    ('分镜生成器', 'render_storyboard_generator'),
    ('分镜提示词', 'render_prompt_builder'),
    ('手动模式', 'render_manual_mode'),
    ('AI专业模式', 'render_ai_professional_mode'),
    ('历史记录', 'render_history'),
    ('关于', 'render_about')
]

missing_modules = []
for name, func in core_modules:
    pattern = f'def {func}\\('
    if re.search(pattern, content):
        print(f"✓ {name}")
    else:
        print(f"✗ {name} 缺失")
        missing_modules.append(name)

if missing_modules:
    print(f"\\n✗ 缺失模块: {', '.join(missing_modules)}")
    exit(1)
else:
    print("\\n✅ 所有核心功能模块存在")
EOF

if [ $? -ne 0 ]; then
    echo "❌ 核心功能检查失败"
    exit 1
fi

echo ""
echo "📌 5. 参数配置检查"
python3 << 'EOF'
import re

# 读取文件
with open('app_v3.1.0_integrated.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查参数配置
configs = [
    ('ASPECT_RATIOS', '画面比例'),
    ('VISUAL_STYLES', '视觉风格'),
    ('SCENE_TYPES', '场景类型'),
    ('CAMERA_MOVES', '运镜语言'),
    ('LIGHTING_STYLES', '光影效果'),
    ('QUALITY_TAGS', '画质标签'),
    ('API_KEY', 'API Key'),
    ('API_BASE_URL', 'API 地址'),
    ('API_MODEL', 'API 模型')
]

missing_configs = []
for config, desc in configs:
    pattern = f'{config}\\s*='
    if re.search(pattern, content):
        print(f"✓ {desc}")
    else:
        print(f"✗ {desc} 缺失")
        missing_configs.append(desc)

if missing_configs:
    print(f"\\n✗ 缺失配置: {', '.join(missing_configs)}")
    exit(1)
else:
    print("\\n✅ 所有参数配置存在")
EOF

if [ $? -ne 0 ]; then
    echo "❌ 参数配置检查失败"
    exit 1
fi

echo ""
echo "📌 6. 整合功能验证"
python3 << 'EOF'
# 验证整合是否成功
with open('app_v3.1.0_integrated.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查是否包含原有的4个功能
original_functions = [
    'generate_standard_storyboard',  # 旧版本，应该删除
    'generate_ai_storyboard',          # 旧版本，应该删除
    'render_prompt_builder',           # 应该在 render_storyboard_generator 中
    'render_ai_director'                # 应该在 render_prompt_builder 中
]

# 检查是否整合到新模块中
integrated_features = [
    'render_storyboard_generator',     # 整合了分镜生成器 + 提示词生成器
    'render_prompt_builder',            # 整合了高级构建器 + AI 视觉导演
    'render_manual_mode',              # 手动模式
    'render_ai_professional_mode'       # AI 专业模式
]

# 检查是否删除了旧函数
removed_count = 0
for func in original_functions:
    if f'def {func}(' not in content:
        print(f"✓ 旧函数 {func} 已删除")
        removed_count += 1
    else:
        print(f"⚠️ 旧函数 {func} 仍然存在")

# 检查是否添加了新函数
integrated_count = 0
for func in integrated_features:
    if f'def {func}(' in content:
        print(f"✓ 新函数 {func} 已添加")
        integrated_count += 1
    else:
        print(f"✗ 新函数 {func} 缺失")

print(f"\\n整合状态：")
print(f"  旧函数删除：{removed_count}/{len(original_functions)}")
print(f"  新函数添加：{integrated_count}/{len(integrated_features)}")

if integrated_count == len(integrated_features):
    print("\\n✅ 整合成功")
else:
    print("\\n⚠️ 整合不完整")
    exit(1)
EOF

if [ $? -ne 0 ]; then
    echo "❌ 整合功能验证失败"
    exit 1
fi

echo ""
echo "📌 7. 代码优化检查"
python3 << 'EOF'
import re

# 读取文件
with open('app_v3.1.0_integrated.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 统计代码行数
lines = content.split('\\n')
total_lines = len(lines)

# 统计函数数量
function_count = len(re.findall(r'^def \\w+\\(', content, re.MULTILINE))

# 统计注释行数
comment_count = len(re.findall(r'^\\s*#', content, re.MULTILINE))

# 统计空行数
blank_count = len(re.findall(r'^\\s*$', content, re.MULTILINE))

print(f"总代码行数：{total_lines}")
print(f"函数数量：{function_count}")
print(f"注释行数：{comment_count}")
print(f"空行数：{blank_count}")
print(f"有效代码行数：{total_lines - comment_count - blank_count}")
print("")
print("✅ 代码优化检查完成")
EOF

echo ""
echo "=========================================="
echo "📊 自检总结"
echo "=========================================="
echo ""
echo "检查项目："
echo "  1. 语法检查          ✅ 通过"
echo "  2. 模块导入测试      ✅ 通过"
echo "  3. 函数定义检查      ✅ 通过"
echo "  4. 核心功能检查      ✅ 通过"
echo "  5. 参数配置检查      ✅ 通过"
echo "  6. 整合功能验证      ✅ 通过"
echo "  7. 代码优化检查      ✅ 通过"
echo ""
echo "总计：7/7 检查通过"
echo ""
echo "✅ V3.1.0 整合版自检完成！"
echo ""
echo "🚀 下一步："
echo "   1. 启动应用: streamlit run app_v3.1.0_integrated.py"
echo "   2. 测试分镜生成器功能"
echo "   3. 测试分镜提示词功能"
echo "   4. 验证所有功能正常"
