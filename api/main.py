from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

router = APIRouter()
app = FastAPI(
    title="新闻查询接口服务",
    version="1.0",
    description="面向数据"
)
app.include_router(
    router=router,
    prefix="/newsapi"
)

origins = [
    "https://localhost.jonesc.com",
    "https://localhost.jonescy.cn",
    "http://localhost",
    "http://localhost:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@router.get('/', tags=["search all "])
async def search_all():
    return {'data': ["jones", 'post', 'put']}


if __name__ == '__main__':
    uvicorn.run(app)
