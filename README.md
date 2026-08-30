# 🚀 Blog Project

A blog made with Python, Flask, HTML, CSS, JavaScript and MongoDB. Visitors can read blog posts, while the admin can add, edit and delete them.

## 🔗 Live Demo

The live website link: https://se-19-se-01.onrender.com/

## 🌟 Project Overview

This project uses one Flask application. Flask handles the website routes, reads and writes data in MongoDB, and uses Jinja templates to create the HTML pages.

The project includes:

- A responsive home page that displays all blog posts
- A page for reading one complete post
- An About page
- An admin login page
- An admin page for adding, editing and deleting posts
- Error and empty states when posts cannot be loaded

## 🛠️ Tech Stack

- **Backend:** Python and Flask
- **Database:** MongoDB Atlas with PyMongo
- **Frontend:** HTML, CSS and JavaScript
- **Server-side rendering:** Jinja templates
- **Production server:** Gunicorn
- **Hosting:** Render
- **Checks:** Python and JavaScript syntax checks

## 🌐 How It Works

1. A visitor opens a page in the browser.
2. Flask receives the request and chooses the correct route.
3. Flask reads the required posts from MongoDB.
4. Jinja puts the post data into the HTML on the server.
5. The browser displays the page.
6. JavaScript counts the posts on the home page and updates the post count.

## 🗃️ Data Model

Posts are saved in the MongoDB `posts` collection. Every post contains:

- `title` — the post title
- `body` — the full post text
- `date` — the date and time the post was created

## 🔄 Dynamic Features

The project demonstrates both types of dynamic rendering required by the module:

- **Server-side:** Jinja renders MongoDB posts into the home, blog and admin pages.
- **Client-side:** JavaScript counts the rendered posts and displays the total.

The admin can also create, update and delete MongoDB entries through HTML forms.

## 📁 Project Structure

```text
app.py              Flask routes, login and MongoDB operations
requirements.txt    Python packages used by the project
static/
  Main.css           Website styling and responsive layout
  Main.js            Post counter and delete confirmation
templates/
  index.html         Home page
  blog.html          Single blog post page
  about.html         About page
  login.html         Admin login page
  admin.html         Add and manage posts
  edit.html          Edit post page
  not_found.html     Page shown when a post is not found
```

## ▶️ Run the Project Locally

1. Download or clone the repository.
2. Create a virtual environment:

```powershell
python -m venv .venv
```

3. Activate the virtual environment on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install the packages:

```powershell
pip install -r requirements.txt
```

5. Copy `.env.example`, rename the copy to `.env`, and add your own values:

```env
MONGO_URI=your-mongodb-connection-string
ADMIN_PASSWORD=your-admin-password
SECRET_KEY=your-random-secret-key
```

6. Start the website:

```powershell
python app.py
```

7. Open `http://127.0.0.1:5000` in a browser.

## ⚙️ Render Deployment

Create one Render web service with these settings:

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`
- **Environment variables:** `MONGO_URI`, `ADMIN_PASSWORD` and `SECRET_KEY`

The same environment variables must be added in the Render dashboard. They should not be written directly in the code.

## 🔒 Security Notes

- `.env` is included in `.gitignore` and must not be uploaded to GitHub.
- The MongoDB connection string and passwords are stored as environment variables.
- The admin pages require a password and use a Flask session.
- The separate API and API key are no longer needed because Flask connects directly to MongoDB.

## ✅ Checks

Run these checks before uploading:

```powershell
python -m compileall -q app.py
node --check static\Main.js
```

---

*Created by Gael Baret — 2026*
