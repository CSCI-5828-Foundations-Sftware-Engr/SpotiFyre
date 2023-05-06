VERSION=
DOCKERUSER=

build:
	docker build -f Dockerfile -t spotifyre-playlist .

push:
	docker tag spotifyre-playlist $(DOCKERUSER)/spotifyre-playlist:$(VERSION)
	docker push $(DOCKERUSER)/spotifyre-playlist:$(VERSION)
	docker tag spotifyre-playlist $(DOCKERUSER)/spotifyre-playlist:latest
	docker push $(DOCKERUSER)/spotifyre-playlist:latest

deploy:
	kubectl apply -f deployment.yaml
