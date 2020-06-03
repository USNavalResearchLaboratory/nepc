"""Utilities for scraping data from PDFs and other docs"""
import re
import numpy as np
from IPython.display import display
import pdfplumber


def get_pdf(pdf_filename):
    """Returns an easily extractable version of a pdf file

    Parameters
    ----------
    pdf_filename : str
        The pdf file which will be opened

    Returns
    -------
    pdfplumber.open(pdf_filename)
        The extractable version of pdf_filename

    """
    return pdfplumber.open(pdf_filename)


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
