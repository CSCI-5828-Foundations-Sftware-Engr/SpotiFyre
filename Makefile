VERSION=v1
DOCKERUSER=
TOPIC_PLAYLIST=playlist-parameters
SUBSCRIBER_PLAYLIST=playlist-parameters-sub
DEAD_LETTER_TOPIC=dead-letter-playlist-parameters
DEAD_LETTER_SUB=dead-letter-playlist-parameters-sub
CLUSTER=spotifyre-prod
ZONE=us-central1-c
PROJECT_ID=polished-time-381400
PUBSUB_SERVICE_ACCOUNT="service-polished-time-381400@gcp-sa-pubsub.iam.gserviceaccount.com"

login:
	gcloud auth login && gcloud config set project $(PROJECT_ID)

helm:
	helm install postgres-db infra/postgresql

# Don't use this for now
build-services:
	cd services/frontend && gcloud builds submit --tag $(DOCKERUSER)/frontend .
	cd services/app_backend && gcloud builds submit --tag $(DOCKERUSER)/app_backend  .
	cd services/playlist_creation && gcloud builds submit --tag $(DOCKERUSER)/playlist_creation .

deploy-pubsub:
	gcloud pubsub topics create $(TOPIC_PLAYLIST) --message-retention-duration=1d && \
	gcloud pubsub subscriptions create $(SUBSCRIBER_PLAYLIST) --topic=$(TOPIC_PLAYLIST)
	gcloud pubsub topics create $(DEAD_LETTER_TOPIC) --message-retention-duration=1d && \
	gcloud pubsub subscriptions create $(DEAD_LETTER_SUB) --topic=$(DEAD_LETTER_TOPIC)
	gcloud pubsub subscriptions update $(SUBSCRIBER_PLAYLIST) \
		--dead-letter-topic=$(DEAD_LETTER_TOPIC) \
		--max-delivery-attempts=5

pubsub-dead-letter-service-account :
	gcloud pubsub topics add-iam-policy-binding $(DEAD_LETTER_TOPIC) \
		--member="serviceAccount:$(PUBSUB_SERVICE_ACCOUNT)"\
		--role="roles/pubsub.publisher"
	gcloud pubsub subscriptions add-iam-policy-binding $(SUBSCRIBER_PLAYLIST) \
		--member="serviceAccount:$(PUBSUB_SERVICE_ACCOUNT)"\
		--role="roles/pubsub.subscriber"

deploy-cluster:
	gcloud container clusters get-credentials $(CLUSTER) --zone $(ZONE) --project $(PROJECT_ID)
	gcloud container clusters update $(CLUSTER) --update-addons=HttpLoadBalancing=ENABLED  --zone $(ZONE)
	kubectl create secret generic credentials --from-env-file .env
	helm install postgresql infra/postgresql
	kubectl apply -f infra/frontend/deployment.xml
	kubectl apply -f infra/app_backend/deployment.xml
	kubectl apply -f infra/app_backend/service.xml
	kubectl apply -f infra/playlist_creation/deployment.xml

clean-everything: 
	gcloud pubsub topics delete $(TOPIC_PLAYLIST)
	gcloud pubsub subscriptions delete $(SUBSCRIBER_PLAYLIST)
	gcloud pubsub topics delete $(DEAD_LETTER_TOPIC)
	gcloud pubsub subscriptions delete $(DEAD_LETTER_SUB)
	gcloud container clusters delete $(CLUSTER) --region=$(REGION)
	helm delete postgresql