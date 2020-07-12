up:
	docker-compose up --remove-orphans -d

api_test:
	docker exec -it script_runner pytest
