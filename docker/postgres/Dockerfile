FROM postgres:16.4

COPY ./docker/postgres/init /docker-entrypoint-initdb.d
COPY ./docker/postgres/init/7-insert_coordinates /docker-entrypoint-initdb.d
