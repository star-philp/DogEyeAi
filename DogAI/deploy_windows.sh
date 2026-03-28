#!/bin/bash

# Windows 서버 배포 스크립트

# 변수 설정
WINDOWS_SERVER="192.168.219.109"
WINDOWS_PORT="2222"
WINDOWS_USER="USER"
REMOTE_DIR="C:/dogai"
SSH_KEY="~/.ssh/id_rsa_windows"

# 압축 파일 생성
echo "프로젝트 파일 압축 중..."
tar --exclude='node_modules' --exclude='.git' --exclude='venv' --exclude='__pycache__' \
    --exclude='*.pyc' --exclude='*.pyo' --exclude='*.pyd' --exclude='.DS_Store' \
    --exclude='dogai_project.tar.gz' -czf dogai_project.tar.gz .

# 원격 디렉토리 생성 (없는 경우)
echo "원격 디렉토리 확인 중..."
ssh -i $SSH_KEY -p $WINDOWS_PORT $WINDOWS_USER@$WINDOWS_SERVER "if not exist $REMOTE_DIR mkdir $REMOTE_DIR"

# 파일 전송
echo "파일 전송 중..."
scp -i $SSH_KEY -P $WINDOWS_PORT dogai_project.tar.gz $WINDOWS_USER@$WINDOWS_SERVER:$REMOTE_DIR/

# 원격 서버에서 압축 해제 및 Docker 실행
echo "원격 서버에서 배포 중..."
ssh -i $SSH_KEY -p $WINDOWS_PORT $WINDOWS_USER@$WINDOWS_SERVER "cd $REMOTE_DIR && tar -xzf dogai_project.tar.gz && docker-compose down && docker-compose up -d && del dogai_project.tar.gz"

# 로컬 압축 파일 삭제
echo "로컬 임시 파일 정리 중..."
rm dogai_project.tar.gz

echo "배포 완료!"
echo "애플리케이션은 http://$WINDOWS_SERVER:8501 에서 접근할 수 있습니다." 