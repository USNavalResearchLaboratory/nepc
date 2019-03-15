""" This module contains code for exploratory data analysis of cross section
data.
"""

import numpy as np

def above_threshold(processes, threshold, target=''):
    """ Finds all processes that have cross sections above a threshold value
    (atp: above threshold processes).

    Parameters
    ----------
    processes: list of dictionaries
        A list with all processes to be examined.

    threshold: float
        Function returns processes with cross sections above this value. Units
        of threshold are cm^2. (LxCat data is often in m^2 so be careful.)

    target: string
        Optional target species for filtering results.

    Returns
    -------
    atp: list of dictionaries
        A list with all processes, in dictionary form, with cross sections
        above the provided threshold (above threshold processes).

    """
    cm2_per_m2 = 1.0e4
    atp = []
    for i in range(len(processes)):
        if (target == '') | (processes[i]['target'] == target):
            process_np = np.array(processes[i]['data'])
            if np.amax(process_np[...,1])*cm2_per_m2 > threshold:
                atp.append(processes[i])

    return atp

