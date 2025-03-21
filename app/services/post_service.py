# app/services/post_service.py
import time
from typing import List, Optional
from app.schemas.post import PostOut

# Simple in-memory cache for user's posts
posts_cache = {}
CACHE_DURATION = 300  # Cache duration in seconds (5 minutes)

def get_cached_posts(user_id: int) -> Optional[List[PostOut]]:
    """
    Returns cached posts for a user if the cache is still valid.
    """
    current_time = time.time()
    if user_id in posts_cache:
        cached_time, posts = posts_cache[user_id]
        if current_time - cached_time < CACHE_DURATION:
            return posts
    return None

def set_cached_posts(user_id: int, posts: List[PostOut]):
    """
    Caches the posts for a user with the current timestamp.
    """
    posts_cache[user_id] = (time.time(), posts)

def invalidate_cache(user_id: int):
    """
    Invalidates the cache for the given user.
    """
    if user_id in posts_cache:
        del posts_cache[user_id]
