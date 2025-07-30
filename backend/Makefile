up-dev:
	docker-compose up -d

up-test:
	docker compose -f docker-compose.test.yml --env-file .env.test -p test up -d

up-prod:
	docker-compose --env-file .env.prod up -d

down-test:
	docker compose -f docker-compose.test.yml -p test down -v