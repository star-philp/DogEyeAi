# DogAI 배포 요약

## 업데이트된 서버 정보

- **Windows 11 서버**:
  - IP 주소: 192.168.219.176 (이전: 192.168.1.100)
  - SSH 포트: 2222
  - 사용자: USER
  - 비밀번호: 007008

## 배포 방법 (Windows)

프로젝트 배포를 위한 두 가지 방법을 구현했습니다:

### 1. 수동 배포 방법

`manual_deployment_steps.md` 파일에 상세한 단계가 설명되어 있습니다:

1. dogai.tar.gz 파일을 Windows 서버로 전송
2. 압축 해제
3. Docker 이미지 빌드
4. Docker 컨테이너 실행
5. 웹 브라우저에서 접속

### 2. 자동화된 배포 스크립트 (권장)

`windows_deploy.ps1` PowerShell 스크립트를 사용하여 배포 과정을 자동화할 수 있습니다:

1. 스크립트 파일을 Windows 서버의 `C:\Users\USER\DogAI` 디렉토리에 저장
2. PowerShell을 관리자 권한으로 실행
3. 실행 정책 변경: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
4. 스크립트 실행: `.\windows_deploy.ps1`

## 변경된 설정 파일

다음 파일들이 새로운 IP 주소로 업데이트되었습니다:

1. ssh_setup_guide.md
2. setup_ssh.sh
3. manual_deployment_steps.md
4. windows_deploy_instructions.md
5. windows_deploy.ps1

## 애플리케이션 접속

배포가 완료되면 다음 URL로 접속할 수 있습니다:

- 서버 내부에서: http://localhost:7000
- 외부에서: http://192.168.219.176:7000

## 문제 해결

- SSH 연결 문제: 방화벽 설정 및 SSH 서비스 상태 확인
- Docker 빌드 실패: Docker Desktop이 실행 중인지 확인
- 포트 충돌: 필요한 경우 포트 번호 변경 (7000 → 다른 포트)
- 로그 확인: `docker logs dogai_app` 명령으로 컨테이너 로그 확인

## 다음 단계

1. Windows 서버에서 `windows_deploy.ps1` 스크립트 실행
2. 애플리케이션 접속 및 정상 작동 확인
3. 필요한 경우 Docker 설정 조정
