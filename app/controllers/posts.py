# app/controllers/posts.py
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.post import PostCreate, PostOut
from app.models.post import Post
from app.db.session import get_db
from app.services.auth_service import get_user_by_token
from app.services.post_service import get_cached_posts, set_cached_posts, invalidate_cache

router = APIRouter()
bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    """
    Dependency that retrieves the current authenticated user using the token.
    """
    token = credentials.credentials
    user = get_user_by_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return user

@router.post("/addpost")
def add_post(
    post_create: PostCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    AddPost endpoint.
    Validates the payload, saves the post, and invalidates the cache.
    """
    new_post = Post(text=post_create.text, owner=current_user)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    invalidate_cache(current_user.id)
    
    return {"postID": new_post.id}

@router.get("/", response_model=list[PostOut])
def get_posts(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    GetPosts endpoint.
    Retrieves all posts of the authenticated user.
    Uses in-memory caching for up to 5 minutes.
    """
    cached = get_cached_posts(current_user.id)
    if cached is not None:
        return cached
    
    posts = db.query(Post).filter(Post.user_id == current_user.id).all()
    posts_out = [PostOut.from_orm(post) for post in posts]
    set_cached_posts(current_user.id, posts_out)
    return posts_out

@router.delete("/deletepost")
def delete_post(
    postID: int = Body(..., embed=True),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    DeletePost endpoint.
    Deletes a post belonging to the authenticated user and invalidates the cache.
    """
    post = db.query(Post).filter(
        Post.id == postID,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    db.delete(post)
    db.commit()
    
    invalidate_cache(current_user.id)
    
    return {"detail": "Post deleted successfully"}
