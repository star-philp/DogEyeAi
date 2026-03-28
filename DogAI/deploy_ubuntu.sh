#!/bin/bash

# Ubuntu 서버 배포 스크립트

# 변수 설정
UBUNTU_SERVER="192.168.219.109"
UBUNTU_USER="woosung"
REMOTE_DIR="/home/woosung/dogai"
SSH_KEY="~/.ssh/id_rsa_ubuntu"

# 압축 파일 생성
echo "프로젝트 파일 압축 중..."
tar --exclude='node_modules' --exclude='.git' --exclude='venv' --exclude='__pycache__' \
    --exclude='*.pyc' --exclude='*.pyo' --exclude='*.pyd' --exclude='.DS_Store' \
    --exclude='dogai_project.tar.gz' -czf dogai_project.tar.gz .

# 원격 디렉토리 생성
echo "원격 디렉토리 확인 중..."
ssh -i $SSH_KEY $UBUNTU_USER@$UBUNTU_SERVER "mkdir -p $REMOTE_DIR"

# 파일 전송
echo "파일 전송 중..."
scp -i $SSH_KEY dogai_project.tar.gz $UBUNTU_USER@$UBUNTU_SERVER:$REMOTE_DIR/

# 원격 서버에서 압축 해제 및 Docker 실행
echo "원격 서버에서 배포 중..."
ssh -i $SSH_KEY $UBUNTU_USER@$UBUNTU_SERVER "cd $REMOTE_DIR && tar -xzf dogai_project.tar.gz && docker-compose down && docker-compose up -d && rm dogai_project.tar.gz"

# 로컬 압축 파일 삭제
echo "로컬 임시 파일 정리 중..."
rm dogai_project.tar.gz

echo "배포 완료!"
echo "애플리케이션은 http://$UBUNTU_SERVER:8501 에서 접근할 수 있습니다." 