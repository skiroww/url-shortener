from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routers import links, auth
from .database import Base, engine
from .exceptions import (
    LinkNotFoundError,
    LinkExpiredError,
    CustomAliasTakenError,
    UnauthorizedError,
    InvalidCredentialsError,
    UserExistsError
)

app = FastAPI(
    title="URL Shortener API",
    description="A service for shortening URLs with analytics, authentication, and caching.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Exception handlers
@app.exception_handler(LinkNotFoundError)
async def link_not_found_handler(request: Request, exc: LinkNotFoundError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(LinkExpiredError)
async def link_expired_handler(request: Request, exc: LinkExpiredError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(CustomAliasTakenError)
async def custom_alias_taken_handler(request: Request, exc: CustomAliasTakenError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(UnauthorizedError)
async def unauthorized_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(UserExistsError)
async def user_exists_handler(request: Request, exc: UserExistsError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# Include routers
app.include_router(auth.router, prefix="", tags=["Auth"])
app.include_router(links.router, prefix="", tags=["Links"])

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "URL Shortener API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }