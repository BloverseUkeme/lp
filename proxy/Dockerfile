FROM  nginx:1.19.2-alpine 


RUN mkdir -p /etc/nginx/ssl

COPY bloverse.com.crt /etc/nginx/ssl
COPY bloverse.com.key /etc/nginx/ssl

RUN chmod 777 /etc/nginx/ssl/bloverse.com.crt
RUN chmod 777 /etc/nginx/ssl/bloverse.com.key
# RUN update-ca-certificates


COPY conf /etc/nginx/conf.d/default.conf 