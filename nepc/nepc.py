"""This package provides the following functionality for NRL Evaluated Plasma
Chemistry (NEPC) style databases:

 - create data files for building a NEPC database from common sources (e.g. LXCat)
 - build a NEPC style database on a MySQL server
 - establishing a connection to a local or remote database
 - access cross section data via the CS class
 - access pre-defined plasma chemistry models via the Model class
 - curate, visualize, and use cross section data
 - perform exploratory data analysis (EDA) of cross section data
 - print statistics about a database (e.g. number of rows in various tables)

Examples
--------
Establish a connection to the database named `nepc` running on a
production server:

    >>> cnx, cursor = nepc.connect()

Establish a connection to the database named `nepc`
running on the local machine:

    >>> cnx, cursor = nepc.connect(local=True, test=True)

Access the pre-defined plasma chemistry model, `fict`, in the `nepc_test` database:

    >>> fict = nepc.Model(cursor, "fict")

Print a summary of the ``fict`` model, including a stylized Pandas dataframe:

    >>> fict.summary()

Additional examples of EDA using nepc are in ``tests/data/eda``. Examples of methods for
building data files for the ``nepc_test`` database, including parsing
`LXCat <https://nl.lxcat.net/data/set_type.php>`_ formatted data,
are in ``tests/data/methods``.

"""
import numpy as np
from pandas import DataFrame
import mysql.connector
import matplotlib.pyplot as plt


def connect(local=False, DBUG=False, test=False):
    """Establish a connection to a NEPC MySQL database

    Parameters
    ----------
    local : bool, optional
        Access a database on localhost; otherwise use the production
        server (default False).
    DBUG : bool, optional
        Print debug info (default False).
    test: bool, optional
        If true, access the `nepc_test` database; otherwise, connect to the `nepc` database.

    Returns
    -------
    cnx : `connection.MySQLConnection <https://dev.mysql.com/doc/connectors/en/connector-python-api-mysqlconnection.html>`_
        A connection to a NEPC MySQL database.
    cursor : `cursor.MySQLCursor <https://dev.mysql.com/doc/connectors/en/connector-python-api-mysqlcursor.html>`_
        A MySQLCursor object that can execute operations such as SQL statements. `cursor` 
        interacts with the NEPC server using the `cnx` connection.

    """
    if local:
        hostname = 'localhost'
    else:
        hostname = '132.250.158.124'

    if DBUG:  # pragma: no cover
        print("\nUsing NEPC database on " + hostname)

    if test:
        database = 'nepc_test'
    else:
        database = 'nepc'

    config = {'user': 'nepc',
              'password': 'nepc',
              'host': hostname,
              'database': database,
              'raise_on_warnings': True}

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    return cnx, cursor


def count_table_rows(cursor, table: str):
    """Return the number of rows in a MySQL table.

    Parameters
    ----------
    cursor : cursor.MySQLCursor
        A MySQLCursor object. See return value ``cursor`` of :func:`.connect`.
    table : str
        Name of a table in the NEPC database at ``cursor``.

    Returns
    -------
    : int
        Number of rows in ``table``.

    """
    cursor.execute("select count(*) from " + table + ";")
    table_rows = cursor.fetchall()
    return table_rows[0][0]


def model_cs_id_list(cursor, model_name):
    """Get a list of ``cs_id``'s for a model in a NEPC database.

    Parameters
    ----------
    cursor : cursor.MySQLCursor
        A MySQLCursor object. See return value ``cursor`` of :func:`.connect`.
    model_name : str
        Name of a model in the NEPC MySQL database

    Returns
    -------
    cs_id_list : list of int
        cs_id's corresponding to cross sections in the model

    """
    cursor.execute("SELECT cs.cs_id as cs_id " +
                   "FROM cs " +
                   "JOIN models2cs m2cs ON (cs.cs_id = m2cs.cs_id) " +
                   "JOIN models m ON (m2cs.model_id = m.model_id) " +
                   "WHERE m.name LIKE '" + model_name + "'")
    cs_id_list = cursor.fetchall()
    cs_id_list = [cs_id[0] for cs_id in cs_id_list]
    return cs_id_list


def cs_e_sigma(cursor, cs_id):
    """Get electron energy and cross section data for a given ``cs_id`` in a NEPC database.

    Parameters
    ----------
    cursor : cursor.MySQLCursor
        A MySQLCursor object. See return value ``cursor`` of :func:`.connect`.
    cs_id : int
        The ``cs_id`` for a cross section dataset in the NEPC database at ``cursor``.

    Returns
    -------
    : list of float
        Electron energies for the cross section dataset corresponding to ``cs_id``.
    : list of float
        Cross sections for the cross section dataset corresponding to ``cs_id``.

    """
    cursor.execute("SELECT e, sigma FROM csdata WHERE cs_id = " +
                   str(cs_id))
    cross_section = cursor.fetchall()
    # print(cross_section)
    e_energy = [i[0] for i in cross_section]
    sigma = [i[1] for i in cross_section]
    return e_energy, sigma


def cs_e(cursor, cs_id):
    """Get the electron energies for a cross section dataset in a NEPC database 
    corresponding to a given ``cs_id``.

    Parameters
    ----------
    cursor : cursor.MySQLCursor
        A MySQLCursor object. See return value ``cursor`` of :func:`.connect`.
    cs_id : int
        The ``cs_id`` for a cross section dataset in the NEPC database at ``cursor``.

    Returns
    -------
    : list of float
        Electron energies for the cross section dataset corresponding to ``cs_id``.

    """
    cursor.execute("SELECT e FROM csdata WHERE cs_id = " +
                   str(cs_id))
    cross_section = cursor.fetchall()
    # print(cross_section)
    return [i[0] for i in cross_section]


def cs_sigma(cursor, cs_id):
    """Get the cross sections for a cross section dataset in a NEPC database
    corresponding to a given ``cs_id``.

    Parameters
    ----------
    cursor : cursor.MySQLCursor
        A MySQLCursor object. See return value ``cursor`` of :func:`.connect`.
    cs_id : int
        The ``cs_id`` for a cross section dataset in the NEPC database at ``cursor``.

    Returns
    -------
    : list of float
        Cross sections for the cross section dataset corresponding to ``cs_id``.

    """
    cursor.execute("SELECT sigma FROM csdata WHERE cs_id = " +
                   str(cs_id))
    sigma = cursor.fetchall()
    # print(sigma)
    return [i[0] for i in sigma]


def cs_metadata(cursor, cs_id):
    """Get metadata for a given ``cs_id`` in a NEPC database.

    Parameters
    ----------
    cursor : cursor.MySQLCursor
        A MySQLCursor object. See return value ``cursor`` of :func:`.connect`.
    cs_id : int
        The ``cs_id`` for a cross section dataset in the NEPC database at ``cursor``.

    Returns
    -------
    list
        See :attr:`CS.metadata`. List items are in same order as :attr:`.CS.metadata`.

    """
    cursor.execute("SELECT A.`cs_id` , "
                   "B.`name` , "
                   "C.`name` , "
                   "A.`units_e`, A.`units_sigma`, A.`ref`, "
                   "D.`name`, E.`name`, "
                   "F.`name`, G.`name`, "
                   "A.`threshold`, A.`wavelength`, A.`lhs_v`, A.`rhs_v`, "
                   "A.`lhs_j`, A.`rhs_j`, "
                   "A.`background`, A.`lpu`, A.`upu`, "
                   "D.`long_name`, E.`long_name`, "
                   "F.`long_name`, G.`long_name`, "
                   "C.`lhs_e`, C.`rhs_e`, "
                   "C.`lhs_hv`, C.`rhs_hv`, "
                   "C.`lhs_v`, C.`rhs_v`, "
                   "C.`lhs_j`, C.`rhs_j` "
                   "FROM `cs` AS A "
                   "LEFT JOIN `species` AS B "
                   "ON B.`id` = A.`specie_id` "
                   "LEFT JOIN `processes` AS C "
                   "ON C.`id` = A.`process_id` "
                   "LEFT JOIN `states` AS D "
                   "ON D.`id` = A.`lhsA_id` "
                   "LEFT JOIN `states` AS E "
                   "ON E.`id` = A.`lhsB_id` "
                   "LEFT JOIN `states` AS F "
                   "ON F.`id` = A.`rhsA_id` "
                   "LEFT JOIN `states` AS G "
                   "ON G.`id` = A.`rhsB_id` "
                   "WHERE A.`cs_id` = " + str(cs_id))

    return list(cursor.fetchall()[0])


class CS:
    r"""A cross section data set, including metadata and cross section data,
    from a NEPC MySQL database.

    Parameters
    ----------
    cursor : cursor.MySQLCursor
        A MySQLCursor object. See return value ``cursor`` of :func:`.connect`.
    cs_id : int
        i.d. of the cross section in `cs` and `csdata` tables

    Attributes
    ----------
    metadata : dict
        cs_id : int
            id of the cross section in `cs` and `csdata` tables
        specie : str
            `name` of specie from `species` table
        process : str
            `name` of process from `processes` table
        units_e : float
            units of electron energy list e in eV
        units_sigma : float
            units of cross section list sigma in m^2
        ref : str
            `ref` from `cs` table corresponding to entry in
            '[nepc]/models/ref.bib'
        lhsA : str
            `name` of lhsA state from `states` table
        lhsB : str
            `name` of lhsB state from `states` table
        rhsA : str
            `name` of rhsA state from `states` table
        rhsB : str
            `name` of rhsB state from `states` table
        wavelength : float
            wavelength of photon involved in process in nanometers (nm)
        lhs_v : int
            vibrational energy level of lhs specie
        rhs_v : int
            vibrational energy level of rhs specie
        lhs_j : int
            rotational energy level of lhs specie
        rhs_j : int
            rotational energy level of rhs specie
        background : str
            background text describing origin of data and other important info
        lpu : float
            lower percent uncertainty
        upu : float
            upper percent uncertainty
        lhsA_long : str
            `long_name` of lhsA state from `states` table
        lhsB_long : str
            `long_name` of lhsB state from `states` table
        rhsA_long : str
            `long_name` of rhsA state from `states` table
        rhsB_long : str
            `long_name` of rhsB state from `states` table
        e_on_lhs : int
            number of electrons on lhs
        e_on_rhs : int
            number of electrons on rhs
        hv_on_lhs : int
            photon on lhs? (0 or 1)
        hv_on_rhs : int
            photon on rhs? (0 or 1)
        v_on_lhs : int
            vibrational energy level on lhs? (0 or 1)
        v_on_rhs : int
            vibrational energy level on rhs? (0 or 1)
        j_on_lhs : int
            rotational energy level on lhs? (0 or 1)
        j_on_rhs : int
            rotational energy level on rhs? (0 or 1)
    data : dict
        e : list of float
            Electron energies in units of ``units_e`` eV (see :attr:`.CS.metadata`).
        sigma : list of float
            Cross sections in units of ``units_sigma`` :math:`m^2` (see :attr:`.CS.metadata`).

    """
    def __init__(self, cursor, cs_id):
        metadata = cs_metadata(cursor, cs_id)
        self.metadata = {"cs_id": metadata[0],
                         "specie": metadata[1],
                         "process": metadata[2],
                         "units_e": metadata[3],
                         "units_sigma": metadata[4],
                         "ref": metadata[5],
                         "lhsA": metadata[6],
                         "lhsB": metadata[7],
                         "rhsA": metadata[8],
                         "rhsB": metadata[9],
                         "threshold": metadata[10],
                         "wavelength": metadata[11],
                         "lhs_v": metadata[12],
                         "rhs_v": metadata[13],
                         "lhs_j": metadata[14],
                         "rhs_j": metadata[15],
                         "background": metadata[16],
                         "lpu": metadata[17],
                         "upu": metadata[18],
                         "lhsA_long": metadata[19],
                         "lhsB_long": metadata[20],
                         "rhsA_long": metadata[21],
                         "rhsB_long": metadata[22],
                         "e_on_lhs": metadata[23],
                         "e_on_rhs": metadata[24],
                         "hv_on_lhs": metadata[25],
                         "hv_on_rhs": metadata[26],
                         "v_on_lhs": metadata[27],
                         "v_on_rhs": metadata[28],
                         "j_on_lhs": metadata[29],
                         "j_on_rhs": metadata[30]}

        e_energy, sigma = cs_e_sigma(cursor, cs_id)
        self.data = {"e": e_energy,
                     "sigma": sigma}


    def __len__(self):
        r"""The number of data points in the cross section data set"""
        return len(self.data['e'])


    def plot(self, units_sigma=1E-20, plot_param_dict={'linewidth': 1},
             xlim_param_dict={'auto': True}, ylim_param_dict={'auto': True},
             ylog=False, xlog=False, show_legend=True, filename=None,
             width=10, height=10):
        r"""Plot a single cross section data set.

        Parameters
        ----------
        units_sigma : float, optional
            desired units of the y-axis in :math:`m^2`
        plot_param_dict : dict, optional
            kwargs to pass to :meth:`matplotlib.axes.Axes.plot`
        xlim_param_dict: dict, optional
            kwargs to pass to :meth:`matplotlib.axes.Axes.set_xlim`
        ylim_param_dict: dict, optional
            kwargs to pass to :meth:`matplotlib.axes.Axes.set_ylim`
        ylog : bool, optional
            whether y-axis is log scale (default is False)
        xlog : bool, optional
            whether x-axis is log scale (default is False)
        show_legend: bool, optional
            whether to display the legend or not (default is True)
        filename: str, optional
            filename for output, if provided (default is to not output a file)
        width: float, optional
            width of plot
        height: float, optional
            height of plot

        Returns
        -------
        :class:`matplotlib.axes.Axes`
            Plot of the cross section data, :attr:`.CS.data`, with formatting
            using information in the metadata, :attr:`.CS.metadata`.

        """
        _, axes = plt.subplots()

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

        reaction = reaction_latex(self)
        label_items = [self.metadata['process'], ": ", reaction]
        label_text = " ".join(item for item in label_items if item)
        e_np = np.array(self.data['e'])
        sigma_np = np.array(self.data['sigma'])

        upu = self.metadata['upu']
        lpu = self.metadata['lpu']
        if upu != -1:
            sigma_upper_np = sigma_np*(1 + upu)
            if lpu == -1:
                sigma_lower_np = sigma_np
        if lpu != -1:
            sigma_lower_np = sigma_np*(1 - lpu)
            if upu == -1:
                sigma_upper_np = sigma_np

        plot = axes.plot(e_np,
                         sigma_np*self.metadata['units_sigma']/units_sigma,
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


class CustomCS(CS):
    """
    Extends :class:`.CS` to provide a custom cross section data set.

    If building upon an existing :class:`.CS`, must provide cursor and cs_id as well
    as one or both of metadata and data.

    If building a :class:`.CustomCS` from scratch, must provide :obj:`.metadata` 
    and :obj:`.data`.

    Parameters
    ----------
    cursor : cursor.MySQLCursor
        A MySQLCursor object. See return value ``cursor`` of :func:`.connect`.
    cs_id : int
        i.d. of the cross section in `cs` and `csdata` tables
    metadata : dict
        one or more of the attributes of :class:`.CS`
    data : dict
        same as attributes of :class:`.CS`

    Attributes
    ----------
    metadata : dict
        see Attributes of :class:`.CS`

    data : dict
        e : list[float]
            electron energy
        sigma : list[float]
            cross section

    """
    def __init__(self, cursor=None, cs_id=None, metadata=None, data=None):
        if ((cursor is None and cs_id is not None) or (cursor is not None and cs_id is None)):
            raise ValueError('If providing cursor or cs_id, must provide both.')
        if (cursor is not None and cs_id is not None):
            super().__init__(cursor, cs_id)
            self.metadata['cs_id'] = None
            if metadata is not None:
                for key in metadata.keys():
                    self.metadata[key] = metadata[key]
            if data is not None:
                self.data = data.copy()
        elif (data is None or metadata is None):
            raise ValueError('must provide data/metadata if not providing cursor/cs_id')
        else:
            self.metadata = metadata.copy()
            self.data = data.copy()


class Model:
    """A pre-defined collection of cross sections from a NEPC database

    Parameters
    ----------
    cursor : cursor.MySQLCursor
        A MySQLCursor object. See return value ``cursor`` of :func:`.connect`.
    model_name :str
        Name of a NEPC model (pre-defined collection of cross sections)

    Attributes
    ----------
    cs: list[:class:`.CS`]
        cross section data in the NEPC format (:class:`.CS`)
    unique: list[float]
        set with :attr:`.Model.set_unique`, all unique electron energies in all :attr:`.CS.data`
        of the :class:`.Model`

    """
    def __init__(self, cursor, model_name):
        _cs_list = []
        _cs_id_list = model_cs_id_list(cursor, model_name)
        for cs_id in _cs_id_list:
            _cs_list.append(CS(cursor, cs_id))

        self.cs = _cs_list

    def __len__(self):
        """number of cross sections in the model"""
        return len(self.cs)

    def subset(self, metadata=None):
        """Select the cross sections in the model matching the provided metadata

        Parameters
        ----------
        metadata: dict
            see :attr:`.CS.metadata`

        Returns
        -------
        cs_subset: list[:class:`.CS`]
            cross section data in the NEPC format (:class:`.CS`)

        """
        if metadata is None or not isinstance(metadata, dict):
            raise Exception("must provide metadata of type dict")
        cs_subset = []
        for cs in self.cs:
            passed_filter = True
            for key in metadata.keys():
                if cs.metadata[key] != metadata[key]:
                    passed_filter = False
            if passed_filter:
                cs_subset.append(cs)
        return cs_subset


    def summary(self, metadata=None, lower=None, upper=None, sort=[]):
        """Summarize the NEPC model.

        Prints the following information:
            - Number of cross sections in the model
            - Number of cross sections matching metadata, if provided

        Returns a stylized Pandas dataframe with headers given by:

        headers = ["cs_id", "specie", "lhsA", "rhsA", "process",
                   "reaction", "threshold", "E_peak", "E_upper",
                   "sigma_max", "lpu", "upu"]

        Parameters
        ----------
        metadata: dict
            see :attr:`.CS.metadata`
        lower : int
            lower bound of model index to include in summary
        upper : int
            upper bound of model index to include in summary
        sort : list[str]
            headers by which the stylized Pandas table is sorted

        Returns
        -------
        cs_df : pandas.io.formats.style.Styler
            A stylized Pandas DataFrame containing the cs_id, process,
            range of electron energies (E_lower, E_upper),
            maximum sigma (sigma_max), and
            lpu/upu's for each cross section in the model (or subset of the
            model if :obj:`metadata` is provided)

        """
        summary_list = []

        headers = ["cs_id", "specie", "lhsA", "rhsA", "process",
                   "reaction", "threshold", "E_peak", "E_upper",
                   "sigma_max", "lpu", "upu"]

        max_e_peak = 0
        min_e_peak = 100000
        max_e_upper = 0
        max_peak_sigma = 0
        min_peak_sigma = 1
        max_lpu = 0.000000001
        max_upu = 0.000000001

        print('Number of cross sections in model: {:d}'.format(len(self.cs)))
        if metadata is not None:
            cs_subset = self.subset(metadata=metadata)
            print('Number of cross sections with '
                  'matching metadata: {:d}'.format(len(cs_subset)))
        else:
            cs_subset = self.cs


        for cs in cs_subset:
            csdata = np.array(list(zip(cs.data['e'], cs.data['sigma'])))
            e_peak = csdata[np.argmax(csdata[:, 1]), 0]
            cs_peak_sigma = np.max(csdata[:, 1])
            e_upper = np.max(csdata[csdata[:, 1] != 0.0][:, 0])
            if e_peak > max_e_peak:
                max_e_peak = e_peak
            if e_peak < min_e_peak:
                min_e_peak = e_peak
            if e_upper > max_e_upper:
                max_e_upper = e_upper
            if cs_peak_sigma > max_peak_sigma:
                max_peak_sigma = cs_peak_sigma
            if cs_peak_sigma < min_peak_sigma:
                min_peak_sigma = cs_peak_sigma
            reaction = reaction_latex(cs)
            cs_lpu = cs.metadata["lpu"]
            cs_upu = cs.metadata["upu"]
            if cs_lpu is not None and cs_lpu > max_lpu:
                max_lpu = cs_lpu
            if cs_upu is not None and cs_upu > max_upu:
                max_upu = cs_upu
            summary_list.append([cs.metadata["cs_id"],
                                 cs.metadata["specie"], cs.metadata["lhsA"], cs.metadata["rhsA"],
                                 cs.metadata["process"], reaction,
                                 cs.metadata["units_e"]*cs.metadata["threshold"],
                                 cs.metadata["units_e"]*e_peak,
                                 cs.metadata["units_e"]*e_upper,
                                 cs.metadata["units_sigma"]*cs_peak_sigma,
                                 cs_lpu, cs_upu])

        cs_df = DataFrame(summary_list, columns=headers)
        if sort:
            cs_df = (cs_df.sort_values(by=sort)
                     .reset_index(drop=True))
        if upper is None:
            upper = len(cs_df)
        if lower is None:
            lower = 0
        return (cs_df.loc[lower:upper]
                .style
                .background_gradient(subset=['threshold', 'E_peak', 'E_upper',
                                             'sigma_max', 'lpu', 'upu'],
                                     cmap='plasma')
                .highlight_null('red'))


    def set_unique(self):
        """sets :attr:`.Model.unique`

        """
        for cs, i in zip(self.cs, range(len(self.cs))):
            if i == 0:
                _unique = np.asarray(cs.data['e'])
            else:
                _unique = np.unique(np.concatenate([_unique, np.asarray(cs.data['e'])]))
        self.unique = list(_unique)


    def plot(self,
             units_sigma=1E-20,
             process='',
             plot_param_dict={'linewidth': 1},
             xlim_param_dict={'auto': True},
             ylim_param_dict={'auto': True},
             ylog=False, xlog=False, show_legend=True,
             filename=None,
             max_plots=10, width=10, height=10):
        """Plot cross section data in the Model.

        Parameters
        ----------
        process: str
            If provided, the process that should be plotted.
        units_sigma : float
            Desired units of the y-axis in m^2.
        plot_param_dict : dict
            kwargs to pass to ax.plot
        xlim(ylim)_param_dict: dict
            dictionary of kwargs to pass to ax.set_x(y)lim
        ylog, xlog: bool
            whether y-, x-axis is log scale
        show_legend: bool
            whether to display the legend or not
        filename: str
            filename for output, if provided (default is to not output a file)
        max_cs : int
            maximum number of CS to put on graph

        Returns
        -------
        :class:`matplotlib.axes.Axes`
            Plot of the cross section data, :attr:`.CS.data`, with formatting
            using information in the metadata, :attr:`.CS.metadata` within the
            model.

        """
        _, axes = plt.subplots()

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
        for i in range(len(self.cs)):
            if plot_num >= max_plots:
                continue
            elif process in ('', self.cs[i].metadata['process']):
                plot_num += 1

                reaction = reaction_latex(self.cs[i])
                label_items = [self.cs[i].metadata['process'], ": ", reaction]
                label_text = " ".join(item for item in label_items if item)
                e_np = np.array(self.cs[i].data['e'])
                sigma_np = np.array(self.cs[i].data['sigma'])

                upu = self.cs[i].metadata['upu']
                lpu = self.cs[i].metadata['lpu']
                if upu != -1:
                    sigma_upper_np = sigma_np*(1 + upu)
                    if lpu == -1:
                        sigma_lower_np = sigma_np
                if lpu != -1:
                    sigma_lower_np = sigma_np*(1 - lpu)
                    if upu == -1:
                        sigma_upper_np = sigma_np

                plot = axes.plot(e_np,
                                 sigma_np*self.cs[i].metadata['units_sigma']/units_sigma,
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


class CustomModel(Model):
    """Extends :class:`.Model` to provide a customized collection of cross sections.

    The cross sections can be of class :class:`.CS`
    (from the NEPC database) or :class:`.CustomCS` (user created/modified).
    Options:

    a. If building upon an existing NEPC model, must provide cursor and model_name. May
       also provide a filter to select cross sections that meet criteria.
    b. If building from existing cross sections, must provide cursor and cs_id_list.
    c. If building from a list of custom cross sections, must provide cs_list.

    Must do at least one of a, b, or c, and can do any combination thereof.

    Parameters
    ----------
    cursor : cursor.MySQLCursor
        A MySQLCursor object. See return value ``cursor`` of :func:`.connect`.
    model_name :str
        The name of a NEPC model (see [nepc.wiki]/models
    cs_id_list : list of int
        List of cs_id's to pull from NEPC database.
    cs_list : list of CustomCS
        List of user-defined cross sections of CustomCS type.
    metadata: dict
        Dictionary of filter criteria to select specific CS's from a Model.

    Attributes
    ----------
    cs: list of :class:`.CS` or :class:`.CustomCS`
        A list of cross section data and metadata of CS or CustomCS type.

    """
    def __init__(self, cursor=None, model_name=None, cs_id_list=[], cs_list=[], metadata=None):
        if model_name is None and not cs_id_list and not cs_list:
            raise ValueError('Must provide at least one of model_name, cs_id_list, or cs_list')

        if cursor is None and (model_name is not None or cs_id_list):
            raise ValueError('Must provide cursor if providing model_name or cs_id_list')

        if cursor is not None and (model_name is None and not cs_id_list):
            raise ValueError('Must provide model_name or cs_id_list if providing cursor.')

        if metadata is not None and (cursor is None or model_name is None):
            raise ValueError('Must provide model_name and cursor if providing metadata.')

        if cs_list:
            _cs_list = cs_list.copy()
        else:
            _cs_list = []

        if cs_id_list:
            _cs_id_list = cs_id_list.copy()
            for cs_id in _cs_id_list:
                _cs_list.append(CS(cursor, cs_id))

        if model_name is not None:
            _model_cs_id_list = model_cs_id_list(cursor, model_name)
            for cs_id in _model_cs_id_list:
                cs = CS(cursor, cs_id)
                if metadata is not None:
                    passed_filter = True
                    for key in metadata.keys():
                        if cs.metadata[key] != metadata[key]:
                            passed_filter = False
                if metadata is None or passed_filter:
                    _cs_list.append(cs)

        self.cs = _cs_list.copy()


def table_as_df(cursor, table, columns="*"):
    """Return a ``table`` in a MySQL database as a pandas DataFrame.

    Parameters
    ----------
    cursor : cursor.MySQLCursor
        A MySQLCursor object. See return value ``cursor`` of :func:`.connect`.
    table : str
        Name of a table in the NEPC database at ``cursor``.
    columns : list of str, optional
        Which columns to get. (Default is to get all columns.)

    Returns
    -------
    DataFrame
        Table in the form of a pandas DataFrame

    """
    column_text = ", ".join(columns)
    cursor.execute("SELECT " + column_text + " FROM " + table)
    return DataFrame(cursor.fetchall())


def reaction_latex(cs):
    """Return the LaTeX for the process involved in a nepc cross section.

    Parameters
    ----------
    cs : :class:`.CS` or :class:`.CustomCS`
        A nepc cross section.

    Returns
    -------
    : str
        The LaTeX for the process involved in a NEPC cross section.

    """
    # FIXME: move this method to the CS Class
    # FIXME: allow for varying electrons and including hv, v, j on rhs and lhs
    # FIXME: decide how to represent total cross sections and implement
    e_on_lhs = cs.metadata['e_on_lhs']
    if e_on_lhs == 0:
        lhs_e_text = None
    elif e_on_lhs == 1:
        lhs_e_text = "e$^-$"
    else:
        lhs_e_text = str(e_on_lhs) + "e$^-$"

    e_on_rhs = cs.metadata['e_on_rhs']
    if e_on_rhs == 0:
        rhs_e_text = None
    elif e_on_rhs == 1:
        rhs_e_text = "e$^-$"
    else:
        rhs_e_text = str(e_on_rhs) + "e$^-$"

    lhsA_text = cs.metadata['lhsA_long']
    if cs.metadata['process'] == 'excitation_v':
        lhsA_text = lhsA_text.replace(")", " v=" + str(cs.metadata['lhs_v']) + ")")
    lhsB_text = cs.metadata['lhsB_long']
    lhs_items = [lhs_e_text,
                 lhsA_text,
                 lhsB_text]
    lhs_text = " + ".join(item for item in lhs_items if item)

    rhsA_text = cs.metadata['rhsA_long']
    if cs.metadata['process'] == 'excitation_v':
        rhsA_text = rhsA_text.replace(")", " v=" + str(cs.metadata['rhs_v']) + ")")
    rhsB_text = cs.metadata['rhsB_long']
    rhs_items = [rhsA_text,
                 rhsB_text,
                 rhs_e_text]
    rhs_text = " + ".join(item for item in rhs_items if item)
    reaction = " $\\rightarrow$ ".join([lhs_text, rhs_text])
    return reaction
