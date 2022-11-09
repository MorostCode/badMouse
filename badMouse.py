# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QMessageBox
from subModule.accessThread import AccessThread
from badMouseUI import Ui_MainWindow
from PyQt5.QtGui import QIcon
import selfQtools
import time
import sys

iconBytes = b"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"


class MainWindow(Ui_MainWindow, QMainWindow):
    # 初始化
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)  # 加载Ui
        self.setFixedSize(640, 160)
        self.setWindowTitle("badMouse_v1.3")
        self.setWindowIcon(QIcon(selfQtools.base642pixmap(iconBytes)))
        selfSize = self.geometry()
        screenSize = QDesktopWidget().screenGeometry()
        newLeft = int((screenSize.width() - selfSize.width()) / 2)
        newTop = int((screenSize.height() - selfSize.height()) / 2)
        self.move(newLeft, newTop)
        self.access_thread_object = None
        self.bind()

    # 绑定按钮
    def bind(self):
        self.pushButtonStart.clicked.connect(self.get_start)

    # 执行函数
    def get_start(self):
        try:
            url = self.lineEdit.text()  # 从GUI界面获取输入url
            if url:
                domainName = url.split("https://")[-1].split(".com")[0]
                if domainName == "www.douyin" or domainName == "space.bilibili":
                    self.access_thread_object = AccessThread(url)
                    self.access_thread_object.start()
                    self.pushButtonStart.setEnabled(False)  # 开始爬取后执行按钮禁用
                    self.textEdit.clear()
                    self.textEdit.append("start")
                    self.textEdit.append("开始获取数据……")
                    self.access_thread_object.update_signal.connect(self.update_ui)
                else:
                    QMessageBox.warning(self, "Warning", "暂不支持除抖音与B站之外的网站链接", QMessageBox.Cancel)
            else:
                QMessageBox.warning(self, "Warning", "链接不可为空", QMessageBox.Cancel)
        except Exception as e:
            error_line = e.__traceback__.tb_lineno
            error_info = '第{error_line}行发生error为: {e}'.format(error_line=error_line, e=str(e))
            self.textEdit.append(error_info)

    # 更新ui
    def update_ui(self, count):
        try:
            self.textEdit.append("end")
            self.textEdit.append("总计{}条数据".format(count))
            time.sleep(1)
            QMessageBox.information(self, "获取完毕", "数据已保存至本地", QMessageBox.Yes)
            self.textEdit.clear()
            self.lineEdit.clear()
            self.pushButtonStart.setEnabled(True)
        except Exception as e:
            error_line = e.__traceback__.tb_lineno
            error_info = '第{error_line}行发生error为: {e}'.format(error_line=error_line, e=str(e))
            self.textEdit.append(error_info)

    # 关闭窗口时弹出确认消息
    def closeEvent(self, event):
        replyA = QMessageBox.question(self, '?', '确认退出？', QMessageBox.Yes, QMessageBox.No)
        if replyA == QMessageBox.Yes:  # 接收到确认关闭信号之后关闭窗口
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
