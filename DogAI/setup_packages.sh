#!/bin/bash

# DogAI 애플리케이션 패키지 설치 스크립트

echo "DogAI 애플리케이션 패키지 설치를 시작합니다..."

# Conda 환경 활성화
source ~/opt/anaconda3/etc/profile.d/conda.sh
conda activate dogai_py310

# NumPy 다운그레이드 (호환성 문제 해결)
echo "NumPy 다운그레이드 중..."
pip install numpy==1.24.3

# 필수 패키지 설치
echo "필수 패키지 설치 중..."
pip install reportlab plotly

# 추가 패키지 설치
echo "추가 패키지 설치 중..."
pip install -r requirements.txt

# Watchdog 설치 (Streamlit 성능 향상)
echo "Watchdog 설치 중..."
xcode-select --install || true
pip install watchdog

echo "패키지 설치가 완료되었습니다."
echo "이제 다음 명령으로 애플리케이션을 실행할 수 있습니다:"
echo "cd Pages && conda activate dogai_py310 && streamlit run main10+db+visual.py" 