.PHONY: build
build:	
	docker build -t py-wechaty-template-bot:latest .

.PHONY: dockerrun
build:
	# this command will run bot with root user
	docker run -it -d -v "$(pwd)":/bot py-wechaty-template-bot:latest --name bot -p 8080:8080

.PHONY: bot 
bot:
	make build
	make dockerrun

.PHONY: run
run:
	python bot.py