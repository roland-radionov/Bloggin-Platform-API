# Blogging Platform API

This is a simple API that allows you to create, modify, and delete posts. You can also find posts based on specific criteria.

## Installation

```bash
# Clone repository
git clone https://github.com/roland-radionov/Bloggin-Platform-API.git
cd Bloggin-Platform-API

# Create environment
python3 -m venv .venv

# On Windows
.venv\Scripts\activate
# On Linux/macOS
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run app
python app.py
```

## Usage

Once the server is running, you can interact with the API using any HTTP client (Postman, curl, etc.).

Base URL: `http://127.0.0.1:5000`

### Endpoints

#### Create new post

**Request:**

```http
POST /posts
Content-Type: application/json

{
  "title": "My First Blog Post",
  "content": "This is the content of the post",
  "category": "Technology",
  "tags": "Python, Flask"
}
```

**Response:**

```json
{
  "message": "Successfully created post with id 1"
}
```

#### Get all posts

**Request:**

```http
GET /posts
```

**Response:**

```json
[
  {
    "category": "Technology",
    "content": "This is the content of my first blog post.",
    "created_at": "2026-06-18 14:49:43",
    "id": 1,
    "tags": ["Tech", "Programming"],
    "title": "My First Blog Post",
    "updated_at": "2026-06-18 14:49:43"
  }
]
```

#### Get a single post

**Request:**

```http
GET /posts/1
```

**Response:**

```json
{
  "category": "Technology",
  "content": "This is the content of my first blog post.",
  "created_at": "2026-06-18 14:49:43",
  "id": 1,
  "tags": ["Tech", "Programming"],
  "title": "My First Blog Post",
  "updated_at": "2026-06-18 14:49:43"
}
```

#### Update a post

**Request:**

```http
PUT /posts/1
Content-Type: application/json

{
  "title": "My First Blog Post",
  "content": "New content",
  "category": "Technology",
  "tags": ["Tech", "Programming"]
}
```

**Response:**

```json
{
  "message": "Successfully changed post with id 1"
}
```

#### Delete a post

**Request:**

```http
DELETE /posts/1
```

**Response:**

```

```

#### Get a post by search term

**Request:**

```http
GET /posts?term=tech
```

**Response:**

```json
[
  {
    "category": "Technology",
    "content": "This is the content of my first blog post.",
    "created_at": "2026-06-18 15:07:44",
    "id": 1,
    "tags": ["Tech", "Programming"],
    "title": "My First Blog Post",
    "updated_at": "2026-06-18 15:07:44"
  }
]
```

### Quick test

```bash
# Создать пост
curl -X POST http://127.0.0.1:5000/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Hello", "content": "World", "category": "Tech", "tags": "Flask"}'

# Получить все посты
curl http://127.0.0.1:5000/posts

# Удалить пост
curl -X DELETE http://127.0.0.1:5000/posts/1
```

## Credits

This project is based on the [Blogging Platform API](https://roadmap.sh/projects/blogging-platform-api) project from [roadmap.sh](https://roadmap.sh/).

## Author

Radionov Roland
