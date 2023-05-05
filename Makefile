VERSION=v1
DOCKERUSER=us-west3-docker.pkg.dev/fse-new/spotifyre
TOPIC_PLAYLIST=playlist-parameters
SUBSCRIBER_PLAYLIST=playlist-parameters-sub
DEAD_LETTER_TOPIC=dead-letter-playlist-parameters
DEAD_LETTER_SUB=dead-letter-playlist-parameters-sub
CLUSTER=autopilot-cluster-1
ZONE=us-central1
PROJECT_ID=fse-new
BUCKET=spotifyre_bucket
PROJECT_NUMBER=$(shell gcloud projects list --filter="project_id:$(PROJECT_ID)" --format='value(project_number)')
SERVICE_ACCOUNT=$(shell gsutil kms serviceaccount -p $(PROJECT_NUMBER))
#PUBSUB_SERVICE_ACCOUNT="service-polished-time-381400@gcp-sa-pubsub.iam.gserviceaccount.com"

login:
	gcloud auth login && gcloud config set project $(PROJECT_ID)

helm:
	helm install postgres-db infra/postgresql

# Don't use this for now
build-services:
# cd services/frontend && gcloud builds submit --tag $(DOCKERUSER)/frontend .
	cd services/login_backend && gcloud builds submit --tag $(DOCKERUSER)/login-backend:latest  .
	cd services/playlist && gcloud builds submit --tag $(DOCKERUSER)/spotifyre-playlist:latest .

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
	helm install postgres-db infra/postgresql
	kubectl apply -f services/login-backend/deployment.xml
	kubectl apply -f services/login-backend/service.xml
	kubectl apply -f services/playlist_creation/deployment.xml

clean-everything: 
	gcloud pubsub topics delete $(TOPIC_PLAYLIST)
	gcloud pubsub subscriptions delete $(SUBSCRIBER_PLAYLIST)
	gcloud pubsub topics delete $(DEAD_LETTER_TOPIC)
	gcloud pubsub subscriptions delete $(DEAD_LETTER_SUB)
	gcloud container clusters delete $(CLUSTER) --region=$(REGION)
	helm delete postgresql

deploy-bucket:
	gsutil mb -l $(REGION) gs://$(BUCKET)
 	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
 	--member serviceAccount:$(SERVICE_ACCOUNT) \
 	--role roles/pubsub.publisher --role roles/eventarc.eventReceiver