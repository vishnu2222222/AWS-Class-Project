from __future__ import annotations

import os
import re
import secrets
import sqlite3
from functools import wraps
from pathlib import Path

from flask import Flask, flash, g, redirect, render_template, request, session, url_for

from .content import (
    ABOUT_SECTIONS,
    BLOG_POSTS,
    CERTIFICATIONS,
    EDUCATION,
    EXPERIENCE,
    FOCUS_AREAS,
    HOME_METRICS,
    HOME_SPOTLIGHTS,
    PROFILE,
    PROJECTS,
    REDIRECTED_RESUME_FILENAME,
    SITE_DESCRIPTION,
    SITE_NAME,
    SKILL_GROUPS,
    SOCIAL_LINKS,
)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        ADMIN_USERNAME=os.environ.get("ADMIN_USERNAME", "admin"),
        ADMIN_PASSWORD=os.environ.get("ADMIN_PASSWORD", "change-me-admin-password"),
        DATABASE_PATH=os.environ.get(
            "DATABASE_PATH",
            str(Path(app.instance_path) / "portfolio.db"),
        ),
    )

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    with app.app_context():
        init_db()

    @app.context_processor
    def inject_site_context() -> dict:
        return {
            "site_name": SITE_NAME,
            "site_description": SITE_DESCRIPTION,
            "social_links": SOCIAL_LINKS,
            "resume_download_filename": REDIRECTED_RESUME_FILENAME,
        }

    @app.route("/")
    def home():
        return render_template(
            "home.html",
            profile=PROFILE,
            metrics=HOME_METRICS,
            focus_spotlights=HOME_SPOTLIGHTS,
            projects=PROJECTS,
            focus_areas=FOCUS_AREAS,
            experience=EXPERIENCE,
        )

    @app.route("/about")
    def about():
        return render_template(
            "about.html",
            profile=PROFILE,
            about_sections=ABOUT_SECTIONS,
            skill_groups=SKILL_GROUPS,
        )

    @app.route("/resume")
    def resume():
        return render_template(
            "resume.html",
            profile=PROFILE,
            education=EDUCATION,
            experience=EXPERIENCE,
            skill_groups=SKILL_GROUPS,
            certifications=CERTIFICATIONS,
        )

    @app.route("/certifications")
    def certifications():
        return render_template("certifications.html", certifications=CERTIFICATIONS)

    @app.route("/projects")
    def projects():
        return render_template("projects.html", projects=PROJECTS)

    @app.route("/blog")
    def blog():
        return render_template("blog.html", posts=BLOG_POSTS)

    @app.route("/services")
    def services():
        return render_template("services.html", focus_areas=FOCUS_AREAS)

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        errors: list[str] = []
        form_data = {
            "name": "",
            "email": "",
            "subject": "",
            "message": "",
        }

        if request.method == "POST":
            form_data = {
                "name": request.form.get("name", "").strip(),
                "email": request.form.get("email", "").strip(),
                "subject": request.form.get("subject", "").strip(),
                "message": request.form.get("message", "").strip(),
            }

            if not form_data["name"]:
                errors.append("Name is required.")
            if not form_data["email"]:
                errors.append("Email is required.")
            elif not EMAIL_PATTERN.match(form_data["email"]):
                errors.append("Please enter a valid email address.")
            if not form_data["subject"]:
                errors.append("Subject is required.")
            if not form_data["message"]:
                errors.append("Message is required.")

            if not errors:
                get_db().execute(
                    """
                    INSERT INTO contact_messages (name, email, subject, message)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        form_data["name"],
                        form_data["email"],
                        form_data["subject"],
                        form_data["message"],
                    ),
                )
                get_db().commit()
                flash("Your message has been sent successfully.", "success")
                return redirect(url_for("contact"))

            for error in errors:
                flash(error, "danger")

        return render_template("contact.html", form_data=form_data)

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            if (
                secrets.compare_digest(username, app.config["ADMIN_USERNAME"])
                and secrets.compare_digest(password, app.config["ADMIN_PASSWORD"])
            ):
                session.clear()
                session["admin_logged_in"] = True
                flash("You are now signed in.", "success")
                return redirect(url_for("admin_messages"))

            flash("Invalid username or password.", "danger")

        return render_template("admin_login.html")

    @app.route("/admin/logout", methods=["POST"])
    def admin_logout():
        session.clear()
        flash("You have been signed out.", "info")
        return redirect(url_for("admin_login"))

    @app.route("/admin/messages")
    @admin_required
    def admin_messages():
        messages = get_db().execute(
            """
            SELECT id, name, email, subject, message, created_at
            FROM contact_messages
            ORDER BY datetime(created_at) DESC, id DESC
            """
        ).fetchall()
        return render_template("admin_messages.html", messages=messages)

    @app.teardown_appcontext
    def close_db(exception: Exception | None) -> None:
        db = g.pop("db", None)
        if db is not None:
            db.close()

    return app


def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("admin_logged_in"):
            flash("Please log in to view the admin dashboard.", "warning")
            return redirect(url_for("admin_login"))
        return view(**kwargs)

    return wrapped_view


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(current_database_path())
        g.db.row_factory = sqlite3.Row
    return g.db


def current_database_path() -> str:
    from flask import current_app

    return current_app.config["DATABASE_PATH"]


def init_db() -> None:
    db_path = Path(current_database_path())
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    try:
        schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
        connection.executescript(schema)
        connection.commit()
    finally:
        connection.close()
