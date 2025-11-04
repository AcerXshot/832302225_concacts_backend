# Contacts App API (Backend)

This is the backend service for the first software engineering assignment, a full-stack contacts application.

This repository contains the **backend** part of the project, built with Python, Flask, and SQLite.

### Project Links

* **Live API URL (Render):** <https://eight32302225-backend.onrender.com/>
* **Live Frontend App (Vercel):** <https://832302225-concacts-frontend.vercel.app/>
* **Frontend Repository (GitHub):** <https://github.com/AcerXshot/832302225_concacts_frontend>

### Features

* **RESTful API:** Provides full `CRUD` (Create, Read, Update, Delete) endpoints for contacts.
* **Persistent Storage:** Uses `SQLite` for data persistence, so data is not lost on restart.
* **Dynamic Search:** Supports live search filtering via `name`, `phone`, or `email` fields.
* **Robust Startup:** Automatically runs `CREATE TABLE IF NOT EXISTS` on startup to ensure the database is always ready, even in a cold-start environment.
* **CORS Enabled:** Pre-configured with `Flask-CORS` to accept requests from the Vercel frontend.

### Tech Stack

* **Python 3:** Core programming language.
* **Flask:** A lightweight web framework for building the API.
* **Gunicorn:** A production-grade WSGI server for deployment on Render.
* **SQLite:** A file-based database for persistent data storage.

### API Endpoints

| Method   | Path                       | Description                                  |
| :------- | :------------------------- | :------------------------------------------- |
| `GET`    | `/`                        | Checks the status of the backend server.     |
| `GET`    | `/api/contacts`            | Gets a list of all contacts.                 |
| `GET`    | `/api/contacts?q={query}`  | Searches contacts by `name`, `phone`, or `email`. |
| `POST`   | `/api/contacts`            | Adds a new contact.                          |
| `PUT`    | `/api/contacts/<int:id>`   | Updates a specific contact by ID.            |
| `DELETE` | `/api/contacts/<int:id>`   | Deletes a specific contact by ID.            |

### How to Run Locally

1.  Clone this repository.
2.  (Recommended) Create and activate a Python virtual environment.
3.  Install dependencies:
    ```bash
    pip install requirement.txt
    ```
4.  Run the application:
    ```bash
    python app.py
    ```