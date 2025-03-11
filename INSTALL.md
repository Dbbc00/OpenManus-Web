# OpenManus Web 安装指南

本文档详细介绍了如何安装和配置OpenManus Web界面。

## 环境要求

- Python 3.11.9 或更高版本
- 稳定的网络连接（用于API调用）
- 现代Web浏览器（推荐使用Chrome、Firefox或Edge的最新版本）

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/OpenManus-Web.git
cd OpenManus-Web
```

### 2. 创建虚拟环境

使用conda:
```bash
conda create -n openmanus_web python=3.11.9
conda activate openmanus_web
```

或者使用venv:
```bash
python -m venv .venv
# Windows上:
.venv\Scripts\activate
# Linux/macOS上:
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

如果安装过程中出现问题，可以尝试单独安装某些可能存在问题的包:
```bash
pip install websockets
pip install fastapi uvicorn
```

### 4. 配置API密钥

1. 在`config`目录中复制示例配置文件:
```bash
cp config/config.example.toml config/config.toml
```

2. 编辑`config/config.toml`，设置您的API密钥:
```toml
[llm]
model = "gpt-4o"  # 或其他支持的模型
base_url = "https://api.openai.com/v1"
api_key = "您的OpenAI API密钥"
```

### 5. 启动Web服务

```bash
python run_web.py
```

可以使用以下命令行参数自定义启动选项:
```bash
# 指定端口
python run_web.py --port 9000

# 不自动打开浏览器
python run_web.py --no-browser

# 指定主机地址
python run_web.py --host 127.0.0.1
```

### 6. 访问Web界面

启动服务后，浏览器会自动打开`http://localhost:8000`（或您指定的端口）。

如果没有自动打开，请手动在浏览器中访问该地址。

## 常见问题

### WebSocket连接错误

如果遇到WebSocket连接问题，请确保:
1. 您已安装`websockets`库: `pip install websockets`
2. 如果使用代理或防火墙，请确保WebSocket连接未被阻止
3. 尝试使用`--host 127.0.0.1`参数启动服务

### API调用失败

如果API调用失败，请检查:
1. 您的API密钥是否正确
2. API密钥是否有足够的配额和权限
3. 您的网络连接是否正常

## 更新

要更新到最新版本，请运行:

```bash
git pull
pip install -r requirements.txt
```

## 卸载

如果需要卸载，只需删除项目目录并删除创建的虚拟环境。

```bash
# 删除虚拟环境
conda remove -n openmanus_web --all  # 如果使用conda
# 或者直接删除.venv目录（如果使用venv）

# 删除项目目录
cd ..
rm -rf OpenManus-Web
``` 