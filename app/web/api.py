import asyncio
import json
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.agent.manus import Manus
from app.logger import logger
from app.schema import AgentState

app = FastAPI(
    title="OpenManus Web",
    description="OpenManus Web界面API服务",
    version="0.1.0",
)

class MessageRequest(BaseModel):
    content: str

class MessageResponse(BaseModel):
    role: str
    content: str

class ConnectionManager:
    """WebSocket连接管理器"""
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.agents: Dict[str, Manus] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """注册新的WebSocket连接"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"新连接已注册: {client_id}, 当前活跃连接数: {len(self.active_connections)}")
    
    def disconnect(self, client_id: str):
        """关闭并移除WebSocket连接"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.agents:
            # 清理代理资源
            try:
                agent = self.agents[client_id]
                if hasattr(agent, 'cleanup') and callable(agent.cleanup):
                    agent.cleanup()
            except Exception as e:
                logger.error(f"清理代理资源时出错: {str(e)}")
            del self.agents[client_id]
        logger.info(f"连接已移除: {client_id}, 剩余活跃连接数: {len(self.active_connections)}")
    
    async def send_message(self, message: str, client_id: str):
        """向指定客户端发送消息"""
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
        else:
            logger.warning(f"尝试发送消息到不存在的连接: {client_id}")
    
    def get_agent(self, client_id: str) -> Optional[Manus]:
        """获取客户端对应的代理实例，如果不存在则创建新实例"""
        if client_id not in self.agents:
            logger.info(f"为客户端创建新代理实例: {client_id}")
            try:
                self.agents[client_id] = create_agent()
            except Exception as e:
                logger.error(f"创建代理实例失败: {str(e)}")
                return None
        return self.agents[client_id]

manager = ConnectionManager()

def create_agent() -> Manus:
    """创建一个新的Manus代理实例"""
    try:
        agent = Manus()
        logger.info("创建新的Manus代理实例成功")
        return agent
    except Exception as e:
        logger.error(f"创建Manus代理实例失败: {str(e)}")
        raise

@app.post("/api/chat", response_model=MessageResponse)
async def chat(message_request: MessageRequest):
    """HTTP API接口，用于处理消息请求"""
    agent = Manus()
    try:
        # 创建一个任务来运行agent
        result = await agent.run(message_request.content)
        return MessageResponse(role="assistant", content=result)
    except Exception as e:
        logger.error(f"处理请求时发生错误: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"message": f"处理请求时发生错误: {str(e)}"},
        )

async def run_agent_with_reasoning(agent: Manus, content: str) -> str:
    """运行代理并添加推理过程输出"""
    logger.info(f"开始执行代理，输入内容: {content[:30]}...")
    
    # 存储原始步骤结果
    original_step_method = agent.step
    reasoning_steps = []
    
    # 创建包装函数以捕获每个步骤的结果
    async def step_with_capture() -> str:
        step_result = await original_step_method()
        reasoning_steps.append(f"步骤 {agent.current_step}: {step_result}")
        return step_result
    
    # 替换step方法
    agent.step = step_with_capture
    
    try:
        # 执行代理
        result = await agent.run(content)
        
        # 添加推理过程
        reasoning = "\n".join(reasoning_steps)
        final_result = f"[推理过程:开始]\n{reasoning}\n[推理过程:结束]\n\n{result}"
        return final_result
    finally:
        # 恢复原始方法
        agent.step = original_step_method

async def run_agent_with_reasoning_stream(agent: Manus, content: str, websocket: WebSocket) -> str:
    """运行代理并实时流式输出推理过程"""
    logger.info(f"开始执行代理，输入内容: {content[:30]}...")
    
    # 存储原始步骤结果
    original_step_method = agent.step
    
    # 初始化推理块
    await websocket.send_json({
        "type": "reasoning_start",
        "content": "推理开始..."
    })
    
    # 创建包装函数以捕获并实时输出每个步骤的结果
    async def step_with_stream() -> str:
        step_result = await original_step_method()
        # 实时发送每个推理步骤
        step_message = f"步骤 {agent.current_step}: {step_result}"
        await websocket.send_json({
            "type": "reasoning_step",
            "content": step_message
        })
        return step_result
    
    # 替换step方法
    agent.step = step_with_stream
    
    try:
        # 执行代理
        result = await agent.run(content)
        
        # 发送推理完成信号
        await websocket.send_json({
            "type": "reasoning_end",
            "content": "推理完成"
        })
        
        # 返回最终结果
        return result
    finally:
        # 恢复原始方法
        agent.step = original_step_method

@app.websocket("/ws/chat/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    logger.info(f"WebSocket连接已建立: {client_id}")
    
    # 创建代理实例或从管理器获取
    agent = manager.get_agent(client_id)
    if agent is None:
        logger.error(f"无法创建代理实例: {client_id}")
        await websocket.send_text("服务器错误：无法创建代理实例")
        await websocket.close(code=1011)
        return
    
    # 用于标记是否已断开连接
    is_disconnected = False
    
    try:
        while True:
            if is_disconnected:
                logger.warning(f"连接已断开，停止接收消息: {client_id}")
                break
                
            try:
                # 接收消息
                data = await websocket.receive_text()
            except WebSocketDisconnect:
                logger.info(f"WebSocket连接已断开: {client_id}")
                is_disconnected = True
                break
            except Exception as e:
                logger.error(f"接收消息错误: {str(e)}")
                is_disconnected = True
                break
                
            # 解析消息
            try:
                message_data = json.loads(data)
                message_type = message_data.get('type', 'message')
                content = message_data.get('content', '')
                
                logger.info(f"收到消息 [{message_type}]: {content[:30]}...")
                
                # 处理消息类型
                if message_type == 'cancel':
                    # 如果是取消消息，停止代理思考
                    if hasattr(agent, 'state') and agent.state == AgentState.THINKING:
                        agent.state = AgentState.CANCELLED
                        await websocket.send_text("操作已取消")
                    continue
                
                # 发送处理中提示
                await websocket.send_json({
                    "type": "processing",
                    "content": "处理中..."
                })
                
                # 执行代理并实时流式输出推理过程
                logger.info(f"执行代理: {content[:30]}...")
                result = await run_agent_with_reasoning_stream(agent, content, websocket)
                
                # 发送最终结果
                logger.info(f"发送最终结果: 长度 {len(result)} 字符")
                await websocket.send_json({
                    "type": "result",
                    "content": result
                })
                
            except json.JSONDecodeError:
                logger.error(f"JSON解析错误: {data}")
                await websocket.send_json({
                    "type": "error",
                    "content": "消息格式错误"
                })
            except Exception as e:
                logger.error(f"处理消息错误: {str(e)}")
                await websocket.send_json({
                    "type": "error",
                    "content": f"处理消息时出错: {str(e)}"
                })
    except WebSocketDisconnect:
        logger.info(f"WebSocket连接已断开: {client_id}")
    except Exception as e:
        logger.error(f"WebSocket错误: {str(e)}")
    finally:
        logger.info(f"WebSocket连接关闭: {client_id}")
        manager.disconnect(client_id)

@app.get("/api/tools")
async def get_available_tools():
    """获取可用工具列表"""
    try:
        agent = Manus()
        tools = agent.available_tools.tool_map
        tool_list = []
        
        for name, tool in tools.items():
            tool_list.append({
                "name": name,
                "description": tool.description
            })
        
        return {"tools": tool_list}
    except Exception as e:
        logger.error(f"获取工具列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取工具列表失败: {str(e)}")

@app.get("/api/version")
async def get_version():
    """获取API版本信息"""
    return {
        "version": app.version,
        "name": "OpenManus Web",
        "status": "running"
    } 