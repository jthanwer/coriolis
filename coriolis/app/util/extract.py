from coriolis.util.code2text import code2text
from PyQt5.QtWidgets import QFileDialog, QMessageBox


def extract_code(self):
    qdialog = QFileDialog(self)
    qdialog.setFixedSize(self.w / 2.5, self.h / 2.5)
    qdialog.setNameFilter("Python (*.py)")
    qdialog.show()
    fname = []

    if qdialog.exec_():
        fname = qdialog.selectedFiles()

    if len(fname) == 1:
        fname = fname[0]
        if os.path.isfile(fname):
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setText("Code extracted the file ?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            reply = msg_box.exec_()
            if reply == QMessageBox.Yes:
                print('Code extracted to {}'.format(fname))
                code2text(fname, self.viz, self.path)
            else:
                return

        else:
            print('Extracting code to {}'.format(fname))
            code2text(fname, self.viz, self.path)

