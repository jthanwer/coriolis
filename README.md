# Coriolis

## What is it ?
Coriolis is a quick visualization software developped using PyQt5 and xarray. 
It allows the user to get a quick insight of a NetCDF file.

It provides 4-D field main statistics, an embedded matplotlib canvas 
to visualize the data you choose to plot and some features to save
the figure, scale the data, change the colorbar, use non-linear axis scales, ...

An animation widget is implemented. However, at this point, matplotlib is not fast enough to enable a 
confortable quickly refreshing plots. Other software such as NcView should be used instead.

More importantly, Coriolis allows the user to precisely select the data to plot.
1-D and 2-D plots are possible.

## How to install it ?

A simple 

conda install coriolis 

is normally sufficient to install the package.

You can then use the package by running your terminal
and using this command :

corio yourfile.nc

## How to customize it ?

You want to customize the figures you're plotting the same way matplotlib
allows you to do it ?

You can modify the file custom.mplstyle and change the settings.