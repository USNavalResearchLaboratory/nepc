"""
Adapted from BOLOS (https://github.com/aluque/bolos). Adaptations:
- replaced 'next()' with '__next__()' for Python 3
- broke out large comments block to add separate dictionary entry for
  'process', param, species, comment, etc.
- combined 'comment' block if present to 'process' as parenthetical
  (particularly useful to catch momentum-transfer elastic processes)
"""
import re
import logging
from decimal import Decimal
import numpy as np

RE_ARROW = re.compile('<?->')
RE_NL = re.compile('\n')
# BOLSIG+'s user guide says that the separators must consist of at least
# five dashes
RE_SEP = re.compile("-----+")


def parse(file_pointer, filename, has_arg=True):
    """ Parses a BOLSIG+ cross-sections file.

    Parameters
    ----------
    file_pointer : file-like
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
    for line in file_pointer:
        try:
            key = line.strip()
            fread = KEYWORDS[key]

            # If the key is not found, we do not reach this line.
            logging.debug("New process of type %s", key)

            file_dict = fread(file_pointer, has_arg)
            file_dict['kind'] = key
            file_dict['filename'] = filename

            # new code to add separate entries for process, param, etc
            comments = [s.strip() for s in RE_NL.split(file_dict['comments'])]
            for elem in enumerate(comments):
                key, value = elem.split(':', 1)
                key = key.lower().replace('.', '')
                value = value.lstrip()
                file_dict[key] = value

            # add 'comment' to 'process'
            if 'comment' in file_dict.keys():
                comment_fixed = file_dict['comment'].lower().replace('.', '')
                file_dict['process'] = (file_dict['process'] +
                                        ' (' + comment_fixed + ')')
                del comment_fixed
                del file_dict['comment']

            del file_dict['comments']

            processes.append(file_dict)

        except KeyError:
            pass

    logging.info("Parsing complete. %d processes read.", len(processes))

    return processes


def _read_until_sep(file_pointer):
    """ Reads lines from file_pointer until a we find a separator line. """
    lines = []
    for line in file_pointer:
        if RE_SEP.match(line.strip()):
            break
        lines.append(line.strip())

    return lines


def _read_block(file_pointer, has_arg=True):
    """ Reads data of a process, contained in a block.
    has_arg indicates wether we have to read an argument line"""
    target = file_pointer.__next__().strip()
    if has_arg:
        arg = file_pointer.__next__().strip()
    else:
        arg = None

    comments = "\n".join(_read_until_sep(file_pointer))

    logging.debug("Read process %s.", target)
    data = np.loadtxt(_read_until_sep(file_pointer))
    # data = np.loadtxt(_read_until_sep(file_pointer)).tolist()

    return target, arg, comments, data

#
# Specialized funcion for each keyword. They all return dictionaries with the
# relevant attibutes.
#


def _read_momentum(file_pointer, has_arg=True):
    """ Reads a MOMENTUM or EFFECTIVE block. """
    target, arg, comments, data = _read_block(file_pointer, has_arg=has_arg)
    mass_ratio = float(arg.split()[0])
    block_dict = dict(target=target,
                      mass_ratio=mass_ratio,
                      comments=comments,
                      data=data)

    return block_dict


def _read_excitation(file_pointer, has_arg=True):
    """ Reads an EXCITATION or IONIZATION block. """
    target, arg, comments, data = _read_block(file_pointer, has_arg=has_arg)
    lhs, rhs = [s.strip() for s in RE_ARROW.split(target)]

    block_dict = dict(target=lhs,
                      product=rhs,
                      comments=comments,
                      data=data)

    if has_arg:
        if '<->' in target.split():
            threshold, weight_ratio = (float(arg.split()[0]),
                                       float(arg.split()[1]))
            block_dict['weight_ratio'] = weight_ratio
        else:
            threshold = float(arg.split()[0])

        block_dict['threshold'] = threshold

    return block_dict


def _read_attachment(file_pointer, has_arg=False):
    """ Reads an ATTACHMENT block. """
    target, _, comments, data = _read_block(file_pointer, has_arg)

    block_dict = dict(comments=comments,
                      data=data,
                      threshold=0.0)
    lhs_rhs = [s.strip() for s in RE_ARROW.split(target)]

    if len(lhs_rhs) == 2:
        block_dict['target'] = lhs_rhs[0]
        block_dict['product'] = lhs_rhs[1]
    else:
        block_dict['target'] = target

    return block_dict


KEYWORDS = {"MOMENTUM": _read_momentum,
            "ELASTIC": _read_momentum,
            "EFFECTIVE": _read_momentum,
            "EXCITATION": _read_excitation,
            "IONIZATION": _read_excitation,
            "ATTACHMENT": _read_attachment}


def lxcat(filename, process_type, process, threshold, species, process_long,
          parameter, updated, columns, data):
    """Writes file in lxCat format."""
    with open(filename, 'w') as file_pointer:
        file_pointer.write(process_type+"\n")
        file_pointer.write(process+"\n")
        file_pointer.write(" "+'{:.6e}'.format(Decimal(threshold))+"\n")
        file_pointer.write("SPECIES: "+species+"\n")
        file_pointer.write("PROCESS: "+process_long+"\n")
        file_pointer.write("PARAM.:  "+parameter+"\n")
        file_pointer.write("UPDATED: "+updated+"\n")
        file_pointer.write("COLUMNS: "+columns+"\n")
        file_pointer.write("-----------------------------\n")
        for i in range(len(data)):
            file_pointer.write(
                '{:.10e}    {:.7e}\n'.format(Decimal(data[i, 0]),
                                             Decimal(data[i, 1]/1.0e20)))
        file_pointer.write("-----------------------------\n\n")


def states_file_to_list(filename):
    """read states (short and long) from nepc formatted states file"""
    with open(filename) as states_file:
        states_lines = states_file.readlines()[1:]

    states_list = []
    for line in states_lines:
        states_list.append(line.split('\t'))

    states = [states_list[i][9] for i in range(1, len(states_list))]
    states_long = [states_list[i][10] for i in range(1, len(states_list))]

    return states, states_long
