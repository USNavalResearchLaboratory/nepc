# -*- coding: utf-8 -*-
"""
Pandas Sparklines
Colin Dietrich 2017
"""

import base64
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from IPython.display import display, HTML

jupyter_table_css = """body {
                        margin: 0;
                        font-family: Helvetica;
                    }
                    table.dataframe {
                        border-collapse: collapse;
                        border: none;
                    }
                    table.dataframe tr {
                        border: none;
                    }
                    table.dataframe td, table.dataframe th {
                        margin: 0;
                        border: 1px solid #000000;
                        padding-left: 0.25em;
                        padding-right: 0.25em;
                    }
                    table.dataframe th:not(:empty) {
                        background-color: #f2f2f2;
                        text-align: left;
                        font-weight: bold;
                    }
                    table.dataframe tr:nth-child(2) th:empty {
                        border-left: none;
                        border-right: 1px dashed #888;
                    }
                    table.dataframe td {
                        border: 1px solid #bababa;
                        background-color: #ffffff;
                    }
                    """

html_head = """<!DOCTYPE html>
            <html>
            <head>
            <style>""" + jupyter_table_css \
            + """</style>
            </head>
            <body>"""

html_tail = """</body>
               </html>"""


def column_sparklines():
    """Set column display width and maximum items displayed to
    prevent sparklines from being truncated
    """
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.max_seq_items', 2)


def column_reset():
    """Reset column display width and maximum items to defaults"""
    pd.reset_option('display.max_colwidth')
    pd.reset_option('display.max_seq_items')


def sparkline(data,
              point=True, point_color='red', point_marker='.',
              point_fill='red', point_size=6, point_alpha=1.0,
              fill=True, fill_color='blue', fill_alpha=0.1,
              figsize=(4, 0.25), xlim=None, ylim=None, **kwargs):
    """Create a single HTML image tag containing a base64 encoded
    sparkline style plot

    Parameters
    ----------
    data : array-like (list, 1d Numpy array, Pandas Series) sequence of
        data to plot
    point : bool, show point marker on last point on right
    point_location : not implemented, always plots rightmost
    point_color : str, matplotlib color code for point, default 'red'
    point_marker : str, matplotlib marker code for point
    point_fill : str, matplotlib marker fill color for point, default 'red'
    point_size : int, matplotlib markersize, default 6
    point_alpha : float, matplotlib alpha transparency for point
    fill : bool, show fill below line
    fill_color : str, matplotlib color code for fill
    fill_alpha : float, matplotlib alpha transparency for fill
    figsize : tuple of float, length and height of sparkline plot.  Attribute
        of matplotlib.pyplot.plot.
    **kwargs : keyword arguments passed to matplotlib.pyplot.plot
    """

    data = list(data)

    fig = plt.figure(figsize=figsize)  # set figure size to be small
    ax = fig.add_subplot(111)
    plot_len = len(data)
    plot_min = min(data)
    point_x = plot_len - 1

    plt.plot(data, **kwargs)

    # turn off all axis annotations
    ax.axis('off')

    # fill between the axes
    plt.fill_between(range(plot_len), data, plot_len*[plot_min],
                     color=fill_color, alpha=fill_alpha)

    # plot the right-most point red, probably on makes sense in timeseries
    plt.plot(point_x, data[point_x], color=point_fill,
             marker=point_marker, markeredgecolor=point_color,
             markersize=point_size,
             alpha=point_alpha, clip_on=False)

    # squeeze axis to the edges of the figure
    fig.subplots_adjust(left=0)
    fig.subplots_adjust(right=0.99)
    fig.subplots_adjust(bottom=0.1)
    fig.subplots_adjust(top=0.9)

    # save the figure to html
    bio = BytesIO()
    plt.savefig(bio)
    plt.close()
    html = """<img src="data:image/png;base64,%s"/>""" % base64.b64encode(bio.getvalue()).decode('utf-8')
    return html


def create(data, **kwargs):
    """Create a column of html image data to render as inline sparklines.

    Parameters
    ----------
    data : Pandas Dataframe, containing all columns that contain data to plot
    **kwargs : keyword arguments to pass to sparkline function

    Returns
    -------
    df : Pandas Dataframe with column named 'sparkline'
    """

    _df = pd.DataFrame()

    def _func(x):
        return sparkline(x, **kwargs)
    _df['sparkline'] = data.apply(_func, axis=1)
    return _df


def show(dataframe, index=False):
    """Display dataframe in Jupyter Notebook.

    Requires '%matplotlib inline' to have been set in the notebook.

    Parameters
    ----------
    dataframe : Pandas Dataframe, dataframe with 'data' column which contains
        array-like data.
    index : bool, optional
        whether to print index (row) labels, default True
    """
    column_sparklines()
    # _repr_html_ escapes HTML so manually handle the rendering
    display(HTML(dataframe.to_html(index=index, escape=False)))
    column_reset()


def to_html(dataframe, filename=None, **kwargs):
    """Save Dataframe with sparklines to html file.

    Parameters
    ----------
    dataframe : Pandas
        Dataframe with sparklines inline
    filename : str
        if set, complete filepath to save output html table to.
        If False, returns HTML generated.
    kwargs : keyword arguments, passed to pandas.DataFrame.to_html
    """

    column_sparklines()
    a = dataframe.to_html(escape=False)
    column_reset()

    if filename is None:
        return a

    f = open(filename + '.html', 'w')
    f.write(html_head)
    f.write(a)
    f.write(html_tail)
    f.close()
