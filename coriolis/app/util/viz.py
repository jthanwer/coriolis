from coriolis.util.format import *
from PyQt5.QtWidgets import QInputDialog


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
    dict_slices = self.get_dict_slices()
    min_val = viz.var_plotted.min().values
    max_val = viz.var_plotted.max().values
    if viz.var.name == viz.abs_name:
        viz.ranges['X-axis'][0] = min_val * 3 / 4 - max_val * 1 / 4
        viz.ranges['X-axis'][1] = min_val * 1 / 4 + max_val * 5 / 4
        viz.ranges['Y-axis'][0] = viz.ord_var[dict_slices[viz.ord_name]].min().values
        viz.ranges['Y-axis'][1] = viz.ord_var[dict_slices[viz.ord_name]].max().values
    elif viz.var.name == viz.ord_name:
        viz.ranges['X-axis'][0] = viz.abs_var[dict_slices[viz.abs_name]].min().values
        viz.ranges['X-axis'][1] = viz.abs_var[dict_slices[viz.abs_name]].max().values
        viz.ranges['Y-axis'][0] = min_val * 3 / 4 - max_val * 1 / 4
        viz.ranges['Y-axis'][1] = min_val * 1 / 4 + max_val * 5 / 4
    else:
        viz.ranges['X-axis'][0] = viz.abs_var[dict_slices[viz.abs_name]].min().values
        viz.ranges['X-axis'][1] = viz.abs_var[dict_slices[viz.abs_name]].max().values
        viz.ranges['Y-axis'][0] = viz.ord_var[dict_slices[viz.ord_name]].min().values
        viz.ranges['Y-axis'][1] = viz.ord_var[dict_slices[viz.ord_name]].max().values
    level_tree.range_x.setText(1, dsp_fmt(viz.ranges['X-axis'][0]))
    level_tree.range_x.setText(2, dsp_fmt(viz.ranges['X-axis'][1]))
    level_tree.range_y.setText(1, dsp_fmt(viz.ranges['Y-axis'][0]))
    level_tree.range_y.setText(2, dsp_fmt(viz.ranges['Y-axis'][1]))
    viz.ranges['Colorbar'][0] = viz.stats['min']
    viz.ranges['Colorbar'][1] = viz.stats['max']
    level_tree.cbar.setText(1, dsp_fmt(viz.ranges['Colorbar'][0]))
    level_tree.cbar.setText(2, dsp_fmt(viz.ranges['Colorbar'][1]))
    viz.plot()
    self.refresh_plotinfos()


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
    viz.stats = {'mean': viz.var_plotted.mean(skipna=True).values,
                 'std': viz.var_plotted.std(skipna=True).values,
                 'min': viz.var_plotted.min(skipna=True).values,
                 'max': viz.var_plotted.max(skipna=True).values}
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
    self.viz.stats = {'mean': self.viz.var_plotted.mean(skipna=True).values,
                      'std': self.viz.var_plotted.std(skipna=True).values,
                      'min': self.viz.var_plotted.min(skipna=True).values,
                      'max': self.viz.var_plotted.max(skipna=True).values}
    self.refresh_plotinfos()
    self.viz.plot()


def scale_data(self):
    num, ok = QInputDialog.getDouble(self, "Scale number", "Enter the float scale number :",
                                     self.viz.scale, 0, 1e20, 3)
    if ok:
        self.viz.scale = num
        self.viz.var = self.viz.scale * self.viz.var
        self.viz.var_plotted = self.viz.scale * self.viz.var_plotted
        self.viz.plot()
        self.refresh_plotinfos()


def change_dpi(self):
    num, ok = QInputDialog.getInt(self, "dpi", "Enter the dpi number :",
                                  self.viz.dpi)
    if ok:
        self.viz.dpi = num
        self.refresh_plotcanvas()


