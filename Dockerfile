FROM ubuntu:22.04
USER root
RUN apt-get -y update
RUN apt-get install -y python3.13 \
    && apt-get install -y python3-pip \
    && apt-get install -y nginx \
    && apt-get install ca-certificates

WORKDIR /opt/program

COPY . .

ENV PATH="/opt/program:${PATH}"
RUN chmod +x /entrypoint.sh


RUN python3.13 -m pip install uv
RUN uv add -r requirements.txt

EXPOSE 8443
CMD ["sh", "entrypoint.sh"]