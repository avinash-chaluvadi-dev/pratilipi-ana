#stage 1

FROM sit1-dtr.anthem.com/core/nodebase:1.0.0 as react-build
USER root
COPY  / ./codebase
WORKDIR /codebase
RUN npm install
#RUN node --expose-gc --max-old-space-size=4096 node_modules/react-scripts/scripts/build.js
RUN npm run build

#stage 2
FROM sit1-dtr.anthem.com/core/nginx-alpine:2.0.0
RUN rm -rf /usr/share/nginx/html/*
#COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=react-build /codebase/build /usr/share/nginx/html/vmt-soa-webapp
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
#CMD ["/bin/sh",  "-c" ] >> /logs/$APP_NAME.$(hostname).log 2>&1
