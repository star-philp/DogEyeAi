# SSH 연결 가이드

## 문제 상황

- 맥에서 서버로 SSH 연결 시도 중 인증 실패
- 서버 정보가 혼동되었음:
  - Windows 11 서버 (192.168.219.109): 사용자 계정은 'USER'
  - Ubuntu 24.0 서버: 사용자 계정은 'woosung'

## 해결 방법

### 1. Windows 11 서버 연결 (USER 계정)

Windows 서버에 직접 접속하여 다음 단계를 수행하세요:

1. **OpenSSH 서버 설정 확인**

   - 관리자 권한으로 PowerShell 실행
   - 다음 명령으로 OpenSSH 서버 상태 확인:
     ```powershell
     Get-Service sshd
     ```
   - 실행 중이 아니라면 다음 명령으로 시작:
     ```powershell
     Start-Service sshd
     Set-Service -Name sshd -StartupType 'Automatic'
     ```

2. **사용자 계정 확인**

   - 다음 명령으로 현재 사용자 확인:
     ```powershell
     whoami
     ```
   - 'USER' 계정이 존재하는지 확인:
     ```powershell
     Get-LocalUser
     ```

3. **SSH 설정 파일 확인**

   - `C:\ProgramData\ssh\sshd_config` 파일 열기
   - 다음 설정이 활성화되어 있는지 확인:
     ```
     PasswordAuthentication yes
     PubkeyAuthentication yes
     ```

4. **SSH 키 설정**

   - `C:\Users\USER\.ssh` 디렉토리 생성 (없는 경우)
   - `C:\Users\USER\.ssh\authorized_keys` 파일 생성
   - 맥에서 생성한 공개 키 내용을 이 파일에 붙여넣기
   - 파일 권한 설정:
     ```powershell
     icacls "C:\Users\USER\.ssh\authorized_keys" /inheritance:r /grant "USER:F"
     ```

5. **SSH 서비스 재시작**
   ```powershell
   Restart-Service sshd
   ```

### 2. Ubuntu 24.0 서버 연결 (woosung 계정)

Ubuntu 서버에 연결하려면:

1. **SSH 키 생성**

   - 터미널에서 다음 명령 실행:
     ```bash
     ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_ubuntu -N ""
     ```
   - 생성된 공개 키를 Ubuntu 서버에 복사:
     ```bash
     ssh-copy-id -i ~/.ssh/id_rsa_ubuntu woosung@192.168.219.109
     ```

2. **SSH 연결 시도**
   - 키 기반 인증:
     ```bash
     ssh -i ~/.ssh/id_rsa_ubuntu woosung@192.168.219.109
     ```
   - 비밀번호 인증:
     ```bash
     ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no woosung@192.168.219.109
     ```

### 3. 맥에서 설정

1. **SSH 설정 파일 수정**

   - `~/.ssh/config` 파일 편집:

     ```
     Host windows-server
         HostName 192.168.219.109
         User USER
         Port 2222
         IdentityFile ~/.ssh/id_rsa_windows
         PreferredAuthentications publickey,password

     Host ubuntu-server
         HostName 192.168.219.109
         User woosung
         IdentityFile ~/.ssh/id_rsa_ubuntu
         PreferredAuthentications publickey,password
     ```

   - 이후 다음 명령으로 연결:
     ```bash
     ssh windows-server
     # 또는
     ssh ubuntu-server
     ```

## 추가 문제 해결

### 방화벽 설정

Windows 서버에서 방화벽이 SSH 연결을 차단할 수 있습니다:

1. Windows 방화벽 설정 열기
2. '인바운드 규칙' 선택
3. '새 규칙' 클릭
4. '포트' 선택 후 '다음'
5. 'TCP' 선택 및 '특정 로컬 포트' 2222 입력
6. '연결 허용' 선택
7. 모든 프로필 선택
8. 이름 입력 (예: 'SSH 2222') 후 완료

### 사용자 계정 설정

Windows에서 SSH 사용자 계정 설정:

1. 로컬 사용자 및 그룹 관리자 열기
2. 'USER' 계정 속성 확인
3. 비밀번호 만료 여부 확인
4. 계정 잠금 상태 확인

### 로그 확인

Windows 서버에서 SSH 로그 확인:

```powershell
Get-WinEvent -LogName "OpenSSH/Operational"
```

## 배포 스크립트 수정

SSH 연결이 성공하면 `deploy_windows.sh` 스크립트를 수정하여 Windows 서버에 배포할 수 있습니다.

============== # 로컬 네트워크 연결 문제 해결 가이드
'http://192.168.219.105:8501' 연결이 안 되는 원인은 여러 가지가 있을 수 있습니다. 아래는 주요 원인과 이를 확인하는 명령어들입니다.

1. 서버 상태 확인
Streamlit 서버 실행 상태 확인

Streamlit 서버 실행 상태 확인
>> ps aux | grep streamlit

이 명령어는 현재 실행 중인 streamlit 프로세스를 보여줍니다. 서버가 실행 중인지 확인할 수 있습니다.
포트 사용 상태 확인
> lsof -i :8501

2. 네트워크 연결 확인
네트워크 인터페이스 확인
>> ifconfig | grep inet
현재 IP 주소를 확인합니다. 192.168.219.105가 정확한 IP인지 확인하세요.

# 방화벽 상태 확인
>>sudo pfctl -s rules
Mac의 방화벽 규칙을 확인합니다. 8501 포트가 차단되어 있을 수 있습니다.

# 포트 연결 테스트
>>nc -vz localhost 8501

3. 애플리케이션 로그 확인
Streamlit 로그 확인
로그에서 "Socket is not connected" 오류가 나타나는 것을 볼 수 있습니다. 이는 클라이언트와 서버 간의 연결이 끊어졌음을 의미합니다.

패키지 의존성 확인
>>>conda list
>>pip list

4. 문제 해결 방법
Streamlit 서버 재시작

>>cd Pages
>>conda activate dogai_py310
>>pkill -f streamlit
>> streamlit run main10+db+visual.py


Streamlit 서버를 중지하고 다시 시작합니다.
포트 변경
>>cd Pages
>>conda activate dogai_py310
>>streamlit run main10+db+visual.py --server.port=8502

# Docker 컨테이너 상태 확인 (Docker 사용 시)
docker ps
docker logs dogai_app
Docker 컨테이너가 실행 중인지, 로그에 오류가 있는지 확인합니다.

# 서버-클라이언트 연결 테스트
curl http://localhost:8501

5. 네트워크 설정 문제 확인
netstat -rn
네트워크 라우팅이 올바르게 설정되어 있는지 확

# 다른 장치에서 서버 연결 테스트
다른 장치에서 브라우저를 열고 http://192.168.219.105:8501에 접속해 보세요. 연결이 되는지 확인합니다.
로그에서 볼 수 있듯이 NumPy 2.x 호환성 문제, 누락된 패키지 문제가 있습니다. 이런 문제는 애플리케이션이 제대로 시작되지 않는 원인이 될 수 있습니다. 위의 명령어로 상황을 확인하고, 문제를 해결할 수 있을 것
=========================================================== 