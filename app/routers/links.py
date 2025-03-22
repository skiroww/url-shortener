from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..database import get_db
from ..models import User
from ..schemas import LinkCreate, LinkUpdate, LinkInfo
from ..services import LinkService, AuthService

router = APIRouter()
security = HTTPBearer()

@router.post("/links/shorten", response_model=LinkInfo)
async def create_short_link(
    link: LinkCreate,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    """
    Create a new short link.
    
    Requires authentication token in the Authorization header.
    Example:
    ```
    Authorization: Bearer your.jwt.token
    ```
    """
    user = await AuthService.get_current_user(token=credentials.credentials, db=db)
    return LinkService.create_link(db, link, user)

@router.get("/{short_code}")
def redirect_link(short_code: str, db: Session = Depends(get_db)):
    """Get the original URL for redirection."""
    link = LinkService.get_link(db, short_code)
    LinkService.increment_click_count(db, link)
    
    # Ensure the URL has a proper scheme
    url = link.original_url
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return {
        "original_url": url,
        "short_code": link.short_code,
        "click_count": link.click_count
    }

@router.delete("/links/{short_code}")
async def delete_link(
    short_code: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    """
    Delete a link.
    
    Requires authentication token in the Authorization header.
    Example:
    ```
    Authorization: Bearer your.jwt.token
    ```
    """
    user = await AuthService.get_current_user(token=credentials.credentials, db=db)
    LinkService.delete_link(db, short_code, user)
    return {"detail": "Link deleted successfully"}

@router.put("/links/{short_code}", response_model=LinkInfo)
async def update_link(
    short_code: str,
    data: LinkUpdate,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    """
    Update a link's original URL.
    
    Requires authentication token in the Authorization header.
    Example:
    ```
    Authorization: Bearer your.jwt.token
    ```
    """
    user = await AuthService.get_current_user(token=credentials.credentials, db=db)
    return LinkService.update_link(db, short_code, data, user)

@router.get("/links/{short_code}/stats", response_model=LinkInfo)
async def link_stats(
    short_code: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    """
    Get statistics for a link.
    
    Requires authentication token in the Authorization header.
    Example:
    ```
    Authorization: Bearer your.jwt.token
    ```
    """
    user = await AuthService.get_current_user(token=credentials.credentials, db=db)
    return LinkService.get_link(db, short_code)

@router.get("/links/search")
def search_link(original_url: str, db: Session = Depends(get_db)):
    """Search for a link by its original URL."""
    link = LinkService.search_by_url(db, original_url)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link
