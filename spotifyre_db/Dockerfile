FROM postgres:latest

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD algo123
ENV POSTGRES_DB spotifyre_db

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
