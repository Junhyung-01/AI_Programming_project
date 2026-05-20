Write-Host "📦 [1/3] 프론트엔드 빌드 시작..." -ForegroundColor Cyan
Set-Location frontend
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 프론트엔드 빌드 중 오류가 발생했습니다. 배포를 중단합니다." -ForegroundColor Red
    Set-Location ..
    exit 1
}

Set-Location ..
Write-Host "✅ [2/3] 프론트엔드 빌드 완료!" -ForegroundColor Green

Write-Host "📤 [3/3] 변경사항 Git 커밋 및 GitHub 푸시 중..." -ForegroundColor Cyan
git add .

# 사용자 입력 혹은 기본 메시지로 커밋
$commitMsg = Read-Host -Prompt "커밋 메시지를 입력하세요 (기본값: 'Update RPG Web Application')"
if ([string]::IsNullOrEmpty($commitMsg)) {
    $commitMsg = "Update RPG Web Application"
}

git commit -m $commitMsg
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n🎉 모든 업데이트가 완료되었습니다!" -ForegroundColor Green
    Write-Host "Render 대시보드에서 자동으로 새로운 빌드 및 배포가 진행됩니다." -ForegroundColor Yellow
} else {
    Write-Host "❌ GitHub 푸시에 실패했습니다." -ForegroundColor Red
}
