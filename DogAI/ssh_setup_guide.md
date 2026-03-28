# SSH 설정 및 배포 가이드

## 서버 정보

- **Windows 11 서버**:

  - IP: 192.168.219.176
  - 포트: 2222
  - 사용자: USER
  - 비밀번호: 007008

- **Ubuntu 24.0 서버**:
  - 사용자: woosung
  - 비밀번호: 007008

## 1. SSH 키 생성 및 설정

### Windows 서버용 SSH 키 설정

1. **SSH 키 생성**:

   ```bash
   ./setup_ssh.sh
   ```

   또는 수동으로:

   ```bash
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_windows -N ""
   ```

2. **공개 키 확인**:

   ```bash
   cat ~/.ssh/id_rsa_windows.pub
   ```

3. **Windows 서버에 키 설정**:
   - Windows 서버에 직접 접속
   - `C:\Users\USER\.ssh` 디렉토리 생성
   - `C:\Users\USER\.ssh\authorized_keys` 파일 생성 후 공개 키 내용 붙여넣기
   - 권한 설정:
     ```powershell
     icacls "C:\Users\USER\.ssh\authorized_keys" /inheritance:r /grant "USER:F"
     ```

### Ubuntu 서버용 SSH 키 설정

1. **SSH 키 생성**:

   ```bash
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_ubuntu -N ""
   ```

2. **공개 키 복사**:
   ```bash
   ssh-copy-id -i ~/.ssh/id_rsa_ubuntu woosung@[Ubuntu-서버-IP]
   ```

## 2. SSH 설정 파일 구성

`~/.ssh/config` 파일에 다음 내용 추가:

```
Host windows-server
    HostName 192.168.219.176
    User USER
    Port 2222
    IdentityFile ~/.ssh/id_rsa_windows
    PreferredAuthentications publickey,password

Host ubuntu-server
    HostName [Ubuntu-서버-IP]
    User woosung
    IdentityFile ~/.ssh/id_rsa_ubuntu
    PreferredAuthentications publickey,password
```

## 3. 연결 테스트

### Windows 서버 연결

```bash
ssh -i ~/.ssh/id_rsa_windows -p 2222 USER@192.168.219.176
```

또는 설정 파일 사용:

```bash
ssh windows-server
```

### Ubuntu 서버 연결

```bash
ssh -i ~/.ssh/id_rsa_ubuntu woosung@[Ubuntu-서버-IP]
```

또는 설정 파일 사용:

```bash
ssh ubuntu-server
```

## 4. 애플리케이션 배포

### 패키지 설치

로컬에서 필요한 패키지 설치:

```bash
./setup_packages.sh
```

### Windows 서버 배포

```bash
./deploy_windows.sh
```

### Ubuntu 서버 배포

Ubuntu 서버 IP 주소 설정 후:

```bash
./deploy_ubuntu.sh
```

## 5. 문제 해결

### NumPy 호환성 문제

NumPy 2.x와 호환성 문제가 있는 경우:

```bash
pip install numpy==1.24.3
```

### 누락된 패키지 설치

필요한 패키지가 누락된 경우:

```bash
pip install reportlab plotly
```

### Docker 컨테이너 관리

```bash
# 컨테이너 상태 확인
docker ps

# 컨테이너 재시작
docker-compose restart app

# 컨테이너 중지 및 제거
docker-compose down

# 컨테이너 시작
docker-compose up -d
```

### 로그 확인

```bash
# 애플리케이션 로그
docker logs dogai_app

# 데이터베이스 로그
docker logs dogai_db
```
