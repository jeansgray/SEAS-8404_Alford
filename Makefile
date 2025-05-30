.PHONY: up down reset configure test

up:
	docker-compose up -d

down:
	docker-compose down

reset: down
	docker-compose down -v
	docker-compose up -d
	sleep 30
	python flask-app/configure_keycloak.py

configure:
	python flask-app/configure_keycloak.py

test:
	curl http://localhost:5000/api/public
	curl -H "Authorization: Bearer INVALID_TOKEN" http://localhost:5000/api/protected 