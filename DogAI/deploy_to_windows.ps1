#!/usr/bin/env pwsh

# DogAI 애플리케이션을 Windows 서버에 배포하는 스크립트
# 사용법: ./deploy_to_windows.ps1 [DOCKER_USERNAME]

param (
    [string]$DOCKER_USERNAME = $null
)

# Docker Hub 사용자 이름이 제공되지 않았을 경우 입력 요청
if (-not $DOCKER_USERNAME) {
    $DOCKER_USERNAME = Read-Host -Prompt "Docker Hub 사용자 이름을 입력하세요"
}

Write-Host "DogAI 애플리케이션 배포를 시작합니다..." -ForegroundColor Green

# 기존 컨테이너 중지 및 삭제
Write-Host "기존 컨테이너를 확인하고 정리합니다..." -ForegroundColor Yellow
$existingContainer = docker ps -a --filter "name=dogai_app" --format "{{.ID}}"
if ($existingContainer) {
    Write-Host "기존 컨테이너를 중지하고 삭제합니다: $existingContainer" -ForegroundColor Yellow
    docker stop dogai_app 2>$null
    docker rm dogai_app 2>$null
}

# Docker Hub에서 이미지 가져오기
Write-Host "Docker Hub에서 최신 이미지를 가져옵니다..." -ForegroundColor Yellow
docker pull ${DOCKER_USERNAME}/dogai:latest

# 컨테이너 실행
Write-Host "새 컨테이너를 시작합니다..." -ForegroundColor Yellow
docker run -d --name dogai_app -p 7000:8501 ${DOCKER_USERNAME}/dogai:latest

# 컨테이너 상태 확인
Start-Sleep -Seconds 5
$containerRunning = docker ps --filter "name=dogai_app" --format "{{.ID}}"

if (-not $containerRunning) {
    Write-Host "컨테이너 시작에 실패했습니다. 오류 로그:" -ForegroundColor Red
    docker logs dogai_app
    exit 1
}

Write-Host "DogAI 애플리케이션이 성공적으로 배포되었습니다!" -ForegroundColor Green
Write-Host "다음 URL에서 애플리케이션에 접속할 수 있습니다: http://localhost:7000" -ForegroundColor Cyan

# 5. 컨테이너 정보 표시
Write-Host "`n컨테이너 정보:" -ForegroundColor Yellow
docker ps -f name=dogai_app 