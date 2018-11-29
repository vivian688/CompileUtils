@echo on

set apkFile=%1
set jarFile=%apkFile%.jar

echo .........dex2jar..........
call _tools\dex2jar\d2j-dex2jar -f %apkFile% -o %jarFile%
echo .........jd-gui...........
call _tools\jd-gui\jd-gui %jarFile%

pause