"""Access the NRL Evaluated Plasma Chemistry (NEPC) database

Utilize the NEPC MySQL database by:
    - establishing a connection to the database
    - printing tables and the number of rows in tables
    - accessing a pre-defined plasma chemistry model (PCM, collection
    of cross sections)

Notes
-----
- [nepc] refers to the base directory of the nepc repository.
- [nepc.wiki] refers to the base directory of the wiki associated with
the nepc repository.

Examples
--------
Establish a connection to the NEPC database running on the
production server:

    cnx, cursor = connect()

Establish a connection to the NEPC database running on the
local machine:

    cnx, cursor = connect(local=True)

TODO
----
- plot: one or more cross-section datasets; an entire PCM; particular
        processes within a PCM; particular species/states within a PCM
        or the entire NEPC database
- consolidate: consolidate cross section data for a particular specie/state
               and process
- inspect: visualize aspects of a PCM such as
              - lpu/upu
              - processes and species/states/quantum numbers included
- background: standardize the background information documented for each cross
              section dataset. Perhaps include additional fields like location
              of data (table/figure number in reference).

"""
from pandas import DataFrame
import mysql.connector


def connect(local=False):
    """Establish a connection to NEPC MySQL database


    Parameters
    ----------
    local : bool
        Use a copy of NEPC on localhost; otherwise use the production
        server (default False).

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

    config = {'user': 'nepc',
              'password': 'nepc',
              'host': hostname,
              'database': 'nepc',
              'raise_on_warnings': True}

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    return cnx, cursor


def print_table(cursor, table):
    """Print a table in a MySQL database

    Parameters
    ----------
    cursor : MySQLCursor
        A MySQLCursor object (see nepc.connect)
    """
    print("\n====================\n " + table + ":\n====================")
    cursor.execute("select * from " + table + ";")
    for item in cursor:
        print(item)


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


def model(cursor, model_name):
    """Return a plasma chemistry model from the NEPC MySQL database

    Parameters
    ----------
    cursor : MySQLCursor
        A MySQLCursor object (see nepc.connect)
    model_name :str
        The name of a NEPC model (see [nepc.wiki]/models

    Returns
    -------
    cs_dicts : list of dict
    A list of dictionaries containing cross section data and
    metadata from NEPC database.  The structure of each cross section
    dictionary:
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
        "e" : list of float
            electron energy
        "sigma" : list of float
            cross section
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


    """
    cs_dicts = []
    cursor.execute("SELECT cs.cs_id as cs_id " +
                   "FROM cs " +
                   "JOIN models2cs m2cs ON (cs.cs_id = m2cs.cs_id) " +
                   "JOIN models m ON (m2cs.model_id = m.model_id) " +
                   "WHERE m.name LIKE '" + model_name + "'")
    cs_array = cursor.fetchall()

    for cs_item in cs_array:
        cs_id = cs_item[0]

        cursor.execute("SELECT A.`cs_id` , "
                       "B.`name` , "
                       "C.`name` , "
                       "A.`units_e`, A.`units_sigma`, A.`ref`, "
                       "D.`name`, E.`name`, "
                       "F.`name`, G.`name`, "
                       "A.`wavelength`, A.`lhs_v`, A.`rhs_v`, "
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

        metadata = cursor.fetchall()[0]

        cursor.execute("SELECT e, sigma FROM csdata WHERE cs_id = " +
                       str(cs_id))
        cross_section = cursor.fetchall()
        e_energy = [i[0] for i in cross_section]
        sigma = [i[1] for i in cross_section]

        cs_dicts.append({"cs_id": metadata[0],
                         "specie": metadata[1],
                         "process": metadata[2],
                         "units_e": metadata[3],
                         "units_sigma": metadata[4],
                         "ref": metadata[5],
                         "lhsA": metadata[6],
                         "lhsB": metadata[7],
                         "rhsA": metadata[8],
                         "rhsB": metadata[9],
                         "wavelength": metadata[10],
                         "lhs_v": metadata[11],
                         "rhs_v": metadata[12],
                         "lhs_j": metadata[13],
                         "rhs_j": metadata[14],
                         "background": metadata[15],
                         "lpu": metadata[16],
                         "upu": metadata[17],
                         "e": e_energy,
                         "sigma": sigma,
                         "lhsA_long": metadata[18],
                         "lhsB_long": metadata[19],
                         "rhsA_long": metadata[20],
                         "rhsB_long": metadata[21],
                         "e_on_lhs": metadata[22],
                         "e_on_rhs": metadata[23],
                         "hv_on_lhs": metadata[24],
                         "hv_on_rhs": metadata[25],
                         "v_on_lhs": metadata[26],
                         "v_on_rhs": metadata[27],
                         "j_on_lhs": metadata[28],
                         "j_on_rhs": metadata[29]})

    return cs_dicts


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
    cs : dict
        A nepc cross section dictionary

    Returns
    -------
    reaction : str
        The LaTeX for a nepc cross section reaction
    """
    # FIXME: allow for varying electrons, hv, v, j on rhs and lhs
    e_on_lhs = cs['e_on_lhs']
    if e_on_lhs == 0:
        lhs_e_text = None
    elif e_on_lhs == 1:
        lhs_e_text = "e$^-$"
    else:
        lhs_e_text = str(e_on_lhs) + "e$^-$"

    e_on_rhs = cs['e_on_rhs']
    if e_on_rhs == 0:
        rhs_e_text = None
    elif e_on_rhs == 1:
        rhs_e_text = "e$^-$"
    else:
        rhs_e_text = str(e_on_rhs) + "e$^-$"

    lhs_items = [lhs_e_text,
                 cs['lhsA_long'],
                 cs['lhsB_long']]
    lhs_text = " + ".join(item for item in lhs_items if item)
    rhs_items = [
                cs['rhsA_long'],
                cs['rhsB_long'],
                rhs_e_text]
    rhs_text = " + ".join(item for item in rhs_items if item)
    reaction = " $\\rightarrow$ ".join([lhs_text, rhs_text])
    return reaction


def model_summary_df(model):
    """Return a summary of a NEPC model as a DataFrame

    Parameters
    ----------
    model : list of dicts
    See the model method above

    Returns
    -------
    : DataFrame
    A DataFrame with containing the processes, range of electron energies,
    lpu/upu's for the model
    """
    summary_list = []

    headers = ["specie", "process", "reaction", "E_lower", "E_upper",
               "sigma_max", "lpu", "upu"]

    for cs in model:
        reaction = reaction_latex(cs)
        e_lower = round(min(cs["e"]), 2)
        e_upper = round(max(cs["e"]), 2)
        summary_list.append([cs["specie"], cs["process"], reaction,
                             e_lower, e_upper,
                             cs["units_sigma"]*max(cs["sigma"]),
                             cs["lpu"], cs["upu"]])

    cs_df = DataFrame(summary_list, columns=headers)
    return cs_df
