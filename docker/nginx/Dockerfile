FROM nginx:1.15.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/nginx.conf

CMD ["nginx", "-g", "daemon off;"]