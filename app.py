from datetime import datetime, timezone
import os

from bson.errors import InvalidId
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Flask, flash, get_flashed_messages, redirect, render_template, request, session, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError


load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/my_blog")
mongo_client = None


def get_posts_collection():
    global mongo_client
    if mongo_client is None:
        mongo_client = MongoClient(MONGO_URI)
    database = mongo_client.get_default_database("my_blog")
    return database.posts


def prepare_post(post):
    if post:
        post["_id"] = str(post["_id"])
    return post


def get_all_posts():
    try:
        posts = get_posts_collection().find().sort("date", -1)
        return [prepare_post(post) for post in posts]
    except PyMongoError:
        return None


def get_one_post(post_id):
    try:
        return prepare_post(get_posts_collection().find_one({"_id": ObjectId(post_id)}))
    except (InvalidId, PyMongoError):
        return None


def create_post(data):
    try:
        data["date"] = datetime.now(timezone.utc)
        get_posts_collection().insert_one(data)
        return True
    except PyMongoError:
        return False


def update_post(post_id, data):
    try:
        result = get_posts_collection().update_one(
            {"_id": ObjectId(post_id)},
            {"$set": data},
        )
        return result.matched_count == 1
    except (InvalidId, PyMongoError):
        return False


def remove_post(post_id):
    try:
        result = get_posts_collection().delete_one({"_id": ObjectId(post_id)})
        return result.deleted_count == 1
    except (InvalidId, PyMongoError):
        return False


def admin_is_logged_in():
    return session.get("admin_logged_in", False)


@app.route("/")
def index():
    posts = get_all_posts()
    return render_template(
        "index.html", posts=posts or [], api_error=posts is None
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<post_id>")
def show_post(post_id):
    post = get_one_post(post_id)
    if post:
        return render_template("blog.html", post=post)
    return render_template("not_found.html"), 404


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            flash("You are now logged in.")
            return redirect(url_for("admin"))
        return render_template("login.html", error="The password was incorrect."), 401
    return render_template("login.html", error="")


@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("index"))


@app.route("/admin")
def admin():
    if not admin_is_logged_in():
        return redirect(url_for("login"))

    posts = get_all_posts()
    messages = get_flashed_messages()
    message = messages[-1] if messages else ""
    return render_template(
        "admin.html",
        posts=posts or [],
        api_error=posts is None,
        form_data={},
        form_error="",
        message=message,
    )


@app.route("/admin/add", methods=["POST"])
def add_post():
    if not admin_is_logged_in():
        return redirect(url_for("login"))

    data = {
        "title": request.form.get("title", "").strip(),
        "body": request.form.get("body", "").strip(),
    }
    if not data["title"] or not data["body"]:
        posts = get_all_posts()
        return render_template(
            "admin.html",
            posts=posts or [],
            api_error=posts is None,
            form_data=data,
            form_error="A title and body are required.",
            message="",
        ), 400

    if not create_post(data):
        posts = get_all_posts()
        return render_template(
            "admin.html",
            posts=posts or [],
            api_error=posts is None,
            form_data=data,
            form_error="The post could not be added. Please try again.",
            message="",
        ), 502

    flash("Post added.")
    return redirect(url_for("admin"))


@app.route("/admin/edit/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if not admin_is_logged_in():
        return redirect(url_for("login"))

    if request.method == "POST":
        data = {
            "title": request.form.get("title", "").strip(),
            "body": request.form.get("body", "").strip(),
        }
        if not data["title"] or not data["body"]:
            data["_id"] = post_id
            return render_template(
                "edit.html", post=data, error="A title and body are required."
            ), 400

        if not update_post(post_id, data):
            data["_id"] = post_id
            return render_template(
                "edit.html",
                post=data,
                error="The post could not be updated. Please try again.",
            ), 502

        flash("Post updated.")
        return redirect(url_for("admin"))

    post = get_one_post(post_id)
    if not post:
        flash("Post not found.")
        return redirect(url_for("admin"))
    return render_template("edit.html", post=post, error="")


@app.route("/admin/delete/<post_id>", methods=["POST"])
def delete_post(post_id):
    if not admin_is_logged_in():
        return redirect(url_for("login"))

    deleted = remove_post(post_id)
    flash("Post deleted." if deleted else "The post could not be deleted.")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)
