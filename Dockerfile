# 숙제 도우미 챗봇 이미지: 앱과 모델 설정 (model.json)을 함께 넣습니다
FROM python:3.12-slim
WORKDIR /app
COPY app.py model.json ./
EXPOSE 8000
CMD ["python", "app.py"]
