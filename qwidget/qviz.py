from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.colors as colors
from qwidget.qgboxes import *


class PlotCanvas(FigureCanvas):
    def __init__(self, var, width, height):
        self.dpi = 100
        fig = Figure(figsize=(width/(2 * self.dpi), height/(2 * self.dpi)), dpi=self.dpi)
        FigureCanvas.__init__(self, fig)
        self.updateGeometry()
        fig.set_tight_layout(True)
        self.var = var
        self.var_plotted = var
        self.abs_name = self.var.dims[0]
        self.abs_var = self.var.coords[self.abs_name]
        self.ord_name = self.var.name
        self.ord_var = self.var
        self.slices = {self.var.dims[i]: [0, var.coords[self.var.dims[i]].shape[0] - 1, 1]
                       for i in range(len(self.var.dims))}
        self.options = {'plot_type': '1d', 'isx_inverted': False, 'isy_inverted': False,
                        'x_scale': 'linear', 'y_scale': 'linear', 'cbar': 'linear',
                        'contourf': False}
        self.vmin_cbar = self.var_plotted.min().values
        self.vmax_cbar = self.var_plotted.max().values
        self.ranges = {'X-axis': [self.abs_var.min().values, self.abs_var.max().values],
                       'Y-axis': [self.vmin_cbar, self.vmax_cbar],
                       'Colorbar': [self.vmin_cbar, self.vmax_cbar]}
        self.plot()

    def plot(self):
        self.figure.clear()
        if self.var.name in [self.abs_name, self.ord_name]:
            self.plot_1d()
        else:
            self.plot_2d()

    def plot_1d(self):
        self.options['plot_type'] = '1d'
        ax = self.figure.add_subplot(111)
        self.var_plotted = self.var_resizing()
        if self.ord_name == self.var.name:
            dim_slices = self.slices[self.abs_name]
            dimension = self.abs_var[dim_slices[0]: dim_slices[1] + 1: dim_slices[2]]
            ax.scatter(dimension.values, self.var_plotted.values)
        else:
            dim_slices = self.slices[self.ord_name]
            dimension = self.ord_var[dim_slices[0]: dim_slices[1] + 1: dim_slices[2]]
            ax.scatter(self.var_plotted.values, dimension.values)
        if self.options['x_scale'] != 'linear':
            ax.set_xscale(self.options['x_scale'])
        if self.options['y_scale'] != 'linear':
            ax.set_yscale(self.options['y_scale'])
        ax.set_xlim(self.ranges['X-axis'][0], self.ranges['X-axis'][1])
        ax.set_ylim(self.ranges['Y-axis'][0], self.ranges['Y-axis'][1])
        if self.options['isx_inverted']:
            ax.invert_xaxis()
        if self.options['isy_inverted']:
            ax.invert_yaxis()
        ax.set_title(self.var.name)
        ax.set_xlabel(self.abs_name)
        ax.set_ylabel(self.ord_name)
        self.draw()

    def plot_2d(self):
        self.options['plot_type'] = '2d'
        ax = self.figure.add_subplot(111)
        abs_slices = self.slices[self.abs_name]
        ord_slices = self.slices[self.ord_name]
        abs_plot = self.abs_var[abs_slices[0]: abs_slices[1] + 1: abs_slices[2]]
        ord_plot = self.ord_var[ord_slices[0]: ord_slices[1] + 1: ord_slices[2]]
        self.var_plotted = self.var_resizing()
        abs_plot2d, ord_plot2d = np.meshgrid(abs_plot, ord_plot)
        vmin = self.ranges['Colorbar'][0]
        vmax = self.ranges['Colorbar'][1]
        try:
            if self.options['cbar'] == 'linear':
                img = ax.pcolormesh(abs_plot2d, ord_plot2d, self.var_plotted,
                                    vmin=vmin, vmax=vmax)
            else:
                img = ax.pcolormesh(abs_plot2d, ord_plot2d, self.var_plotted,
                                    norm=colors.LogNorm(vmin=vmin, vmax=vmax))
        except TypeError:
            if self.options['cbar'] == 'linear':
                img = ax.pcolormesh(abs_plot2d, ord_plot2d, np.swapaxes(self.var_plotted, 0, 1),
                                    vmin=vmin, vmax=vmax)
            else:
                img = ax.pcolormesh(abs_plot2d, ord_plot2d, np.swapaxes(self.var_plotted, 0, 1),
                                    norm=colors.LogNorm(vmin=vmin, vmax=vmax))
        if self.options['x_scale'] != 'linear':
            ax.set_xscale(self.options['x_scale'])
        if self.options['y_scale'] != 'linear':
            ax.set_yscale(self.options['y_scale'])
        ax.set_xlim(self.ranges['X-axis'][0], self.ranges['X-axis'][1])
        ax.set_ylim(self.ranges['Y-axis'][0], self.ranges['Y-axis'][1])
        if self.options['isx_inverted']:
            ax.invert_xaxis()
        if self.options['isy_inverted']:
            ax.invert_yaxis()
        ax.set_title(self.var.name)
        ax.set_xlabel(self.abs_name)
        ax.set_ylabel(self.ord_name)
        self.figure.colorbar(img)
        self.draw()

    def var_resizing(self):
        dict_slices = {dim: slice(self.slices[dim][0], self.slices[dim][1] + 1, self.slices[dim][2])
                       for dim in self.var.dims}
        var_mean = self.var[dict_slices]
        axis = [a for a in range(len(self.var.dims))]
        if self.abs_name != self.var.name:
            axis.remove(self.var.dims.index(self.abs_name))
        if self.ord_name != self.var.name:
            axis.remove(self.var.dims.index(self.ord_name))
        axis = tuple(axis)
        if len(axis) != 0:
            var_mean = var_mean.mean(axis=axis)
        return var_mean

    def swap_axes(self):
        self.figure.clear()
        (self.abs_name, self.ord_name) = (self.ord_name, self.abs_name)
        (self.abs_var, self.ord_var) = (self.ord_var, self.abs_var)
        (self.ranges['X-axis'][0], self.ranges['Y-axis'][0]) = \
            (self.ranges['Y-axis'][0], self.ranges['X-axis'][0])
        (self.ranges['X-axis'][1], self.ranges['Y-axis'][1]) = \
            (self.ranges['Y-axis'][1], self.ranges['X-axis'][1])
        self.plot()

    def invert_xaxis(self):
        self.options['isx_inverted'] = not self.options['isx_inverted']
        ax = self.figure.axes[0]
        ax.invert_xaxis()
        self.draw()

    def invert_yaxis(self):
        self.options['isy_inverted'] = not self.options['isy_inverted']
        ax = self.figure.axes[0]
        ax.invert_yaxis()
        self.draw()
