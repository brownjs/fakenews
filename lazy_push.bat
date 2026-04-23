@echo off
git add .
set /p msg="請輸入 Commit 訊息: "
git commit -m "%msg%"
git push
echo ✅ 推送完成！
pause