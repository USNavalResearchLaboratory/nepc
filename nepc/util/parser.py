# import sys
import re
import numpy as np
import logging
from decimal import Decimal
"""
Adapted from BOLOS (https://github.com/aluque/bolos). Adaptations:
- replaced 'next()' with '__next__()' for Python 3
- broke out large comments block to add separate dictionary entry for
  'process', param, species, comment, etc.
- compined 'comment' block if present to 'process' as parenthetical
  (particularly useful to catch momentum-transfer elastic processes)
"""

""" This module contains the code required to parse BOLSIG+-compatible files.
To make the code re-usabe in other projects it is independent from the rest of
the BOLOS code.

Most user would only use the method :func:`parse` in this module, which is
documented below.
"""

RE_NL = re.compile('\n')


def parse(fp, filename, has_arg=True):
    """ Parses a BOLSIG+ cross-sections file.

    Parameters
    ----------
    fp : file-like
        A file object pointing to a Bolsig+-compatible cross-sections file.

    filename: str
        Name of the file.

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
    for line in fp:
        try:
            key = line.strip()
            fread = KEYWORDS[key]

            # If the key is not found, we do not reach this line.
            logging.debug("New process of type '%s'" % key)

            d = fread(fp, has_arg)
            d['kind'] = key
            d['filename'] = filename

            # new code to add separate entries for process, param, etc
            comments = [s.strip() for s in RE_NL.split(d['comments'])]
            for i in range(len(comments)):
                key, value = comments[i].split(':', 1)
                key = key.lower().replace('.', '')
                value = value.lstrip()
                d[key] = value

            # add 'comment' to 'process'
            if 'comment' in d.keys():
                comment_fixed = d['comment'].lower().replace('.', '')
                d['process'] = d['process'] + ' (' + comment_fixed + ')'
                del comment_fixed
                del d['comment']

            del d['comments']

            processes.append(d)

        except KeyError:
            pass

    logging.info("Parsing complete. %d processes read." % len(processes))

    return processes


# BOLSIG+'s user guide says that the separators must consist of at least
# five dashes
RE_SEP = re.compile("-----+")


def _read_until_sep(fp):
    """ Reads lines from fp until a we find a separator line. """
    lines = []
    for line in fp:
        if RE_SEP.match(line.strip()):
            break
        lines.append(line.strip())

    return lines


def _read_block(fp, has_arg=True):
    """ Reads data of a process, contained in a block.
    has_arg indicates wether we have to read an argument line"""
    target = fp.__next__().strip()
    if has_arg:
        arg = fp.__next__().strip()
    else:
        arg = None

    comments = "\n".join(_read_until_sep(fp))

    logging.debug("Read process '%s'" % target)
    data = np.loadtxt(_read_until_sep(fp))
    # data = np.loadtxt(_read_until_sep(fp)).tolist()

    return target, arg, comments, data

#
# Specialized funcion for each keyword. They all return dictionaries with the
# relevant attibutes.
#


def _read_momentum(fp, has_arg=True):
    """ Reads a MOMENTUM or EFFECTIVE block. """
    target, arg, comments, data = _read_block(fp, has_arg=has_arg)
    mass_ratio = float(arg.split()[0])
    d = dict(target=target,
             mass_ratio=mass_ratio,
             comments=comments,
             data=data)

    return d


RE_ARROW = re.compile('<?->')


def _read_excitation(fp, has_arg=True):
    """ Reads an EXCITATION or IONIZATION block. """
    target, arg, comments, data = _read_block(fp, has_arg=has_arg)
    lhs, rhs = [s.strip() for s in RE_ARROW.split(target)]

    d = dict(target=lhs,
             product=rhs,
             comments=comments,
             data=data)

    if (has_arg):
        if '<->' in target.split():
            threshold, weight_ratio = (float(arg.split()[0]),
                                       float(arg.split()[1]))
            d['weight_ratio'] = weight_ratio
        else:
            threshold = float(arg.split()[0])

        d['threshold'] = threshold

    return d


def _read_attachment(fp, has_arg=False):
    """ Reads an ATTACHMENT block. """
    target, _, comments, data = _read_block(fp, has_arg=False)

    d = dict(comments=comments,
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


def lxcat(filename,
          process_type,
          process,
          threshold,
          species,
          process_long,
          parameter,
          updated,
          columns,
          data):
    with open(filename, 'w') as fp:
        fp.write(process_type+"\n")
        fp.write(process+"\n")
        fp.write(" "+'{:.6e}'.format(Decimal(threshold))+"\n")
        fp.write("SPECIES: "+species+"\n")
        fp.write("PROCESS: "+process_long+"\n")
        fp.write("PARAM.:  "+parameter+"\n")
        fp.write("UPDATED: "+updated+"\n")
        fp.write("COLUMNS: "+columns+"\n")
        fp.write("-----------------------------\n")
        for i in range(len(data)):
            fp.write('{:.10e}    {:.7e}\n'.format(Decimal(data[i, 0]),
                                                  Decimal(data[i, 1]/1.0e20)))
        fp.write("-----------------------------\n\n")


def states_file_to_list(filename):
    """read states (short and long) from nepc formatted states file"""
    with open(filename) as f:
        states_lines = f.readlines()[1:]

    states_list = []
    for line in states_lines:
        states_list.append(line.split('\t'))

    states = [states_list[i][9] for i in range(1, len(states_list))]
    states_long = [states_list[i][10] for i in range(1, len(states_list))]

    return states, states_long
