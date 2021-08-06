import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect,Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers.mvt_router import mvt_router
from routers.ws_router import ws_router
from routers.mng_router import mng_router
from routers.anls_router import anls_router
from utils.apscheduler import run_schd
app = FastAPI(title='智慧大屏api', description='系统后端restful api')


# 跨域 CORS问题解决
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.include_router(base_router)
# 可以加前缀 prefix
app.include_router(mvt_router, prefix="/api/mvt")
app.include_router(mng_router, prefix="/api/mng")
app.include_router(anls_router, prefix="/api/anls")
app.include_router(ws_router)

run_schd()

@app.get("/")
def read_root(request: Request):
    client =   request.client
    return {"message": "ok","client":client}

@app.get("/index")
def index():
    time.sleep(5)
    return "wc"



# 调试服务
if __name__ == '__main__':
    uvicorn.run(app='main:app', host="0.0.0.0",
                port=8065, reload=True, debug=True)
