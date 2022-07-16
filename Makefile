P=$(shell pwd)

.PHONY: build
build:	
	docker build -t py-wechaty-template-bot:latest .

.PHONY: dockerrun
dockerrun:
	docker stop bot && docker rm bot
	docker run -it -d -v $(P):/bot --name bot -p 8004:8004 py-wechaty-template-bot:latest

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