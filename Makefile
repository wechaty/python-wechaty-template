.PHONY: build
build:	
	docker build -t py-wechaty-template-bot:latest .

.PHONY: dockerrun
dockerrun:
	docker stop bot && docker rm bot
	# this command will run bot with root user
	docker run -it -d -v "$(pwd)":/bot --name bot -p 8080:8080 py-wechaty-template-bot:latest

.PHONY: bot 
bot:
	make build
	make dockerrun

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: run
run:
	python bot.py