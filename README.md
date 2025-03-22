# URL Shortener API

A modern URL shortener service built with FastAPI, featuring authentication, analytics, and link previews.

## Features

- URL shortening with custom aliases
- User authentication with JWT tokens
- Link analytics (click count, last accessed)
- Link preview generation
- Link expiration
- URL validation and safety checks
- CORS support

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite (can be easily switched to PostgreSQL)
- Pydantic
- JWT Authentication
- BeautifulSoup4 for link previews

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `POST /auth/login/json` - Login with JSON data

### Links
- `POST /links/shorten` - Create a new short link
- `GET /{short_code}` - Redirect to original URL
- `DELETE /links/{short_code}` - Delete a link
- `PUT /links/{short_code}` - Update a link
- `GET /links/{short_code}/stats` - Get link statistics
- `GET /links/search` - Search for a link by URL

## Environment Variables

Create a `.env` file in the root directory with the following variables:
```
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Deployment

This application is configured for deployment on Render.io. The `render.yaml` file contains the necessary configuration.

## License

MIT License 