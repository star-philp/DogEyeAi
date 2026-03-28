# Ubuntu 서버 SSH 연결 가이드

## 서버 정보

- 서버: Ubuntu 24.0
- 사용자: woosung
- 비밀번호: 007008

## SSH 연결 설정

### 1. SSH 키 생성

맥에서 Ubuntu 서버 연결용 SSH 키를 생성합니다:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_ubuntu -N ""
```

생성된 키는 다음 위치에 저장됩니다:

- 개인 키: `~/.ssh/id_rsa_ubuntu`
- 공개 키: `~/.ssh/id_rsa_ubuntu.pub`

### 2. 공개 키 복사

Ubuntu 서버에 공개 키를 복사합니다:

```bash
ssh-copy-id -i ~/.ssh/id_rsa_ubuntu woosung@[Ubuntu-서버-IP]
```

또는 수동으로 설정:

1. 공개 키 내용 확인:

   ```bash
   cat ~/.ssh/id_rsa_ubuntu.pub
   ```

2. Ubuntu 서버에 접속하여 다음 작업 수행:
   ```bash
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   echo "공개키내용" >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   ```

### 3. SSH 연결 테스트

키 기반 인증으로 연결:

```bash
ssh -i ~/.ssh/id_rsa_ubuntu woosung@[Ubuntu-서버-IP]
```

비밀번호 인증으로 연결:

```bash
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no woosung@[Ubuntu-서버-IP]
```

### 4. SSH 설정 파일 구성

`~/.ssh/config` 파일에 다음 내용 추가:

```
Host ubuntu-server
    HostName [Ubuntu-서버-IP]
    User woosung
    IdentityFile ~/.ssh/id_rsa_ubuntu
    PreferredAuthentications publickey,password
```

이후 다음 명령으로 간편하게 연결:

```bash
ssh ubuntu-server
```

## 문제 해결

### 1. 연결 거부 문제

Ubuntu 서버에서 다음 설정 확인:

```bash
sudo nano /etc/ssh/sshd_config
```

다음 설정이 활성화되어 있는지 확인:

```
PasswordAuthentication yes
PubkeyAuthentication yes
```

설정 변경 후 SSH 서비스 재시작:

```bash
sudo systemctl restart sshd
```

### 2. 방화벽 설정

Ubuntu 서버에서 SSH 포트가 열려있는지 확인:

```bash
sudo ufw status
```

필요시 SSH 포트 허용:

```bash
sudo ufw allow ssh
sudo ufw enable
```

### 3. 로그 확인

연결 문제 발생 시 로그 확인:

```bash
sudo tail -f /var/log/auth.log
```

## Ubuntu 서버 배포

DogAI 애플리케이션을 Ubuntu 서버에 배포하려면:

1. 배포 스크립트 생성:

   ```bash
   nano deploy_ubuntu.sh
   ```

2. 다음 내용 추가:

   ```bash
   #!/bin/bash

   # 변수 설정
   UBUNTU_SERVER="[Ubuntu-서버-IP]"
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
   ```

3. 스크립트에 실행 권한 부여:

   ```bash
   chmod +x deploy_ubuntu.sh
   ```

4. 배포 실행:
   ```bash
   ./deploy_ubuntu.sh
   ```
