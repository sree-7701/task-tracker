# Task Tracker

A simple task manager built with Flask and SQLite, with a REST API and a Bootstrap frontend.

## Features
- Add, update, complete and delete tasks (CRUD)
- REST API returning JSON with proper status codes (201, 400, 404)
- Bootstrap web page that uses fetch() to call the API
- Automated tests with pytest

## Tech Stack
Python, Flask, SQLite, HTML, Bootstrap, JavaScript, pytest

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/tasks | List all tasks |
| POST | /api/tasks | Create a task (`{"title": "..."}`) |
| PUT | /api/tasks/<id> | Update title or done status |
| DELETE | /api/tasks/<id> | Delete a task |

## Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install flask pytest
python app.py
```
Open http://127.0.0.1:5000 in your browser.

## Run Tests
```bash
pytest
```