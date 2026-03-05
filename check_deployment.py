#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit Cloud 部署状态检查器
检查应用是否已部署在 Streamlit Cloud 上
"""

import requests
import json
from datetime import datetime

# 配置
REPO_NAME = "jinshanguzhou1021-afk/seedance-tool-streamlit"
EXPECTED_URL = "https://seedance-tool-streamlit.streamlit.app"

def check_deployment():
    """检查部署状态"""

    print("=========================================")
    print("  Streamlit Cloud 部署状态检查")
    print("=========================================")
    print("")

    print(f"📋 检查目标：{REPO_NAME}")
    print(f"🌐 预期 URL：{EXPECTED_URL}")
    print("")

    # 检查 URL 是否可访问
    print("🔍 检查应用 URL...")

    try:
        response = requests.get(EXPECTED_URL, timeout=10)

        if response.status_code == 200:
            print("✅ 应用已部署并可访问")
            print(f"   状态码：{response.status_code}")
            print(f"   URL：{EXPECTED_URL}")
            print("")

            # 检查是否是 Streamlit 应用
            content = response.text
            if 'streamlit' in content.lower() or '即梦提示词工具' in content:
                print("✅ 确认为是正确的应用")
                print("")

                # 保存部署 URL
                with open('.streamlit_deployed', 'w') as f:
                    f.write(EXPECTED_URL)

                print("=========================================")
                print("  部署状态：✅ 已部署")
                print("=========================================")
                print("")
                print("🌐 应用地址：")
                print(f"   {EXPECTED_URL}")
                print("")
                print("📊 查看部署日志：")
                print("   https://share.streamlit.io")
                print("")
                print("🔄 自动部署：")
                print("   代码更新后自动重新部署（1-3 分钟）")
                print("")

                return True
            else:
                print("⚠️  URL 可访问，但内容不匹配")
                print("   可能不是正确的应用")
                print("")
                return False
        else:
            print(f"⚠️  应用响应异常：{response.status_code}")
            print("   可能正在部署或配置错误")
            print("")
            return False

    except requests.exceptions.Timeout:
        print("⚠️  请求超时")
        print("   应用可能正在启动或网络问题")
        print("")
        return False

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到应用")
        print("   应用尚未部署或 URL 错误")
        print("")
        print("📋 首次部署步骤：")
        print("")
        print("1. 访问 Streamlit Cloud：")
        print("   https://share.streamlit.io")
        print("")
        print("2. 点击 'New app'")
        print("")
        print("3. 配置应用：")
        print(f"   Repository: {REPO_NAME}")
        print("   Branch: main")
        print("   Main file path: app.py")
        print("")
        print("4. 点击 'Deploy'")
        print("")
        print("5. 等待 1-3 分钟")
        print("")
        return False

    except Exception as e:
        print(f"❌ 检查失败：{e}")
        print("")
        return False

def main():
    """主函数"""

    deployed = check_deployment()

    if deployed:
        # 显示快捷命令
        print("=========================================")
        print("  快捷命令")
        print("=========================================")
        print("")
        print("打开应用：")
        print(f"  open {EXPECTED_URL}")
        print("")
        print("自动部署脚本：")
        print("  ./auto-deploy.sh")
        print("")
        print("检查部署状态：")
        print("  python3 check_deployment.py")
        print("")
    else:
        print("=========================================")
        print("  部署状态：⏳ 未部署")
        print("=========================================")
        print("")
        print("请按照上面的步骤进行首次部署")
        print("")

if __name__ == "__main__":
    main()
