from fastapi import APIRouter
from app.controllers import auth, posts

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(posts.router, prefix="/posts", tags=["posts"])