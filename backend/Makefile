up-dev:
	docker-compose up -d

up-test:
	docker compose -f docker-compose.yml -f docker-compose.override.yml --env-file .env.test up -d

up-prod:
	docker-compose --env-file .env.prod up -d

down:
	docker-compose down