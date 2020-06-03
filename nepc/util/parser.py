"""Adapted from BOLOS (https://github.com/aluque/bolos). Adaptations:
 - replaced 'next()' with '__next__()' for Python 3
 - broke out large comment to add separate dictionary entries for ``process``,
   ``param``, ``species``, etc.

Notes
-----
This module contains the code required to parse BOLSIG+-compatible files.
To make the code re-usabe in other projects it is independent from the rest of
the BOLOS code.

Most users would only use the method :func:`parse` in this module, which is
documented below.

"""
import re
import numpy as np
from nepc.util import config as nepc_config

RE_NL = re.compile('\n')
def parse(filename, has_arg=True, debug=False):
    """ Parses a BOLSIG+ cross-sections file.

    Parameters
    ----------
    filename: str
        Name of a Bolsig+-compatible cross-sections file.

    has_arg: bool, optional
        Whether threshold values are present in each block

    Returns
    -------
    processes : list of dict
        A list with all processes, in dictionary form, included in the file.

    Notes
    -----
    This function does not return :class:`process.Process` instances so that
    the parser is independent of the rest of the code and can be re-used in
    other projects.  If you want to convert a process in dictionary form `d` to
    a :class:`process.Process` instance, use

    >>> process = process.Process(**d)

    """
    processes = []
    with open(filename) as fp:
        for line in fp:
            try:
                key = line.strip()
                fread = KEYWORDS[key]

                # If the key is not found, we do not reach this line.
                if debug:
                    print('New process of type {}'.format(key))

                d = fread(fp, has_arg, debug=debug)
                d['kind'] = key
                d['filename'] = filename
                # refactored comment to header
                # old code called header comment which collided with key comment
                d['comment'] = []

                # new code to add separate entries for process, param, etc
                header = [s.strip() for s in RE_NL.split(d['header'])]
                for i in range(len(header)):
                    if debug:
                        print('processing header[{:d}]: {}'.format(i, header[i]))
                    key, value = header[i].split(':',1)
                    key = key.lower().replace('.','')
                    value = value.lstrip()
                    if key == 'comment':
                        d['comment'].append(value)
                    else:
                        d[key] = value

                del d['header']
                d['comment'] = ' '.join(d['comment'])

                processes.append(d)

            except KeyError:
                pass

    if debug:
        print('Parsing complete. {:d} processes read.'.format(len(processes)))

    return processes


# BOLSIG+'s user guide saye that the separators must consist of at least five dashes
def _read_until_sep(fp, debug=False):
    """ Reads lines from fp until we find a separator line. 

    """
    RE_SEP = re.compile("-----+")
    lines = []
    for line in fp:
        if RE_SEP.match(line.strip()):
            break
        lines.append(line.strip())

    return lines


def _read_block(fp, has_arg=True, debug=False):
    """ Reads data of a process, contained in a block.
    ``has_arg`` indicates wether we have to read an argument line.

    """
    target = fp.__next__().strip()
    if has_arg:
        arg = fp.__next__().strip()
    else:
        arg = None

    header = "\n".join(_read_until_sep(fp, debug=debug))

    if debug:
        print('Read process {}'.format(target))
    data = np.loadtxt(_read_until_sep(fp, debug=debug)).tolist()

    return target, arg, header, data

#
# Specialized funcion for each keyword. They all return dictionaries with the
# relevant attibutes.
# 
def _read_momentum(fp, has_arg=True, debug=False):
    """ Reads a MOMENTUM or EFFECTIVE block.

    """
    target, arg, header, data = _read_block(fp, has_arg=has_arg, debug=debug)
    mass_ratio = float(arg.split()[0])
    d = dict(target=target,
             mass_ratio=mass_ratio,
             header=header,
             data=data)

    return d

RE_ARROW = re.compile('<?->')
def _read_excitation(fp, has_arg=True, debug=False):
    """ Reads an EXCITATION or IONIZATION block. 

    """
    target, arg, header, data = _read_block(fp, has_arg=has_arg, debug=debug)
    lhs, rhs = [s.strip() for s in RE_ARROW.split(target)]

    d = dict(target=lhs,
             product=rhs,
             header=header,
             data=data)

    if (has_arg):
        if '<->' in target.split():
            threshold, weight_ratio = float(arg.split()[0]), float(arg.split()[1])
            d['weight_ratio'] = weight_ratio
        else:
            threshold = float(arg.split()[0])

        d['threshold'] = threshold

    return d


def _read_attachment(fp, has_arg=False, debug=False):
    """ Reads an ATTACHMENT block.

    """
    target, arg, header, data = _read_block(fp, has_arg=False, debug=debug)

    d = dict(header=header,
             data=data,
             threshold=0.0)
    lr = [s.strip() for s in RE_ARROW.split(target)]

    if len(lr) == 2:
        d['target'] = lr[0]
        d['product'] = lr[1]
    else:
        d['target'] = target

    return d


KEYWORDS = {"MOMENTUM": _read_momentum, 
            "ELASTIC": _read_momentum, 
            "EFFECTIVE": _read_momentum,
            "EXCITATION": _read_excitation,
            "IONIZATION": _read_excitation,
            "ATTACHMENT": _read_attachment}


def write_data_to_file(data_array, filename, start_csdata_id):
    """Given an array of electron energies and corresponding cross sections,
    write the data to a file in the correct format for a NEPC database.

    Parameters
    ----------
    data_array : :class:`numpy.ndarray`
        A numpy array of values to be entered into the filenumpy array. Each row is of
        length 2 (e, sigma).
    filename: str
        Name of the file where values of ``data_array`` should be written.
    start_csdata_id : int
        The first ``csdata_id`` for the supplied data.

    Returns
    -------
    : int
        The next csdata_id to use.

    """
    csdata_id = start_csdata_id
    write_f = open(filename, "x")
    write_f.write("\t".join(['csdata_id', 'e_energy', 'sigma']) + "\n")
    for i in range(len(data_array)):
        write_f.write(str(csdata_id) + "\t" + str(data_array[i, 0])
                      + "\t" + str(data_array[i, 1]) + "\n")
        csdata_id = csdata_id + 1
    write_f.close()
    return csdata_id


def write_pd_data_to_file(data_frame, filename, start_csdata_id):
    """Given a dataframe of csdata, write this to a file in the correct format
    Parameters
    ----------
    data_frame: pandas DataFrame
    A DataFrame containing cross section data to be entered into the file

    filename: file
    Name of the file where values of data_frame should be entered

    start_cs_data_id : int
    The id where the data should be placed

    Return
    ------
    csdata_id
    The next csdata_id to use
    """
    csdata_id = start_csdata_id
    write_f = open(filename, "x")
    write_f.write("\t".join(['csdata_id', 'e_energy', 'sigma']) + "\n")
    for i in range(len(data_frame)):
        write_f.write(str(csdata_id) + "\t" + str(data_frame.iloc[i]['e_energy'])
                      + "\t" + str(data_frame.iloc[i]['sigma']) + "\n")
        csdata_id = csdata_id + 1
    write_f.close()
    return csdata_id


def write_metadata_to_file(filename, cs_id, specie, process,
                           units_e, units_sigma, ref='\\N',
                           lhs_a='\\N', lhs_b='\\N',
                           rhs_a='\\N', rhs_b='\\N', threshold='-1', wavelength='-1',
                           lhs_v=-1, rhs_v=-1, lhs_j=-1, rhs_j=-1,
                           background='\\N', lpu='-1', upu='-1'):
    """Given metadata for a cross section data set,
    write the metadata to a file in the correct format for a NEPC database.

    Parameters
    ----------
    filename: str
        Name of the file where values of ``data_array`` should be written.
    cs_id: int
        ``cs_id`` corresponding to the cross section in the database.
    specie: str
        The short name corresponding to the specie in the database.
    process: str
        The short name corresponding to the electron scattering process in the 
        database.
    units_e: float
        The units, in eV, of the electron energies.
    units_sigma: float
        The units, in :math:`m^2`, of the cross sections.
    ref: str
        The short name for the reference corresponding to the dataset.
    lhs_a: str
        The short name for the lhs_a state for the process.
    lhs_b: str
        The short name for the lhs_b state.
    rhs_a: str
        The short name for the rhs_a state.
    rhs_b: str
        The short name for the rhs_b state.
    threshold: float
        The threshold electron energy for the process.
    wavelength: float
        The wavelength of the photon associated with the process, if applicable.
    lhs_v: int
        The vibrational energy associated with the LHS state, if applicable.
    rhs_v: int
        The vibrational energy associated with the RHS state, if applicable.
    lhs_j: int
        The rotational energy associated with the LHS state, if applicable.
    rhs_j: int
        The rotational energy associated with the RHS state, if applicable.
    background: str
        Background information for the cross section data.
    lpu: float
        Lower percent uncertainty of the cross section data.
    upu: float
        Upper percent uncertainty of the cross section data.

    Returns
    -------
    : int
        The next cs_id to use.

    """
    write_met = open(filename, "x")
    write_met.write(
        "\t".join(
            ('cs_id',
             'specie',
             'process',
             'units_e',
             'units_sigma',
             'ref',
             'lhs_a',
             'lhs_b',
             'rhs_a',
             'rhs_b',
             'threshold',
             'wavelength',
             'lhs_v',
             'rhs_v',
             'lhs_j',
             'rhs_j',
             'background',
             'lpu',
             'upu')) + "\n")
    write_met.write(
        "\t".join(
            (str(cs_id),
             specie,
             process,
             str(units_e),
             str(units_sigma),
             ref,
             lhs_a,
             lhs_b,
             rhs_a,
             rhs_b,
             str(threshold),
             str(wavelength),
             str(lhs_v),
             str(rhs_v),
             str(lhs_j),
             str(rhs_j),
             background,
             str(lpu),
             str(upu))))
    write_met.close()
    return cs_id + 1


def write_cs_to_file(filename, data_array, cs_id, start_csdata_id, specie,
                     process, units_e, units_sigma, ref='\\N',
                     lhs_a='\\N', lhs_b='\\N', rhs_a='\\N', rhs_b='\\N',
                     threshold='-1',
                     wavelength='-1',
                     lhs_v=-1, rhs_v=-1, lhs_j=-1, rhs_j=-1,
                     background='\\N', lpu='-1', upu='-1'):
    """Write both the cross-section data and metadata to a file
    Parameters
    ----------
    Contains a combination of parameters from write_data_to_file and
    write_metadata_to_file"""
    next_csdata_id = write_data_to_file(data_array, filename+".dat",
                                        start_csdata_id)
    next_cs_id = write_metadata_to_file(filename+".met", cs_id, specie,
                                        process, units_e, units_sigma,
                                        ref, lhs_a, lhs_b, rhs_a, rhs_b,
                                        threshold, wavelength, lhs_v, rhs_v,
                                        lhs_j, rhs_j, background, lpu, upu)
    return (next_cs_id, next_csdata_id)




def write_next_id_to_file(
        next_cs_id, next_csdata_id, test=False):
    """Write out the next id's for the database to a file.

    Parameters
    ----------
    next_cs_id : int
        The next cs_id to use
    next_csdata_id: int
        The next csdata_id to use
    test: bool, optional
        If true, the command is run for the ``nepc_test`` database. Otherwise,
        it is run for the ``nepc`` database. (Default is the ``nepc`` database.)

    """
    if test:
        nepc_data_home = nepc_config.nepc_home() + '/tests/data/'
    else:
        nepc_data_home = nepc_config.nepc_cs_home() + '/data/'
    filename = nepc_data_home + "/next_id.tsv"
    id_file = open(filename, "w+")
    id_file.write(
        "\t".join(
            ('next_cs_id',
             'next_csdata_id')) + "\n")
    id_file.write(
        "\t".join(
            (str(next_cs_id),
             str(next_csdata_id))))
    id_file.close()


def write_models_to_file(filename, models_array):
    """Write model data to a file.

    Parameters
    ----------
    filename : str
        The name of the file where the model data should be stored.
    models_array: list of str
        A list of models that should be added to ``filename``.

    """
    model_f = open(filename, "x")
    model_f.write("model_name\n")
    for i in range(len(models_array)):
        model_f.write(models_array[i] + "\n")
    model_f.close()


def get_next_ids(test=False):
    """Get the next ids from a file

    Parameters
    ----------
    test: bool, optional
        If true, the command is run for the ``nepc_test`` database. Otherwise,
        it is run for the ``nepc`` database. (Default is the ``nepc`` database.)

    Returns
    -------
    : int
        Next cs_id to use
    : int
        Next csdata_id to use

    """
    if test:
        nepc_data_home = nepc_config.nepc_home() + '/tests/data/'
    else:
        nepc_data_home = nepc_config.nepc_cs_home() + '/data/'
    filename = nepc_data_home + "/next_id.tsv"
    with open(filename) as id_file:
        id_line = id_file.readlines()
    next_cs_id, next_csdata_id = id_line[1].split('\t')
    return int(next_cs_id), int(next_csdata_id)


def get_states(test=False):
    """Get lists of name's and long_name's from states.tsv file."""
    if test:
        nepc_data_home = nepc_config.nepc_home() + '/tests/data/'
    else:
        nepc_data_home = nepc_config.nepc_cs_home() + '/data/'
    filename = nepc_data_home + 'states.tsv'
    with open(filename) as states_f:
        states_lines = states_f.readlines()[1:]

    states = []
    for line in states_lines:
        states.append(line.split('\t'))
    return ([states[i][1] for i in range(len(states))],
            [states[i][2] for i in range(len(states))])


def remove_crs(mystring):
    """Removes new lines"""
    return mystring.replace('\n', ' ').replace('\r', '')


def text_array_to_float_array(text_array, omit_regexp=''):
    """Convert an array of strings to an array of floats

    Parameters
    ----------
    text_array : str array
    An array of strings to be converted

    Returns
    -------
    data : float array
    An array of floats containing float-converted data
    from text_array"""
    data = np.empty(shape=(0, 1))
    for inde in range(0, len(text_array)):
        if (omit_regexp == '' or not(
                bool(re.search(omit_regexp, text_array[inde])))):
            data = np.append(data, [[float(text_array[inde])]], axis=0)
    return data


