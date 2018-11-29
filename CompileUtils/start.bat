@echo on
echo 1、反编译完成后会在当前目录下生成apk同名的文件夹，里面存放了反编译出来的文件。apks目录	下生成对应jar文件，并且启动jd-gui查看
echo 2、回编译完成后会自动给apk签名，输出在out文件夹中，未签名apk保存在项目目录下dist文件夹
echo 3、apk重签名，需要将apk文件放于apks文件夹中
echo.
@set PATH=%~dp0\_tools;%PATH%
@python.exe _tools\utils.py
@pause
