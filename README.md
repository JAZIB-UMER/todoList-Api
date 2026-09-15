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

**Trickiest part:** Honestly, nothing here was technically hard — the task is intentionally small. The part I spent the most time thinking about was scope: how much to add versus how much to leave out. It's tempting to reach for things like input validation libraries, a proper data layer, or auth, but for a 3-endpoint in-memory API those add more surface area than value.

**Why I made the choices I did:**
- **Flask over a bigger framework (FastAPI, Django):** Flask has almost no ceremony — one file gets you a working API, which fits an exercise like this. FastAPI would've given free request validation and docs, which is nice, but felt like more than the task called for.
- **In-memory list instead of even SQLite:** The prompt explicitly said this was fine, and a list plus a counter is the simplest thing that can possibly work. No schema, no migrations, nothing to reason about across restarts.
- **`python:3.11-slim` base image:** Small image, still has pip and a full Python install, avoids the extra complexity of Alpine's musl/libc quirks with some Python packages.
- **CI just builds, doesn't deploy:** That's what was asked for, and it's also the honest boundary of what a "does this still build" check should do without more infrastructure (a registry, credentials, a target environment) to deploy into.

**If I had another day, I'd:**
- Add a real test suite (pytest + Flask's test client) and run it in CI, not just the Docker build.
- Add basic input validation/error handling for malformed JSON, wrong types, etc.
- Swap in SQLite or Postgres so data survives a restart, with a simple migration story.
- Add pagination and filtering on `GET /tasks` (e.g. `?done=true`) once the list could realistically grow.
- Add OpenAPI/Swagger docs, which is one of the reasons FastAPI becomes more attractive once the API is beyond a toy.
- Pin dependencies more strictly and add a `.dockerignore` and non-root user in the Dockerfile for a slightly more production-minded image.
