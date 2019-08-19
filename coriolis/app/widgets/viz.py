from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.colors as colors
import cartopy.crs as ccrs
from .gboxes import *


class PlotCanvas(FigureCanvas):
    def __init__(self, var, width, height, dpi=80):
        self.dpi = dpi
        self.w = width
        self.h = height
        fig = Figure(figsize=(self.w/(2 * self.dpi), self.h/(2 * self.dpi)),
                     dpi=self.dpi)
        FigureCanvas.__init__(self, fig)
        self.updateGeometry()
        fig.set_tight_layout(True)
        self.var = var
        self.var_plotted = var
        self.scale = 1.
        self.abs_name = self.var.dims[0]
        self.abs_var = self.var.coords[self.abs_name]
        self.ord_name = self.var.name
        self.ord_var = self.var
        self.slices = {self.var.dims[i]: [0, var.coords[self.var.dims[i]].shape[0] - 1, 1]
                       for i in range(len(self.var.dims))}
        self.options = dict(plot_type='1d', isx_inverted=False, isy_inverted=False,
                            x_scale='linear', y_scale='linear', cbar_scale='linear',
                            contourf=False, map=False, cmap='viridis')
        self.stats = {'mean': self.var_plotted.mean(skipna=True).values,
                      'std': self.var_plotted.std(skipna=True).values,
                      'min': self.var_plotted.min(skipna=True).values,
                      'max': self.var_plotted.max(skipna=True).values}
        self.ranges = {'X-axis': [self.abs_var.min().values, self.abs_var.max().values],
                       'Y-axis': [self.stats['min'], self.stats['max']],
                       'Colorbar': [self.stats['min'], self.stats['max']]}
        self.var_plotted = self.var_resizing()
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
        opts = self.options
        opts['plot_type'] = '2d'
        self.var_plotted = self.var_resizing()
        vmin = self.ranges['Colorbar'][0]
        vmax = self.ranges['Colorbar'][1]
        if opts['map']:
            ax = self.figure.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
            ax.coastlines()
        else:
            ax = self.figure.add_subplot(111)
        if opts['cbar_scale'] == 'linear':
            self.var_plotted.plot.pcolormesh(self.abs_name, self.ord_name,
                                             ax=ax, vmin=vmin, vmax=vmax, cmap=plt.get_cmap(opts['cmap']))
        elif opts['cbar_scale'] == 'log':
            self.var_plotted.plot.pcolormesh(self.abs_name, self.ord_name,
                                             ax=ax, norm=colors.LogNorm(vmin=vmin, vmax=vmax),
                                             cmap=plt.get_cmap(opts['cmap']))
        ax.set_xlim(self.ranges['X-axis'][0], self.ranges['X-axis'][1])
        ax.set_ylim(self.ranges['Y-axis'][0], self.ranges['Y-axis'][1])
        ax.set_xscale(opts['x_scale']) if opts['x_scale'] != 'linear' else None
        ax.set_yscale(opts['y_scale']) if opts['y_scale'] != 'linear' else None
        ax.invert_xaxis() if opts['isx_inverted'] else None
        ax.invert_yaxis() if opts['isy_inverted'] else None

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
