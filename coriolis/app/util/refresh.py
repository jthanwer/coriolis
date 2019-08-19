from coriolis.app.widgets.gboxes import *
from coriolis.app.widgets.viz import *


def refresh_plotcanvas(self):
    """
    Refresh PlotCanvas when dpi or figsize have been changed
    """
    self.layout.removeWidget(self.viz)
    self.viz.deleteLater()
    (abs_name, ord_name) = (self.viz.abs_name, self.viz.ord_name)
    (abs_var, ord_var) = (self.viz.abs_var, self.viz.ord_var)
    slices = self.viz.slices
    options = self.viz.options
    stats = self.viz.stats
    ranges = self.viz.ranges
    self.viz = PlotCanvas(self.viz.var, self.viz.w, self.viz.h, self.viz.dpi)
    self.layout.addWidget(self.viz, 0, 0, 1, 3)
    (self.viz.abs_name, self.viz.ord_name) = (abs_name, ord_name)
    (self.viz.abs_var, self.viz.ord_var) = (abs_var, ord_var)
    self.viz.slices = slices
    self.viz.options = options
    self.viz.stats = stats
    self.viz.ranges = ranges
    self.viz.var_plotted = self.viz.var_resizing()
    self.viz.plot()
    self.show()
    self.bactions_box.button_invertx.clicked.connect(self.viz.invert_xaxis)
    self.bactions_box.button_inverty.clicked.connect(self.viz.invert_yaxis)


def refresh_dims(self):
    """
    Refresh the Dimensions Selection Buttons Widget
    """
    self.dimselect_box.layout.removeWidget(self.dimselect_box.dims_selection)
    self.dimselect_box.dims_selection.deleteLater()
    self.dimselect_box.dims_selection = self.dimselect_box.DimsSelection(self.viz.var, self)
    self.dimselect_box.layout.addWidget(self.dimselect_box.dims_selection, 0, 0)
    self.show()


def refresh_selec_dims(self, abscissa, ordinate):
    """
    Refresh the Dimensions Selected Widget
    """
    self.dimselect_box.layout.removeWidget(self.dimselect_box.dims_selected)
    self.dimselect_box.dims_selected.deleteLater()
    self.dimselect_box.dims_selected = self.dimselect_box.DimsSelected(abscissa, ordinate, self)
    self.dimselect_box.layout.addWidget(self.dimselect_box.dims_selected, 1, 0)
    self.show()


def refresh_varinfos(self):
    """
    Refresh the Variable Information Widget
    """
    self.layout.removeWidget(self.var_infos_box)
    self.var_infos_box.deleteLater()
    self.var_infos_box = VarInfosGroupBox(self.viz.var, self)
    self.layout.addWidget(self.var_infos_box, 1, 3, 3, 1)
    self.show()


def refresh_plotinfos(self):
    """
    Refresh the Plot Information Widget
    """
    self.layout.removeWidget(self.plot_infos_box)
    self.plot_infos_box.deleteLater()
    self.plot_infos_box = PlotInfosGroupBox(self.viz, self)
    self.layout.addWidget(self.plot_infos_box, 0, 3)
    self.show()


def refresh_adactions(self):
    """
    Refresh the Advanced Actions Widget
    """
    self.layout.removeWidget(self.adactions_box)
    self.adactions_box.deleteLater()
    self.adactions_box = AdvancedActionsGroupBox(self.viz, self)
    self.layout.addWidget(self.adactions_box, 1, 1, 3, 1)
    self.show()


def refresh_cusplot_tree(self):
    """
    Refresh the Custom Plot Widget
    """
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
    self.dimstable_box = DimsTableGroupBox(self.viz.var, self)
    self.layout.addWidget(self.dimstable_box, 0, 4, 4, 1)
    self.show()


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
