import sys
import os
import xarray as xr
import matplotlib.pyplot as plt
from netCDF4 import Dataset


workdir = os.path.dirname(os.path.dirname(__file__))
plt.style.use(workdir + '/custom.mplstyle')


def init_app():
    print('Initializing Coriolis')
    print('Parsing data')
    (file_name, file_path) = argument_parser()
    dataset = file_analysis(file_name, file_path)
    return dataset, file_path


def argument_parser():
    try:
        file_name = sys.argv[1]
        file_path = os.path.realpath(file_name)
    except IndexError as e:
        print("File Error : No NetCDF file path given")
        sys.exit(1)
    return file_name, file_path


def file_analysis(file_name, file_path):
    try:
        var2exclude = netcdf_analysis(file_path)
        dataset = xr.open_dataset(file_path, drop_variables=var2exclude)
    except FileNotFoundError as e:
        print('The file %s was not found at the path given' % file_name)
        sys.exit(1)
    except OSError as e:
        print('The file format has to be NetCDF format')
        sys.exit(1)
    except xr.core.variable.MissingDimensionsError as e:
        print('Variables are preventing xarray from working correctly. Here is the error : \n%s. \n\n' % e)
        var2exclude = netcdf_analysis(file_path)
        print('Excluding variables : ')
        print(var2exclude)
        dataset = xr.open_dataset(file_path, drop_variables=var2exclude)
    except:
        print('An error has occured')
        sys.exit(1)
    return dataset


def netcdf_analysis(file_path):
    dataset = Dataset(file_path)
    var2exclude = []
    for var in dataset.variables:
        var_set = {var}
        dim_set = set(dataset.variables[var].dimensions)
        inter = var_set.intersection(dim_set)
        if len(inter) > 0 and len(dim_set) > 1:
            var2exclude.append(var)
    return var2exclude

