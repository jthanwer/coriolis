from .widgets.gboxes import *
from .widgets.viz import *
from .widgets.menu import *
from .util.refresh import *
from .util.viz import *
from .util.save import *
from .util.extract import *
import os
from types import MethodType


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
        self.vars_box = VarsGroupBox(self.vars_name, self)
        self.dimselect_box = DimsGroupBox(self.viz.var, parent=self)
        self.var_infos_box = VarInfosGroupBox(self.viz.var, self)
        self.plot_infos_box = PlotInfosGroupBox(self.viz, self)
        self.bactions_box = BasicActionsGroupBox(self)
        self.adactions_box = AdvancedActionsGroupBox(self.viz, self)
        self.cusplot_box = CustomPlotGroupBox(self.viz.var, self.viz.abs_name, self.viz.ord_name, self)
        self.dimstable_box = DimsTableGroupBox(self.viz.var, self)
        self.layout = QGridLayout(self.main_widget)
        self.initiate_methods()
        self.init_ui()

    def initiate_methods(self):
        # Refresh app widgets
        self.refresh_plotinfos = MethodType(refresh_plotinfos, self)
        self.refresh_adactions = MethodType(refresh_adactions, self)
        self.refresh_cusplot_dimsgif = MethodType(refresh_cusplot_dimsgif, self)
        self.refresh_cusplot_tree = MethodType(refresh_cusplot_tree, self)
        self.refresh_dims = MethodType(refresh_dims, self)
        self.refresh_dimstable = MethodType(refresh_dimstable, self)
        self.refresh_selec_dims = MethodType(refresh_selec_dims, self)
        self.refresh_varinfos = MethodType(refresh_varinfos, self)
        self.delete_cusplot_dimsgif = MethodType(delete_cusplot_dimsgif, self)
        self.reset_dim_slices = MethodType(reset_dim_slices, self)

        self.refresh_plotcanvas = MethodType(refresh_plotcanvas, self)
        self.refresh_data_viz = MethodType(refresh_data_viz, self)
        self.adjust_viz = MethodType(adjust_viz, self)
        self.swap_axes = MethodType(swap_axes, self)
        self.auto_range = MethodType(auto_range, self)
        self.scale_data = MethodType(scale_data, self)

        self.save_fig = MethodType(save_fig, self)
        self.extract_code = MethodType(extract_code, self)
        self.change_dpi = MethodType(change_dpi, self)

        self.init_menu = MethodType(init_menu, self)

    def init_ui(self):
        """
        Initialize the window with the multiple app
        """
        self.setWindowTitle("Coriolis {}".format(os.path.basename(self.path)))
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
        # self.vars_box.vars_buttons[self.viz.var.name].setChecked(True)
        self.bactions_box.button_swap.clicked.connect(self.swap_axes)
        self.bactions_box.button_invertx.clicked.connect(self.viz.invert_xaxis)
        self.bactions_box.button_inverty.clicked.connect(self.viz.invert_yaxis)
        # for button in self.vars_box.vars_buttons.values():
        #     button.clicked.connect(self.change_vars)
        self.vars_box.var_combo.currentTextChanged.connect(self.change_vars)

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

    def change_vars(self, value):
        """
        Get the selected variable and change the window
        """
        # sender = self.sender()
        # self.viz.var = self.ds[sender.text()]
        self.viz.var = self.ds[value]
        self.viz.scale = 1.
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
            self.adactions_box.cmap_cbox.setEnabled(False)
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

    def start_animation(self):
        """
        Start the plotting animation and refresh all the data at each time step
        """
        dim_selec = self.cusplot_box.dimsgif.combobox_dims.currentText()
        dimsgif = self.cusplot_box.dimsgif
        dimsgif.animation_but.setText('Stop\nAnimation')
        dimsgif.qcheckboxes[dim_selec].setChecked(True)
        spin_value = dimsgif.qspinboxes[dim_selec].value()
        dict_slices = self.get_dict_slices()
        dict_slices[dim_selec] = slice(0, self.viz.var.coords[dim_selec].shape[0], 1)
        while dimsgif.animation_but.isChecked():
            pace_value = dimsgif.slider_pace.value()
            dimsgif.qspinboxes[dim_selec].setValue(spin_value)
            QTest.qWait(pace_value)
            spin_value = (spin_value + 1) % (dimsgif.qspinboxes[dim_selec].maximum() + 1)
        dimsgif.animation_but.setText('Start\nAnimation')

    def get_dict_slices(self):
        viz = self.viz
        dict_slices = {dim: slice(viz.slices[dim][0], viz.slices[dim][1] + 1, viz.slices[dim][2])
                       for dim in viz.var.dims}
        return dict_slices




