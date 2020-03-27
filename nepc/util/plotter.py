"""Plot cross section data from NEPC"""
import numpy as np
import matplotlib.pyplot as plt
from nepc import nepc


def plot_nepc_model(axes, model, units_sigma,
                    process='',
                    plot_param_dict={'linewidth': 1},
                    xlim_param_dict={'auto': True},
                    ylim_param_dict={'auto': True},
                    ylog=False, xlog=False, show_legend=True,
                    filename=None,
                    max_plots=10, width=10, height=10):
    """
    A helper function to plot cross sections from a NEPC model on one plot.

    Parameters
    ----------
    axes : Axes
        The axes to draw to

    model : list of dict
        A list of dictionaries containing cross section data and
        metadata from the NEPC database (perhaps an object returned
        from nepc.model).

    units_sigma : float
        Desired units of the y-axis in m^2.

    process: str
        If provided, the process that should be plotted.

    plot_param_dict : dict
       dictionary of kwargs to pass to ax.plot

    xlim(ylim)_param_dict: dict
        dictionary of kwargs to pass to ax.set_x(y)lim

    ylog, xlog: bool
        whether y-, x-axis is log scale

    show_legend: bool
        whether to display the legend or not

    filename: str
        filename for output, if provided (default is to not output a file)

    max_plots : int
        maximum number of plots to put on graph

    Returns
    -------
    axes: matplotlib.axes._subplots.AxesSubplot object
        plot of a collection of cross sections, perhaps output from nepc.model
    """
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

            upu = model[i]['upu']
            lpu = model[i]['lpu']
            if upu != -1:
                sigma_upper_np = sigma_np*(1 + upu)
                if lpu == -1:
                    sigma_lower_np = sigma_np
            if lpu != -1:
                sigma_lower_np = sigma_np*(1 - lpu)
                if upu == -1:
                    sigma_upper_np = sigma_np
            
            plot = axes.plot(e_np,
                             sigma_np*model[i]['units_sigma']/units_sigma,
                             **plot_param_dict,
                             label='{}'.format(label_text))

            if upu != -1 or lpu != -1:
                fill_color = plot[0].get_color()
                axes.fill_between(e_np, sigma_lower_np, sigma_upper_np,
                        color=fill_color, alpha=0.4)

    if show_legend:
        axes.legend(fontsize=12, ncol=2, frameon=False,
                    bbox_to_anchor=(1.0, 1.0))
        # ax.legend(box='best',
        #           bbox_to_anchor=(0.5, 0.75), ncol=1, loc='center left')

    if filename is not None:
        plt.savefig(filename)

    return axes
