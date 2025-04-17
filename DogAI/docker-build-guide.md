# Windows 서버에서 Docker 빌드 가이드

## Docker 빌드 오류 해결 방법

Windows 서버에서 Docker 이미지 빌드 시 RPC 오류가 발생할 경우 다음 단계를 수행하세요.

### 1. .dockerignore 파일 문제 해결

```powershell
# .dockerignore 파일이 있는 경우 이름 변경 (임시로 비활성화)
Rename-Item .dockerignore .dockerignore.bak
```

### 2. Docker BuildKit 비활성화

Docker Desktop에서 다음과 같이 BuildKit을 비활성화합니다:

1. Docker Desktop 앱 실행
2. 설정(Settings) 메뉴 클릭
3. Docker Engine 탭 선택
4. 다음 설정 추가 또는 수정:
   ```json
   {
     "buildkit": false
   }
   ```
5. Apply & Restart 버튼 클릭

### 3. Windows 서버에서 빌드 및 실행

```powershell
# 1. DogAI 디렉토리로 이동
cd C:\Users\USER\DogAI

# 2. Docker 이미지 빌드
docker build -t dogeyeai .

# 3. Docker 컨테이너 실행 (빌드가 성공적으로 완료된 후)
docker run -d --name dogai_app -p 7000:8501 dogeyeai
```

### 4. 다른 해결 방법

만약 위 방법으로도 문제가 해결되지 않는다면 다음을 시도해보세요:

1. Docker Desktop 재시작
2. 기본 이미지 미리 풀하기
   ```powershell
   docker pull python:3.10-slim
   ```
3. 컴퓨터 재시작
4. Docker 데몬 재시작
   ```powershell
   Restart-Service *docker*
   ```

## 애플리케이션 접속

빌드 및 실행이 성공적으로 완료되면 다음 URL로 접속할 수 있습니다:

```
http://192.168.219.109:7000

```
==============
이제 CI/CD 구성과 Windows 서버의 Docker 빌드 문제 해결 가이드를 작성했습니다. 지금까지 진행한 내용을 정리해드리겠습니다:

1. GitHub Actions CI/CD 파이프라인 설정:
- .github/workflows/docker-build-deploy.yml 파일을 생성하여 CI/CD 워크플로우 설정
- GitHub Secrets에 DOCKER_USERNAME과 DOCKER_PASSWORD 등록 완료
- Docker Hub에 이미지를 자동으로 빌드하고 푸시하도록 구성

2. Windows 서버에서 Docker 빌드 오류 해결 방법:
- .dockerignore 파일 관련 문제 해결
- BuildKit 비활성화 설정
- 다양한 문제 해결 방법을 담은 가이드 문서 작성

# 이제 GitHub에 코드를 푸시하면 GitHub Actions가 자동으로 Docker 이미지를 빌드하고 Docker Hub에 푸시합니다. 그리고 Windows 서버에서는 빌드 가이드 문서를 참고하여 빌드 오류를 해결할 수 있습니다.
추가적인 작업이 필요하거나 질문이 있으시면 알려주세요.
