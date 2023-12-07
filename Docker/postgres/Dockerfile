FROM postgres:latest
LABEL authors="shrike"

COPY ./db_init.sh /docker-entrypoint-initdb.d/

EXPOSE 5432

USER 999



