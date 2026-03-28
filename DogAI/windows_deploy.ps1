# DogAI 애플리케이션 배포 스크립트
# 관리자 권한으로 실행하세요

# 작업 디렉토리 확인 및 생성
$workDir = "C:\Users\USER\DogAI"
if (-not (Test-Path $workDir)) {
    Write-Host "작업 디렉토리 생성: $workDir" -ForegroundColor Green
    mkdir -p $workDir | Out-Null
}

# 현재 경로 저장
$currentPath = Get-Location

# 프로젝트 디렉토리로 이동
cd $workDir
Write-Host "작업 디렉토리로 이동: $workDir" -ForegroundColor Green

# Docker 실행 여부 확인
try {
    docker info | Out-Null
    Write-Host "Docker가 실행 중입니다." -ForegroundColor Green
}
catch {
    Write-Host "Docker가 실행 중이지 않습니다. Docker Desktop을 실행해주세요." -ForegroundColor Red
    Write-Host "Docker Desktop을 실행한 후 이 스크립트를 다시 실행하세요." -ForegroundColor Yellow
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    cd $currentPath
    exit 1
}

# 기존 컨테이너 확인 및 제거
$containerExists = docker ps -a --filter "name=dogai_app" --format "{{.ID}}"
if ($containerExists) {
    Write-Host "기존 컨테이너를 중지하고 제거합니다: dogai_app" -ForegroundColor Yellow
    docker stop dogai_app 2>$null
    docker rm dogai_app 2>$null
}

# Docker 이미지 빌드
Write-Host "Docker 이미지를 빌드합니다..." -ForegroundColor Green
docker build -t dogai .

# 빌드 성공 확인
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker 이미지 빌드에 실패했습니다. 오류를 확인하세요." -ForegroundColor Red
    cd $currentPath
    exit 1
}

# Docker 컨테이너 실행
Write-Host "Docker 컨테이너를 실행합니다..." -ForegroundColor Green
docker run -d --name dogai_app -p 7000:8501 dogai

# 컨테이너 실행 확인
$containerRunning = docker ps --filter "name=dogai_app" --format "{{.ID}}"
if ($containerRunning) {
    Write-Host "DogAI 애플리케이션이 성공적으로 배포되었습니다!" -ForegroundColor Green
    Write-Host "다음 URL에서 애플리케이션에 접속할 수 있습니다: http://localhost:7000" -ForegroundColor Cyan
    Write-Host "외부에서 접속하려면: http://192.168.219.176:7000" -ForegroundColor Cyan
}
else {
    Write-Host "컨테이너 시작에 실패했습니다. 오류 로그:" -ForegroundColor Red
    docker logs dogai_app
}

# 작업 완료 후 원래 경로로 복귀
cd $currentPath 