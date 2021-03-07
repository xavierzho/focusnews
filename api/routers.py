from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
router = APIRouter()
origins = [
    "https://localhost.jonesc.com",
    "https://localhost.jonescy.cn",
    "http://localhost",
    "http://localhost:8000"
]


@router.get('/', tags=["search all "])
async def search_all():
    return {'data': ["jones", 'post', 'put']}
