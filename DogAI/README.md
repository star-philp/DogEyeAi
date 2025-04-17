# DogAI - 강아지 눈 건강 검사기

강아지 눈 건강 상태를 분석하는 AI 기반 웹 애플리케이션입니다.

## 기능

- 강아지 눈 이미지 업로드 및 분석
- 결막염 여부 진단
- 히트맵 시각화
- 심각도 평가
- PDF 보고서 생성
- 분석 결과 데이터베이스 저장 및 시각화

## 기술 스택

- Python 3.10
- FastAI / PyTorch
- Streamlit
- PostgreSQL
- Docker

## 배포 방법

### Docker를 사용한 배포

1. Docker와 Docker Compose 설치

2. 프로젝트 클론

   ```bash
   git clone <repository-url>
   cd DogAI
   ```

3. Docker Compose로 실행

   ```bash
   docker-compose up -d
   ```

4. 웹 브라우저에서 접속
   ```
   http://localhost:8501
   ```

## 환경 변수

- `DB_HOST`: 데이터베이스 호스트 (기본값: localhost)
- `DB_PORT`: 데이터베이스 포트 (기본값: 5432)
- `DB_NAME`: 데이터베이스 이름 (기본값: dog_health)
- `DB_USER`: 데이터베이스 사용자 (기본값: rainstar)
- `DB_PASSWORD`: 데이터베이스 비밀번호 (기본값: 12341234)
