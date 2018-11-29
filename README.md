# CompileUtils
**apk一键反编译工具，支持批量反编译，回编译以及重签名.**
*	把需要反编译的apk放到apks目录下，双击"点击执行"文件按提示操作
*	回编译会自动重签名，签名成功后保存在out文件夹中
*	apk签名同样把需要签名的apk文件放到apks目录下，在命令中选择输入apk名字，签名完成后保存在out文件夹中

> 如果需要更换签名文件，把自己的签名文件复制到_tools目录下，然后修改utils.py脚本里
```javascript
keystore = os.path.join(_tools, 'test.jks')
keyalias = 'test'
keypwd = '147258369'
```
     keystore参数里的test.jks改为你的签名文件名字 
     keyalias为别名 
     keypwd为签名密码  
