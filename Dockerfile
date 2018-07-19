FROM ubuntu:16.04

ENV DOCK_ROOT='/home/ubuntu'
ENV DOCK_SRC=${DOCK_ROOT}/src
ENV DOCK_WSGI=${DOCK_ROOT}/uwsgi
ENV DEBIAN_FRONTEND noninteractive
ENV PG_SECRET_KEY $PG_SECRET_KEY
ENV PG_FCM_SERVER_KEY $PG_FCM_SERVER_KEY


RUN apt-get -y update && apt-get -y --no-install-recommends upgrade

RUN apt-get install -y --no-install-recommends apt-utils \
    gfortran \
    gcc \
    git \
    vim \
    nginx \
    supervisor \
    python3 \
    python3-pip \
    python3-dev \
    python3-setuptools && \
    pip3 install -U pip && pip install uwsgi

RUN mkdir ${DOCK_ROOT} && mkdir ${DOCK_SRC} && mkdir ${DOCK_WSGI}

COPY manage.py requirements.txt ${DOCK_SRC}/
RUN cd ${DOCK_SRC} && pip3 install -r requirements.txt

COPY pg_rest_api ${DOCK_SRC}/pg_rest_api
COPY apps ${DOCK_SRC}/apps
COPY api ${DOCK_SRC}/api

RUN echo "daemon off;" >> /etc/nginx/nginx.conf && \
    cd ${DOCK_WSGI}
COPY build/uwsgi_params build/uwsgi.ini ${DOCK_WSGI}/
COPY build/nginx.conf /etc/nginx/sites-available/default
COPY build/supervisor.conf /etc/supervisor/conf.d/

EXPOSE 80
CMD ["supervisord", "-n"]
