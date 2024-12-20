-include .env

app-up:
	docker compose build && docker compose up -d && docker compose logs -f

app-db:
	docker exec -it $(DB_HOST) psql -U $(DB_USER) -d $(DB_NAME)

app-down:
	docker compose down --remove-orphans

app-destroy:
	docker compose down --rmi all --volumes

app-logs:
	docker compose logs -f

app-restart:
	rm -rf ./docker/postgres/data && docker compose down && docker compose build && docker compose up -d && docker compose logs -f

spy-up:
	docker compose -f docker-compose-spy.yml up --build --force-recreate spy
	docker rm spy
	docker compose -f docker-compose-spy.yml up -d --build nginx_schemaspy

spy-down:
	docker compose -f docker-compose-spy.yml down --remove-orphans

spy-destroy:
	docker compose -f docker-compose-spy.yml down --rmi all --volumes

delete:
	rm -rf docker/postgres/data/ && rm -rf output/

all-restart:
	make delete && make app-down && make spy-down && make app-destroy && make spy-destroy && make app-up && make spy-up