echo "# Social Media API

A Django REST Framework project providing user registration, login, and profile management with token-based authentication.

## Project Setup

### 1. Clone the repository
\`\`\`bash
git clone <your-github-repo-url>
cd social_media_api
\`\`\`

### 2. Create a virtual environment and install dependencies
\`\`\`bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

### 3. Run initial migrations
\`\`\`bash
python manage.py migrate
\`\`\`

### 4. Start the development server
\`\`\`bash
python manage.py runserver
\`\`\`

## API Endpoints

### Register a new user
POST /api/accounts/register/
Body:
\`\`\`json
{
  \"username\": \"your_username\",
  \"email\": \"you@example.com\",
  \"password\": \"strongpassword\",
  \"bio\": \"About me\"
}
\`\`\`

### Login
POST /api/accounts/login/
Body:
\`\`\`json
{
  \"username\": \"your_username\",
  \"password\": \"strongpassword\"
}
\`\`\`

### Access Profile
GET /api/accounts/profile/
Header: Authorization: Token YOUR_TOKEN_HERE

## User Model Overview
Custom User model with fields: username, email, password, bio, followers.
" > README.md
