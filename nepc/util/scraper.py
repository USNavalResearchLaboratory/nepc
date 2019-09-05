"""Part of the NEPC Python module including functions for
writing and reading files"""
import re
import os
import shutil
from subprocess import check_output
from IPython.display import display
import numpy as np
import pdfplumber
from nepc.util import config


def wc_fxn(file_to_count):
    "return the number of lines in a file using wc"
    return int(check_output(["wc", "-l", file_to_count]).split()[0])


def get_pdf(pdf_filename):
    """Returns an easily extractable version of a pdf file
    Parameters
    ----------
    pdf_filename : file
    The pdf file which will be opened

    Returns
    -------
    pdfplumber.open(pdf_filename)
    The extractable version of pdf_filename

    """
    return pdfplumber.open(pdf_filename)


def rmdir(outdir):
    """Try to remove a tree, raise an exception if this isn't possible

    Parameters
    ----------
    outdir : tree
    The tree to be removed
    """
    try:
        shutil.rmtree(outdir)
    except OSError as exc:
        print("Error: %s - %s." % (exc.filename, exc.strerror))


def rmfile(filename):
    """Try to remove a file, raise an exception if the file path
    does not exist

    Parameters
    ----------
    filename : file
    The file that should be removed
    """
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(filename + " does not exist")


def mkdir(outdir):
    """Try to make a directory, raise an exception if the
    directory already exists
    Parameters
    ----------
    outdir : directory
    The directory to be made"""
    try:
        os.mkdir(outdir)
    except OSError as excep:
        print("Error: %s - %s." % (excep.filename, excep.strerror))


def remove_unnecessary(lst):
    """Removes unnecessary elements from
    a list"""
    for i in lst:
        if i == '':
            lst.remove(i)
    """def reader(fil_name, delimiter=''):
    ""Given a file name, return a list containing each line
    w/ the delimiter separating each line""
    fil = open(fil_name, mode='r', newline=delimiter)
    lst = fil.readline()
    str_fi = ''.join(lst)
    toappend = ''
    newlst = []
    for elem in enumerate(str_fi):
        i = 0
        if str_fi[i] == '\t' or i == len(str_fi)-1:
            if i == len(str_fi)-1:
                toappend = toappend + str_fi[i]
                newlst.append(toappend)
            else:
                newlst.append(toappend)
                toappend = ''
        else: toappend = toappend + str_fi[i]
        i = i + 1
    return remove_unnecessary(newlst)"""


# TODO: look at neha's version to see if it can be incorporated
def get_table_data(pdf,
                   page_number, crop_dim_array,
                   locate_tables=False, omit_regex=''):
    """Get the table data from a pdf

    Parameters
    ----------
    pdf : pdf
    The pdf file from which data will be extracted

    page_number : int
    The page number from which the data should be extracted

    Returns
    -------
    data : N-dimensional array
    An N-dimensional array containing all of the table data
    from the pdf"""
    pages = pdf.pages[page_number]
    # data = [[] for i in range(len(crop_dim_array))]
    data = np.empty(shape=(0, 2))
    for i in range(len(crop_dim_array)):
        page_cropped = pages.crop(crop_dim_array[i])
        if (locate_tables):
            display(page_cropped.to_image().reset().draw_rects(
                page_cropped.chars))
        else:
            text_space_delim = page_cropped.extract_text().split("\n")
            for j in range(len(text_space_delim)):
                if (omit_regex == '' or not(
                        bool(re.search(omit_regex, text_space_delim[j])))):
                    text_array = text_space_delim[j].split(' ')
                    data = np.append(data, [[float(text_array[0]),
                                             float(text_array[1])]], axis=0)
    return data


"""neha's version
def get_table_data(pdf, page_number, crop_dim_array,
                   locate_tables=False, omit_regexp=''):
    Get the table data from a pdf

    Parameters
    ----------
    pdf : pdf
    The pdf file from which data will be extracted

    page_number : int
    The page number from which the data should be extracted

    Returns
    -------
    data : N-dimensional array
    An N-dimensional array containing all of the table data
    from the pdf
    pages = pdf.pages[page_number]
    # data = [[] for i in range(len(crop_dim_array))]
    data = np.empty(shape=(0, 2))
    for elem in enumerate(crop_dim_array):
        pg_cropped = pages.crop(elem)
        if locate_tables:
            display(pg_cropped.to_image().reset().draw_rects(pg_cropped.chars))
        else:
            text_space_delim = pg_cropped.extract_text().split("\n")
            for ele in enumerate(text_space_delim):
                if (omit_regexp == '' or not(
                        bool(re.search(omit_regexp, ele)))):
                    text_array = ele.split(' ')
                    data = np.append(data, [[float(text_array[0]),
                                             float(text_array[1])]], axis=0)
    return data
"""


def get_column_data(pdf, page_number, crop_dim_array,
                    locate_tables=False, omit_regex=''):
    pg = pdf.pages[page_number]
    data = np.empty(shape=(0, 1))
    for i in range(len(crop_dim_array)):
        pgCropped = pg.crop(crop_dim_array[i])
        if (locate_tables):
            display(pgCropped.to_image().reset().draw_rects(pgCropped.chars))
        else:
            textSpaceDelim = pgCropped.extract_text().split("\n")
            for j in range(len(textSpaceDelim)):
                if (omit_regex == '' or not(
                        bool(re.search(omit_regex, textSpaceDelim[j])))):
                    data = np.append(
                        data, [[float(textSpaceDelim[j])]],
                        axis=0)
    return data


"""neha's version
def get_column_data(pdf, page_number, crop_dim_array,
                    locate_tables=False, omit_regexp=''):
    Get column data from a pdf

    Parameters
    ----------
    pdf : pdf
    The pdf file from which data will be extracted

    page_number : int
    The page number from which the data should be extracted
    Returns
    -------
    data : N-dimensional array
    An N-dimensional array containing all of the data in a
    column of the pdf (fix this docstring)

    page = pdf.pages[page_number]
    data = np.empty(shape=(0, 1))
    for ele in enumerate(crop_dim_array):
        pg_cropped = page.crop(ele)
        if locate_tables:
            display(pg_cropped.to_image().reset().draw_rects(pg_cropped.chars))
        else:
            text_space_delim = pg_cropped.extract_text().split("\n")
            for elem in enumerate(text_space_delim):
                if (omit_regexp == '' or not(
                        bool(re.search(omit_regexp, elem)))):
                    data = np.append(
                        data, [[float(elem)]],
                        axis=0)
    return data
"""


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


def get_column_strings(pdf, page_number, crop_dim_array,
                       locate_tables=False, omit_regex=''):
    pg = pdf.pages[page_number]
    data = []
    pgCropped = pg.crop(crop_dim_array)
    if (locate_tables):
        display(pgCropped.to_image().reset().draw_rects(pgCropped.chars))
    else:
        textSpaceDelim = pgCropped.extract_text().split("\n")
        for j in range(len(textSpaceDelim)):
            if (omit_regex == '' or not(
                    bool(re.search(omit_regex, textSpaceDelim[j])))):
                # textArray = textSpaceDelim[j].split(' ')
                # data.append([textArray[0], textArray[1]])
                data.append(textSpaceDelim[j])
    return data


"""neha version
def get_column_strings(pdf, page_number, crop_dim_array,
                       locate_tables=False, omit_regexp=''):
    Get column data as strings from a pdf

    Parameters
    ----------
    pdf : pdf
    The pdf file from which data will be extracted

    page_number : int
    The page number from which the data should be extracted
    Returns
    -------
    data : list
    A list containing all of the data in a
    column of the pdf (fix this docstring)
    pages = pdf.pages[page_number]
    data = []
    pg_cropped = pages.crop(crop_dim_array)
    if locate_tables:
        display(pg_cropped.to_image().reset().draw_rects(pg_cropped.chars))
    else:
        text_space_delim = pg_cropped.extract_text().split("\n")
        for elem in enumerate(text_space_delim):
            if (omit_regexp == '' or not(
                    bool(re.search(omit_regexp, elem)))):
                # textArray = textSpaceDelim[j].split(' ')
                # data.append([textArray[0], textArray[1]])
                data.append(elem)
    return data
end neha version"""


def write_data_to_file(data_array, filename, start_csdata_id):
    """Given an array of data, write this to a file in the correct format
    Parameters
    ----------
    data_array : arr
    An array of values to be entered into the file

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
                           units_e, units_sigma, ref,
                           lhs_a='\\N', lhs_b='\\N',
                           rhs_a='\\N', rhs_b='\\N', wavelength='-1',
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
        next_cs_id, next_csdata_id):
    """Write out the next id's for the database to a file

    Parameters
    ----------
    next_cs_id : int
    The next cs_id to use

    next_csdata_id: int
    The next csdata_id to use
    """
    nepc_home = config.nepc_home()
    filename = nepc_home + "/data/next_id.tsv"
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


def write_cs_to_file(filename, data_array, cs_id, start_csdata_id, specie,
                     process, units_e, units_sigma, ref,
                     lhs_a='\\N', lhs_b='\\N', rhs_a='\\N', rhs_b='\\N',
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
                                        wavelength, lhs_v, rhs_v,
                                        lhs_j, rhs_j, background, lpu, upu)
    return (next_cs_id, next_csdata_id)


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


def get_next_ids():
    """Get the next ids from a file

    Return
    ------
    next_cs_id: int
    Next cs_id to use

    next_csdata_id: int
    Next csdata_id to use
    """
    nepc_home = config.nepc_home()
    filename = nepc_home + "/data/next_id.tsv"
    with open(filename) as id_file:
        id_line = id_file.readlines()
    next_cs_id, next_csdata_id = id_line[1].split('\t')
    return int(next_cs_id), int(next_csdata_id)


def get_states(filename):
    """Get name's and long_name's from state.tsv file"""
    with open(filename) as states_f:
        states_lines = states_f.readlines()[1:]

    states = []
    for line in states_lines:
        states.append(line.split('\t'))
    return ([states[i][2] for i in range(len(states))],
            [states[i][3] for i in range(len(states))])


def get_cs_id_from_met_file(filename):
    """Get cs_id from second line, first column of .met file"""
    with open(filename) as met_file:
        met_lines = met_file.readlines()[1:]

    for line in met_lines:
        metadata = line.split('\t')
    return metadata[0]
