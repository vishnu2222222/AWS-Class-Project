from __future__ import annotations

import os
import re
import secrets
import sqlite3
from functools import wraps
from pathlib import Path

from flask import Flask, flash, g, redirect, render_template, request, session, url_for

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

PROJECTS = [
    {
        "title": "AWS Hardening Lab",
        "summary": "A cloud security lab focused on IAM least privilege, S3 access controls, and network segmentation.",
        "stack": "AWS IAM, S3, VPC",
        "outcome": "Created a reusable checklist for locking down basic AWS workloads."
    },
    {
        "title": "Phishing Awareness Toolkit",
        "summary": "A lightweight awareness program with email examples, reporting guidance, and user training materials.",
        "stack": "Security awareness, documentation, incident workflow",
        "outcome": "Reduced confusion around suspicious emails through simple step-by-step guidance."
    },
    {
        "title": "Incident Response Playbook Draft",
        "summary": "A starter playbook for triage, containment, and evidence preservation during common incidents.",
        "stack": "IR process, logging, communication",
        "outcome": "Turned ad hoc response notes into a repeatable process."
    },
]

CERTIFICATIONS = [
    {
        "name": "CompTIA Security+",
        "status": "In progress / target certification",
        "details": "Focused on foundational security operations, risk management, and network defense."
    },
    {
        "name": "AWS Cloud Practitioner",
        "status": "Planned",
        "details": "Supports cloud literacy, pricing awareness, and AWS service selection."
    },
    {
        "name": "Hands-on labs and course projects",
        "status": "Active",
        "details": "Portfolio projects in Linux, networking, AWS, and web application security."
    },
]

BLOG_POSTS = [
    {
        "title": "Why IAM Misconfigurations Stay Dangerous",
        "date": "April 2026",
        "excerpt": "A practical look at how small permission mistakes create outsized risk in cloud environments."
    },
    {
        "title": "What I Learned Building a Security Portfolio Site",
        "date": "April 2026",
        "excerpt": "Designing a portfolio is also an exercise in threat thinking, uptime planning, and defensive defaults."
    },
    {
        "title": "Three Habits That Improve Incident Readiness",
        "date": "March 2026",
        "excerpt": "Good logging, documented ownership, and simple response checklists go further than most teams expect."
    },
]

SERVICES = [
    {
        "title": "Portfolio Website Reviews",
        "description": "Security-minded feedback on personal sites, contact flows, and basic hardening."
    },
    {
        "title": "Cloud Security Starter Audits",
        "description": "Entry-level reviews of IAM, storage exposure, and common AWS misconfigurations."
    },
    {
        "title": "Incident Response Documentation",
        "description": "Simple playbooks and communication checklists for small teams and student organizations."
    },
]

RESUME_HIGHLIGHTS = [
    "Cybersecurity student building practical cloud and web security projects.",
    "Comfortable with Python, Linux basics, Flask, AWS fundamentals, and documentation-driven workflows.",
    "Interested in security operations, cloud defense, and secure application deployment.",
]

SKILLS = [
    "Python",
    "Flask",
    "HTML / CSS / Bootstrap",
    "AWS Lightsail",
    "SQLite",
    "Linux fundamentals",
    "Basic IAM and access control",
    "Technical writing",
]


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
        return {"site_name": "CyberFolio"}

    @app.route("/")
    def home():
        return render_template("home.html", projects=PROJECTS[:2], services=SERVICES[:2])

    @app.route("/about")
    def about():
        return render_template("about.html", skills=SKILLS)

    @app.route("/resume")
    def resume():
        return render_template("resume.html", highlights=RESUME_HIGHLIGHTS, skills=SKILLS)

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
        return render_template("services.html", services=SERVICES)

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
