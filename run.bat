@echo off
REM Streamlit 应用启动脚本 (Windows)

echo =========================================
echo   即梦（Seedance）提示词工具
echo   Streamlit Web 应用
echo =========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python
    echo 请先安装 Python 3.8 或更高版本
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python 版本：
python --version
echo.

REM 检查 Streamlit
echo 检查 Streamlit...
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] Streamlit 未安装
    echo.
    echo 正在安装依赖...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo [错误] 安装依赖失败
        pause
        exit /b 1
    )
    echo.
    echo [OK] Streamlit 安装完成
) else (
    echo [OK] Streamlit 已安装
)
echo.

REM 创建 .streamlit 配置目录
if not exist .streamlit mkdir .streamlit

REM 启动应用
echo 启动 Streamlit 应用...
echo =========================================
echo   应用地址：http://localhost:8501
echo =========================================
echo.

streamlit run app.py --server.port=8501

REM 如果应用异常退出
if %errorlevel% neq 0 (
    echo.
    echo =========================================
    echo 应用异常退出
    echo =========================================
    echo.
    echo 故障排查：
    echo 1. 检查 Python 版本：python --version
    echo 2. 重新安装依赖：pip install -r requirements.txt
    echo 3. 查看完整错误信息
    echo.
    pause
)
