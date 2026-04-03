# chatbot-archiver

A FastAPI service that persists AI assistant messages to PostgreSQL.

## Setup

```bash
cp .env.example .env
```

The defaults in `.env` work out of the box for local development. For production, replace all values with strong secrets:

```bash
openssl rand -hex 32  # for API_KEY
openssl rand -hex 16  # for POSTGRES_PASSWORD (update DATABASE_URL too)
```

> **CI/CD note:** Store secrets as [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) and inject them as environment variables — never commit `.env` to the repository.

## Running with Docker

```bash
make up    # build and start in the background
make down  # stop containers, keep data
```

To also delete the database volume:

```bash
docker compose down -v
```

To follow logs:

```bash
docker compose logs -f
```

The API will be available at `http://localhost:8000`.

Interactive API docs (Swagger UI): `http://localhost:8000/docs`

### Authentication

All endpoints require an `X-API-Key` header. In Swagger UI, click **Authorize** and enter the value of `API_KEY` from your `.env`.

## Testing

No local Python setup required — runs inside Docker:

```bash
make test
```

## Development

Developed with AI-assisted tooling (Claude).

## TODO

- [ ] Pagination for `GET /messages`
- [ ] Secrets management (use GitHub Secrets for CI/CD, platform env vars for production)

## Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/messages` | Create a message |
| `PATCH` | `/messages/{message_id}` | Update a message |
| `GET` | `/messages` | List all messages |
