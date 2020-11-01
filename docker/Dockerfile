FROM python:3.7-slim
ARG DB_USER
ARG DB_PASS
WORKDIR /opt/kanava14fi/blog-platform

COPY config /opt/kanava14fi/blog-platform
COPY app /opt/kanava14fi/blog-platform
RUN python -m pip install .
RUN python -m pip install -e ".[develop]"

COPY config/development.ini.sample /opt/kanava14fi/blog-platform/development.ini
RUN session_secret=$(< /dev/urandom tr -dc A-Za-z0-9 | head -c${1:-15}) && \
    sed -i "s/__secret__/$session_secret/g" development.ini && \
    sed -i "s/__username__/${DB_USER}/g" development.ini && \
    sed -i "s/__password__/${DB_PASS}/g" development.ini && \
    sed -i "s/__host__/db/g" development.ini && \
    sed -i "s/__port__/5432/g" development.ini && \
    sed -i "s/__table__/kanava14/g" development.ini

COPY docker/start-docker.sh ./

CMD ["/bin/bash", "./start-docker.sh"]
