#from cycler import cycler
import numpy as np
import matplotlib.pyplot as plt

def lxcat_plot_zats(ax, processes, plot_line_style_list, 
                    plot_param_dict = {'linewidth':1}, 
                    xlim_param_dict = {'auto':True}, 
                    ylim_param_dict = {'auto':True},
                    ylog = False, xlog = False, show_legend = True, 
                    filename = 'default.png'):
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

    if (ylog):
        plt.yscale('log')
        
    if (xlog):
        plt.xscale('log')
        
    plt.ylabel(r'Cross Section ($10^{-16}$ cm$^2$)')
    plt.xlabel(r'Electron Energy (eV)')

    ax.set_xlim(**xlim_param_dict)
    ax.set_ylim(**ylim_param_dict)
    
    ax.tick_params(direction='in', which = 'both',
                   bottom=True, top=True, left=True, right=True)
    
    for i in range(len(processes)):
        process_np = np.array(processes[i]['data'])
        ax.plot(process_np[...,0], process_np[...,1]/1E-20, plot_line_style_list[i],
                **plot_param_dict,
                label='{}'.format(processes[i]['process']))
                                       #processes[i]['filename']))

    if (show_legend):
        ax.legend(fontsize=8, ncol=1, loc='best', frameon=False)
        #ax.legend(box='best', bbox_to_anchor=(0.5, 0.75), ncol=1, loc='center left')

    plt.savefig(filename)

    return ax


def lxcat_plot_zats_top6(ax, processes,
                         plot_param_dict = {'linewidth':1},
                         ylog = False, xlog = False, show_legend = True):
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
    out : list
        list of artists added
    """

    if (ylog):
        plt.yscale('log')

    if (xlog):
        plt.xscale('log')

    fig, ax = plt.subplots(len(processes), sharex=False, sharey=False, figsize=(5,10))

    for i in range(len(processes)):
        if i==len(processes)/2: ax[i].set_ylabel(r'Cross Section ($10^{-16}$ cm$^2$)')
        if i==len(processes)-1: ax[i].set_xlabel(r'Electron Energy (eV)')
        ax[i].tick_params(direction='in', which = 'both',
                          bottom=True, top=True, left=True, right=True)
        ax[i].tick_params(direction='in', which = 'both',
                          bottom=True, top=True, left=True, right=True)
        process_np = np.array(processes[i]['data'])
        ax[i].plot(process_np[...,0], process_np[...,1]/1E-20, 'r-', 
                   **plot_param_dict,
                   label='{}'.format(processes[i]['process']))
        if (show_legend):
            ax[i].legend(fontsize=8, ncol=1, loc='best', frameon=False)

    return ax

def n_plot_zats(ax, data, process, plot_line_style, 
                plot_param_dict = {'linewidth':0.8}, 
                xlim_param_dict = {'auto':True}, 
                ylim_param_dict = {'auto':True},
                ylog = False, xlog = False, show_legend = True, 
                filename = 'default.png'):
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
    out : list
        list of artists added
    """

    if (ylog):
        plt.yscale('log')
        
    if (xlog):
        plt.xscale('log')
        
    plt.ylabel(r'Cross Section ($10^{-16}$ cm$^2$)')
    plt.xlabel(r'Electron Energy (eV)')

    ax.set_xlim(**xlim_param_dict)
    ax.set_ylim(**ylim_param_dict)
    
    ax.tick_params(direction='in', which = 'both',
                   bottom=True, top=True, left=True, right=True)
    
    ax.plot(data[...,0], 
            data[...,1], 
            plot_line_style,
            **plot_param_dict,
            label='{}'.format(process))
                                       #processes[i]['filename']))

    if (show_legend):
        ax.legend(fontsize=8, ncol=1, loc='best', frameon=False)
        #ax.legend(box='best', bbox_to_anchor=(0.5, 0.75), ncol=1, loc='center left')

    plt.savefig(filename)

    return ax

