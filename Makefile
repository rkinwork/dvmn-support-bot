build_image:
	docker build -f Dockerfile . -t pycharm-dvmn-support-bot

start_tg:
	docker compose run --rm -e DVMN_BOT__TELEGRAM_MODE=True bot

start_vk:
	docker compose run --rm -e DVMN_BOT__VK_MODE=True bot

start_train:
	docker compose run --rm -e DVMN_BOT__TRAIN_MODE=True bot

stop:
	docker-compose kill -s SIGINT

run_server_tg:
	export $(cat .env | xargs) && export DVMN_BOT__TELEGRAM_MODE=True && python src/main.py

run_server_vk:
	export $(cat .env | xargs) && export DVMN_BOT__VK_MODE=True && python src/main.py

