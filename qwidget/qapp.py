from qwidget.qgboxes import *
from qwidget.qviz import *
import os
from util.extract_code import extract_code


class App(QMainWindow):
    def __init__(self, dataset, file_path, width_scr, height_scr):
        super(QMainWindow, self).__init__()
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()
        self.path = file_path
        self.w = width_scr
        self.h = height_scr
        self.ds = dataset
        self.vars_name = [var for var in self.ds.data_vars]

        self.viz = PlotCanvas(self.ds[self.vars_name[0]], self.w, self.h)
        self.main_widget = QWidget(self)
        self.vars_box = VarsGroupBox(self.vars_name, self.main_widget)
        self.dimselect_box = DimsGroupBox(self.viz.var, parent=self.main_widget)
        self.var_infos_box = VarInfosGroupBox(self.viz.var, self.main_widget)
        self.plot_infos_box = PlotInfosGroupBox(self.viz, self.main_widget)
        self.bactions_box = BasicActionsGroupBox(self.main_widget)
        self.adactions_box = AdvancedActionsGroupBox(self.viz, self.main_widget)
        self.cusplot_box = CustomPlotGroupBox(self.viz.var, self.viz.abs_name, self.viz.ord_name, self.main_widget)
        self.dimstable_box = DimsTableGroupBox(self.viz.var, self.main_widget)
        self.layout = QGridLayout(self.main_widget)
        self.init_ui()

    def init_ui(self):
        """
        Initialize the window with the multiple widgets
        """
        self.setWindowTitle("Coriolis")
        # super(FigureCanvas, self.viz).setFixedSize(2500, 1200)
        # self.setFixedSize(3700, 2000)
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()
        self.showMaximized()

        self.layout.addWidget(self.viz, 0, 0, 1, 3)
        self.layout.addWidget(self.plot_infos_box, 0, 3)
        self.layout.addWidget(self.dimstable_box, 0, 4, 4, 1)
        self.layout.addWidget(self.vars_box, 1, 0)
        self.layout.addWidget(self.dimselect_box, 2, 0)
        self.layout.addWidget(self.bactions_box, 3, 0)
        self.layout.addWidget(self.adactions_box, 1, 1, 3, 1)
        self.layout.addWidget(self.cusplot_box, 1, 2, 3, 1)
        self.layout.addWidget(self.var_infos_box, 1, 3, 3, 1)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 1)
        self.layout.setColumnStretch(3, 1)
        self.layout.setColumnStretch(4, 1)
        self.init_md_buttons()
        self.init_op_buttons()

        self.setCentralWidget(self.main_widget)

        self.init_menu()
        self.show()

    def init_md_buttons(self):
        """
        Initialize the mandatory buttons actions
        """
        self.vars_box.vars_buttons[self.viz.var.name].setChecked(True)
        self.bactions_box.button_swap.clicked.connect(self.swap_axes)
        self.bactions_box.button_invertx.clicked.connect(self.viz.invert_xaxis)
        self.bactions_box.button_inverty.clicked.connect(self.viz.invert_yaxis)
        for button in self.vars_box.vars_buttons.values():
            button.clicked.connect(self.change_vars)
        for button in self.dimselect_box.dims_selection.dim_buttons.values():
            button.clicked.connect(self.change_dims)

    def init_op_buttons(self):
        """
        Initialize the optional buttons actions
        """
        self.cusplot_box.apply_button.clicked.connect(self.adjust_viz)
        self.cusplot_box.dimsgif.animation_but.clicked.connect(self.start_animation)
        self.cusplot_box.dimsgif.animation_but.setCheckable(True)
        self.adactions_box.apply_ranges.clicked.connect(self.adjust_viz)
        self.adactions_box.auto_range.clicked.connect(self.auto_range)
        for item in self.cusplot_box.dimsgif.qspinboxes.values():
            item.valueChanged.connect(self.change_slices)
        for item in self.cusplot_box.dimsgif.qcheckboxes.values():
            item.toggled.connect(self.reset_dim_slices)
        self.cusplot_box.dimsgif.animation_but.setShortcut('Ctrl+C')

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

    def change_vars(self):
        """
        Get the selected variable and change the window
        """
        sender = self.sender()
        self.viz.var = self.ds[sender.text()]
        self.viz.var_plotted = self.viz.var
        self.refresh_varinfos()
        self.refresh_dims()
        self.refresh_cusplot_tree()
        self.delete_cusplot_dimsgif()
        self.refresh_dimstable()
        self.viz.slices = self.cusplot_box.tree.slices
        # self.statusBar().showMessage(sender.text() + ' selected')
        for but in self.vars_box.vars_buttons.values():
            if but != sender:
                but.setChecked(False)
        for button in self.dimselect_box.dims_selection.dim_buttons.values():
            button.clicked.connect(self.change_dims)
        self.cusplot_box.apply_button.setEnabled(False)
        self.cusplot_box.reset_button.setEnabled(False)
        self.adactions_box.log_xaxis_but.setEnabled(False)
        self.adactions_box.log_yaxis_but.setEnabled(False)
        if self.viz.options['plot_type'] == '2d':
            self.adactions_box.log_cbar_but.setEnabled(False)
        self.adactions_box.auto_range.setEnabled(False)
        self.adactions_box.apply_ranges.setEnabled(False)

    def change_dims(self):
        """
        Get the dimension selected and plot when 2 dimensions are selected
        """
        sender = self.sender()
        if self.cusplot_box.switch_dimsgif == 'on':
            self.cusplot_box.dimsgif.animation_but.setChecked(False)
        dims_selection = self.dimselect_box.dims_selection
        dims_selected = self.dimselect_box.dims_selected
        viz = self.viz
        if sender.isChecked():
            if dims_selection.var_count == 0:
                viz.abs_name = sender.text()
                dims_selected.abs = sender.text()
                dims_selected.ord = 'None'
                self.refresh_selec_dims(dims_selected.abs, dims_selected.ord)
                for but in dims_selection.dim_buttons.values():
                    if but != sender:
                        but.setChecked(False)
            elif dims_selection.var_count == 1:
                viz.ord_name = sender.text()
                dims_selected.ord = sender.text()
                self.refresh_data_viz()
                self.refresh_cusplot_dimsgif()
                self.auto_range()
                self.refresh_adactions()
                self.init_op_buttons()
            dims_selection.var_count = (dims_selection.var_count + 1) % 2
        else:
            dims_selection.var_count = (dims_selection.var_count - 1) % 2
            dims_selected.abs = 'None'
        self.refresh_selec_dims(dims_selected.abs, dims_selected.ord)

    def refresh_data_viz(self):
        """
        Refresh visualisation data after the dimensions have been changed
        """
        viz = self.viz
        dims_selected = self.dimselect_box.dims_selected
        dims_selection = self.dimselect_box.dims_selection
        self.viz.abs_name = dims_selected.abs
        self.viz.ord_name = dims_selected.ord
        if viz.abs_name == viz.var.name:
            viz.abs_var = viz.var
            viz.ord_var = viz.var.coords[viz.ord_name]
        elif viz.ord_name == viz.var.name:
            viz.abs_var = viz.var.coords[viz.abs_name]
            viz.ord_var = viz.var
        else:
            viz.abs_var = viz.var.coords[viz.abs_name]
            viz.ord_var = viz.var.coords[viz.ord_name]
        self.viz.slices = self.cusplot_box.tree.slices
        viz.var_plotted = self.viz.var_resizing()
        for button in dims_selection.dim_buttons.values():
            button.setChecked(False)
        self.cusplot_box.apply_button.setEnabled(True)
        self.cusplot_box.reset_button.setEnabled(True)

    def adjust_viz(self):
        """
        Adjust visualisation after the slices have been changed
        """
        self.viz.slices = self.cusplot_box.tree.slices
        self.viz.ranges = self.adactions_box.levels_tree.ranges
        self.viz.plot()
        self.refresh_plotinfos()
        self.show()

    def change_slices(self):
        """
        Change the slices in the SlicesTree when changed in the SpinBox.
        """
        sender = self.sender()
        text = sender.objectName()
        self.cusplot_box.tree.children[text].setText(1, str(sender.value()))
        self.cusplot_box.tree.children[text].setText(2, str(sender.value()))
        self.cusplot_box.tree.slices[text][0] = sender.value()
        self.cusplot_box.tree.slices[text][1] = sender.value()
        self.adjust_viz()

    def reset_dim_slices(self):
        """
        Refresh one dimension slices when the associated SpinBox is disabled
        """
        sender = self.sender()
        dim = sender.text()
        if not sender.isChecked():
            self.cusplot_box.tree.slices[dim] = [0, self.viz.var.coords[dim].shape[0] - 1, 1]
            self.cusplot_box.tree.children[dim].setText(1, '0')
            self.cusplot_box.tree.children[dim].setText(2, str(self.viz.var.coords[dim].shape[0] - 1))
            self.cusplot_box.tree.children[dim].setText(3, '1')
            self.adjust_viz()

    def start_animation(self):
        dim_selec = self.cusplot_box.dimsgif.combobox_dims.currentText()
        dimsgif = self.cusplot_box.dimsgif
        dimsgif.animation_but.setText('Stop\nAnimation')
        dimsgif.qcheckboxes[dim_selec].setChecked(True)
        spin_value = dimsgif.qspinboxes[dim_selec].value()
        dict_slices = self.get_dict_slices()
        dict_slices[dim_selec] = slice(0, self.viz.var.coords[dim_selec].shape[0], 1)
        # self.viz.vmin_cbar = self.viz.var[dict_slices].min(skipna=True).values
        # self.viz.vmax_cbar = self.viz.var[dict_slices].max(skipna=True).values
        while dimsgif.animation_but.isChecked():
            pace_value = dimsgif.slider_pace.value()
            dimsgif.qspinboxes[dim_selec].setValue(spin_value)
            QTest.qWait(pace_value)
            spin_value = (spin_value + 1) % (dimsgif.qspinboxes[dim_selec].maximum() + 1)
        dimsgif.animation_but.setText('Start\nAnimation')

    def refresh_dims(self):
        self.dimselect_box.layout.removeWidget(self.dimselect_box.dims_selection)
        self.dimselect_box.dims_selection.deleteLater()
        self.dimselect_box.dims_selection = self.dimselect_box.DimsSelection(self.viz.var, self.main_widget)
        self.dimselect_box.layout.addWidget(self.dimselect_box.dims_selection, 0, 0)
        self.show()

    def refresh_selec_dims(self, abscissa, ordinate):
        self.dimselect_box.layout.removeWidget(self.dimselect_box.dims_selected)
        self.dimselect_box.dims_selected.deleteLater()
        self.dimselect_box.dims_selected = self.dimselect_box.DimsSelected(abscissa, ordinate, self.main_widget)
        self.dimselect_box.layout.addWidget(self.dimselect_box.dims_selected, 1, 0)
        self.show()

    def refresh_varinfos(self):
        self.layout.removeWidget(self.var_infos_box)
        self.var_infos_box.deleteLater()
        self.var_infos_box = VarInfosGroupBox(self.viz.var, self.main_widget)
        self.layout.addWidget(self.var_infos_box, 1, 3, 3, 1)
        self.show()

    def refresh_plotinfos(self):
        self.layout.removeWidget(self.plot_infos_box)
        self.plot_infos_box.deleteLater()
        self.plot_infos_box = PlotInfosGroupBox(self.viz, self.main_widget)
        self.layout.addWidget(self.plot_infos_box, 0, 3)
        self.show()

    def refresh_adactions(self):
        self.layout.removeWidget(self.adactions_box)
        self.adactions_box.deleteLater()
        self.adactions_box = AdvancedActionsGroupBox(self.viz, self.main_widget)
        self.layout.addWidget(self.adactions_box, 1, 1, 3, 1)
        self.show()

    def refresh_cusplot_tree(self):
        self.cusplot_box.var = self.viz.var
        self.cusplot_box.layout.removeWidget(self.cusplot_box.tree)
        self.cusplot_box.tree.deleteLater()
        self.cusplot_box.tree = self.cusplot_box.SlicesTree(self.viz.var)
        self.cusplot_box.layout.addWidget(self.cusplot_box.tree, 1, 0, 1, 2)
        self.show()

    def refresh_cusplot_dimsgif(self):
        viz = self.viz
        if self.cusplot_box.switch_dimsgif == 'on':
            self.cusplot_box.layout.removeWidget(self.cusplot_box.dimsgif)
            self.cusplot_box.dimsgif.deleteLater()
            self.cusplot_box.switch_dimsgif = 'off'
        self.cusplot_box.dimsgif = self.cusplot_box.DimsGif(viz.var, viz.abs_name, viz.ord_name)
        if self.cusplot_box.dimsgif.qspinboxes.values():
            self.cusplot_box.layout.addWidget(self.cusplot_box.dimsgif, 0, 0, 1, 2)
            for item in self.cusplot_box.dimsgif.qspinboxes.values():
                item.valueChanged.connect(self.change_slices)
            self.cusplot_box.dimsgif.animation_but.clicked.connect(self.start_animation)
            self.cusplot_box.switch_dimsgif = 'on'
        self.show()

    def delete_cusplot_dimsgif(self):
        if self.cusplot_box.switch_dimsgif == 'on':
            self.cusplot_box.layout.removeWidget(self.cusplot_box.dimsgif)
            self.cusplot_box.dimsgif.deleteLater()
            self.cusplot_box.switch_dimsgif = 'off'
            self.show()
        else:
            pass

    def refresh_dimstable(self):
        self.layout.removeWidget(self.dimstable_box)
        self.dimstable_box.deleteLater()
        self.dimstable_box = DimsTableGroupBox(self.viz.var, self.main_widget)
        self.layout.addWidget(self.dimstable_box, 0, 4, 4, 1)
        self.show()

    def swap_axes(self):
        self.viz.ranges = self.adactions_box.levels_tree.ranges
        self.viz.swap_axes()
        self.adactions_box.levels_tree.range_x.setText(1, dsp_fmt(self.viz.ranges['X-axis'][0]))
        self.adactions_box.levels_tree.range_x.setText(2, dsp_fmt(self.viz.ranges['X-axis'][1]))
        self.adactions_box.levels_tree.range_y.setText(1, dsp_fmt(self.viz.ranges['Y-axis'][0]))
        self.adactions_box.levels_tree.range_y.setText(2, dsp_fmt(self.viz.ranges['Y-axis'][1]))
        self.refresh_plotinfos()

    def auto_range(self):
        viz = self.viz
        level_tree = self.adactions_box.levels_tree
        viz.ranges['X-axis'][0] = viz.abs_var.min().values
        viz.ranges['X-axis'][1] = viz.abs_var.max().values
        viz.ranges['Y-axis'][0] = viz.ord_var.min().values
        viz.ranges['Y-axis'][1] = viz.ord_var.max().values
        level_tree.range_x.setText(1, dsp_fmt(viz.ranges['X-axis'][0]))
        level_tree.range_x.setText(2, dsp_fmt(viz.ranges['X-axis'][1]))
        level_tree.range_y.setText(1, dsp_fmt(viz.ranges['Y-axis'][0]))
        level_tree.range_y.setText(2, dsp_fmt(viz.ranges['Y-axis'][1]))
        viz.ranges['Colorbar'][0] = viz.var_plotted.min(skipna=True).values
        viz.ranges['Colorbar'][1] = viz.var_plotted.max(skipna=True).values
        level_tree.cbar.setText(1, dsp_fmt(viz.ranges['Colorbar'][0]))
        level_tree.cbar.setText(2, dsp_fmt(viz.ranges['Colorbar'][1]))
        viz.plot()
        self.refresh_plotinfos()

    def get_dict_slices(self):
        viz = self.viz
        dict_slices = {dim: slice(viz.slices[dim][0], viz.slices[dim][1] + 1, viz.slices[dim][2])
                       for dim in viz.var.dims}
        return dict_slices

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
                    extract_code(fname, self.viz, self.path)
                else:
                    return

            else:
                print('Extracting code to {}'.format(fname))
                extract_code(fname, self.viz, self.path)

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

