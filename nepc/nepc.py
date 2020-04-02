"""Access the NRL Evaluated Plasma Chemistry (NEPC) database

Utilize the NEPC MySQL database by:
    - establishing a connection to the database
    - accessing cross sections via CS class
    - accessing pre-defined plasma chemistry models via Model class
    - printing statistics about the database (e.g. number of rows in various tables)

Notes
-----
- [nepc] refers to the base directory of the nepc repository.
- [nepc.wiki] refers to the base directory of the wiki associated with
the nepc repository.

Examples
--------
Establish a connection to the NEPC database running on the
production server:

    cnx, cursor = nepc.connect()

Establish a connection to the NEPC database running on the
local machine:

    cnx, cursor = nepc.connect(local=True)
"""
import numpy as np
from pandas import DataFrame
import mysql.connector
import matplotlib.pyplot as plt


def connect(local=False, DBUG=False):
    """Establish a connection to NEPC MySQL database


    Parameters
    ----------
    local : bool
        Use a copy of NEPC on localhost; otherwise use the production
        server (default False).
    DBUG : bool
        Print debug info (default False).

    Returns
    -------
    cnx : MySQLConnection
        A connection to the NEPC MySQL database
    cursor : MySQLCursor
        A MySQLCursor object that can execute operations such as SQL
        statements. `cursor` interacts with the NEPC server using the
        `cnx` connection
    """

    if local:
        hostname = 'localhost'
    else:
        hostname = '132.250.158.124'

    if DBUG:  # pragma: no cover
        print("\nUsing NEPC database on " + hostname)

    config = {'user': 'nepc',
              'password': 'nepc',
              'host': hostname,
              'database': 'nepc',
              'raise_on_warnings': True}

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    return cnx, cursor


def count_table_rows(cursor, table):
    """return the number of rows in a MySQL table

    Parameters
    ----------
    cursor : MySQLCursor
        A MySQLCursor object (see nepc.connect)
    table : str
        Name of a table in the MySQL database

    Return
    ------
        : int
    Number of rows in table
    """
    cursor.execute("select count(*) from " + table + ";")
    table_rows = cursor.fetchall()
    return table_rows[0][0]


def model_cs_id_list(cursor, model_name):
    """return a list of cs_id's for a model in the NEPC database

    Parameters
    ----------
    cursor : MySQLCursor
        A MySQLCursor object (see nepc.connect)
    model_name : str
        Name of a model in the NEPC MySQL database

    Return
    ------
    cs_id_list : list of ints
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
    """get e_energy and sigma data for a given cs_id from NEPC database"""
    cursor.execute("SELECT e, sigma FROM csdata WHERE cs_id = " +
                   str(cs_id))
    cross_section = cursor.fetchall()
    # print(cross_section)
    e_energy = [i[0] for i in cross_section]
    sigma = [i[1] for i in cross_section]
    return e_energy, sigma


def cs_e(cursor, cs_id):
    """get e_energy only for a given cs_id from NEPC database"""
    cursor.execute("SELECT e FROM csdata WHERE cs_id = " +
                   str(cs_id))
    cross_section = cursor.fetchall()
    # print(cross_section)
    return [i[0] for i in cross_section]


def cs_sigma(cursor, cs_id):
    """get sigma only for a given cs_id from NEPC database"""
    cursor.execute("SELECT sigma FROM csdata WHERE cs_id = " +
                   str(cs_id))
    sigma = cursor.fetchall()
    # print(sigma)
    return [i[0] for i in sigma]


def cs_metadata(cursor, cs_id):
    """Get metadata for cross section in the NEPC database"""
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
    """A cross section data set, including metadata and cross section data,
    from the NEPC MySQL database."""
    def __init__(self, cursor, cs_id):
        """Initialize a cross section data set

        Parameters
        ----------
        cursor : MySQLCursor
            A MySQLCursor object (see nepc.connect)
        cs_id : int
            i.d. of the cross section in `cs` and `csdata` tables

        Attributes
        ----------
        metadata : dictionary of the metadata
            "cs_id" : int
                id of the cross section in `cs` and `csdata` tables
            "specie" : str
                `name` of specie from `species` table
            "process" : str
                `name` of process from `processes` table
            "units_e" : float
                units of electron energy list "e" in eV
            "units_sigma" : float
                units of cross section list "sigma" in m^2
            "ref" : str
                `ref` from `cs` table corresponding to entry in
                '[nepc]/models/ref.bib'
            "lhsA" : str
                `name` of lhsA state from `states` table
            "lhsB" : str
                `name` of lhsB state from `states` table
            "rhsA" : str
                `name` of rhsA state from `states` table
            "rhsB" : str
                `name` of rhsB state from `states` table
            "wavelength" : float
                wavelength of photon involved in process in nanometers (nm)
            "lhs_v" : int
                vibrational energy level of lhs specie
            "rhs_v" : int
                vibrational energy level of rhs specie
            "lhs_j" : int
                rotational energy level of lhs specie
            "rhs_j" : int
                rotational energy level of rhs specie
            "background" : str
                background text describing origin of data and other important info
            "lpu" : float
                lower percent uncertainty
            "upu" : float
                upper percent uncertainty
            "lhsA_long" : str
                `long_name` of lhsA state from `states` table
            "lhsB_long" : str
                `long_name` of lhsB state from `states` table
            "rhsA_long" : str
                `long_name` of rhsA state from `states` table
            "rhsB_long" : str
                `long_name` of rhsB state from `states` table
            "e_on_lhs" : int
                number of electrons on lhs
            "e_on_rhs" : int
                number of electrons on rhs
            "hv_on_lhs" : int
                photon on lhs? (0 or 1)
            "hv_on_rhs" : int
                photon on rhs? (0 or 1)
            "v_on_lhs" : int
                vibrational energy level on lhs? (0 or 1)
            "v_on_rhs" : int
                vibrational energy level on rhs? (0 or 1)
            "j_on_lhs" : int
                rotational energy level on lhs? (0 or 1)
            "j_on_rhs" : int
                rotational energy level on rhs? (0 or 1)
        data : dictionary of the cross section data
            "e" : list of float
                electron energy
            "sigma" : list of float
                cross section
        """
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


    def plot(self,
             units_sigma=1E-20,
             plot_param_dict={'linewidth': 1},
             xlim_param_dict={'auto': True},
             ylim_param_dict={'auto': True},
             ylog=False, xlog=False, show_legend=True,
             filename=None,
             width=10, height=10):
        """
        A helper function to plot a single cross section data set

        Parameters
        ----------
        units_sigma : float
            Desired units of the y-axis in m^2.

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

        Returns
        -------
        f: FIXME
            plot of a single cross section data set
        """
        fig, axes = plt.subplots()

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
    """A custom cross section data set, including metadata and cross section data.
    Two options:
    a. If building upon an existing NEPC CS, must provide cursor and cs_id as well
    as one or both of metadata and data.

    b. If building a CustomCS from scratch, must provide metadata and data."""
    def __init__(self, cursor=None, cs_id=None, metadata=None, data=None):
        """Initialize a cross section data set

        Parameters
        ----------
        cursor : MySQLCursor
            A MySQLCursor object (see nepc.connect)
        cs_id : int
            i.d. of the cross section in `cs` and `csdata` tables
        metadata : dictionary of the metadata
            See Attributes of CS class.
        data : dictionary of the cross section data
            See Attributes of CS class.

        Attributes
        ----------
        metadata : dictionary of the metadata
            See Attributes of CS class.
        data : dictionary of the cross section data
            See Attributes of CS class.
        """
        if ((cursor is None and cs_id is not None) or
            (cursor is not None and cs_id is None)):
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
    """A pre-defined collection of cross sections from the NEPC MySQL database"""
    def __init__(self, cursor, model_name):
        """
        Parameters
        ----------
        cursor : MySQLCursor
            A MySQLCursor object (see nepc.connect)
        model_name :str
            The name of a NEPC model (see [nepc.wiki]/models

        Attributes
        ----------
        cs: list of CS
            A list of cross section data and
            metadata of CS type.
        """
        _cs_list = []
        _cs_id_list = model_cs_id_list(cursor, model_name)
        for cs_id in _cs_id_list:
            _cs_list.append(CS(cursor, cs_id))

        self.cs = _cs_list

    def filter(self, specie=None, process=None, ref=None):
        """return a subset of the model"""
        subset_dicts = []
        if specie is None and process is None and ref is None:
            raise Exception("You must specify the specie, process or " +
                            "ref to narrow the search results.")
        if specie is not None and process is not None:
            for i in range(len(self.cs)):
                if (self.cs[i].metadata['specie'] == specie and
                    self.cs[i].metadata['process'] == process):
                    subset_dicts.append(self.cs[i])
        elif specie is not None:
            for i in range(len(self.cs)):
                if self.cs[i].metadata['specie'] == specie:
                    subset_dicts.append(self.cs[i])
        return subset_dicts


    def subset(self, filter=None):
        """return a subset of the model using a dictionary of filter criteria"""
        if filter is None:
            raise Exception("You must provide a dictionary of filter " +
                            "criteria via the filter argument.")
        cs_subset = []
        for cs in self.cs:
            passed_filter = True
            for key in filter.keys():
                if cs.metadata[key] != filter[key]:
                    passed_filter = False
            if passed_filter:
                cs_subset.append(cs)
        return cs_subset


    def summary(self, filter=None, lower=None, upper=None):
        """Return a summary of a NEPC model
    
        Parameters
        ----------
        lower : int
            lower bound of model index to include in summary
        upper : int
            upper bound of model index to include in summary
    
        Output 
        ------
        In addition to returning a DataFrame as described below,
        prints the following information:
            - Number of cross sections/rates in the model
            - Number of data sets in model that match filter criteria (if provided)

        Returns
        -------
        cs_df : pandas DataFrame
            A DataFrame containing the cs_id, process,
            range of electron energies (E_lower, E_upper),
            maximum sigma (sigma_max), and
            lpu/upu's for each cross section in the model
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
        if filter is not None:
            cs_subset = self.subset(filter=filter)
            print('Number of cross sections that '
                  'match filter criteria: {:d}'.format(len(cs_subset)))
        else:
            cs_subset = self.cs


        for cs in cs_subset:
            csdata = np.array(list(zip(cs.data['e'], cs.data['sigma'])))
            e_peak = csdata[np.argmax(csdata[:,1]),0]
            cs_peak_sigma = np.max(csdata[:,1])
            e_upper = np.max(csdata[csdata[:,1]!=0.0][:,0])
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
        cs_df = (cs_df.sort_values(by=["process", "cs_id"])
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
        """
        A helper function to plot cross sections from a NEPC model on one plot.

        Parameters
        ----------
        process: str
            If provided, the process that should be plotted.

        units_sigma : float
            Desired units of the y-axis in m^2.

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

        max_cs : int
            maximum number of CS to put on graph

        Returns
        -------
        f: FIXME
            plot of a collection of cross sections from a Model
        """
        fig, axes = plt.subplots()

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
    """A customized collection of cross sections. The cross sections can be of CS Class
    (from the NEPC database) or CustomCS Class (user created).
    Options:

    a. If building upon an existing NEPC model, must provide cursor and model_name.

    b. If building from existing cross sections, must provide cursor and cs_id_list.

    c. If building from a list of custom cross sections, must provide cs_list.

    Must do at least one of a, b, or c, and can do any combination thereof."""
    def __init__(self, cursor=None, model_name=None, cs_id_list=[], cs_list=[]):
        """
        Parameters
        ----------
        cursor : MySQLCursor
            A MySQLCursor object (see nepc.connect)
        model_name :str
            The name of a NEPC model (see [nepc.wiki]/models
        cs_id_list : list of int
            List of cs_id's to pull from NEPC database.
        cs_list : list of CustomCS
            List of user-defined cross sections of CustomCS type.
        Attributes
        ----------
        cs: list of CS and CustomCS
            A list of cross section data and
            metadata of CS or CustomCS type.
        """
        if model_name is None and not cs_id_list and not cs_list:
            raise ValueError('Must provide at least one of model_name, cs_id_list, or cs_list')

        if cursor is None and (model_name is not None or cs_id_list):
            raise ValueError('Must provide cursor if providing model_name or cs_id_list')

        if cs_list:
            _cs_list = cs_list.copy()
        else:
            _cs_list = []

        if cursor is not None:
            if model_name is None and not cs_id_list:
                raise ValueError('Must provide model_name or cs_id_list if providing cursor.')

            if model_name is not None:
                _cs_id_list = cs_id_list.copy() + model_cs_id_list(cursor, model_name)
            else:
                _cs_id_list = cs_id_list.copy()

            for cs_id in _cs_id_list:
                _cs_list.append(CS(cursor, cs_id))

        self.cs = _cs_list.copy()


def table_as_df(cursor, table, columns="*"):
    """Return a MySQL table as a pandas DataFrame

    Parameters
    ----------
    cursor : MySQLCursor
        A MySQLCursor object (see nepc.connect)
    table : str
        The name of a table in the MySQL database
    columns : list of strings
        Which columns to get. If None, then get all columns.

    Return
    ------
        : DataFrame
    table in the form of a pandas DataFrame
    """
    column_text = ", ".join(columns)
    cursor.execute("SELECT " + column_text + " FROM " + table)
    return DataFrame(cursor.fetchall())


def reaction_latex(cs):
    """Return the LaTeX for the reaction from a nepc cross section

    Arguments
    ---------
    cs : nepc.CS or nepc.CustomCS
        A nepc cross section

    Returns
    -------
    reaction : str
        The LaTeX for a nepc cross section reaction
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
