import numpy as np
import datetime


def dsp_fmt(x):
    """
    Format display for numbers
    """
    if isinstance(x, np.datetime64):
        x = np.datetime64(x)
        x = datetime.datetime.utcfromtimestamp(x.astype('O') / 1e9)
        return x.strftime('%Y-%m-%dT%H:%M')
    else:
        if -999 < x < 999 and (x < -1 or 1 < x):
            return '%.1f' % x
        elif x == 0:
            return '0'
        else:
            return '%.3e' % x


def dims_fmt(x):
    """
    Format display for dimensions statistics
    """
    if np.issubdtype(x.dtype, np.datetime64):
        x = datetime.datetime.utcfromtimestamp(x.astype('O') / 1e9)
        return x.strftime('%Y-%m-%dT%H:%M')
    else:
        return '%s' % x


def analyse_fmt(x):
    try:
        return float(x)
    except ValueError:
        return np.datetime64(x, 'ns')
