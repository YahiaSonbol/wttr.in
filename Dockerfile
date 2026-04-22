# Build stage
FROM golang:1-alpine AS builder

WORKDIR /app

COPY . /app

RUN apk add --no-cache git build-base

RUN cd /app && CGO_ENABLED=1 CGO_CFLAGS="-D_LARGEFILE64_SOURCE" go build -o wttr.in .


# Application stage
FROM alpine:3.21.1

WORKDIR /app

COPY ./requirements.txt /app

ENV LLVM_CONFIG=/usr/bin/llvm15-config

RUN apk add --no-cache --virtual .build \
    autoconf \
    automake \
    g++ \
    gcc \
    jpeg-dev \
    llvm15-dev\
    make \
    zlib-dev \
    && apk add --no-cache \
    python3 \
    py3-pip \
    py3-scipy \
    py3-wheel \
    py3-gevent \
    zlib \
    jpeg \
    llvm15 \
    libtool \
    supervisor \
    py3-numpy-dev \
    bash \
    python3-dev && \
    mkdir -p /app/cache && \
    mkdir -p /app/log && \
    mkdir -p /var/log/supervisor && \
    mkdir -p /etc/supervisor/conf.d && \
    chmod -R o+rw /var/log/supervisor && \
    chmod -R o+rw /app/log && \
    chmod -R o+rw /var/run && \
    pip install -r requirements.txt --no-cache-dir --break-system-packages && \
    apk del --no-cache -r .build

COPY ./GeoLite2-City.mmdb /app/
COPY ./wwo.key /app/

COPY --from=builder /app/wttr.in /app/bin/wttr.in
COPY ./bin /app/bin
COPY ./lib /app/lib
COPY ./share /app/share
COPY share/docker/supervisord.conf /etc/supervisor/supervisord.conf

ENV WTTR_MYDIR="/app"
ENV WTTR_GEOLITE="/app/GeoLite2-City.mmdb"
ENV WTTR_WEGO="/app/bin/wttr.in"
ENV WTTR_LISTEN_HOST="0.0.0.0"
ENV WTTR_LISTEN_PORT="8002"
ENV WTTR_WWO_KEY_FILE="/app/wwo.key"
ENV WTTR_USER_AGENT="wttr.in/1.0 (https://github.com/chubin/wttr.in; igor@chubin.org)"

EXPOSE 8002

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
