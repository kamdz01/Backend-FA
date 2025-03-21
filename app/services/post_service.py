import time
from typing import List, Optional
from app.schemas.post import PostOut

posts_cache = {}
CACHE_DURATION = 300  

def get_cached_posts(user_id: int) -> Optional[List[PostOut]]:
    current_time = time.time()
    if user_id in posts_cache:
        cached_time, posts = posts_cache[user_id]
        if current_time - cached_time < CACHE_DURATION:
            return posts
    return None

def set_cached_posts(user_id: int, posts: List[PostOut]):
    posts_cache[user_id] = (time.time(), posts)

def invalidate_cache(user_id: int):
    if user_id in posts_cache:
        del posts_cache[user_id]
