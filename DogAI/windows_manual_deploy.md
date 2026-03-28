# Windows 서버 수동 배포 가이드

## 1. 필요한 파일 준비

먼저 로컬 Mac에서 필요한 파일들을 압축합니다:

```bash
tar --exclude='bin' --exclude='include' --exclude='lib' --exclude='__pycache__' \
    --exclude='.git' --exclude='.DS_Store' --exclude='*.pdf' \
    -czf dogai_project.tar.gz \
    Pages models Dockerfile docker-compose.yml requirements.txt README.md .dockerignore
```

## 2. 파일 전송 방법

Windows 서버에 파일을 전송하는 방법은 다음과 같습니다:

### 2.1 USB 드라이브 사용

- 압축 파일을 USB 드라이브에 복사
- Windows 서버에 USB 드라이브 연결
- 파일을 `C:\DogAI` 디렉토리로 복사

### 2.2 웹 기반 파일 공유 서비스 사용

- Dropbox, Google Drive 등에 파일 업로드
- Windows 서버에서 다운로드

### 2.3 네트워크 공유 사용

- Windows 파일 공유 기능 활성화
- 네트워크 드라이브 매핑
- 파일 복사

## 3. Windows 서버에서 실행할 명령어

파일을 서버에 전송한 후, Windows 서버에 직접 접속하여 다음 명령어를 실행하세요:

### 3.1 디렉토리 생성

```cmd
mkdir C:\DogAI
cd C:\DogAI
```

### 3.2 압축 해제 (Git Bash 또는 WSL 사용)

Git Bash를 사용하는 경우:

```bash
tar -xzf dogai_project.tar.gz
```

WSL을 사용하는 경우:

```bash
wsl tar -xzf dogai_project.tar.gz
```

### 3.3 Docker 컨테이너 빌드 및 실행

```cmd
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 3.4 압축 파일 삭제

```cmd
del dogai_project.tar.gz
```

## 4. 배포 확인

배포가 완료된 후, 웹 브라우저에서 다음 URL에 접속하여 애플리케이션이 정상적으로 실행되는지 확인하세요:

```
http://192.168.219.109:8501
```

## 5. 문제 해결 가이드

### 5.1 Docker 관련 문제

Docker 관련 문제가 발생하는 경우:

```powershell
# Docker Desktop 설치 확인
docker --version
docker-compose --version

# Docker Desktop 서비스 확인
Get-Service com.docker.service

# Docker Desktop 재시작
Restart-Service com.docker.service
```

### 5.2 애플리케이션 실행 문제

애플리케이션 실행 문제가 발생하는 경우:

```cmd
# 로그 확인
docker-compose logs app

# 컨테이너 상태 확인
docker ps
docker-compose ps

# 포트 확인
netstat -an | findstr 8501
```

### 5.3 NumPy 및 모듈 관련 문제

로컬 환경에서 발생한 NumPy 및 모듈 관련 문제는 Docker 환경에서는 발생하지 않을 가능성이 높습니다. Docker 컨테이너는 독립적인 환경을 제공하며, `requirements.txt`에 명시된 패키지 버전을 사용합니다.

만약 Docker 환경에서도 문제가 발생한다면, `requirements.txt` 파일에서 NumPy 버전을 1.24.3으로 고정했으므로 문제가 해결될 것입니다.
