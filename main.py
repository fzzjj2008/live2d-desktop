# -*- coding: utf-8 -*-
# Create on: 2021/02/12 19:34:29
# Author   : fzzjj2008
"""
main.py
"""
import os
import sys
from pathlib import Path
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtWebEngineWidgets import *
from PySide2.QtWebChannel import QWebChannel
from pynput import mouse


class L2DView(QWebEngineView):
    """
    浏览器页面
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setWindowOpacity(1)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 屏蔽浏览器鼠标事件
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.page().setBackgroundColor(Qt.transparent)
        data_dir = Path(os.path.abspath(os.path.dirname(__file__)))
        url = QUrl.fromLocalFile(f"{data_dir}/index.html")
        self.load(url)

    def mouse_move_event(self, x, y):
        print(x, y)
        # channel = QWebChannel()
        # channel.registerObject("backend", QPoint(x, y))
        # self.page().setWebChannel(channel)

class MainWindow(QMainWindow):
    """
    主窗口
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        # 初始化控件
        self.l2d_view = L2DView(self)
        # self.tray_icon_init()
        self.context_menu_init()
        self.win_init()
        # 鼠标拖拽事件
        self.is_moving = False
        self.mouse_drag_pos = self.pos()
        # 全局鼠标监听
        self.mouse_listener = mouse.Listener(on_move=self.on_move)
        self.mouse_listener.start()

    def context_menu_init(self):
        # 右键菜单
        reload_action = QAction('重载', self, triggered=self.win_reload)
        quit_action = QAction('退出', self, triggered=self.win_quit)
        self.context_menu = QMenu(self)
        self.context_menu.addAction(reload_action)
        self.context_menu.addAction(quit_action)

    def tray_icon_init(self):
        # 任务栏托盘
        quit_action = QAction('退出', self, triggered=self.win_quit)
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("app.ico"))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

    def win_init(self):
        # 窗口无边框透明
        win_width = 200
        win_height = 300
        scr_width = QApplication.desktop().width()
        scr_height = QApplication.desktop().height()
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(win_width, win_height)
        self.move(scr_width - win_width, scr_height - win_height)
        self.setCentralWidget(self.l2d_view)

    def win_reload(self):
        self.l2d_view.reload()

    def win_quit(self):
        self.mouse_listener.stop()
        self.close()
        sys.exit()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(QCursor(Qt.ClosedHandCursor))
            self.is_moving = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
        elif event.button() == Qt.RightButton:
            self.context_menu.exec_(QCursor.pos())
            event.accept()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_moving:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.is_moving = False

    def on_move(self, x, y):
        self.l2d_view.mouse_move_event(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.setMouseTracking(True)
    win.show()
    sys.exit(app.exec_())
