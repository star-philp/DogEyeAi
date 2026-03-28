# DogAI 프로젝트 주요 정보

이 문서는 DogAI 프로젝트의 주요 기술 스택, 설정 방법, 실행 방법 등 핵심 정보를 담고 있습니다.

## 1. 프로젝트 개요

- **목표**: 반려견 건강 상태 분석 및 시각화를 위한 AI 기반 웹 애플리케이션.
- **주요 기능**: `analysis_results` 테이블을 보면, 특정 상태(예: 'Positive')를 분류하고 그 결과를 저장 및 시각화하는 것으로 보입니다.

## 2. 기술 스택

- **언어**: Python 3.10
- **프레임워크**: Streamlit (웹 UI)
- **데이터베이스**: PostgreSQL
- **주요 라이브러리**: Pandas (데이터 처리)
- **환경 관리**: Conda

## 3. 개발 환경 설정

1.  **Conda 가상환경 생성**:

    ```bash
    conda create -n dogai_py310 python=3.10 -y
    ```

2.  **가상환경 활성화**:

    ```bash
    conda activate dogai_py310
    ```

3.  **필요 라이브러리 설치**:
    프로젝트에 필요한 라이브러리(streamlit, pandas, psycopg2-binary 등)를 설치해야 합니다. `requirements.txt` 파일이 있다면 아래 명령어를 사용하세요. 없다면 생성하는 것을 권장합니다.
    ```bash
    # requirements.txt가 있는 경우
    pip install -r requirements.txt
    ```

## 4. 애플리케이션 실행

1.  **`Pages` 디렉토리로 이동**:

    ```bash
    cd Pages
    ```

2.  **Streamlit 앱 실행**:

    ```bash
    streamlit run main10+db+visual.py
    ```

3.  **실행 옵션 (포트 지정 등)**:

    ```bash
    streamlit run main10+db+visual.py --server.port 8502
    ```

4.  **접속 URL**:
    - [http://localhost:8502](http://localhost:8502)

## 5. 데이터베이스 정보

- **DB 종류**: PostgreSQL
- **DB 이름**: `dog_health`
- **사용자**: `rainstar`
- **주요 테이블**: `analysis_results`
- **DB 설정**:
  - `command.txt` 파일에 사용자 생성 및 권한 부여 SQL이 포함되어 있습니다.
  ```sql
  CREATE DATABASE dog_health;
  CREATE USER rainstar WITH PASSWORD 'your_password'; -- 보안을 위해 패스워드 확인 필요
  GRANT ALL PRIVILEGES ON DATABASE dog_health TO rainstar;
  ```
- **도커 환경(Windows) DB 연결 주의사항**: 
  - Windows 기반 Docker 환경 구동 시, 앱 컨테이너(`dogai_app`)와 DB 컨테이너(`dogai_db`)가 각각 구동되어 DNS를 찾지 못하는 문제가 있습니다.
  - 이를 해결하기 위해 앱 내 파이썬 코드(`Pages/db_handler.py`)는 `host.docker.internal` 주소와 `5433` (포워딩된 호스트 포트)를 사용하여 윈도우 본체를 거쳐 DB 컨테이너로 접속하도록 설정되어 있습니다.

## 6. 주요 파일

- `Pages/main10+db+visual.py`: Streamlit 애플리케이션의 메인 실행 파일.
- `Pages/db_handler.py`: 데이터베이스 연결 및 쿼리를 처리하는 모듈.

## 7. 향후 개선 방향

- **SQLAlchemy 사용**: 현재 `db_handler.py`에서 `pandas.read_sql` 사용 시 SQLAlchemy 사용을 권장하는 경고가 발생합니다. 향후 성능 및 안정성을 위해 SQLAlchemy로 마이그레이션하는 것을 고려해볼 수 있습니다.
- **SOLID 원칙 적용**: 코드의 유지보수성과 확장성을 높이기 위해 SOLID 원칙을 적용하는 것을 권장합니다. 예를 들어, `db_handler.py`에서 데이터베이스 연결, 데이터 조회, 데이터 변경 등 각기 다른 책임을 갖는 기능들을 별도의 클래스나 함수로 분리하여 단일 책임 원칙(SRP)을 따를 수 있습니다.
- **Streamlit 캐시 관리**: 앱 동작에 문제가 있을 경우 Streamlit 캐시를 지우는 것이 도움이 될 수 있습니다.
  ```bash
  rm -rf ~/.streamlit/cache
  ```
