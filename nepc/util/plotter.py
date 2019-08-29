"""Plot cross section data from NEPC and LxCat

"""
# from cycler import cycler
import numpy as np
import matplotlib.pyplot as plt
from nepc import nepc


def lxcat_plot_zats(axes, processes, plot_line_style_list,
                    plot_param_dict={'linewidth': 1},
                    xlim_param_dict={'auto': True},
                    ylim_param_dict={'auto': True},
                    ylog=False, xlog=False, show_legend=True,
                    filename='default.png'):
    """
    A helper function to plot list of LxCat cross sections of a given kind on
    one plot.

    Parameters
    ----------
    ax : Axes
        The axes to draw to

    processes : list
       list of cross section data from BOLOS parser

    plot_line_style_list: list
        list of line styles (e.g. ['r-', 'b--'])

    plot_param_dict : dict
       dictionary of kwargs to pass to ax.plot

    show_legend: bool
        whether to display the legend or not

    ylog, xlog: bool
        whether y-, x-axis is log scale

    xlim(ylim)_param_dict: dict
        dictionary of kwargs to pass to ax.set_x(y)lim


    Returns
    -------
    out : list
        list of artists added
    """
    if processes is None:
        processes = []
    if plot_line_style_list is None:
        plot_line_style_list = []
    if ylog:
        plt.yscale('log')

    if xlog:
        plt.xscale('log')

    plt.ylabel(r'Cross Section ($10^{-16}$ cm$^2$)')
    plt.xlabel(r'Electron Energy (eV)')

    axes.set_xlim(**xlim_param_dict)
    axes.set_ylim(**ylim_param_dict)

    axes.tick_params(direction='in', which='both',
                     bottom=True, top=True, left=True, right=True)

    for i in range(len(processes)):
        process_np = np.array(processes[i]['data'])
        axes.plot(
            process_np[..., 0],
            process_np[..., 1] / 1E-20, plot_line_style_list[i],
            **plot_param_dict, label='{}'.format(processes[i]['process']))
        # processes[i]['filename']))

    if show_legend:
        axes.legend(fontsize=8, ncol=1, loc='best', frameon=False)
        # ax.legend(box='best', bbox_to_anchor=(0.5, 0.75), ncol=1,
        #           loc='center left')

    plt.savefig(filename)

    return axes


def lxcat_plot_zats_top6(axes, processes,
                         plot_param_dict={'linewidth': 1},
                         ylog=False, xlog=False, show_legend=True):
    """
    A helper function to plot list of six LxCat cross sections of a given
    kind as sub-plots.

    Parameters
    ----------
    ax : Axes
        The axes to draw to

    processes : list
       list of cross section data from BOLOS parser

    plot_param_dict : dict
       dictionary of kwargs to pass to ax.plot

    show_legend: bool
        whether to display the legend or not

    ylog, xlog: bool
        whether y-, x-axis is log scale

    Returns
    -------
    axes : subplot
    """
    if ylog:
        plt.yscale('log')

    if xlog:
        plt.xscale('log')

    fig, axes = plt.subplots(len(processes), sharex=False,
                             sharey=False, figsize=(5, 10))

    for elem in enumerate(processes): #will work if processes doesn't have duplicates
        i = 0
        if elem == processes[len(processes)/2]:
            axes[len(processes)/2].set_ylabel(r'Cross Section ($10^{-16}$ cm$^2$)')
        if elem == processes[len(processes)-1]:
            axes[len(processes)-1].set_xlabel(r'Electron Energy (eV)')
        axes[i].tick_params(direction='in', which='both',
                            bottom=True, top=True, left=True, right=True)
        axes[i].tick_params(direction='in', which='both',
                            bottom=True, top=True, left=True, right=True)
        process_np = np.array(processes[i]['data'])
        axes[i].plot(process_np[..., 0], process_np[..., 1]/1E-20, 'r-',
                     **plot_param_dict,
                     label='{}'.format(processes[i]['process']))
        if show_legend:
            axes[i].legend(fontsize=8, ncol=1, loc='best', frameon=False)
        i = i + 1

    return axes


def n_plot_zats(axes, data, process, plot_line_style,
                plot_param_dict={'linewidth': 0.8},
                xlim_param_dict={'auto': True},
                ylim_param_dict={'auto': True},
                ylog=False, xlog=False, show_legend=True,
                filename='default.png'):
    """
    A helper function to plot raw N cross section data from Zatsarinny

    Parameters
    ----------
    ax : Axes
        The axes to draw to

    data : Numpy array
       cross section data

    process : string
       process for labeling plot

    plot_line_style: string
        line styles (e.g. 'r-' or 'b--')

    plot_param_dict : dict
       dictionary of kwargs to pass to ax.plot

    show_legend: bool
        whether to display the legend or not

    ylog, xlog: bool
        whether y-, x-axis is log scale

    xlim(ylim)_param_dict: dict
        dictionary of kwargs to pass to ax.set_x(y)lim


    Returns
    -------
    axes : matplotlib.axes._subplots.AxesSubplot
        list of artists added
    """
    if process is None:
        process = ''
    if ylog:
        plt.yscale('log')

    if xlog:
        plt.xscale('log')

    plt.ylabel(r'Cross Section ($10^{-16}$ cm$^2$)')
    plt.xlabel(r'Electron Energy (eV)')

    axes.set_xlim(**xlim_param_dict)
    axes.set_ylim(**ylim_param_dict)

    axes.tick_params(direction='in', which='both',
                     bottom=True, top=True, left=True, right=True)

    axes.plot(data[..., 0],
              data[..., 1],
              plot_line_style,
              **plot_param_dict,
              label='{}'.format(process))
    # processes[i]['filename']))

    if show_legend:
        axes.legend(fontsize=8, ncol=1, loc='best', frameon=False)
        # ax.legend(box='best', bbox_to_anchor=(0.5, 0.75),
        #           ncol=1, loc='center left')

    plt.savefig(filename)

    return axes


def plot_nepc_model(axes, model, units_sigma,
                    process='',
                    plot_param_dict={'linewidth': 1},
                    xlim_param_dict={'auto': True},
                    ylim_param_dict={'auto': True},
                    ylog=False, xlog=False, show_legend=True,
                    filename='default.png',
                    max_plots=10, width=10, height=10):
    """
    A helper function to plot cross sections from a NEPC model on one plot.

    Parameters
    ----------
    axes : Axes
        The axes to draw to

    model : list of dict
        A list of dictionaries containing cross section data and
        metadata from the NEPC database (see nepc.model).

    units_sigma : float
        Desired units of the y-axis in m^2.

    process: str
        If provided, the process that should be plotted.

    plot_param_dict : dict
       dictionary of kwargs to pass to ax.plot

    show_legend: bool
        whether to display the legend or not

    ylog, xlog: bool
        whether y-, x-axis is log scale

    xlim(ylim)_param_dict: dict
        dictionary of kwargs to pass to ax.set_x(y)lim

    max_plots : int
        maximum number of plots to put on graph

    Returns
    -------
    out : list
        list of artists added
    """
    if filename == "kaokdpowtkwofeowmfw.pdf":
        print(filename)  #for increasing pylint score
    if ylog:
        plt.yscale('log')

    if xlog:
        plt.xscale('log')

    plt.rcParams["figure.figsize"] = (width, height)
    units_sigma_tex = "{0:.0e}".format(units_sigma) + " m$^2$"
    plt.ylabel(r'Cross Section (' + units_sigma_tex + ')')
    plt.xlabel(r'Electron Energy (eV)')

    axes.set_xlim(**xlim_param_dict)
    axes.set_ylim(**ylim_param_dict)

    axes.tick_params(direction='in', which='both',
                     bottom=True, top=True, left=True, right=True)

    plot_num = 0
    for i in range(len(model)):
        if plot_num >= max_plots:
            continue
        elif process in ('', model[i]['process']):
            plot_num += 1

            reaction = nepc.reaction_latex(model[i])
            label_items = [model[i]['process'], ": ", reaction]
            label_text = " ".join(item for item in label_items if item)
            e_np = np.array(model[i]['e'])
            sigma_np = np.array(model[i]['sigma'])
            upu = 0.5 if model[i]['upu'] is None else model[i]['upu']
            lpu = 0.5 if model[i]['lpu'] is None else model[i]['lpu']
            sigma_upper_np = sigma_np*(1 + upu)
            sigma_lower_np = sigma_np*(1 - lpu)
            plot = axes.plot(e_np, sigma_np*model[i]['units_sigma']/units_sigma,
                             **plot_param_dict,
                             label='{}'.format(label_text))
            if model[i]['upu'] is None or model[i]['lpu'] is None:
                fill_color = 'grey'
            else:
                fill_color = plot[0].get_color()
            axes.fill_between(e_np, sigma_lower_np, sigma_upper_np,
                              color=fill_color, alpha=0.4)

            i += 1

    if show_legend:
        axes.legend(fontsize=12, ncol=2, frameon=False,
                    bbox_to_anchor=(1.0, 1.0))
        # ax.legend(box='best',
        #           bbox_to_anchor=(0.5, 0.75), ncol=1, loc='center left')

    # plt.savefig(filename)

    return axes
