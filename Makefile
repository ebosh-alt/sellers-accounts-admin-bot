generate-ssl:
	openssl req -new -newkey rsa:2048 -nodes -keyout data/server.key -out data/server.csr && \
	openssl x509 -req -in data/server.csr -signkey data/server.key -out data/server.crt

init-tg-client:
	@echo "init_tg_client is not required for admin-bot"

test_db:
	docker compose up --build -d db_accounts

start:
	python main.py

remove:
	docker compose down db_accounts bot_and_fastapi -v

restart:
	make remove
	make test_db
	python main.py test_data

start_prod:
	docker compose --profile prod up --build -d

restart_prod:
	make remove
	make start_prod

check:
	python -m compileall -q .
