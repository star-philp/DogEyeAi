# DogAI 프로젝트

DogAI는 반려견 이미지 분석 및 시각화 애플리케이션입니다. 이 프로젝트는 Docker를 사용하여 배포할 수 있으며, 로컬 또는 원격 서버에서 실행할 수 있습니다.

## 시스템 요구사항

- Python 3.10
- Docker Desktop (배포 시)
- 최소 4GB RAM
- 최소 20GB 디스크 공간

## 로컬에서 실행하기

1. 가상환경 활성화:

   ```bash
   conda activate dogai_py310
   ```

2. 필요한 패키지 설치:

   ```bash
   ./setup_packages.sh
   ```

3. Streamlit 애플리케이션 실행:

   ```bash
   cd Pages && streamlit run main10+db+visual.py
   ```

4. 브라우저에서 접속:
   ```
   http://localhost:8501
   ```

## Docker 배포 (Windows 서버)

Windows 서버에서 Docker를 사용하여 배포하려면 `manual_deployment_steps.md` 문서의 지침을 따르세요.

### 주요 단계

1. 프로젝트 압축 파일(dogai.tar.gz)을 Windows 서버로 전송
2. Docker 이미지 빌드
3. Docker 컨테이너 실행
4. 브라우저에서 서비스 접속

## 문제 해결

- 데이터베이스 연결 문제
- Docker 빌드 및 실행 오류
- SSH 연결 문제

자세한 문제 해결 방법은 `manual_deployment_steps.md` 문서를 참조하세요.

## 주요 파일

- `Pages/main10+db+visual.py`: 메인 Streamlit 애플리케이션
- `Dockerfile`: Docker 이미지 빌드 설정
- `requirements.txt`: 필요한 Python 패키지
- `setup_packages.sh`: 패키지 설치 스크립트
- `setup_ssh.sh`: SSH 키 설정 스크립트
- `manual_deployment_steps.md`: 수동 배포 가이드

## 주요 기능

- 반려견 이미지 분석을 통한 건강 상태 평가
- 시각적인 데이터 대시보드 제공
- 데이터베이스를 활용한 반려견 정보 관리
- 맞춤형 건강 리포트 생성

## 기술 스택

- **프론트엔드**: Streamlit
- **백엔드**: Python, FastAI
- **데이터베이스**: PostgreSQL
- **배포**: Docker, GitHub Actions
- **이미지 분석**: PyTorch, TorchVision

## 프로젝트 구조

```
DogAI/
├── Pages/                 # 애플리케이션 메인 코드
│   ├── analyzers/         # 이미지 분석 모듈
│   ├── reports/           # 리포트 생성 모듈
│   ├── visualizers/       # 데이터 시각화 모듈
│   └── main10+db+visual.py # 메인 엔트리 포인트
├── .github/workflows/     # GitHub Actions 워크플로우
├── Dockerfile             # Docker 이미지 빌드 설정
├── requirements.txt       # Python 패키지 의존성
└── README.md              # 프로젝트 문서
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 연락처

질문이나 제안이 있으시면 이슈를 등록해주세요.
