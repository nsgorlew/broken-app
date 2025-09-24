#!/bin/bash

# auto generate SSL certs
mkdir -p /opt/program/config
rm -rf /opt/program/config/*.pem

openssl req \
    -x509 \
    -newkey rsa:2048 \
    -keyout /opt/program/config/key.pem \
    -out /opt/program/config/cert.pem \
    -days 365 \
    -nodes \
    -sub "/C=TR/ST=Ankara/L=Ankara/O=Tekniko Yazılım Çözümleri/OU=Engineering/CN=tekniko.local"

ls -l /opt/program/config/*.pem

echo "injecting CONTEXTROOTPATH into nginx.conf"
if ["CONTEXTROOTPATH" == ""]; then
  CONTEXTROOTPATH="/"
fi
sed "s|CONTEXTROOTPATH|$CONTEXTROOTPATH|g" /opt/program/nginx.conf.template > /opt/program/nginx.conf

export PYTHONPATH=/opt/program/:/opt/program/pylib:/opt/program/appß

cd /opt/program/src
uv run serve.py
