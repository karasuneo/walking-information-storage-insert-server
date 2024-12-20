-include .env

up:
	docker compose build && docker compose up -d && docker compose logs -f

db:
	docker exec -it $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME)

down:
	docker compose down --remove-orphans

destroy:
	docker compose down --rmi all --volumes

logs:
	docker compose logs -f

re-up:
	rm -rf ./docker/postgres/data && docker compose down && docker compose build && docker compose up -d && docker compose logs -f

format:
	black . && isort . && ruff check --fix