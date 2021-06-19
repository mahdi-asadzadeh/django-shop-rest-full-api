FROM nginx:1.15
LABEL MAINTAINER="Mahdi Asadzadeh | https://mahdiasadzadeh.com | mahdi.asadzadeh.programing@gmail.com"

COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]