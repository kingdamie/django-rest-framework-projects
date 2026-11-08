# DRF Practice Projects

Two small Django REST Framework projects built while learning DRF.

| Project | What it is |
| --- | --- |
| [`peoplehub/`](peoplehub) | CRUD API for people, with token auth, user registration and pagination |
| [`todo/`](todo) | Todo API where each user only sees and edits their own todos |

## Setup

Requires Python 3.9+.

```bash
git clone <your-repo-url>
cd DRF

python3 -m venv env
source env/bin/activate        # Windows: env\Scripts\activate

pip install -r requirements.txt
```

Run a project (example: peoplehub):

```bash
cd peoplehub
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

The API is then available at `http://127.0.0.1:8000/`.

## peoplehub

A `Person` has `name`, `age` and `city`.

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/auth/register/` | Create a user (`username`, `password`) |
| POST | `/auth/login/` | Get a token (`username`, `password`) |
| POST | `/auth/logout/` | Log out |
| GET | `/multipleobj/` | List people (paginated, 10 per page, `?page=2`) |
| POST | `/multipleobj/` | Create a person |
| GET / PUT / PATCH / DELETE | `/singleobj/<id>/` | Read or change one person |

Send the token on protected endpoints:

```
Authorization: Token <your-token>
```

List responses are paginated:

```json
{
  "count": 23,
  "next": "http://127.0.0.1:8000/multipleobj/?page=2",
  "previous": null,
  "results": []
}
```

## todo

A `Todo` has `title`, `description`, `completed` and `created_at`, and belongs to a user.

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | API root |
| GET | `/todo/` | List your todos |
| POST | `/todo/` | Create a todo (assigned to you) |
| GET / PUT / PATCH / DELETE | `/todo/<id>/` | Read or change one of your todos |

Todos are filtered by the logged-in user, so other users' todos return 404.
These views need authentication configured in `todo/todo/settings.py`
(`REST_FRAMEWORK` auth and permission classes, plus a login endpoint).

## Built with

- Python 3
- Django 4.2
- Django REST Framework 3.16
