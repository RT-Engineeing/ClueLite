# FROM node:16-alpine3.11 AS init
FROM nikolaik/python-nodejs:latest
ENV NODE_ENV=production
WORKDIR /app
COPY ["package.json", "package-lock.json*", "npm-shrinkwrap.json*", "./"]
RUN npm install --production --silent
RUN mv node_modules ../
COPY . .
EXPOSE 3000
EXPOSE 443
# FROM python:3.8-slim-buster
EXPOSE 8080
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
# WORKDIR /app
# COPY --from=init /usr/src/app .
RUN ls -la
COPY . /app
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser
CMD ["sh","startup.sh"]