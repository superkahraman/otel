@echo off
set /p commit="Enter commit: "
git add *
git commit -m "%commit%"
git push -u origin master
