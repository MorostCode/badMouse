import os

name = "badMouse"

# ui文件转py
os.system("python -m PyQt5.uic.pyuic {0}.ui -o {0}UI.py".format(name))
print("{0}.ui已转为{0}UI.py".format(name))

# 生产单个exe文件
os.system("pyinstaller -w -F -i badMouse.ico {}.py --upx-dir ./upx-3.96-win64/".format(name))
print("{}.exe文件已生成".format(name))
