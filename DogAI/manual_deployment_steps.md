# DogAI 수동 배포 가이드

다음 단계는 Windows 서버에서 직접 수행해야 합니다. SSH 연결이 어려울 경우, 이 안내를 따라 직접 Windows 서버에서 작업하세요.

## 1. 사전 준비

1. Windows 서버에 Docker Desktop이 설치되어 있는지 확인하세요.
2. Docker Desktop이 실행 중인지 확인하세요.
3. 필요한 경우 Docker Hub에 로그인하세요.
4. DogAI 프로젝트 파일을 압축한 `dogai.tar.gz` 파일을 Windows 서버로 전송하세요. (예: 이메일, 클라우드 스토리지 등 사용)

## 2. PowerShell 명령어

Windows 서버의 PowerShell을 관리자 권한으로 실행하고 다음 명령어를 순서대로 실행하세요:

### 작업 디렉토리 생성 및 이동

```powershell
# 작업 디렉토리 생성
mkdir -p C:\Users\USER\DogAI

# 압축 파일이 있는 위치로 이동 (다운로드 경로에 따라 조정)
# 예: 다운로드 폴더에 압축 파일이 있는 경우
cd C:\Users\USER\Downloads

# 압축 파일 추출
tar -xzf dogai.tar.gz -C C:\Users\USER\DogAI

# 추출된 디렉토리로 이동
cd C:\Users\USER\DogAI
```

### Docker 이미지 빌드

```powershell
# Docker 이미지 빌드
docker build -t dogai .
```

### Docker 컨테이너 실행

```powershell
# 기존 컨테이너 중지 및 제거 (이미 있는 경우)
docker stop dogai_app 2>$null
docker rm dogai_app 2>$null

# 새 컨테이너 실행
docker run -d --name dogai_app -p 7000:8501 dogai
```

## 3. 애플리케이션 접속

브라우저에서 다음 URL로 접속하세요:

```
http://localhost:7000
```

다른 컴퓨터에서 접속하려면 Windows 서버의 IP 주소를 사용하세요:

```
http://192.168.219.176:7000
```

## 4. 문제 해결

### Docker 빌드 실패

Docker 빌드가 실패하면 다음 문제를 확인하세요:

1. Docker Desktop이 실행 중인지 확인
2. Docker가 로그인 상태인지 확인 (필요한 경우 `docker login` 실행)
3. 빌드 로그 확인:
   ```powershell
   docker build -t dogai . --progress=plain
   ```

### 컨테이너 실행 문제

컨테이너가 실행되지 않는 경우:

```powershell
# 컨테이너 로그 확인
docker logs dogai_app

# 컨테이너 상태 확인
docker ps -a | findstr dogai
```

### 포트 충돌

7000번 포트가 이미 사용 중인 경우 다른 포트로 변경하세요:

```powershell
docker run -d --name dogai_app -p 8000:8501 dogai
```

그리고 `http://localhost:8000` 또는 `http://192.168.219.176:8000`으로 접속하세요.

## 5. 자동화된 배포 스크립트 사용 (PowerShell)

PowerShell 스크립트를 사용하여 배포 과정을 자동화할 수 있습니다:

1. `windows_deploy.ps1` 파일을 Windows 서버의 `C:\Users\USER\DogAI` 디렉토리에 저장합니다.
2. PowerShell을 관리자 권한으로 실행합니다.
3. 다음 명령어를 실행하여 PowerShell 실행 정책을 변경합니다:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
4. 스크립트가 있는 디렉토리로 이동합니다:
   ```powershell
   cd C:\Users\USER\DogAI
   ```
5. 스크립트를 실행합니다:
   ```powershell
   .\windows_deploy.ps1
   ```

이 스크립트는 다음 작업을 자동으로 수행합니다:

- Docker 실행 여부 확인
- 기존 컨테이너 중지 및 제거
- Docker 이미지 빌드
- 새 컨테이너 실행
- 배포 성공 여부 확인 및 접속 URL 안내
