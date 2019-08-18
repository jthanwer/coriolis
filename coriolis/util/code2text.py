def code2text(fname, viz, path):
    code = 'import matplotlib.pyplot as plt\n'
    code += 'import xarray as xr\n\n\n'
    code += 'dataset = xr.open_dataset(\'{}\')'.format(path)
    code += 'variable = dataset[{}]'.format(viz.var.name)
    code += 'abs_var = variable.coords[\'{}\']'.format(viz.abs_name)
    code += 'ord_var = variable.coords[\'{}\']'.format(viz.abs_name)
    code += 'fig = plt.figure()\n'
    if viz.options['plot_type'] == '2d':
        code += 'ax = fig.add_subplot(111)\n'
        code += 'abs_slices = {}\n'.format(viz.slices[viz.abs_name])
        code += 'ord_slices = {}\n'.format(viz.slices[viz.ord_name])
        code += 'abs_plot = abs_var[abs_slices[0]: abs_slices[1] + 1: abs_slices[2]]\n'
        code += 'ord_plot = ord_var[ord_slices[0]: ord_slices[1] + 1: ord_slices[2]]\n'
        code += 'abs_plot2d, ord_plot2d = np.meshgrid(abs_plot, ord_plot)\n'
        # viz.var_plotted = viz.var_resizing()
        code += 'vmin = {}\n'.format(viz.ranges['Colorbar'][0])
        code += 'vmax = {}\n'.format(viz.ranges['Colorbar'][1])
        code += 'try:\n'
        if viz.options['cbar_scale'] == 'linear':
            code += '\timg = ax.pcolormesh(abs_plot2d, ord_plot2d, var_plotted, ' \
                    'vmin=vmin, vmax=vmax)\n'
        else:
            code += '\timg = ax.pcolormesh(abs_plot2d, ord_plot2d, viz.var_plotted, ' \
                    'norm=colors.LogNorm(vmin=vmin, vmax=vmax))\n'
        code += 'except TypeError:'
        if viz.options['cbar_scale'] == 'linear':
            code += 'img = ax.pcolormesh(abs_plot2d, ord_plot2d, np.swapaxes(viz.var_plotted, 0, 1), ' \
                'vmin=vmin, vmax=vmax)\n'
        else:
            code += 'img = ax.pcolormesh(abs_plot2d, ord_plot2d, np.swapaxes(viz.var_plotted, 0, 1), ' \
                    'norm=colors.LogNorm(vmin=vmin, vmax=vmax))\n'
        if viz.options['x_scale'] != 'linear':
            code += 'ax.set_xscale({})\n'.format(viz.options['x_scale'])
        if viz.options['y_scale'] != 'linear':
            code += 'ax.set_yscale({})\n'.format(viz.options['y_scale'])
        code += 'ax.set_xlim({}, {})'.format(viz.ranges['X-axis'][0], viz.ranges['X-axis'][1])
        code += 'ax.set_xlim({}, {})'.format(viz.ranges['Y-axis'][0], viz.ranges['Y-axis'][1])
        if viz.options['isx_inverted']:
            code += 'ax.invert_xaxis()'
        if viz.options['isy_inverted']:
            code += 'ax.invert_yaxis()'
        code += 'ax.set_title(\'{}\')'.format(viz.var.name)
        code += 'ax.set_xlabel(\'{}\')'.format(viz.abs_name)
        code += 'ax.set_ylabel(\'{}\')'.format(viz.ord_name)
        code += 'fig.colorbar(img)'
        code += 'plt.show()'

    with open(fname, 'w') as f:
        f.write(code)

