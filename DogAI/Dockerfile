# Python 3.10 베이스 이미지 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치 및 캐시 정리
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY . .

# Streamlit 설정 파일 생성
RUN mkdir -p /root/.streamlit && \
    echo '\
    [server]\n\
    address = "0.0.0.0"\n\
    port = 8501\n\
    enableCORS = false\n\
    enableXsrfProtection = false\n\
    maxUploadSize = 200\n\
    \n\
    [browser]\n\
    serverAddress = "0.0.0.0"\n\
    serverPort = 8501\n\
    \n\
    [logger]\n\
    level = "info"\n\
    ' > /root/.streamlit/config.toml

# 포트 노출
EXPOSE 8501

# 환경 변수 설정
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_PORT=8501

# 헬스체크 설정
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 실행 명령
ENTRYPOINT ["streamlit", "run", "Pages/main10+db+visual.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.maxUploadSize=200", \
    "--server.enableCORS=false", \
    "--server.enableXsrfProtection=false"] 