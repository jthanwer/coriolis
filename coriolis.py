import sys
from PyQt5.QtWidgets import QApplication
from qwidget.qapp import App
from util.preproc import init_app
from util.postproc import exit_app
from util.style_sheet import get_style_sheet
from functools import partial


if __name__ == '__main__':
    dataset, file_path = init_app()
    print('......')

    style_sheet = get_style_sheet()

    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()

    mw = App(dataset, file_path, width, height)
    app.setStyleSheet(style_sheet)

    app.aboutToQuit.connect(partial(exit_app, mw))
    sys.exit(app.exec_())


