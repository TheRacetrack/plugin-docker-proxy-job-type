FROM golang:1.19-alpine

RUN apk add hugo

WORKDIR /src/hugo_site
COPY hugo_site/. /src/hugo_site/

CMD hugo server -D --bind 0.0.0.0 --port 8000

EXPOSE 8000
LABEL racetrack-component="fatman"
