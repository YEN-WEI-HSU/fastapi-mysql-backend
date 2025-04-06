#!/bin/bash

echo " 啟動 MySQL 容器..."
docker run -d \
  --name mysql \
  -e MYSQL_ROOT_PASSWORD=root123 \
  -e MYSQL_DATABASE=testdb \
  -e MYSQL_USER=testuser \
  -e MYSQL_PASSWORD=test123 \
  -p 3306:3306 \
  -v mysql-data:/var/lib/mysql \
  mysql:8.0

echo " 啟動 phpMyAdmin 容器..."
docker run -d \
  --name phpmyadmin \
  --link mysql \
  -e PMA_HOST=mysql \
  -e PMA_USER=testuser \
  -e PMA_PASSWORD=test123 \
  -p 8080:80 \
  phpmyadmin/phpmyadmin

echo " 啟動 FastAPI（使用 pipenv）..."
cd ~/dev-projects/fastapi-mysql-backend/fastapi-backend/
pipenv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

echo " 一鍵部署完成！"
echo " FastAPI:     http://localhost:8000/docs"
echo " phpMyAdmin: http://localhost:8080"
