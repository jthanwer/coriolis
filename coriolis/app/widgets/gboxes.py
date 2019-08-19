from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtTest import QTest
from coriolis.util.format import dsp_fmt, dims_fmt, analyse_fmt
from coriolis.util.analyze_dims import detect_grid
from coriolis.util.analyze_dims import detect_grid
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np


class VarsGroupBox(QGroupBox):
    """
    Deals with the group of app that allow to select the variable.
    Display the variables buttons.
    """
    def __init__(self, vars_names, parent=None):
        super(QGroupBox, self).__init__('Select Variable', parent)
        self.vars_names = vars_names
        self.vars_hlay = QGridLayout(self)
        self.vars_buttons = {}
        self.nline = 4

        self.var_combo = QComboBox()
        for var in vars_names:
            self.var_combo.addItem(var)
        self.vars_hlay.addWidget(self.var_combo, 0, 0)

        # nb_var_buttons = 0
        # for var in self.vars_names:
        #     self.vars_buttons[var] = QPushButton(var, self)
        #     self.vars_buttons[var].setCheckable(True)
        #     self.vars_hlay.addWidget(self.vars_buttons[var], nb_var_buttons // self.nline,
        #                              nb_var_buttons % self.nline)
        #     nb_var_buttons += 1
        # self.var_count = 0


class DimsGroupBox(QGroupBox):
    """
    Deals with the group of app that allow to select the dimensions to plot.
    """
    def __init__(self, var, abscissa='None', ordinate='None', parent=None):
        super(QGroupBox, self).__init__('Select Dimensions', parent)
        self.layout = QGridLayout(self)
        self.dims_selection = self.DimsSelection(var, self)
        self.dims_selected = self.DimsSelected(abscissa, ordinate, self)
        self.layout.addWidget(self.dims_selection, 0, 0)
        self.layout.addWidget(self.dims_selected, 1, 0)

    class DimsSelection(QWidget):
        def __init__(self, var, parent=None):
            super(QWidget, self).__init__(parent)
            self.layout = QGridLayout(self)
            self.dim_buttons = {}
            self.nline = 4
            nb_dim_buttons = 0
            for coord in var.dims:
                self.dim_buttons[coord] = QPushButton(coord, self)
                self.dim_buttons[coord].setCheckable(True)
                self.layout.addWidget(self.dim_buttons[coord], nb_dim_buttons // self.nline,
                                      nb_dim_buttons % self.nline)
                nb_dim_buttons += 1
            self.dim_buttons[var.name] = QPushButton(var.name, self)
            self.dim_buttons[var.name].setCheckable(True)
            self.layout.addWidget(self.dim_buttons[var.name], nb_dim_buttons // 4 + 2, 0)
            # min_height = self.dim_buttons[var.name].frameGeometry().height()
            self.layout.setRowMinimumHeight(nb_dim_buttons // 4 + 1, 15)
            self.var_count = 0

    class DimsSelected(QWidget):
        def __init__(self, abscissa='None', ordinate='None', parent=None):
            super(QWidget, self).__init__(parent)
            self.abs = abscissa
            self.ord = ordinate
            self.layout = QGridLayout(self)
            text1 = "Abscisse selected : {}".format(self.abs)
            self.label1 = QLabel(text1)
            text2 = "Ordinate selected : {}".format(self.ord)
            self.label2 = QLabel(text2)
            self.layout.addWidget(self.label1, 0, 0)
            self.layout.addWidget(self.label2, 1, 0)


class VarInfosGroupBox(QGroupBox):
    """
    Deals with the group of app that display some information about the variable selected.
    """
    def __init__(self, var, parent=None):
        super(QGroupBox, self).__init__('Variable Information', parent)
        self.layout = QVBoxLayout(self)
        self.statistics = {'Mean': dsp_fmt(var.mean(skipna=True).values),
                           'Std': dsp_fmt(var.std(skipna=True).values),
                           'Max': dsp_fmt(var.max(skipna=True).values),
                           'Min': dsp_fmt(var.min(skipna=True).values),
                           }
        tree = QTreeWidget()
        tree.headerItem().setText(0, 'Name')
        tree.headerItem().setText(1, 'Value')
        tree.headerItem().setTextAlignment(0, Qt.AlignHCenter)
        tree.headerItem().setTextAlignment(1, Qt.AlignHCenter)
        variable = QTreeWidgetItem(tree)
        variable.setText(0, 'Variable')
        variable.setText(1, var.name)
        attributes = QTreeWidgetItem(tree)
        attributes.setText(0, 'Attributes')
        attributes.setExpanded(True)
        for (attr, value) in var.attrs.items():
            child = QTreeWidgetItem(attributes)
            child.setText(0, str(attr))
            child.setText(1, str(value))
        dimensions = QTreeWidgetItem(tree)
        dimensions.setText(0, 'Dimensions')
        dimensions.setExpanded(True)
        for dim in var.dims:
            child = QTreeWidgetItem(dimensions)
            child.setText(0, str(dim))
            child.setText(1, str(var.coords[dim].shape[0]))
        stats = QTreeWidgetItem(tree)
        stats.setText(0, 'Statistics')
        stats.setExpanded(True)
        for (stat, value) in self.statistics.items():
            child = QTreeWidgetItem(stats)
            child.setText(0, str(stat))
            child.setText(1, str(value))
        tree.resizeColumnToContents(0)
        # tree.setAlternatingRowColors(True)

        self.layout.addWidget(tree)


class PlotInfosGroupBox(QGroupBox):
    """
    Deals with the group of app that display some information about the plot.
    """
    def __init__(self, viz, parent=None):
        super(QGroupBox, self).__init__('Plot Information', parent)
        self.layout = QVBoxLayout(self)
        ax = viz.figure.axes[0]
        self.statistics = {'Mean': dsp_fmt(viz.stats['mean']),
                           'Std': dsp_fmt(viz.stats['std']),
                           'Max': dsp_fmt(viz.stats['max']),
                           'Min': dsp_fmt(viz.stats['min']),
                           'Scale': dsp_fmt(viz.scale),
                           }
        tree = QTreeWidget()
        tree.headerItem().setText(0, 'Name')
        tree.headerItem().setText(1, 'Value 1')
        tree.headerItem().setText(2, 'Value 2')
        tree.headerItem().setTextAlignment(0, Qt.AlignHCenter)
        tree.headerItem().setTextAlignment(1, Qt.AlignHCenter)
        tree.headerItem().setTextAlignment(2, Qt.AlignHCenter)
        variable = QTreeWidgetItem(tree)
        variable.setText(0, 'Variable')
        variable.setText(1, viz.var.name)

        abscissa = QTreeWidgetItem(tree)
        abscissa.setText(0, 'Abscissa')
        child = QTreeWidgetItem(abscissa)
        child.setText(0, 'Name')
        child.setText(1, viz.abs_name)
        child = QTreeWidgetItem(abscissa)
        child.setText(0, 'Range')
        child.setText(1, dsp_fmt(ax.get_xlim()[0]))
        child.setText(2, dsp_fmt(ax.get_xlim()[1]))
        abscissa.setExpanded(True)

        ordinate = QTreeWidgetItem(tree)
        ordinate.setText(0, 'Ordinate')
        child = QTreeWidgetItem(ordinate)
        child.setText(0, 'Name')
        child.setText(1, viz.ord_name)
        child = QTreeWidgetItem(ordinate)
        child.setText(0, 'Range')
        child.setText(1, dsp_fmt(ax.get_ylim()[0]))
        child.setText(2, dsp_fmt(ax.get_ylim()[1]))
        ordinate.setExpanded(True)

        stats = QTreeWidgetItem(tree)
        stats.setText(0, 'Statistics')
        stats.setExpanded(True)
        for (stat, value) in self.statistics.items():
            child = QTreeWidgetItem(stats)
            child.setText(0, str(stat))
            child.setText(1, str(value))
        tree.resizeColumnToContents(0)

        self.layout.addWidget(tree)


class BasicActionsGroupBox(QGroupBox):
    """
    Deals with the group of app that allows to do basic actions on plot.
    """
    def __init__(self, parent=None):
        super(QGroupBox, self).__init__('Basic Actions', parent)
        self.layout = QGridLayout(self)
        self.button_swap = QPushButton('Swap axes', self)
        self.button_invertx = QPushButton('Invert X-axis', self)
        self.button_inverty = QPushButton('Invert Y-axis', self)
        self.layout.addWidget(self.button_swap, 0, 0)
        self.layout.addWidget(self.button_invertx, 0, 1)
        self.layout.addWidget(self.button_inverty, 0, 2)
        self.button_invertx.setCheckable(True)
        self.button_inverty.setCheckable(True)


class AdvancedActionsGroupBox(QGroupBox):
    """
    Deals with the group of app that allows to do advanced actions on plot.
    """
    def __init__(self, viz, parent=None):
        super(QGroupBox, self).__init__('Advanced Actions', parent)
        self.viz = viz
        self.parent = parent
        self.layout = QGridLayout(self)
        self.auto_range = QPushButton('Auto-Range')
        self.apply_ranges = QPushButton('Apply Ranges\n(from below)')
        self.map_but = QPushButton('Draw Map')
        self.log_xaxis_but = QPushButton('Log X-axis')
        self.log_xaxis_but.setCheckable(True)
        self.log_yaxis_but = QPushButton('Log Y-axis')
        self.log_yaxis_but.setCheckable(True)

        if self.viz.options['x_scale'] == 'log':
            self.log_xaxis_but.setChecked(True)
        if self.viz.options['y_scale'] == 'log':
            self.log_yaxis_but.setChecked(True)
        self.levels_tree = self.LevelsTree(self.viz)
        self.layout.addWidget(self.auto_range, 1, 0, 1, 3)
        self.layout.addWidget(self.apply_ranges, 2, 0, 1, 3)
        self.layout.addWidget(self.levels_tree, 3, 0, 1, 3)
        self.layout.addWidget(self.log_xaxis_but, 4, 0)
        self.layout.addWidget(self.log_yaxis_but, 4, 1)
        if detect_grid(viz):
            self.layout.addWidget(self.map_but, 5, 0, 1, 3)
            self.map_but.setCheckable(True)
            if self.viz.options['map']:
                self.map_but.setChecked(True)
        if self.viz.options['plot_type'] == '2d':
            self.cmap_cbox = QComboBox()
            cmaps = ['viridis', 'jet', 'plasma', 'OrRd', 'coolwarm',  'gist_rainbow', 'terrain',
                     'rainbow']
            for cmap in cmaps:
                self.cmap_cbox.addItem(cmap)
            self.log_cbar_but = QPushButton('Log Colorbar')
            self.log_cbar_but.setCheckable(True)
            if self.viz.options['cbar_scale'] == 'log':
                self.log_cbar_but.setChecked(True)
            self.layout.addWidget(self.cmap_cbox, 0, 0, 1, 3)
            self.layout.addWidget(self.log_cbar_but, 4, 2)
            self.log_cbar_but.clicked.connect(self.log_cbar)
            self.cmap_cbox.currentTextChanged.connect(self.select_cbar)
        self.log_xaxis_but.clicked.connect(self.log_xaxis)
        self.log_yaxis_but.clicked.connect(self.log_yaxis)
        self.map_but.clicked.connect(self.map)

    def log_xaxis(self):
        sender = self.sender()
        if sender.isChecked():
            self.viz.options['x_scale'] = 'log'
        else:
            self.viz.options['x_scale'] = 'linear'
        self.viz.plot()

    def log_yaxis(self):
        sender = self.sender()
        if sender.isChecked():
            self.viz.options['y_scale'] = 'log'
        else:
            self.viz.options['y_scale'] = 'linear'
        self.viz.plot()

    def log_cbar(self):
        sender = self.sender()
        if sender.isChecked():
            self.viz.options['cbar_scale'] = 'log'
        else:
            self.viz.options['cbar_scale'] = 'linear'
        self.viz.plot()

    def map(self):
        sender = self.sender()
        self.viz.options['map'] = sender.isChecked()
        if 'lon' in self.viz.abs_name.lower():
            self.viz.plot()
        else:
            self.parent.swap_axes()
            self.viz.plot()

    def select_cbar(self, value):
        self.viz.options['cmap'] = value
        self.viz.plot()

    class LevelsTree(QTreeWidget):
        """
        Sub-class : Allows to select ranges and levels for the plot
        """
        def __init__(self, viz):
            super(QTreeWidget, self).__init__()
            ax = viz.figure.axes[0]
            self.ranges = {'X-axis': [viz.ranges['X-axis'][0], viz.ranges['X-axis'][1]],
                           'Y-axis': [viz.ranges['Y-axis'][0], viz.ranges['Y-axis'][1]],
                           'Colorbar': [viz.var_plotted.min(skipna=True).values,
                                        viz.var_plotted.max(skipna=True).values]}
            self.headerItem().setText(0, 'Range')
            self.headerItem().setText(1, 'Min')
            self.headerItem().setText(2, 'Max')
            self.headerItem().setTextAlignment(0, Qt.AlignHCenter)
            self.headerItem().setTextAlignment(1, Qt.AlignHCenter)
            self.headerItem().setTextAlignment(2, Qt.AlignHCenter)
            self.range_x = QTreeWidgetItem(self)
            self.range_x.setText(0, 'X-axis')
            self.range_x.setText(1, dsp_fmt(self.ranges['X-axis'][0]))
            self.range_x.setText(2, dsp_fmt(self.ranges['X-axis'][1]))
            self.range_x.setFlags(self.range_x.flags() | Qt.ItemIsEditable)
            self.range_x.setTextAlignment(0, Qt.AlignHCenter)
            self.range_x.setTextAlignment(1, Qt.AlignHCenter)
            self.range_x.setTextAlignment(2, Qt.AlignHCenter)

            self.range_y = QTreeWidgetItem(self)
            self.range_y.setText(0, 'Y-axis')
            self.range_y.setText(1, dsp_fmt(self.ranges['Y-axis'][0]))
            self.range_y.setText(2, dsp_fmt(self.ranges['Y-axis'][1]))
            self.range_y.setFlags(self.range_y.flags() | Qt.ItemIsEditable)
            self.range_y.setTextAlignment(0, Qt.AlignHCenter)
            self.range_y.setTextAlignment(1, Qt.AlignHCenter)
            self.range_y.setTextAlignment(2, Qt.AlignHCenter)

            self.cbar = QTreeWidgetItem(self)
            self.cbar.setText(0, 'Colorbar')
            self.cbar.setText(1, dsp_fmt(viz.var_plotted.min().values))
            self.cbar.setText(2, dsp_fmt(viz.var_plotted.max().values))
            self.cbar.setFlags(self.cbar.flags() | Qt.ItemIsEditable)
            self.cbar.setTextAlignment(0, Qt.AlignHCenter)
            self.cbar.setTextAlignment(1, Qt.AlignHCenter)
            self.cbar.setTextAlignment(2, Qt.AlignHCenter)
            if viz.options['plot_type'] == '1d':
                self.cbar.setHidden(True)

            self.resizeColumnToContents(0)
            # self.resizeColumnToContents(1)
            # self.resizeColumnToContents(2)
            self.itemChanged.connect(self.change_ranges)
            self.setSelectionMode(QAbstractItemView.ContiguousSelection)

        def change_ranges(self):
            """
            Change the attributes ranges so we can use this data after
            """
            selected_item = self.selectedItems()
            if selected_item:
                base_node = selected_item[0]
                self.ranges[base_node.text(0)][0] = analyse_fmt(base_node.text(1))
                self.ranges[base_node.text(0)][1] = analyse_fmt(base_node.text(2))
                self.clearSelection()

        def keyPressEvent(self, e):
            if e.key() == Qt.Key_Escape:
                self.clearSelection()


class CustomPlotGroupBox(QGroupBox):
    """
    Deals with the group of app that allow to select the slices of data and to launch animation.
    """
    def __init__(self, var, abs_name, ord_name, parent=None):
        super(QGroupBox, self).__init__('Set the Data', parent)
        self.layout = QGridLayout(self)
        self.var = var
        self.dims = self.var.dims
        self.apply_button = QPushButton('Apply\nSlices')
        self.reset_button = QPushButton('Reset\nSlices')
        self.tree = self.SlicesTree(self.var)
        self.switch_dimsgif = 'on'
        self.dimsgif = self.DimsGif(self.var, abs_name, ord_name)
        self.layout.addWidget(self.dimsgif, 0, 0, 1, 2)
        self.layout.addWidget(self.tree, 1, 0, 1, 2)
        self.layout.addWidget(self.reset_button, 2, 0)
        self.layout.addWidget(self.apply_button, 2, 1)
        self.reset_button.clicked.connect(self.reset_all_slices)

    def reset_all_slices(self):
        self.tree.slices = {self.var.dims[i]: [0, self.var.coords[self.var.dims[i]].shape[0] - 1, 1]
                            for i in range(len(self.var.dims))}
        for dim in self.var.dims:
            self.tree.children[dim].setText(1, '0')
            self.tree.children[dim].setText(2, str(self.var.coords[dim].shape[0] - 1))
            self.tree.children[dim].setText(3, '1')
        for item in self.dimsgif.qcheckboxes.values():
            item.setChecked(False)

    def reset_dim_slices(self):
        sender = self.sender()
        dim = sender.text()
        if not sender.isChecked():
            self.tree.slices[dim] = [0, self.var.coords[dim].shape[0] - 1, 1]
            self.tree.children[dim].setText(1, '0')
            self.tree.children[dim].setText(2, str(self.var.coords[dim].shape[0] - 1))
            self.tree.children[dim].setText(3, '1')

    class SlicesTree(QTreeWidget):
        """
        Sub-class : Allows to select data slices
        """
        def __init__(self, var):
            super(QTreeWidget, self).__init__()
            self.slices = {var.dims[i]: [0, var.coords[var.dims[i]].shape[0] - 1, 1]
                           for i in range(len(var.dims))}
            self.headerItem().setText(0, 'Dim.')
            self.headerItem().setText(1, 'Start')
            self.headerItem().setText(2, 'Stop')
            self.headerItem().setText(3, 'Step')
            self.headerItem().setTextAlignment(0, Qt.AlignHCenter)
            self.headerItem().setTextAlignment(1, Qt.AlignHCenter)
            self.headerItem().setTextAlignment(2, Qt.AlignHCenter)
            self.headerItem().setTextAlignment(3, Qt.AlignHCenter)
            self.children = {}
            for dim in var.dims:
                self.children[dim] = QTreeWidgetItem(self)
                self.children[dim].setText(0, dim)
                self.children[dim].setText(1, '0')
                self.children[dim].setText(2, str(var.coords[dim].shape[0] - 1))
                self.children[dim].setText(3, '1')
                self.children[dim].setFlags(self.children[dim].flags() | Qt.ItemIsEditable)
                self.children[dim].setTextAlignment(1, Qt.AlignHCenter)
                self.children[dim].setTextAlignment(2, Qt.AlignHCenter)
                self.children[dim].setTextAlignment(3, Qt.AlignHCenter)
            self.resizeColumnToContents(0)
            self.resizeColumnToContents(1)
            self.resizeColumnToContents(2)
            self.resizeColumnToContents(3)
            self.itemChanged.connect(self.change_slices)

        def change_slices(self):
            """
            Change the attributes slices so we can use this data after
            """
            selected_item = self.selectedItems()
            if selected_item:
                base_node = selected_item[0]
                self.slices[base_node.text(0)][0] = int(base_node.text(1))
                self.slices[base_node.text(0)][1] = int(base_node.text(2))
                self.slices[base_node.text(0)][2] = int(base_node.text(3))

    class DimsGif(QWidget):
        """
        Sub-class : Allows to launch animations and deal with one-value slices.
        """
        def __init__(self, var, abs_name, ord_name):
            super(QWidget, self).__init__()
            self.layout = QGridLayout(self)
            self.dims = list(var.dims)
            if abs_name != var.name:
                self.dims.remove(abs_name)
            if ord_name != var.name:
                self.dims.remove(ord_name)
            self.qcheckboxes = {}
            self.qspinboxes = {}
            self.combobox_dims = QComboBox()
            self.animation_but = QPushButton('Start\nAnimation')
            self.animation_but.setCheckable(True)
            self.slider_pace = QSlider(Qt.Horizontal)
            self.slider_pace.setRange(50, 1000)
            self.slider_pace.setTickPosition(2)
            self.slider_pace.setTickInterval(100)
            self.slider_pace.setSingleStep(50)
            self.slider_pace.setValue(200)
            label1 = QLabel('with this dimension :')
            label2 = QLabel('with this frequency :')
            self.label3 = QLabel('{} ms'.format(self.slider_pace.value()))
            for (i, dim) in enumerate(self.dims):
                self.qcheckboxes[dim] = QCheckBox(dim)
                self.qcheckboxes[dim].setObjectName(dim)
                self.qspinboxes[dim] = QSpinBox()
                self.qspinboxes[dim].setWrapping(True)
                self.qspinboxes[dim].setEnabled(False)
                self.qspinboxes[dim].setRange(0, var.coords[dim].shape[0] - 1)
                self.qspinboxes[dim].setObjectName(dim)
                self.layout.addWidget(self.qcheckboxes[dim], i, 0)
                self.layout.addWidget(self.qspinboxes[dim], i, 2)
                self.combobox_dims.addItem(dim)

            position = len(self.dims) + 1
            if position > 1:
                self.layout.addWidget(self.animation_but, position, 0)
                self.layout.addWidget(label1, position, 1)
                self.layout.addWidget(self.combobox_dims, position, 2)
                self.layout.addWidget(label2, position + 1, 1)
                self.layout.addWidget(self.label3, position + 1, 2)
                self.layout.addWidget(self.slider_pace, position + 2, 2)
            self.layout.setRowMinimumHeight(position - 1, 15)

            for item in self.qcheckboxes.values():
                item.toggled.connect(self.toggle_checkbox)
            self.slider_pace.valueChanged.connect(self.change_frequency)

        def toggle_checkbox(self):
            sender = self.sender()
            dim = sender.text()
            if sender.isChecked():
                self.qspinboxes[dim].setEnabled(True)
                value = self.qspinboxes[dim].value()
                self.qspinboxes[dim].setValue(value - 1)
                self.qspinboxes[dim].setValue(value)
            else:
                self.qspinboxes[sender.text()].setEnabled(False)

        def change_frequency(self):
            sender = self.sender()
            self.label3.setText('{} ms'.format(sender.value()))


class DimsTableGroupBox(QGroupBox):
    """
    Deals with the group that display dimensions values
    """
    def __init__(self, var, parent=None):
        super(QGroupBox, self).__init__('Dimensions Table', parent)
        self.tab = QTabWidget()
        self.layout = QGridLayout(self)
        self.tables = {}
        for dim in var.dims:
            values = var.coords[dim].values
            dim_range = var.coords[dim].values.shape[0]
            self.tables[dim] = QTableWidget(dim_range, 1)
            for i in range(dim_range):
                new_item = QTableWidgetItem(dims_fmt(values[i]))
                self.tables[dim].setItem(i, 0, new_item)
            self.tables[dim].setHorizontalHeaderLabels([dim])
            self.tables[dim].setVerticalHeaderLabels([str(i) for i in range(dim_range)])
            self.tab.addTab(self.tables[dim], dim)
            self.tables[dim].resizeColumnToContents(0)
        self.layout.addWidget(self.tab, 0, 0)

