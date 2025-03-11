# OpenManus Web

OpenManus Web是一个现代化的AI交互界面，将强大的OpenManus框架带入浏览器，创造类似ChatGPT的用户体验，同时提供独特的AI思考过程可视化功能。

## 项目亮点

✨ **全新的用户体验**：精心设计的界面让AI交互变得简单直观，支持历史记录管理和会话保存

🔍 **实时思考过程展示**：独特的实时推理功能让您能够"看见"AI的思考步骤，不再是黑盒操作

🔄 **WebSocket实时通信**：基于WebSocket的流式输出，实现无缝交互体验

⚙️ **丰富的自定义选项**：可配置的设置菜单，让您控制界面行为和显示偏好

📱 **全设备兼容**：响应式设计确保在桌面和移动设备上都有出色表现

## 技术特色

本项目基于OpenManus框架构建，将复杂的AI能力通过现代Web技术呈现：

- **前端**：原生JavaScript和CSS3实现流畅交互，无需框架依赖
- **后端**：基于FastAPI和WebSocket的高性能服务
- **AI能力**：完整继承OpenManus的多工具、多步骤处理能力
- **实时推理**：创新的推理捕获和流式显示技术

## 为谁打造？

- **AI开发者**：希望理解和调试AI思考过程的开发人员
- **教育工作者**：展示AI如何解决问题的教学工具
- **技术爱好者**：想要部署私人AI助手又需要更好界面的用户
- **研究人员**：需要记录和分析AI推理步骤的学者

## 开发背景

OpenManus Web界面由李璇开发，旨在为OpenManus框架提供一个易用的Web访问层，让更多人能够体验这一强大的开源AI代理平台，同时提供独特的AI思考过程可视化功能，增强AI应用的透明度和可解释性。

## 截图展示

![image](https://github.com/user-attachments/assets/96ef5bd1-12e6-4975-838e-422e76caed94)


## 安装指南

1. 克隆仓库:
```bash
git clone https://github.com/Dbbc00/OpenManus-Web.git
cd OpenManus-Web


2. 安装依赖:
```bash
pip install -r requirements.txt
```

3. 配置API密钥:
在`config/config.example.toml`中添加您的OpenAI API密钥:
```toml
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "你的API密钥"
```

4. 启动Web服务:
```bash
python run_web.py
```

5. 访问Web界面:
在浏览器中打开 http://localhost:8000

## 显示推理过程

OpenManus Web界面的一个独特特性是能够显示AI的实时推理过程:

1. 在右下角点击"设置"按钮
2. 开启"显示推理过程"选项
3. 发送消息给AI
4. 观察AI如何一步步思考并解决问题

## 技术栈

- **后端**: FastAPI, WebSockets, asyncio
- **前端**: 原生JavaScript, CSS3
- **数据存储**: 浏览器LocalStorage
- **AI框架**: OpenManus

## 贡献

欢迎贡献代码和提出改进建议！

## 开发者

- 李璇 (主要开发者)

## 许可证

MIT License

## 鸣谢

- 基于[OpenManus](https://github.com/mannaandpoem/OpenManus)框架开发

---

*OpenManus Web让AI不再是神秘的黑盒，而是一个您可以看到其思考过程的透明伙伴。* 
