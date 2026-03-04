#!/usr/bin/env python3
"""
环境测试脚本 - 验证应用运行环境
"""

import sys
import os

def test_python_version():
    """测试 Python 版本"""
    print("=" * 50)
    print("Python 版本测试")
    print("=" * 50)

    version = sys.version_info
    print(f"Python 版本：{version.major}.{version.minor}.{version.micro}")

    if version.major >= 3 and version.minor >= 8:
        print("✓ Python 版本符合要求 (≥ 3.8)")
        return True
    else:
        print("✗ Python 版本过低（需要 ≥ 3.8）")
        print("请升级 Python：https://www.python.org/downloads/")
        return False

def test_streamlit():
    """测试 Streamlit 安装"""
    print("\n" + "=" * 50)
    print("Streamlit 测试")
    print("=" * 50)

    try:
        import streamlit
        print(f"✓ Streamlit 已安装 (版本: {streamlit.__version__})")
        print("  安装位置：", streamlit.__file__)

        # 检查版本
        version_parts = streamlit.__version__.split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1]) if len(version_parts) > 1 else 0

        if major > 1 or (major == 1 and minor >= 28):
            print("✓ Streamlit 版本符合要求 (≥ 1.28)")
            return True
        else:
            print("✗ Streamlit 版本过低（需要 ≥ 1.28）")
            print("请升级：pip install --upgrade streamlit")
            return False
    except ImportError:
        print("✗ Streamlit 未安装")
        print("安装命令：pip install streamlit")
        return False

def test_app_file():
    """测试应用文件"""
    print("\n" + "=" * 50)
    print("应用文件测试")
    print("=" * 50)

    if os.path.exists("app.py"):
        print("✓ app.py 文件存在")

        # 检查文件大小
        size = os.path.getsize("app.py")
        print(f"  文件大小：{size} 字节 ({size/1024:.1f} KB)")

        # 检查是否可以导入
        try:
            # 尝试导入（不执行）
            import ast
            with open("app.py", 'r', encoding='utf-8') as f:
                ast.parse(f.read())
            print("✓ app.py 语法正确")
            return True
        except SyntaxError as e:
            print(f"✗ app.py 语法错误：{e}")
            return False
    else:
        print("✗ app.py 文件不存在")
        return False

def test_config():
    """测试配置文件"""
    print("\n" + "=" * 50)
    print("配置文件测试")
    print("=" * 50)

    # 测试 .streamlit 目录
    if os.path.exists(".streamlit"):
        print("✓ .streamlit 目录存在")
    else:
        print("○ .streamlit 目录不存在（将在运行时创建）")

    # 测试 config.toml
    if os.path.exists(".streamlit/config.toml"):
        print("✓ config.toml 文件存在")
        try:
            import tomli
            print("  注意：tomli 未安装，无法验证配置")
        except ImportError:
            print("  配置文件存在（跳过验证）")
    else:
        print("○ config.toml 文件不存在（使用默认配置）")

    return True

def test_history_file():
    """测试历史记录文件"""
    print("\n" + "=" * 50)
    print("历史记录测试")
    print("=" * 50)

    from pathlib import Path
    history_file = Path.home() / ".seedance_streamlit_history.json"

    if history_file.exists():
        print(f"✓ 历史记录文件存在：{history_file}")

        # 检查文件大小
        size = history_file.stat().st_size
        print(f"  文件大小：{size} 字节 ({size/1024:.1f} KB)")

        # 尝试读取
        try:
            import json
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            print(f"✓ 历史记录文件可读（{len(history)} 条记录）")
        except Exception as e:
            print(f"✗ 历史记录文件读取失败：{e}")
            return False
    else:
        print("○ 历史记录文件不存在（将在首次运行时创建）")

    return True

def test_network():
    """测试网络连接"""
    print("\n" + "=" * 50)
    print("网络连接测试")
    print("=" * 50)

    import socket

    try:
        # 测试连接到 Streamlit
        socket.create_connection(("streamlit.io", 443), timeout=5)
        print("✓ 可以连接到 Streamlit.io")
        return True
    except Exception as e:
        print(f"⚠️ 无法连接到 Streamlit.io：{e}")
        print("  注意：应用仍可离线运行，但无法访问在线资源")
        return False

def test_port_availability():
    """测试端口可用性"""
    print("\n" + "=" * 50)
    print("端口可用性测试")
    print("=" * 50)

    import socket

    port = 8501
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.bind(('localhost', port))
        print(f"✓ 端口 {port} 可用")
        sock.close()
        return True
    except OSError:
        print(f"✗ 端口 {port} 已被占用")
        print("  解决方案：")
        print("  1. 停止占用端口的进程")
        print("  2. 使用其他端口：streamlit run app.py --server.port=8502")
        return False
    finally:
        sock.close()

def main():
    """主函数"""
    print("\n")
    print("╔═══════════════════════════════════════════╗")
    print("║   即梦提示词工具 - 环境测试脚本             ║")
    print("╚═══════════════════════════════════════════╝")
    print("\n")

    results = []

    # 运行测试
    results.append(("Python 版本", test_python_version()))
    results.append(("Streamlit", test_streamlit()))
    results.append(("应用文件", test_app_file()))
    results.append(("配置文件", test_config()))
    results.append(("历史记录", test_history_file()))
    results.append(("网络连接", test_network()))
    results.append(("端口可用", test_port_availability()))

    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:.<30} {status}")

    print(f"\n总计：{passed}/{total} 测试通过")

    if passed == total:
        print("\n✅ 所有测试通过！环境配置正确。")
        print("\n启动应用：")
        print("  bash run.sh (Linux/Mac)")
        print("  run.bat (Windows)")
        print("  streamlit run app.py (直接启动）")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查上述错误。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
