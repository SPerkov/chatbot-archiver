.PHONY: up down test

up:
	docker compose up --build -d

down:
	docker compose down

test:
	docker run --rm -v $(PWD):/app -w /app python:3.12-slim \
		sh -c "pip install -r requirements.txt -r requirements-dev.txt -q && python3 -m pytest -v"
