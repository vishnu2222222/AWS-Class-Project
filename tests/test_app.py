import sqlite3
import shutil
import uuid
from pathlib import Path

import pytest

from cyberfolio import create_app


@pytest.fixture()
def app():
    runtime_root = Path(".test-runtime")
    runtime_root.mkdir(exist_ok=True)
    runtime_dir = runtime_root / uuid.uuid4().hex
    runtime_dir.mkdir()
    database_path = runtime_dir / "test.db"
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "ADMIN_USERNAME": "admin",
            "ADMIN_PASSWORD": "super-secret",
            "DATABASE_PATH": str(database_path),
        }
    )
    try:
        yield app
    finally:
        shutil.rmtree(runtime_dir, ignore_errors=True)


@pytest.fixture()
def client(app):
    return app.test_client()


def test_public_pages_load(client):
    pages = [
        "/",
        "/about",
        "/resume",
        "/certifications",
        "/projects",
        "/blog",
        "/services",
        "/contact",
        "/admin/login",
    ]

    for page in pages:
        response = client.get(page)
        assert response.status_code == 200


def test_updated_portfolio_content_is_rendered(client):
    home_response = client.get("/")
    assert b"Vishnu Gangula | CyberFolio" in home_response.data
    assert b"Download Redacted Resume" in home_response.data

    about_response = client.get("/about")
    assert b"builder's mindset" in about_response.data
    assert b"linkedin.com/in/vishnugangula" in about_response.data

    resume_response = client.get("/resume")
    assert b"Information Security Intern" in resume_response.data
    assert b"The University of Texas at Dallas" in resume_response.data


def test_projects_page_links_to_selected_repositories(client):
    response = client.get("/projects")
    body = response.data.decode("utf-8")

    assert "ASA Log Sentinel" in body
    assert "https://github.com/vishnu2222222/ASA-Log-Sentinel" in body
    assert "https://github.com/vishnu2222222/Workout-Tracker-" in body
    assert "https://github.com/vishnu2222222/AWS-Class-Project" in body


def test_certifications_page_uses_resume_based_content(client):
    response = client.get("/certifications")
    assert b"Qualys Vulnerability Management, Detection &amp; Response (VMDR)" in response.data
    assert b"CyberDefender Level 1 (CCDL1)" in response.data
    assert b"CompTIA Security+" in response.data


def test_redacted_resume_is_served(client):
    response = client.get("/static/resume/vishnu-gangula-resume-redacted.pdf")
    assert response.status_code == 200
    assert response.mimetype == "application/pdf"


def test_contact_submission_is_saved(client, app):
    response = client.post(
        "/contact",
        data={
            "name": "Alex Analyst",
            "email": "alex@example.com",
            "subject": "Consultation",
            "message": "I would like to talk about a cloud review.",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Your message has been sent successfully." in response.data

    connection = sqlite3.connect(app.config["DATABASE_PATH"])
    try:
        row = connection.execute(
            "SELECT name, email, subject, message FROM contact_messages"
        ).fetchone()
    finally:
        connection.close()

    assert row == (
        "Alex Analyst",
        "alex@example.com",
        "Consultation",
        "I would like to talk about a cloud review.",
    )


def test_contact_validation_rejects_bad_email(client):
    response = client.post(
        "/contact",
        data={
            "name": "Alex Analyst",
            "email": "not-an-email",
            "subject": "Consultation",
            "message": "Please contact me.",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Please enter a valid email address." in response.data


def test_admin_requires_login(client):
    response = client.get("/admin/messages", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to view the admin dashboard." in response.data


def test_admin_can_view_messages_after_login(client):
    client.post(
        "/contact",
        data={
            "name": "Jamie",
            "email": "jamie@example.com",
            "subject": "Question",
            "message": "Testing the admin dashboard.",
        },
    )

    login_response = client.post(
        "/admin/login",
        data={"username": "admin", "password": "super-secret"},
        follow_redirects=True,
    )

    assert login_response.status_code == 200
    assert b"Saved contact submissions" in login_response.data
    assert b"jamie@example.com" in login_response.data


def test_messages_persist_across_app_restart():
    runtime_root = Path(".test-runtime")
    runtime_root.mkdir(exist_ok=True)
    runtime_dir = runtime_root / uuid.uuid4().hex
    runtime_dir.mkdir()
    database_path = runtime_dir / "persisted.db"

    try:
        first_app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-secret",
                "ADMIN_USERNAME": "admin",
                "ADMIN_PASSWORD": "super-secret",
                "DATABASE_PATH": str(database_path),
            }
        )
        first_client = first_app.test_client()
        first_client.post(
            "/contact",
            data={
                "name": "Taylor",
                "email": "taylor@example.com",
                "subject": "Persistence",
                "message": "This should still exist after restart.",
            },
        )

        second_app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-secret",
                "ADMIN_USERNAME": "admin",
                "ADMIN_PASSWORD": "super-secret",
                "DATABASE_PATH": str(database_path),
            }
        )
        second_client = second_app.test_client()
        response = second_client.post(
            "/admin/login",
            data={"username": "admin", "password": "super-secret"},
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"taylor@example.com" in response.data
    finally:
        shutil.rmtree(runtime_dir, ignore_errors=True)
