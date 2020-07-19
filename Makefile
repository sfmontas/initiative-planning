up:
	docker-compose up --remove-orphans -d

api_test:
	docker exec -it script_runner pytest -n 2

rebuild_images:
	docker-compose up --build -d

logs:
	docker-compose logs -f
