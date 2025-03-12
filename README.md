# Article Blog API

## Overview
The **Article Blog API** is a Django REST Framework (DRF)-based application that allows users to create, manage, and categorize articles. Users can comment on articles and flag inappropriate comments. Authentication is handled using Django's built-in user system, ensuring secure access to features.

## Features
- User authentication (Sign Up, Sign In, Token-based authentication)
- CRUD operations for articles
- Articles categorized into multiple categories (e.g., Sports, Political, Finance, etc.)
- View articles based on selected categories
- Users can comment on articles (both their own and others')
- Comment flagging system (only article authors can flag comments)

---
## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Django 4.x
- Django REST Framework
- SQLite (default database)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/article-blog-api.git
   cd article-blog-api
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
5. Create a superuser (optional, for admin access):
   ```sh
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```sh
   python manage.py runserver
   ```

---
## API Endpoints

### Authentication
- `POST /api/auth/register/` → Register a new user
- `POST /api/auth/login/` → Log in and obtain a token

### Articles
- `GET /api/articles/` → List all articles
- `POST /api/articles/` → Create a new article (Auth required)
- `GET /api/articles/{id}/` → Retrieve a single article
- `PUT /api/articles/{id}/` → Update an article (Auth required)
- `DELETE /api/articles/{id}/` → Delete an article (Auth required)

### Categories
- `GET /api/categories/` → List all categories
- `GET /api/articles/?category={id}` → Filter articles by category

### Comments
- `GET /api/articles/{article_id}/comments/` → Get comments on an article
- `POST /api/articles/{article_id}/comments/` → Add a comment (Auth required)
- `PATCH /api/comments/{comment_id}/flag/` → Flag/unflag a comment (Only article author)

### User-Specific Endpoints
- `GET /api/user/articles/` → Get articles created by the logged-in user
- `GET /api/user/comments/` → Get comments made by the logged-in user

---
## Usage
### Example API Requests using Postman
1. **Get all articles**:
   - Method: `GET`
   - URL: `http://127.0.0.1:8000/api/articles/`
2. **Create an article**:
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/api/articles/`
   - Headers: `{ Authorization: Token <your_token> }`
   - Body:
     ```json
     {
       "title": "My First Article",
       "content": "This is my first article.",
       "published": true,
       "categories": [1, 2]
     }
     ```
3. **Get articles by category (e.g., category ID 1)**:
   - Method: `GET`
   - URL: `http://127.0.0.1:8000/api/articles/?category=1`
4. **Post a comment on an article (ID 1)**:
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/api/articles/1/comments/`
   - Body:
     ```json
     {
       "text": "Great article!"
     }
     ```
5. **Flag/unflag a comment (ID 5)**:
   - Method: `PATCH`
   - URL: `http://127.0.0.1:8000/api/comments/5/flag/`

---
## Database Schema
- **User**: Handles authentication
- **Article**:
  - `id` (Primary Key)
  - `title`
  - `content`
  - `published` (Boolean)
  - `author` (Foreign Key → User)
  - `categories` (Many-to-Many → Category)
- **Category**:
  - `id` (Primary Key)
  - `name`
- **Comment**:
  - `id` (Primary Key)
  - `article` (Foreign Key → Article)
  - `user` (Foreign Key → User)
  - `text`
  - `flagged` (Boolean, default=False)

---
## License
This project is open-source and available under the MIT License.

## Contributors
- Naman Shrimali (@Naman049)

## Contact
For questions or issues, open an issue on GitHub or reach out to `namanshrimali49@gmail.com`.

