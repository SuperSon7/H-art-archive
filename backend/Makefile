up-dev:
	docker-compose up --build -d

up-test:
	docker compose -f docker-compose.test.yml --env-file .env.test -p test up --build -d

up-prod:
	docker-compose --env-file .env.prod up -d

down-test:
	docker compose -f docker-compose.test.yml -p test down -v

exec-dev:
	docker exec -it backend-web-1 bash
