@echo off
pushd %~dp0
setlocal EnableDelayedExpansion

set fileName = %1
set startTime = %2
set endTime = %3
set Num=1
for /r %%i in (*.avi) do (
    ffmpeg -i "%%~fi" -ss %2 -to %3 -c copy "%1!Num!.mp4"
    set /a Num+=1
)
pause