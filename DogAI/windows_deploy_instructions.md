# Windows 서버에서 DogAI 배포 방법

## 준비 사항

- Docker Desktop이 설치되어 있어야 합니다.
- 프로젝트 파일(dogai.tar.gz)이 서버에 전송되어 있어야 합니다.

## 배포 단계

### 1. 프로젝트 파일 압축 해제

PowerShell에서 다음 명령을 실행합니다:

```powershell
# 디렉토리 생성
mkdir -p C:\Users\USER\DogAI

# 압축 파일 위치로 이동
cd C:\Users\USER

# 압축 해제
tar -xzf dogai.tar.gz -C DogAI
```

### 2. Docker 이미지 빌드

```powershell
# 프로젝트 디렉토리로 이동
cd C:\Users\USER\DogAI

# Docker 이미지 빌드
docker build -t dogai .
```

### 3. Docker 컨테이너 실행

```powershell
# Docker 컨테이너 실행 (포트 7000을 8501로 매핑)
docker run -d --name dogai_app -p 7000:8501 dogai
```

### 4. 서비스 접속

브라우저에서 다음 URL로 접속합니다:

```
http://192.168.219.176:7000
```

## 문제 해결

### Docker 로그인 문제

Docker Hub에 로그인이 필요한 경우:

```powershell
docker login
```

### 컨테이너 관리

```powershell
# 컨테이너 상태 확인
docker ps

# 컨테이너 중지
docker stop dogai_app

# 컨테이너 제거
docker rm dogai_app

# 컨테이너 로그 확인
docker logs dogai_app
```
