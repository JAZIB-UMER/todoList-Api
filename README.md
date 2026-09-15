# Todo API

A minimal to-do list API built with Flask. Storage is in-memory (a Python list) — no database, so data resets whenever the app restarts. This was built as a small take-home style exercise, kept intentionally simple.

## Running it

### Option 1: Locally with Python

```bash
pip install -r requirements.txt
python app.py
```

The API will be available at `http://localhost:5000`.

### Option 2: With Docker

```bash
docker build -t todo-api .
docker run -p 5000:5000 todo-api
```

## Endpoints

| Method | Path              | Description                          |
|--------|-------------------|---------------------------------------|
| POST   | `/tasks`          | Add a new task                       |
| GET    | `/tasks`          | List all tasks                       |
| PATCH  | `/tasks/<id>/done`| Mark a task as done                  |
| GET    | `/health`         | Basic health check                   |

### `POST /tasks`

Create a new task.

Request body:
```json
{ "title": "Buy milk" }
```

Response (`201 Created`):
```json
{ "id": 1, "title": "Buy milk", "done": false }
```

Returns `400 Bad Request` if `title` is missing or empty.

### `GET /tasks`

Returns all tasks as a JSON array.

```json
[
  { "id": 1, "title": "Buy milk", "done": false },
  { "id": 2, "title": "Walk the dog", "done": true }
]
```

### `PATCH /tasks/<id>/done`

Marks the task with the given `id` as done.

Response (`200 OK`):
```json
{ "id": 1, "title": "Buy milk", "done": true }
```

Returns `404 Not Found` if the task doesn't exist.

### Quick test with curl

```bash
curl -X POST localhost:5000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
curl localhost:5000/tasks
curl -X PATCH localhost:5000/tasks/1/done
```

## CI

A GitHub Actions workflow (`.github/workflows/docker-build.yml`) builds the Docker image on every push and pull request, just to catch broken builds early. It doesn't push the image anywhere or deploy it.

## Reflection

There was nothing tricking in there. it's simple.

The choice I made of python is that i am familiar with that and with other languages don't have much experience in development. Although I can understand them as well but I though python would be easy.

If I got another day then obviously i will add in Interface for the todo list so user could interact with that instead of manually sending requests.
