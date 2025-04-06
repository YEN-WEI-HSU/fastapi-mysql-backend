



#!/bin/bash

echo "🛑 關閉 FastAPI（背景啟動）..."
pkill -f "uvicorn main:app" 2>/dev/null

echo "🛑 停止 phpMyAdmin..."
docker stop phpmyadmin && docker rm phpmyadmin

echo "🛑 停止 MySQL..."
docker stop mysql && docker rm mysql

echo "✅ 所有服務已關閉"
