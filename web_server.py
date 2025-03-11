import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.web.api import app
from app.logger import logger

# 设置静态文件目录
static_path = Path(__file__).parent / "static"
static_path.mkdir(exist_ok=True)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# 设置根路由返回index.html
@app.get("/")
async def read_index():
    index_path = static_path / "index.html"
    return FileResponse(str(index_path))

# 健康检查接口
@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    logger.info("启动OpenManus Web服务...")
    logger.info(f"静态文件目录: {static_path}")
    logger.info("访问地址: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000) 