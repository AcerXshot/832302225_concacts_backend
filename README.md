# Contacts Application API (Backend)

This is the first assignment for the Software Engineering course at Fuzhou University, focusing on building a contacts application with a separated frontend and backend architecture.

This repository contains the **backend** part of the project.

**Live API Endpoint:** [https://eight32302225-backend.onrender.com/api/contacts](https://eight32302225-backend.onrender.com/api/contacts)

**Frontend Application:** [https://832302225-concacts-frontend.vercel.app/](https://832302225-concacts-frontend.vercel.app/)

## Project Description

This is a simple RESTful API built with Python and the Flask framework. It provides full CRUD (Create, Read, Update, Delete) functionality for managing contacts.

**Frontend Repository:** [Click Here](https://github.com/AcerXshot/832302225_concacts_frontend)

## Tech Stack

* **Language:** Python 3
* **Framework:** Flask
* **Server:** Gunicorn
* **Database:** SQLite
* **Libraries:** Flask-CORS

## API Endpoints

| Method   | Path                       | Description              |
| -------- | -------------------------- | ------------------------ |
| `GET`    | `/`                        | Server status check      |
| `GET`    | `/api/contacts`            | Get all contacts         |
| `POST`   | `/api/contacts`            | Add a new contact        |
| `PUT`    | `/api/contacts/<int:id>`   | Update a specific contact |
| `DELETE` | `/api/contacts/<int:id>`   | Delete a specific contact |

## How to Run Locally

1.  Clone this repository.
2.  Create and activate a Python virtual environment.
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the application:
    ```bash
    python app.py
    ```
5.  The API will be running at `http://127.0.0.1:5000`.