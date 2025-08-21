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

# 더미 데이터 생성 관련 명령어
create-dummy-data:
	docker-compose exec web python create_dummy_data_simple.py

create-dummy-data-django:
	docker-compose exec web python manage.py create_dummy_data

create-dummy-data-custom:
	docker-compose exec web python manage.py create_dummy_data --users 30 --artists 20 --artworks 100

check-data:
	docker-compose exec web python manage.py shell -c "from django.contrib.auth import get_user_model; from apps.artists.models import Artist; from apps.artworks.models import Artwork; User = get_user_model(); print(f'👥 총 사용자: {User.objects.count()}명'); print(f'🎭 총 작가: {Artist.objects.count()}명'); print(f'🖼️ 총 작품: {Artwork.objects.count()}개')"

clear-dummy-data:
	docker-compose exec web python manage.py shell -c "from django.contrib.auth import get_user_model; from apps.artists.models import Artist; from apps.artworks.models import Artwork, ArtworkImage; from apps.interactions.models import Follow, Wishlist, PurchaseInquiry; User = get_user_model(); User.objects.filter(email__contains='@example.com').delete(); Artist.objects.all().delete(); Artwork.objects.all().delete(); ArtworkImage.objects.all().delete(); Follow.objects.all().delete(); Wishlist.objects.all().delete(); PurchaseInquiry.objects.all().delete(); print('✅ 더미 데이터 삭제 완료')"
