# -*- coding: utf-8 -*
import os
import sys
import subprocess
import shutil
import zipfile

PARENT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
_tools = os.path.join(PARENT_DIR, "_tools")
# 签名输出文件夹
outDir = os.path.join(PARENT_DIR, "out")
# 需要操作的apk所在文件夹
apksDir = os.path.join(PARENT_DIR, "apks")

keystore = os.path.join(_tools, 'test.jks')
keyalias = 'test'
keypwd = '147258369'


def decompilation(filename, dir):
    apktool_cmd = "apktool.jar d \"" + filename + "\" -f -o \"" + PARENT_DIR + "\"/" + dir
    print(u"正在反编译中...")
    os.system(apktool_cmd)
    print(u"反编译完成")
    dex2jar(filename)


def dex2jar(filename):
    subprocess.Popen(_tools + '/dex2jar.bat \"' + filename + "\"", shell=False)


def decompilationback(dirName):
    print(u"正在回编译并自动签名中...")
    apktool_cmd = "apktool.jar b " + dirName
    os.system(apktool_cmd)
    print(u"回编译完成")
    dir = os.path.join(PARENT_DIR, dirName + "/dist")
    signed(dir, dirName + ".apk", False)


def copy_files(name, newName, tempname):
    zin = zipfile.ZipFile(name, 'r')
    zout = zipfile.ZipFile(newName, 'w')
    for item in zin.infolist():
        buffer = zin.read(item.filename)
        if 'META-INF' not in item.filename:
            zout.writestr(item, buffer)
    zout.close()
    zin.close()
    signed(apksDir, tempname, True)


def copy_file(apkName):
    allFiles = os.listdir(apksDir)
    for i in allFiles:
        if i.endswith('.apk'):
            if apkName == i[:len(i) - 4]:
                oldname = os.path.join(apksDir, i)
                newname = os.path.join(apksDir, apkName + "_temp.apk")
                tempname = apkName + "_temp.apk"
                copy_files(oldname, newname, tempname)


def signed(dir, file, delete):
    _out = os.path.exists('out')
    if not _out:
        os.mkdir('out')

    print(u"正在签名...")
    signedFile = os.path.join(outDir, inputData + "_sign.apk")
    outFile = os.path.join(outDir, inputData + "_signed.apk")
    f = os.path.join(dir, file)

    # v1签名
    signcmd = 'jarsigner -sigalg SHA1withRSA -digestalg SHA1 -keystore "%s" -storepass "%s" -signedjar "%s" "%s" "%s"' % (
        keystore, keypwd, signedFile, f, keyalias)
    os.system(signcmd)

    # zipalign优化
    aligncmd = 'zipalign -f 4 "%s" "%s"' % (signedFile, outFile)
    os.system(aligncmd)

    # # v2签名
    # signcmd2 = 'apksigner sign --ks %s --ks-pass pass:%s --ks-key-alias %s %s' % (keystore, keypwd, keyalias, outFile)
    # os.system(signcmd2)

    # 删除临时文件
    if (delete):
        os.remove(f)
    os.remove(signedFile)


def inputTransform(inputData):
    inputData = str(inputData[:len(inputData) - 4])
    return inputData


if __name__ == '__main__':
    chStr = u"1.反编译\n2.回编译\n3.apk签名"
    print(chStr)
    sys.stdout.write(u"请选择一个操作(输入对应序号)：")
    sys.stdout.flush()

    selectedNum = raw_input()
    selectedNum = str(selectedNum)

    if selectedNum == '1':
        sys.stdout.write(u"请输入apks目录下需要反编译的apk名(多个以逗号隔开,全部输入*)：")
        sys.stdout.flush()

        inputData = raw_input()
        if inputData.endswith(".apk"):
            inputData = inputTransform(inputData)

        if inputData == '*':
            for f in os.listdir(apksDir):
                if f.endswith(".apk"):
                    filename = os.path.join(apksDir, f)
                    decompilation(filename, inputTransform(f))
        else:
            for i in inputData.split(','):
                i = i.strip()
                for f in os.listdir(apksDir):
                    if f.endswith(".apk"):
                        if i == inputTransform(f):
                            filename = os.path.join(apksDir, f)
                            decompilation(filename, i)

    elif selectedNum == '2':
        sys.stdout.write(u"请输入需要回编译的文件夹名：")
        sys.stdout.flush()

        inputData = raw_input()
        inputData = str(inputData)

        if os.path.exists(inputData):
            decompilationback(inputData)
        else:
            print(u"文件夹不存在")

    elif selectedNum == '3':
        sys.stdout.write(u"请输入apks目录下需要重签名的apk名：")
        sys.stdout.flush()

        inputData = raw_input()
        if inputData.endswith(".apk"):
            inputData = inputTransform(inputData)

        copy_file(inputData)
    else:
        print(u"你很调皮⊙﹏⊙")
