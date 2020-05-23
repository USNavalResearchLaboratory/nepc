"""Adapted from BOLOS (https://github.com/aluque/bolos). Adaptations:
 - replaced 'next()' with '__next__()' for Python 3
 - broke out large comment to add separate dictionary entry for 'process', param, species, etc.

Notes
-----
This module contains the code required to parse BOLSIG+-compatible files.
To make the code re-usabe in other projects it is independent from the rest of
the BOLOS code.

Most user would only use the method :func:`parse` in this module, which is
documented below.
"""

import sys
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

    has_arg: bool
        Whether threshold values are present in each block

    Returns
    -------
    processes : list of dictionaries
        A list with all processes, in dictionary form, included in the file.

    Note
    ----
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
RE_SEP = re.compile("-----+")
def _read_until_sep(fp, debug=False):
    """ Reads lines from fp until a we find a separator line. """
    lines = []
    for line in fp:
        if RE_SEP.match(line.strip()):
            break
        lines.append(line.strip())

    return lines


def _read_block(fp, has_arg=True, debug=False):
    """ Reads data of a process, contained in a block. 
    has_arg indicates wether we have to read an argument line"""
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
    """ Reads a MOMENTUM or EFFECTIVE block. """
    target, arg, header, data = _read_block(fp, has_arg=has_arg, debug=debug)
    mass_ratio = float(arg.split()[0])
    d = dict(target=target,
             mass_ratio=mass_ratio,
             header=header,
             data=data)

    return d

RE_ARROW = re.compile('<?->')
def _read_excitation(fp, has_arg=True, debug=False):
    """ Reads an EXCITATION or IONIZATION block. """
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
    """ Reads an ATTACHMENT block. """
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
    """Given an array of data, write this to a file in the correct format
    Parameters
    ----------
    data_array : numpy array
    A numpy array of values to be entered into the filenumpy array. Each row is of
    length 2 (e, sigma).

    filename: file
    Name of the file where values of data_array should be entered

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
    for i in range(len(data_array)):
        write_f.write(str(csdata_id) + "\t" + str(data_array[i, 0])
                      + "\t" + str(data_array[i, 1]) + "\n")
        csdata_id = csdata_id + 1
    write_f.close()
    return csdata_id


def write_metadata_to_file(filename, cs_id, specie, process,
                           units_e, units_sigma, ref='\\N',
                           lhs_a='\\N', lhs_b='\\N',
                           rhs_a='\\N', rhs_b='\\N', threshold='-1', wavelength='-1',
                           lhs_v=-1, rhs_v=-1, lhs_j=-1, rhs_j=-1,
                           background='\\N', lpu='-1', upu='-1'):
    """Write out metadata to the file called filename

    Parameters
    ----------
    filename : file
    The file to which information will be written out

    cs_id : int
    The id to start with when filling out information
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


def write_next_id_to_file(
        next_cs_id, next_csdata_id, test=False):
    """Write out the next id's for the database to a file

    Parameters
    ----------
    next_cs_id : int
        The next cs_id to use

    next_csdata_id: int
        The next csdata_id to use

    test: bool
        Flag to indicate whether the command is run for a test.
    """
    if test:
        nepc_data_home = nepc_config.nepc_home() + '/tests'
    else:
        nepc_data_home = nepc_config.nepc_data_home()
    filename = nepc_data_home + "/data/next_id.tsv"
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
    """Write the models to a file
    Parameters
    ----------
    filename : file
    The name of the file where the model data should be located

    models_array: arr of strs
    A list of models that should be added to the filename"""
    model_f = open(filename, "x")
    model_f.write("model_name\n")
    for i in range(len(models_array)):
        model_f.write(models_array[i] + "\n")
    model_f.close()


def get_next_ids(test=False):
    """Get the next ids from a file

    Parameters
    ----------
    test: bool
        Flag to indicate whether the command is run for a test.

    Return
    ------
    next_cs_id: int
        Next cs_id to use

    next_csdata_id: int
        Next csdata_id to use
    """
    if test:
        nepc_data_home = nepc_config.nepc_home() + '/tests'
    else:
        nepc_data_home = nepc_config.nepc_data_home()
    filename = nepc_data_home + "/data/next_id.tsv"
    with open(filename) as id_file:
        id_line = id_file.readlines()
    next_cs_id, next_csdata_id = id_line[1].split('\t')
    return int(next_cs_id), int(next_csdata_id)
