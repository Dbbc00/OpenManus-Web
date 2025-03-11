# GitHub上传清单

以下是需要上传到GitHub仓库的文件和目录清单：

## 核心文件
- [x] run_web.py (Web服务启动脚本)
- [x] requirements.txt (依赖列表)
- [x] LICENSE (MIT许可证)
- [x] README.md (项目介绍)
- [x] .gitignore (Git忽略规则)

## 文档
- [x] INSTALL.md (安装指南)
- [x] README_GITHUB.md (详细的GitHub README文件)

## 配置
- [x] config/config.example.toml (示例配置文件)
- [ ] config/config.toml (实际配置文件，**不要上传**，包含敏感信息)

## 应用代码
- [x] app/ (所有应用代码目录)
  - [x] agent/ (代理相关代码)
  - [x] flow/ (流程控制相关代码)
  - [x] llm/ (LLM接口代码)
  - [x] prompt/ (提示词模板)
  - [x] schema/ (数据模型和架构)
  - [x] tool/ (工具实现)
  - [x] web/ (Web相关代码)
    - [x] api.py (Web API实现，包含修改后的推理过程显示)

## 静态资源
- [x] static/ (静态资源目录)
  - [x] css/
    - [x] styles.css (样式文件)
  - [x] js/
    - [x] main.js (主JavaScript文件，包含修改后的实时推理显示)
  - [x] index.html (主HTML文件)

## 其他
- [x] screenshots/ (截图目录，用于README中展示)
  - [x] main_interface.jpg (主界面截图)

## 不要上传的文件
- [ ] __pycache__/ 和所有.pyc文件
- [ ] 虚拟环境目录 (.venv/, env/)
- [ ] 包含API密钥的实际配置文件
- [ ] 个人开发环境配置
- [ ] 日志文件

## 上传前检查
1. 确保所有敏感信息已从代码中移除
2. 确保示例配置文件不包含真实API密钥
3. 检查代码是否包含完整功能
4. 确保所有必要依赖都在requirements.txt中列出 