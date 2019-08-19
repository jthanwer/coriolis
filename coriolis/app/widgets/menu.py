from PyQt5.QtWidgets import QAction


def init_menu(self):
    menubar = self.menuBar()

    file_menu = menubar.addMenu('Figure')
    save_fig = QAction('&Save Figure\t', self)
    save_fig.setShortcut('Ctrl+S')
    save_fig.triggered.connect(self.save_fig)
    file_menu.addAction(save_fig)

    file_menu = menubar.addMenu('Code')
    ext_code = QAction('Extract C&ode\t', self)
    ext_code.setShortcut('Ctrl+O')
    ext_code.triggered.connect(self.extract_code)
    file_menu.addAction(ext_code)

    file_menu = menubar.addMenu('Data')
    sc_data = QAction('Sc&ale\t', self)
    sc_data.setShortcut('Ctrl+A')
    sc_data.triggered.connect(self.scale_data)
    file_menu.addAction(sc_data)

    file_menu = menubar.addMenu('Config')
    dpi_config = QAction('Change dpi\t', self)
    dpi_config.triggered.connect(self.change_dpi)
    file_menu.addAction(dpi_config)


