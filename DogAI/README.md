# Dog Eye Health Checker (DogAI) 🐶

반려견 눈(결막염) 이미지를 업로드하면 AI가 **정상(Negative) / 염증(Positive)** 여부를 진단하고, 심각도 평가·권장사항·PDF 분석 보고서를 제공하는 Streamlit 웹 애플리케이션입니다.

## 주요 기능

- 이미지 업로드 → AI 진단 (Negative/Positive) + 신뢰도 표시
- 심각도 1~10단계 평가 및 진단에 따른 맞춤 권장사항
- PDF 분석 보고서 다운로드
- 히트맵 시각화 (현재는 placeholder 구현)
- (DB 설정 시) 분석 이력 저장 및 시계열/분포 차트 제공

## 기술 스택

- **언어/프레임워크**: Python 3.10, Streamlit
- **AI 모델**: fastai 2.7, PyTorch 2.0 (Negative/Positive 2클래스 분류기)
- **데이터베이스**: PostgreSQL (로컬 또는 Supabase) — *선택*
- **시각화/보고서**: plotly, reportlab, pandas

## 시스템 요구사항

- Python 3.10 (Conda 권장)
- 최소 4GB RAM
- 모델 파일(`models/best_model.pkl`) — Git LFS로 관리됨

## 로컬에서 실행하기

```bash
conda activate dogai_py310

# 최초 1회: Git LFS 모델 파일 복원
git lfs pull

cd DogAI
streamlit run Pages/main10+db+visual.py
```

브라우저에서 접속: `http://localhost:8501`

> **DB 없이도 분석 기능은 동작합니다.** DB 미설정 시 이력 저장만 "데이터베이스가 설정되지 않아" 안내되며, 분석·PDF는 정상 이용할 수 있습니다.

## 데이터베이스 설정 (선택)

분석 이력 저장과 차트를 사용하려면 PostgreSQL이 필요합니다.

### 1. 로컬 PostgreSQL

```sql
CREATE DATABASE dog_health;
CREATE USER rainstar WITH PASSWORD '007008';
GRANT ALL PRIVILEGES ON DATABASE dog_health TO rainstar;
```

### 2. 연결 정보 설정 (`.streamlit/secrets.toml`)

```toml
[database]
DB_HOST = "localhost"          # 로컬 또는 Supabase 호스트
DB_PORT = "5432"
DB_NAME = "dog_health"
DB_USER = "rainstar"
DB_PASSWORD = "007008"
```

> ⚠️ `.streamlit/secrets.toml`은 `.gitignore`에 포함되어 있어 GitHub에 올라가지 않습니다. 클라우드 배포 시에는 Streamlit Cloud의 **Secrets** 설정에 동일 내용을 입력하세요.

### 3. 클라우드 DB (Supabase) 사용 시

Supabase에서 프로젝트를 생성한 뒤 `.streamlit/secrets.toml`의 `DB_HOST`/`DB_PASSWORD` 등을 연결 정보로 교체하세요.

## 클라우드 배포 (Streamlit Community Cloud)

1. 코드를 GitHub에 push합니다. (모델 파일은 Git LFS로 관리)
2. [share.streamlit.io](https://share.streamlit.io)에 GitHub 계정으로 로그인합니다.
3. 앱 설정:
   - Repository: `star-philp/DogEyeAi`
   - Branch: `main`
   - Main file path: `DogAI/Pages/main10+db+visual.py`
4. (선택) Advanced settings → Secrets에 `[database]` 섹션 입력 → DB 연동
5. **Deploy** 클릭 후 배포 완료 시 공개 URL 확인 (첫 배포는 의존성 설치로 10~20분 소요)

## Docker 배포 (Windows 서버)

Windows 11 + Docker Desktop 환경에서 배포하려면 `docker-compose.yml`(앱 + PostgreSQL 컨테이너)을 사용하세요. 자세한 방법은 `manual_deployment_steps.md`를 참고하세요.

```bash
docker compose up -d --build
```

## 프로젝트 구조

```
DogAI/
├── Pages/                    # 애플리케이션 메인 코드
│   ├── main10+db+visual.py   # 메인 엔트리 포인트
│   ├── db_handler.py         # DB 연결/저장 모듈
│   ├── analyzers/            # 진단·심각도 분석 모듈
│   ├── reports/              # PDF 리포트 생성 모듈
│   └── visualizers/          # plotly 시각화 모듈
├── models/best_model.pkl     # AI 모델 (Git LFS)
├── images/                   # 샘플 이미지
├── .streamlit/secrets.toml   # DB 연결 정보 (gitignore)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 문제 해결

| 증상 | 해결 방법 |
|---|---|
| `Model file not found` | `git lfs pull`로 모델 파일 복원 |
| `Database connection failed` | Supabase 프로젝트가 삭제/일시정지된 경우 → 새 프로젝트 생성 후 secrets 갱신 |
| Negative인데 "진료 필요"로 표시 | 코드가 오래된 버전인 경우 → 최신 코드 pull |
| 클라우드 앱이 수면 상태 | 접속 후 버튼을 한 번 클릭해 깨우기 |

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
