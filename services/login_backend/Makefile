VERSION=v9
DOCKERUSER=tejas1812

build:
	docker build -f Dockerfile -t login-backend .

push:
	docker tag login-backend $(DOCKERUSER)/login-backend:$(VERSION)
	docker push $(DOCKERUSER)/login-backend:$(VERSION)
	docker tag login-backend $(DOCKERUSER)/login-backend:latest
	docker push $(DOCKERUSER)/login-backend:latest

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml
