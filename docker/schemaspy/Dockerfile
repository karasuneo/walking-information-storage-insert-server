FROM openjdk:8u212-jdk-alpine

ENV APP_URL https://github.com/schemaspy/schemaspy/releases/download/v6.1.0/schemaspy-6.1.0.jar

WORKDIR /

RUN apk --update add graphviz ttf-dejavu gettext && \
    apk --update add --virtual .builddep tzdata wget libressl && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    wget -O schemaspy.jar ${APP_URL} && \
    apk del .builddep && \
    rm -rf /var/cache/apk/*

COPY ./docker/schemaspy/schemaspy.properties.template /schemaspy.properties.template
COPY ./docker/schemaspy/run_schemaspy.sh /usr/local/bin/run_schemaspy.sh
RUN chmod +x /usr/local/bin/run_schemaspy.sh

CMD ["/usr/local/bin/run_schemaspy.sh"]
