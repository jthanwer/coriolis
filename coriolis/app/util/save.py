from PyQt5.QtWidgets import QFileDialog, QMessageBox


def save_fig(self):
    qdialog = QFileDialog(self)
    qdialog.setFixedSize(self.w / 2.5, self.h / 2.5)
    qdialog.show()
    fname = []

    if qdialog.exec_():
        fname = qdialog.selectedFiles()

    if len(fname) == 1:
        fname = fname[0]
        if os.path.isfile(fname):
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setText("Overwrite the file ?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            reply = msg_box.exec_()
            if reply == QMessageBox.Yes:
                self.viz.figure.savefig(fname)
                print('Figure saved to {}'.format(fname))
            else:
                return

        else:
            print('Figure saved to {}'.format(fname))
            self.viz.figure.savefig(fname)
