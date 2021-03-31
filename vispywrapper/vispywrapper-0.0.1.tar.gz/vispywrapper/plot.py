import numpy as np
import itertools
from math import floor, ceil, sqrt

from vispy import plot as vp


def rectangular_grid(plots_no):
    """Calculate the size of the matrix fitting 'plots_no' plots.

    Args:
        plots_no (int): the number of plots in the matrix.
    Returns:
        tuple containing the number of row 'rows_no' and columns 'cols_no'.
    """
    rows_no = floor(sqrt(plots_no))
    cols_no = rows_no + ceil((plots_no - rows_no**2)/rows_no)
    return rows_no, cols_no


def surface_plot(I, x=None, y=None, show=True, size=(800, 400)):
    figure = vp.Fig(size=size, show=False)
    if x is None or y is None:
        p1 = figure[0, 0].surface(zdata=I)
    else:
        p1 = figure[0, 0].surface(zdata=I, x=x, y=x)
    if show:
        figure.show(run=True)
    else:
        return figure


def get_figure(size=(800, 400), show=False):
    return vp.Fig(size=size, show=False)


def surfaces(figure, datasets, nrow=None, ncol=None):
    if nrow is None or ncol is None:
        nrow, ncol = rectangular_grid(len(datasets))

    for (i,j), data in zip(itertools.product(range(nrow),
                                             range(ncol)),
                           datasets):
        if isinstance(data, tuple):
            I,x,y = data
            figure[i,j].surface(zdata=I, x=x, y=y)
        else:    
            figure[i,j].surface(zdata=data)

