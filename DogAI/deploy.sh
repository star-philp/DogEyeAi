#!/bin/bash

# 변수 설정 - Windows 11 서버 정보
WIN_SERVER="USER@192.168.219.109"  # 사용자 이름을 USER로 수정
WIN_PORT="22"
WIN_REMOTE_DIR="C:/DogAI"  # Windows 경로 형식으로 수정
WIN_PASSWORD="R@instar64"  # Windows 서버 비밀번호

# 변수 설정 - Ubuntu 24.04 서버 정보
UBUNTU_SERVER="woosung@192.168.219.109"
UBUNTU_PORT="2222"
UBUNTU_REMOTE_DIR="/home/woosung/dogai"  # Ubuntu 서버의 실제 경로로 수정
UBUNTU_PASSWORD="woosung"  # Ubuntu 서버 비밀번호

# SSH 키 경로 설정 (기본값은 ~/.ssh/id_rsa)
SSH_KEY="$HOME/.ssh/id_rsa"

# 배포할 서버 선택 (win 또는 ubuntu)
SERVER_TYPE="ubuntu"  # 기본값을 Ubuntu로 변경

# 명령줄 인수로 서버 타입 받기
if [ "$1" == "win" ]; then
    SERVER_TYPE="win"
    echo "Windows 서버로 배포합니다..."
else
    echo "Ubuntu 서버로 배포합니다..."
fi

# SSH 키 존재 여부 확인
if [ ! -f "$SSH_KEY" ]; then
    echo "SSH 키가 존재하지 않습니다. 새로운 SSH 키를 생성합니다..."
    ssh-keygen -t rsa -b 4096 -f "$SSH_KEY" -N ""
    
    echo "생성된 SSH 키를 서버에 복사합니다..."
    if [ "$SERVER_TYPE" == "ubuntu" ]; then
        ssh-copy-id -i "$SSH_KEY" -p $UBUNTU_PORT $UBUNTU_SERVER
    else
        ssh-copy-id -i "$SSH_KEY" -p $WIN_PORT $WIN_SERVER
    fi
fi

# sshpass 설치 확인
if ! command -v sshpass &> /dev/null; then
    echo "sshpass가 설치되어 있지 않습니다. 설치를 진행합니다..."
    brew install sshpass
fi

# 필요한 파일들 압축
echo "프로젝트 파일 압축 중..."
tar --exclude='bin' --exclude='include' --exclude='lib' --exclude='__pycache__' \
    --exclude='.git' --exclude='.DS_Store' --exclude='*.pdf' \
    -czf dogai_project.tar.gz \
    Pages models Dockerfile docker-compose.yml requirements.txt README.md .dockerignore

# 선택된 서버로 파일 전송 및 배포
if [ "$SERVER_TYPE" == "ubuntu" ]; then
    # Ubuntu 서버로 파일 전송
    echo "Ubuntu 서버로 파일 전송 중..."
    sshpass -p "$UBUNTU_PASSWORD" scp -P $UBUNTU_PORT -o StrictHostKeyChecking=no dogai_project.tar.gz $UBUNTU_SERVER:$UBUNTU_REMOTE_DIR/

    # SSH로 Ubuntu 서버에 접속하여 배포 명령 실행
    echo "Ubuntu 서버에서 배포 명령 실행 중..."
    sshpass -p "$UBUNTU_PASSWORD" ssh -p $UBUNTU_PORT -o StrictHostKeyChecking=no $UBUNTU_SERVER << EOF
        # 디렉토리가 없으면 생성
        mkdir -p $UBUNTU_REMOTE_DIR
        cd $UBUNTU_REMOTE_DIR
        tar -xzf dogai_project.tar.gz
        
        # Docker 및 Docker Compose 설치 확인
        if ! command -v docker &> /dev/null; then
            echo "Docker가 설치되어 있지 않습니다. 설치를 진행합니다..."
            sudo apt-get update
            sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
            sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu \$(lsb_release -cs) stable"
            sudo apt-get update
            sudo apt-get install -y docker-ce
            sudo usermod -aG docker \$USER
        fi
        
        if ! command -v docker-compose &> /dev/null; then
            echo "Docker Compose가 설치되어 있지 않습니다. 설치를 진행합니다..."
            sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-\$(uname -s)-\$(uname -m)" -o /usr/local/bin/docker-compose
            sudo chmod +x /usr/local/bin/docker-compose
        fi
        
        # Docker 컨테이너 빌드 및 실행
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        
        # 압축 파일 삭제
        rm dogai_project.tar.gz
        
        echo "Ubuntu 서버 배포 완료!"
        echo "애플리케이션 접속 URL: http://192.168.219.109:8501"
EOF
else
    # Windows 서버로 파일 전송
    echo "Windows 서버로 파일 전송 중..."
    
    # Windows 명령어로 디렉토리 생성 (mkdir -p 대신 if not exist + md 사용)
    sshpass -p "$WIN_PASSWORD" ssh -p $WIN_PORT -o StrictHostKeyChecking=no $WIN_SERVER "if not exist C:\\DogAI md C:\\DogAI"
    
    # 파일 전송
    sshpass -p "$WIN_PASSWORD" scp -P $WIN_PORT -o StrictHostKeyChecking=no dogai_project.tar.gz $WIN_SERVER:$WIN_REMOTE_DIR/

    # SSH로 Windows 서버에 접속하여 배포 명령 실행
    echo "Windows 서버에서 배포 명령 실행 중..."
    sshpass -p "$WIN_PASSWORD" ssh -p $WIN_PORT -o StrictHostKeyChecking=no $WIN_SERVER << EOF
        cd $WIN_REMOTE_DIR
        
        # Windows에서 tar 명령어가 있는지 확인하고 압축 해제
        where tar >nul 2>&1 && (
            tar -xzf dogai_project.tar.gz
        ) || (
            echo "tar 명령어를 찾을 수 없습니다. Git Bash 또는 WSL을 통해 압축을 해제해주세요."
        )
        
        # Docker 명령어 실행
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        
        # 압축 파일 삭제
        del dogai_project.tar.gz
        
        echo "Windows 서버 배포 완료!"
        echo "애플리케이션 접속 URL: http://192.168.219.109:8501"
EOF
fi

# 로컬 압축 파일 삭제
rm dogai_project.tar.gz

echo "배포 스크립트 실행 완료!" 