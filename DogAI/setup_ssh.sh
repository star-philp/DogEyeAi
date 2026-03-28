#!/bin/bash

# DogAI 프로젝트를 위한 SSH 키 설정 스크립트

echo "SSH 키 생성 중..."
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_windows -N ""

echo "Windows 서버용 SSH 키가 생성되었습니다!"
echo "공개 키 내용:"
cat ~/.ssh/id_rsa_windows.pub

echo "
다음 단계:
1. Windows 서버에 직접 접속하세요.
2. C:\\Users\\USER\\.ssh 디렉토리를 생성하세요.
3. 위의 공개 키 내용을 C:\\Users\\USER\\.ssh\\authorized_keys 파일에 복사하세요.
4. 권한 설정을 위해 다음 PowerShell 명령을 실행하세요:
   icacls \"C:\\Users\\USER\\.ssh\\authorized_keys\" /inheritance:r /grant \"USER:F\"
5. 다음 명령으로 SSH 연결을 테스트하세요:
   ssh -i ~/.ssh/id_rsa_windows -p 2222 USER@192.168.219.176
"

# SSH 설정 파일 업데이트
echo "SSH 설정 파일 업데이트 중..."
if [ ! -f ~/.ssh/config ]; then
    touch ~/.ssh/config
    chmod 600 ~/.ssh/config
fi

# Windows 서버 설정 추가
if ! grep -q "Host windows-server" ~/.ssh/config; then
    echo "
Host windows-server
    HostName 192.168.219.176
    User USER
    Port 2222
    IdentityFile ~/.ssh/id_rsa_windows
    PreferredAuthentications publickey,password
" >> ~/.ssh/config
    echo "SSH 설정 파일이 업데이트되었습니다!"
else
    echo "SSH 설정이 이미 존재합니다."
fi

echo "설정이 완료되었습니다!" 